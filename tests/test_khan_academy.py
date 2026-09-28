"""Khan tooling must expose uncertain results and preserve lesson ownership."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/khan-academy/scripts'))

from probe_mcp import inspect_result, probe
from review_video_blocks import review
from tests.test_lesson_contract import valid_lesson, valid_v2_course


class KhanProbeTests(unittest.TestCase):
    def test_challenge_is_unusable_even_without_error_flag(self):
        result = inspect_result({'content': [{'type': 'text', 'text':
            '## Client Challenge\n**Type:** Video\n**URL:** https://www.khanacademy.org/'}]})
        self.assertEqual(result['status'], 'unusable')

    def test_empty_search_does_not_claim_absence_of_coverage(self):
        result = inspect_result({'content': [{'type': 'text', 'text':
            'No results found for "slope".'}]})
        self.assertEqual(result['status'], 'unverified')
        self.assertIn('coverage', ' '.join(result['warnings']))

    def test_thumbnail_is_not_playback_verification(self):
        result = inspect_result({'content': [
            {'type': 'image', 'mimeType': 'image/jpeg', 'data': 'PRIVATE_BASE64'},
            {'type': 'text', 'text': '## Intro to slope\n**YouTube:** https://www.youtube.com/watch?v=MeU-KzdCBps'}]})
        self.assertEqual(result['status'], 'needs-review')
        self.assertNotIn('PRIVATE_BASE64', json.dumps(result))
        self.assertEqual(result['content'][0]['type'], 'image')

    def test_protocol_handles_notifications_and_records_stderr(self):
        server = '''import json, sys
for line in sys.stdin:
    msg = json.loads(line)
    if 'id' not in msg: continue
    print(json.dumps({'jsonrpc':'2.0','method':'notifications/message','params':{}}), flush=True)
    if msg['method'] == 'initialize': result = {'protocolVersion':'2024-11-05','capabilities':{},'serverInfo':{'name':'fixture','version':'1'}}
    elif msg['method'] == 'tools/list': result = {'tools':[{'name':'search','inputSchema':{'type':'object'}}]}
    else:
        print('upstream unavailable', file=sys.stderr, flush=True)
        result = {'isError':True,'content':[{'type':'text','text':'fetch failed'}]}
    print(json.dumps({'jsonrpc':'2.0','id':msg['id'],'result':result}), flush=True)
'''
        result = probe([sys.executable, '-u', '-c', server], 'search', {'query':'slope'}, timeout=3)
        self.assertEqual(result['result']['status'], 'unusable')
        self.assertIn('upstream unavailable', result['stderr'])
        self.assertEqual(result['server']['name'], 'fixture')

    def test_timeout_stops_child(self):
        with self.assertRaises(TimeoutError):
            probe([sys.executable, '-c', 'import time; time.sleep(30)'], timeout=0.15)


class VideoReviewTests(unittest.TestCase):
    def test_embed_supplies_origin_without_disclosing_lesson_path(self):
        sys.path.insert(0, str(ROOT / 'skills/course-viewer/scripts'))
        from render_viewer import render_block
        course, lesson = self.make_pair()
        from html.parser import HTMLParser

        class Frames(HTMLParser):
            attrs = None

            def handle_starttag(self, tag, attrs):
                if tag == 'iframe':
                    self.attrs = dict(attrs)

        parser = Frames()
        parser.feed(render_block(lesson['blocks'][1], {}, course['sources']))
        self.assertEqual(parser.attrs.get('referrerpolicy'), 'strict-origin-when-cross-origin')
        self.assertIn('youtube-nocookie.com/embed/MeU-KzdCBps?start=78&end=195', parser.attrs['src'])

    def make_pair(self):
        course = valid_v2_course()
        route = 'skills/khan-academy/SKILL.md'
        topic = course['chapters'][0]['topics'][0]
        topic['skill_routes'].append(route)
        topic['resource_ids'].append('khan-slope')
        course['sources']['khan-slope'] = {
            'title':'Intro to slope', 'type':'khan-video',
            'url':'https://www.khanacademy.org/math/algebra/v/introduction-to-slope',
            'youtube_id':'MeU-KzdCBps', 'checked_on':'2026-09-27',
            'sections':['Slope'], 'verification_notes':'Synthetic test fixture.'}
        lesson = valid_lesson(course)
        lesson['publication'] = 'draft'
        lesson['skill_routes'].append(route)
        lesson['blocks'][1] = {
            'id':'video', 'type':'khan-video', 'concepts':['math.derivative'],
            'source_id':'khan-slope', 'purpose':'Review rate.', 'text':'Compare changes.',
            'clip_start_seconds':78, 'clip_end_seconds':195,
            'production':{'skill_route':route, 'brief':'Inspect the clip.',
                'must_include':['Rate'], 'continuity':['Same axes'],
                'acceptance_checks':['Complete explanation'], 'depends_on_block_ids':['intro']}}
        return course, lesson

    def test_review_shows_neighbors_forms_and_course_reuse(self):
        course, lesson = self.make_pair()
        report = review(course, lesson)
        self.assertEqual(report['videos'][0]['previous_block'], 'intro')
        self.assertEqual(report['videos'][0]['next_block'], 'graph')
        self.assertEqual(report['videos'][0]['clip_seconds'], 117)
        self.assertIn('interactive-graph', report['other_block_types'])
        self.assertEqual(report['videos'][0]['course_topics_using_source'], ['local-change'])
        self.assertFalse(report['content_verified'])

    def test_video_only_sequence_is_flagged_not_certified(self):
        course, lesson = self.make_pair()
        lesson['blocks'] = [lesson['blocks'][1]]
        lesson['blocks'][0]['production']['depends_on_block_ids'] = []
        lesson['exercises'] = []
        report = review(course, lesson)
        self.assertTrue(report['warnings'])
        self.assertIsNone(report['videos'][0]['next_block'])

    def test_invalid_clip_is_rejected_by_existing_contract(self):
        course, lesson = self.make_pair()
        lesson['blocks'][1]['clip_end_seconds'] = 20
        with self.assertRaises(ValueError):
            review(course, lesson)


if __name__ == '__main__':
    unittest.main()
