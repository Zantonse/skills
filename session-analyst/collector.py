#!/usr/bin/env python3
"""
collector.py — Collect Claude session data for the session-analyst skill.
Outputs structured JSON to stdout.

Usage: python3 collector.py [--days N]
"""

import json
import os
import sys
import glob
from datetime import datetime, timedelta, timezone
from pathlib import Path


def get_cutoff_timestamp(days: int) -> int:
    """Return Unix timestamp in milliseconds for N days ago."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return int(cutoff.timestamp() * 1000)


def load_history(history_path: str, cutoff_ms: int) -> list:
    """Load history.jsonl entries at or after cutoff_ms."""
    entries = []
    try:
        with open(history_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get('timestamp', 0) >= cutoff_ms:
                        entries.append(entry)
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return entries


def detect_slash_commands(entries: list) -> dict:
    """Count slash command invocations from history entries."""
    counts = {}
    for entry in entries:
        display = entry.get('display', '').strip()
        if display.startswith('/'):
            parts = display.split()
            cmd = parts[0] if parts else display
            counts[cmd] = counts.get(cmd, 0) + 1
    return counts


def get_session_ids(entries: list) -> set:
    """Extract unique session IDs from history entries."""
    return {e['sessionId'] for e in entries if 'sessionId' in e}


def analyze_session_file(filepath: str) -> dict:
    """Extract tool usage, skill invocations, and metadata from a session JSONL."""
    tool_counts = {}
    skill_counts = {}
    timestamps = []
    message_count = 0

    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            ts = entry.get('timestamp')
            if ts:
                timestamps.append(ts)

            entry_type = entry.get('type')
            if entry_type in ('assistant', 'user'):
                message_count += 1

            if entry_type == 'assistant':
                content = entry.get('message', {}).get('content', [])
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get('type') == 'tool_use':
                            tool_name = block.get('name', 'unknown')
                            tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
                            if tool_name == 'Skill':
                                skill = block.get('input', {}).get('skill', 'unknown')
                                skill_counts[skill] = skill_counts.get(skill, 0) + 1

    duration_minutes = 0.0
    if len(timestamps) >= 2:
        try:
            if isinstance(timestamps[0], str):
                t0 = datetime.fromisoformat(timestamps[0].replace('Z', '+00:00'))
                t1 = datetime.fromisoformat(timestamps[-1].replace('Z', '+00:00'))
                duration_minutes = (t1 - t0).total_seconds() / 60
            else:
                duration_minutes = (max(timestamps) - min(timestamps)) / 60000
        except (ValueError, TypeError):
            pass

    return {
        'tool_counts': tool_counts,
        'skill_counts': skill_counts,
        'message_count': message_count,
        'duration_minutes': round(duration_minutes, 1),
    }


def get_project_category(path: str) -> str:
    """Infer a human-readable category from a project path."""
    path_lower = path.lower()
    if '/accounts/' in path_lower:
        return 'account-work'
    if '/hobbies/' in path_lower or '/personal/' in path_lower:
        return 'personal'
    if '/devtools/' in path_lower or '/github/' in path_lower:
        return 'dev-tools'
    if '/work/' in path_lower:
        return 'work'
    return 'other'


def get_installed_skills(skills_dir: str) -> list:
    """List installed skill names from the skills directory."""
    try:
        return sorted([
            d for d in os.listdir(skills_dir)
            if os.path.isdir(os.path.join(skills_dir, d))
        ])
    except FileNotFoundError:
        return []


def find_session_files(projects_dir: str, session_ids: set) -> list:
    """Find JSONL files matching the given session IDs."""
    files = []
    for session_id in session_ids:
        pattern = os.path.join(projects_dir, '*', f'{session_id}.jsonl')
        files.extend(glob.glob(pattern))
    return files


def main(days: int = 90):
    home = str(Path.home())
    history_path = os.path.join(home, '.claude', 'history.jsonl')
    projects_dir = os.path.join(home, '.claude', 'projects')
    skills_dir = os.path.join(home, '.claude', 'skills')

    if not os.path.exists(history_path):
        print(json.dumps({'error': f'history.jsonl not found at {history_path}'}))
        sys.exit(1)

    cutoff_ms = get_cutoff_timestamp(days)
    history_entries = load_history(history_path, cutoff_ms)

    # Build project summary
    project_counts = {}
    for e in history_entries:
        p = e.get('project', 'unknown')
        if p not in project_counts:
            project_counts[p] = {'prompt_count': 0, 'session_ids': set()}
        project_counts[p]['prompt_count'] += 1
        if 'sessionId' in e:
            project_counts[p]['session_ids'].add(e['sessionId'])

    projects = sorted([
        {
            'path': p,
            'category': get_project_category(p),
            'prompt_count': v['prompt_count'],
            'session_count': len(v['session_ids']),
        }
        for p, v in project_counts.items()
    ], key=lambda x: -x['prompt_count'])[:20]

    # Prompt samples (up to 500, most recent, exclude slash commands)
    sorted_entries = sorted(history_entries, key=lambda x: -x.get('timestamp', 0))
    prompt_samples = [
        {
            'text': e.get('display', ''),
            'project': e.get('project', ''),
            'timestamp': datetime.fromtimestamp(
                e['timestamp'] / 1000, tz=timezone.utc
            ).isoformat() if 'timestamp' in e else '',
        }
        for e in sorted_entries
        if e.get('display', '').strip() and not e.get('display', '').strip().startswith('/')
    ][:500]

    slash_commands = detect_slash_commands(history_entries)

    # Analyze session files
    session_ids = get_session_ids(history_entries)
    session_files = find_session_files(projects_dir, session_ids)

    all_tool_counts = {}
    all_skill_counts = {}
    total_duration = 0.0
    sessions_analyzed = 0

    for filepath in session_files:
        try:
            result = analyze_session_file(filepath)
            for tool, count in result['tool_counts'].items():
                all_tool_counts[tool] = all_tool_counts.get(tool, 0) + count
            for skill, count in result['skill_counts'].items():
                all_skill_counts[skill] = all_skill_counts.get(skill, 0) + count
            total_duration += result['duration_minutes']
            sessions_analyzed += 1
        except Exception:
            continue

    active_days = len({
        datetime.fromtimestamp(e['timestamp'] / 1000, tz=timezone.utc).date().isoformat()
        for e in history_entries if 'timestamp' in e
    })

    output = {
        'window': f'last_{days}_days',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'summary': {
            'sessions_in_window': len(session_ids),
            'sessions_analyzed': sessions_analyzed,
            'total_prompts': len(history_entries),
            'active_days': active_days,
            'avg_prompts_per_day': round(len(history_entries) / max(active_days, 1), 1),
            'avg_session_duration_minutes': round(total_duration / max(sessions_analyzed, 1), 1),
        },
        'projects': projects,
        'prompt_samples': prompt_samples,
        'skill_usage': dict(sorted(all_skill_counts.items(), key=lambda x: -x[1])),
        'tool_usage': dict(sorted(all_tool_counts.items(), key=lambda x: -x[1])),
        'slash_commands': dict(sorted(slash_commands.items(), key=lambda x: -x[1])),
        'installed_skills': get_installed_skills(skills_dir),
    }

    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Collect Claude session data for analysis.')
    parser.add_argument('--days', type=int, default=90, help='Analysis window in days (default: 90)')
    args = parser.parse_args()
    main(args.days)
