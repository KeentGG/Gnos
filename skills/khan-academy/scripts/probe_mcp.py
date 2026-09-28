#!/usr/bin/env python3
"""Inspect the configured Khan stdio MCP without installing a Python SDK.

This diagnostic client lists tools or calls one read-only Khan tool. It does
not select sources, approve clips, or write course/learner files.
"""
import argparse
import json
import os
from pathlib import Path
import queue
import re
import signal
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[3]
READ_ONLY_TOOLS = {'search', 'list_subjects', 'get_topic_tree', 'get_content',
                   'get_course', 'get_transcript', 'get_article', 'get_lesson',
                   'study_guide', 'embed_video', 'get_exercise', 'get_quiz'}


def inspect_result(result):
    """Keep text and image metadata; never mistake a tool success for verification."""
    content = []
    for item in result.get('content', []):
        if item.get('type') == 'text':
            content.append({'type': 'text', 'text': item.get('text', '')})
        else:
            content.append({'type': item.get('type'), 'mimeType': item.get('mimeType'),
                            'payload_omitted': True})
    text = '\n'.join(item.get('text', '') for item in content)
    warnings = []
    status = 'needs-review'
    if result.get('isError') or re.search(
            r'(?im)^\s*(?:#+\s*)?(?:client challenge|access denied|just a moment|error[: ])', text):
        status = 'unusable'
        warnings.append('Tool error or challenge page; do not register this as teaching content.')
    elif not text.strip() or re.search(
            r'(?im)^(?:No results found|Could not get transcript|(?:Video|Article|Exercise|Content) not found)', text):
        status = 'unverified'
        warnings.append('Missing data does not establish absence of Khan coverage; inspect the official page.')
    warnings.append('Inspect topic fit, identity, timestamps, and actual playback separately.')
    return {'status': status, 'warnings': warnings, 'content': content}


def probe(command, tool=None, arguments=None, timeout=45, env=None):
    if timeout <= 0:
        raise ValueError('timeout must be positive')
    if tool is not None and tool not in READ_ONLY_TOOLS:
        raise ValueError('Only read-only Khan tools are supported')
    messages, diagnostics = queue.Queue(), []
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, encoding='utf-8',
                               env=env, start_new_session=True)

    def read_stdout():
        for line in process.stdout:
            try:
                messages.put(json.loads(line))
            except ValueError:
                diagnostics.append('Non-JSON stdout: ' + line[:500])
        messages.put(None)

    def read_stderr():
        for line in process.stderr:
            diagnostics.append(line.rstrip()[:1000])

    readers = [threading.Thread(target=read_stdout, daemon=True),
               threading.Thread(target=read_stderr, daemon=True)]
    for reader in readers:
        reader.start()
    next_id = 0

    def send(message):
        process.stdin.write(json.dumps({'jsonrpc': '2.0', **message}) + '\n')
        process.stdin.flush()

    def request(method, params):
        nonlocal next_id
        next_id += 1
        send({'id': next_id, 'method': method, 'params': params})
        deadline = time.monotonic() + timeout
        while True:
            try:
                response = messages.get(timeout=max(0, deadline - time.monotonic()))
            except queue.Empty as exc:
                raise TimeoutError(f'{method} exceeded {timeout:g}s') from exc
            if response is None:
                raise RuntimeError('MCP exited before replying: ' + '\n'.join(diagnostics[-5:]))
            if not isinstance(response, dict):
                continue
            if response.get('id') != next_id:
                continue
            if 'error' in response:
                raise RuntimeError(json.dumps(response['error']))
            return response.get('result', {})

    report = {}
    try:
        initialized = request('initialize', {'protocolVersion': '2024-11-05',
            'capabilities': {}, 'clientInfo': {'name': 'gnos-khan-inspector', 'version': '1.0'}})
        report['server'] = initialized.get('serverInfo', {})
        report['protocol_version'] = initialized.get('protocolVersion')
        send({'method': 'notifications/initialized'})
        listing = request('tools/list', {})
        report['tools'] = listing.get('tools', [])
        if tool:
            if tool not in {item['name'] for item in report['tools']}:
                raise ValueError(f'{tool} is not exposed by this server')
            report['call'] = {'name': tool, 'arguments': arguments or {}}
            report['result'] = inspect_result(request('tools/call', report['call']))
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=2)
        for reader in readers:
            reader.join(timeout=1)
        for pipe in (process.stdin, process.stdout, process.stderr):
            pipe.close()
    report['stderr'] = '\n'.join(diagnostics[-40:])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / '.mcp.json')
    parser.add_argument('--server', default='aicoder2009-khanacademymcp')
    parser.add_argument('--tool', choices=sorted(READ_ONLY_TOOLS))
    parser.add_argument('--args', default='{}', help='JSON tool arguments; public topic terms only')
    parser.add_argument('--timeout', type=float, default=45, help='Seconds per MCP request')
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text())['mcpServers'][args.server]
        arguments = json.loads(args.args)
        if not isinstance(arguments, dict):
            raise ValueError('--args must be a JSON object')
        if 'command' not in config:
            raise ValueError('This helper supports stdio servers only')
        report = probe([config['command'], *config.get('args', [])], args.tool, arguments,
                       args.timeout, {**os.environ, **config.get('env', {})})
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 2 if report.get('result', {}).get('status') in {'unusable', 'unverified'} else 0
    except (OSError, ValueError, KeyError, RuntimeError, TimeoutError) as exc:
        print(json.dumps({'status': 'unusable', 'error': str(exc)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
