#!/usr/bin/env python3
"""
collector.py — Collect Claude session data for the session-analyst skill.
Outputs structured JSON to stdout.

Enhanced version: adds subagent analysis, token/cost tracking, tool-chain
sequence detection, per-session detail, and model usage breakdown.

Usage: python3 collector.py [--days N]
"""

import json
import os
import sys
import glob
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


def get_cutoff_timestamp(days: int) -> int:
    """Return Unix timestamp in milliseconds for N days ago."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return int(cutoff.timestamp() * 1000)


def get_cutoff_iso(days: int) -> str:
    """Return ISO timestamp string for N days ago."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return cutoff.isoformat()


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


def parse_iso_timestamp(ts_str: str) -> datetime:
    """Parse ISO timestamp, handling Z suffix."""
    return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))


def analyze_session_file(filepath: str, cutoff_iso: str = None, include_subagents: bool = True) -> dict:
    """Extract tool usage, skill invocations, tokens, tool chains, and metadata."""
    tool_counts = Counter()
    skill_counts = Counter()
    model_counts = Counter()
    timestamps = []
    message_count = 0
    total_input_tokens = 0
    total_output_tokens = 0
    total_cache_read_tokens = 0
    total_cache_creation_tokens = 0
    tool_sequence = []  # ordered list of tool names called in this session
    task_dispatches = []  # subagent tasks spawned
    compaction_count = 0

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
                # Skip entries before cutoff if provided
                if cutoff_iso and isinstance(ts, str) and ts < cutoff_iso:
                    continue
                timestamps.append(ts)

            entry_type = entry.get('type')

            if entry_type == 'system':
                subtype = entry.get('subtype', '')
                if 'compact' in subtype:
                    compaction_count += 1

            if entry_type in ('assistant', 'user'):
                message_count += 1

            if entry_type == 'assistant':
                msg = entry.get('message', {})

                # Track model usage
                model = msg.get('model', '')
                if model:
                    model_counts[model] += 1

                # Track token usage
                usage = msg.get('usage', {})
                total_input_tokens += usage.get('input_tokens', 0)
                total_output_tokens += usage.get('output_tokens', 0)
                total_cache_read_tokens += usage.get('cache_read_input_tokens', 0)
                total_cache_creation_tokens += usage.get('cache_creation_input_tokens', 0)

                content = msg.get('content', [])
                if isinstance(content, list):
                    for block in content:
                        if not isinstance(block, dict):
                            continue
                        if block.get('type') == 'tool_use':
                            tool_name = block.get('name', 'unknown')
                            tool_counts[tool_name] += 1
                            tool_sequence.append(tool_name)

                            if tool_name == 'Skill':
                                skill = block.get('input', {}).get('skill', 'unknown')
                                skill_counts[skill] += 1

                            if tool_name == 'Task':
                                task_input = block.get('input', {})
                                task_dispatches.append({
                                    'description': task_input.get('description', ''),
                                    'subagent_type': task_input.get('subagent_type', ''),
                                    'model': task_input.get('model', ''),
                                })

    duration_minutes = 0.0
    if len(timestamps) >= 2:
        try:
            if isinstance(timestamps[0], str):
                t0 = parse_iso_timestamp(timestamps[0])
                t1 = parse_iso_timestamp(timestamps[-1])
                duration_minutes = (t1 - t0).total_seconds() / 60
            else:
                duration_minutes = (max(timestamps) - min(timestamps)) / 60000
        except (ValueError, TypeError):
            pass

    # Compute tool-chain pairs (bigrams): consecutive tool calls
    chain_pairs = Counter()
    for i in range(len(tool_sequence) - 1):
        pair = f"{tool_sequence[i]} -> {tool_sequence[i+1]}"
        chain_pairs[pair] += 1

    # Compute tool-chain trigrams for deeper pattern detection
    chain_trigrams = Counter()
    for i in range(len(tool_sequence) - 2):
        trigram = f"{tool_sequence[i]} -> {tool_sequence[i+1]} -> {tool_sequence[i+2]}"
        chain_trigrams[trigram] += 1

    # Analyze subagent files if requested
    subagent_stats = {'count': 0, 'total_tokens': 0, 'types': Counter()}
    if include_subagents:
        session_dir = os.path.splitext(filepath)[0]
        subagent_dir = os.path.join(session_dir, 'subagents')
        if os.path.isdir(subagent_dir):
            for sa_file in glob.glob(os.path.join(subagent_dir, '*.jsonl')):
                subagent_stats['count'] += 1
                try:
                    sa_result = analyze_session_file(sa_file, cutoff_iso, include_subagents=False)
                    subagent_stats['total_tokens'] += sa_result['tokens']['input'] + sa_result['tokens']['output']
                    # Count subagent types from task dispatches in parent
                    for tool, count in sa_result['tool_counts'].items():
                        tool_counts[tool] += count
                except Exception:
                    continue

    for td in task_dispatches:
        sa_type = td.get('subagent_type', 'unknown')
        subagent_stats['types'][sa_type] += 1

    return {
        'tool_counts': dict(tool_counts),
        'skill_counts': dict(skill_counts),
        'model_counts': dict(model_counts),
        'message_count': message_count,
        'duration_minutes': round(duration_minutes, 1),
        'tokens': {
            'input': total_input_tokens,
            'output': total_output_tokens,
            'cache_read': total_cache_read_tokens,
            'cache_creation': total_cache_creation_tokens,
            'total': total_input_tokens + total_output_tokens,
        },
        'tool_chain_pairs': dict(chain_pairs.most_common(30)),
        'tool_chain_trigrams': dict(chain_trigrams.most_common(20)),
        'task_dispatches': task_dispatches,
        'subagent_stats': {
            'count': subagent_stats['count'],
            'total_tokens': subagent_stats['total_tokens'],
            'types': dict(subagent_stats['types']),
        },
        'compaction_count': compaction_count,
    }


def get_project_name(path: str) -> str:
    """Extract a human-readable project name from a full path."""
    parts = path.rstrip('/').split('/')
    # Return last 2 meaningful path components
    meaningful = [p for p in parts if p and p not in ('Users', 'Documents')]
    if len(meaningful) >= 2:
        return '/'.join(meaningful[-2:])
    return meaningful[-1] if meaningful else path


def get_project_category(path: str) -> str:
    """Infer a human-readable category from a project path."""
    path_lower = path.lower()
    if '/accounts/' in path_lower:
        return 'account-work'
    if '/hobbies/' in path_lower:
        return 'personal-project'
    if '/personal/' in path_lower and '/life/' in path_lower:
        return 'personal-life'
    if '/personal/' in path_lower:
        return 'personal'
    if '/devtools/' in path_lower or '/github/' in path_lower:
        return 'dev-tools'
    if '/work/' in path_lower:
        return 'work'
    if '/vibes/' in path_lower:
        return 'vibe-coding'
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


def extract_project_from_slug(slug: str) -> str:
    """Convert a project directory slug back to a readable path."""
    # Slugs look like: -Users-craigverzosa-Documents-Personal-Hobbies-Tennis
    return slug.replace('-', '/').lstrip('/')


def main(days: int = 20):
    home = str(Path.home())
    history_path = os.path.join(home, '.claude', 'history.jsonl')
    projects_dir = os.path.join(home, '.claude', 'projects')
    skills_dir = os.path.join(home, '.claude', 'skills')

    if not os.path.exists(history_path):
        print(json.dumps({'error': f'history.jsonl not found at {history_path}'}))
        sys.exit(1)

    cutoff_ms = get_cutoff_timestamp(days)
    cutoff_iso = get_cutoff_iso(days)
    history_entries = load_history(history_path, cutoff_ms)

    print(f"[collector] Found {len(history_entries)} prompts in last {days} days", file=sys.stderr)

    # Build project summary
    project_data = {}
    for e in history_entries:
        p = e.get('project', 'unknown')
        if p not in project_data:
            project_data[p] = {'prompt_count': 0, 'session_ids': set(), 'timestamps': []}
        project_data[p]['prompt_count'] += 1
        if 'sessionId' in e:
            project_data[p]['session_ids'].add(e['sessionId'])
        if 'timestamp' in e:
            project_data[p]['timestamps'].append(e['timestamp'])

    projects = sorted([
        {
            'path': p,
            'name': get_project_name(p),
            'category': get_project_category(p),
            'prompt_count': v['prompt_count'],
            'session_count': len(v['session_ids']),
            'first_active': datetime.fromtimestamp(
                min(v['timestamps']) / 1000, tz=timezone.utc
            ).strftime('%Y-%m-%d') if v['timestamps'] else '',
            'last_active': datetime.fromtimestamp(
                max(v['timestamps']) / 1000, tz=timezone.utc
            ).strftime('%Y-%m-%d') if v['timestamps'] else '',
        }
        for p, v in project_data.items()
    ], key=lambda x: -x['prompt_count'])[:25]

    # Prompt samples (up to 500, most recent, exclude slash commands)
    sorted_entries = sorted(history_entries, key=lambda x: -x.get('timestamp', 0))
    prompt_samples = [
        {
            'text': e.get('display', ''),
            'project': get_project_name(e.get('project', '')),
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

    print(f"[collector] Analyzing {len(session_files)} session files...", file=sys.stderr)

    all_tool_counts = Counter()
    all_skill_counts = Counter()
    all_model_counts = Counter()
    all_chain_pairs = Counter()
    all_chain_trigrams = Counter()
    total_duration = 0.0
    total_tokens = {'input': 0, 'output': 0, 'cache_read': 0, 'cache_creation': 0, 'total': 0}
    total_subagents = 0
    total_subagent_tokens = 0
    subagent_types = Counter()
    total_compactions = 0
    sessions_analyzed = 0
    per_session_details = []

    for i, filepath in enumerate(session_files):
        if (i + 1) % 10 == 0:
            print(f"[collector] Processed {i+1}/{len(session_files)} sessions...", file=sys.stderr)
        try:
            result = analyze_session_file(filepath, cutoff_iso, include_subagents=True)

            for tool, count in result['tool_counts'].items():
                all_tool_counts[tool] += count
            for skill, count in result['skill_counts'].items():
                all_skill_counts[skill] += count
            for model, count in result['model_counts'].items():
                all_model_counts[model] += count
            for pair, count in result['tool_chain_pairs'].items():
                all_chain_pairs[pair] += count
            for trigram, count in result['tool_chain_trigrams'].items():
                all_chain_trigrams[trigram] += count

            for key in total_tokens:
                total_tokens[key] += result['tokens'].get(key, 0)

            sa = result['subagent_stats']
            total_subagents += sa['count']
            total_subagent_tokens += sa['total_tokens']
            for sa_type, count in sa['types'].items():
                subagent_types[sa_type] += count

            total_compactions += result['compaction_count']
            total_duration += result['duration_minutes']
            sessions_analyzed += 1

            # Extract project name from filepath
            dir_slug = os.path.basename(os.path.dirname(filepath))
            session_id = os.path.splitext(os.path.basename(filepath))[0]

            per_session_details.append({
                'session_id': session_id,
                'project': extract_project_from_slug(dir_slug),
                'duration_minutes': result['duration_minutes'],
                'message_count': result['message_count'],
                'tokens': result['tokens']['total'],
                'tools_used': len(result['tool_counts']),
                'top_tools': dict(Counter(result['tool_counts']).most_common(5)),
                'skills_used': list(result['skill_counts'].keys()),
                'subagents_spawned': sa['count'],
                'compactions': result['compaction_count'],
            })
        except Exception as e:
            print(f"[collector] Error analyzing {filepath}: {e}", file=sys.stderr)
            continue

    print(f"[collector] Done. Analyzed {sessions_analyzed} sessions.", file=sys.stderr)

    active_days = len({
        datetime.fromtimestamp(e['timestamp'] / 1000, tz=timezone.utc).date().isoformat()
        for e in history_entries if 'timestamp' in e
    })

    # Time-of-day distribution (hour buckets)
    hour_distribution = Counter()
    day_distribution = Counter()
    for e in history_entries:
        if 'timestamp' in e:
            dt = datetime.fromtimestamp(e['timestamp'] / 1000, tz=timezone.utc)
            # Adjust for Pacific time (approximate, -7 or -8 depending on DST)
            local_dt = dt - timedelta(hours=7)
            hour_distribution[local_dt.hour] += 1
            day_distribution[local_dt.strftime('%A')] += 1

    # Sort sessions by token usage (heaviest first)
    heaviest_sessions = sorted(per_session_details, key=lambda x: -x['tokens'])[:10]

    # Sort sessions by duration
    longest_sessions = sorted(per_session_details, key=lambda x: -x['duration_minutes'])[:10]

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
            'total_duration_hours': round(total_duration / 60, 1),
        },
        'tokens': {
            'total_input': total_tokens['input'],
            'total_output': total_tokens['output'],
            'total_combined': total_tokens['total'],
            'cache_read': total_tokens['cache_read'],
            'cache_creation': total_tokens['cache_creation'],
            'cache_hit_rate': round(
                total_tokens['cache_read'] / max(total_tokens['input'] + total_tokens['cache_read'], 1) * 100, 1
            ),
        },
        'models': dict(all_model_counts.most_common()),
        'projects': projects,
        'prompt_samples': prompt_samples,
        'skill_usage': dict(sorted(all_skill_counts.items(), key=lambda x: -x[1])),
        'tool_usage': dict(all_tool_counts.most_common()),
        'slash_commands': dict(sorted(slash_commands.items(), key=lambda x: -x[1])),
        'installed_skills': get_installed_skills(skills_dir),
        'workflow_patterns': {
            'tool_chain_pairs': dict(all_chain_pairs.most_common(25)),
            'tool_chain_trigrams': dict(all_chain_trigrams.most_common(15)),
        },
        'subagent_analysis': {
            'total_spawned': total_subagents,
            'total_tokens': total_subagent_tokens,
            'types': dict(subagent_types.most_common()),
        },
        'session_health': {
            'total_compactions': total_compactions,
            'avg_compactions_per_session': round(total_compactions / max(sessions_analyzed, 1), 1),
        },
        'time_patterns': {
            'hour_distribution': dict(sorted(hour_distribution.items())),
            'day_distribution': dict(day_distribution.most_common()),
        },
        'heaviest_sessions': heaviest_sessions,
        'longest_sessions': longest_sessions,
    }

    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Collect Claude session data for analysis.')
    parser.add_argument('--days', type=int, default=20, help='Analysis window in days (default: 20)')
    args = parser.parse_args()
    main(args.days)
