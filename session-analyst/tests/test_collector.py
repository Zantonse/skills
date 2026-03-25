import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from collector import get_cutoff_timestamp
from datetime import datetime, timezone


def test_cutoff_is_in_the_past():
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    cutoff = get_cutoff_timestamp(90)
    assert cutoff < now_ms


def test_cutoff_90_days_is_roughly_correct():
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    cutoff = get_cutoff_timestamp(90)
    days_diff = (now_ms - cutoff) / (1000 * 60 * 60 * 24)
    assert 89 < days_diff < 91


def test_cutoff_30_days():
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    cutoff = get_cutoff_timestamp(30)
    days_diff = (now_ms - cutoff) / (1000 * 60 * 60 * 24)
    assert 29 < days_diff < 31


import json
import tempfile
import os
from collector import load_history, detect_slash_commands


def _make_history_file(entries):
    """Write entries to a temp JSONL file, return path."""
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False)
    for e in entries:
        f.write(json.dumps(e) + '\n')
    f.close()
    return f.name


def test_load_history_filters_by_timestamp():
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    old_ms = now_ms - (100 * 24 * 60 * 60 * 1000)  # 100 days ago
    recent_ms = now_ms - (10 * 24 * 60 * 60 * 1000)  # 10 days ago

    entries = [
        {"display": "old prompt", "timestamp": old_ms, "sessionId": "aaa"},
        {"display": "recent prompt", "timestamp": recent_ms, "sessionId": "bbb"},
    ]
    path = _make_history_file(entries)
    try:
        cutoff = get_cutoff_timestamp(90)
        result = load_history(path, cutoff)
        assert len(result) == 1
        assert result[0]["display"] == "recent prompt"
    finally:
        os.unlink(path)


def test_load_history_skips_malformed_lines():
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False)
    f.write('{"display": "valid", "timestamp": 9999999999999}\n')
    f.write('NOT VALID JSON\n')
    f.write('{"display": "also valid", "timestamp": 9999999999999}\n')
    f.close()
    try:
        result = load_history(f.name, 0)
        assert len(result) == 2
    finally:
        os.unlink(f.name)


def test_detect_slash_commands_counts_correctly():
    entries = [
        {"display": "/commit "},
        {"display": "/commit "},
        {"display": "/brainstorming "},
        {"display": "not a slash command"},
        {"display": "/commit "},
    ]
    result = detect_slash_commands(entries)
    assert result["/commit"] == 3
    assert result["/brainstorming"] == 1
    assert "not a slash command" not in result


def test_detect_slash_commands_empty():
    result = detect_slash_commands([])
    assert result == {}


from collector import analyze_session_file, get_session_ids


def _make_session_file(messages):
    """Write session messages to a temp JSONL file."""
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False)
    for m in messages:
        f.write(json.dumps(m) + '\n')
    f.close()
    return f.name


def test_analyze_session_counts_tool_calls():
    messages = [
        {
            "type": "assistant",
            "message": {
                "content": [
                    {"type": "tool_use", "name": "Bash", "id": "t1", "input": {}},
                    {"type": "tool_use", "name": "Read", "id": "t2", "input": {}},
                    {"type": "tool_use", "name": "Bash", "id": "t3", "input": {}},
                ]
            },
            "timestamp": "2026-01-01T10:00:00Z"
        }
    ]
    path = _make_session_file(messages)
    try:
        result = analyze_session_file(path)
        assert result['tool_counts']['Bash'] == 2
        assert result['tool_counts']['Read'] == 1
    finally:
        os.unlink(path)


def test_analyze_session_extracts_skill_invocations():
    messages = [
        {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Skill",
                        "id": "t1",
                        "input": {"skill": "account-research"}
                    },
                    {
                        "type": "tool_use",
                        "name": "Skill",
                        "id": "t2",
                        "input": {"skill": "brainstorming"}
                    },
                ]
            },
            "timestamp": "2026-01-01T10:00:00Z"
        }
    ]
    path = _make_session_file(messages)
    try:
        result = analyze_session_file(path)
        assert result['skill_counts']['account-research'] == 1
        assert result['skill_counts']['brainstorming'] == 1
    finally:
        os.unlink(path)


def test_analyze_session_skips_malformed_lines():
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False)
    f.write('{"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "id": "x", "input": {}}]}, "timestamp": "2026-01-01T10:00:00Z"}\n')
    f.write('NOT JSON\n')
    f.close()
    try:
        result = analyze_session_file(f.name)
        assert result['tool_counts']['Bash'] == 1
    finally:
        os.unlink(f.name)


def test_get_session_ids():
    entries = [
        {"sessionId": "abc", "display": "a"},
        {"sessionId": "def", "display": "b"},
        {"sessionId": "abc", "display": "c"},
        {"display": "no session id"},
    ]
    result = get_session_ids(entries)
    assert result == {"abc", "def"}


from collector import get_project_category, get_installed_skills


def test_get_project_category_account():
    assert get_project_category('/Users/craig/Documents/Work/Accounts/NetApp') == 'account-work'


def test_get_project_category_personal():
    assert get_project_category('/Users/craig/Documents/Personal/Hobbies/Tennis') == 'personal'


def test_get_project_category_devtools():
    assert get_project_category('/Users/craig/Documents/Work/DevTools/ClaudeCode') == 'dev-tools'


def test_get_project_category_work():
    assert get_project_category('/Users/craig/Documents/Work/Okta') == 'work'


def test_get_project_category_other():
    assert get_project_category('/some/unknown/path') == 'other'


def test_get_installed_skills_returns_list(tmp_path):
    (tmp_path / 'skill-a').mkdir()
    (tmp_path / 'skill-b').mkdir()
    (tmp_path / 'not-a-dir.md').write_text('file')
    result = get_installed_skills(str(tmp_path))
    assert 'skill-a' in result
    assert 'skill-b' in result
    assert 'not-a-dir.md' not in result


def test_get_installed_skills_missing_dir():
    result = get_installed_skills('/nonexistent/path/that/does/not/exist')
    assert result == []
