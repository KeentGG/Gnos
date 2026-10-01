#!/usr/bin/env python3
"""Validate a course/lesson pair and expose Khan placement for human review.

Read-only: no lesson publication, source verification, or learner progress.
Warnings are review prompts, not quotas or automatic pedagogical judgments.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'skills/course-design/scripts'))
from course_contract import validate_course
from lesson_contract import validate_lesson


def review(course, lesson):
    course = validate_course(course)
    lesson = validate_lesson(lesson, course)
    blocks = lesson['blocks']
    videos, warnings = [], []
    for index, block in enumerate(blocks):
        if block['type'] != 'khan-video':
            continue
        source = course['sources'][block['source_id']]
        start, end = block.get('clip_start_seconds'), block.get('clip_end_seconds')
        videos.append({
            'block_id': block['id'], 'source_id': block['source_id'],
            'title': source['title'], 'url': source['url'], 'youtube_id': source['youtube_id'],
            'purpose': block['purpose'], 'watch_prompt': block.get('text', ''),
            'clip_start_seconds': start, 'clip_end_seconds': end,
            'clip_seconds': end - start if start is not None else None,
            'previous_block': blocks[index - 1]['id'] if index else None,
            'next_block': blocks[index + 1]['id'] if index + 1 < len(blocks) else None,
            'checked_on': source['checked_on'], 'verification_notes': source['verification_notes'],
            'course_topics_using_source': [topic['id'] for chapter in course['chapters']
                for topic in chapter['topics'] if block['source_id'] in topic['resource_ids']],
        })
        if not index or index + 1 == len(blocks):
            warnings.append(f"{block['id']}: inspect the missing setup or return to GNOS teaching.")
        if index and blocks[index - 1]['type'] == 'khan-video':
            warnings.append(f"{block['id']}: consecutive videos need a distinct purpose and a connecting explanation.")
    other_types = sorted({block['type'] for block in blocks
                          if block['type'] not in {'khan-video', 'exercise', 'feedback'}})
    if videos and not other_types:
        warnings.append('Video-only teaching: develop GNOS explanation and representations for the remaining reasoning.')
    return {'lesson_id': lesson['id'], 'content_verified': False, 'videos': videos,
            'other_block_types': other_types, 'warnings': warnings,
            'review_required': ['Match each video to one section and learner action.',
                'Check the actual interval, duration, captions, and player.',
                'Preserve diagrams, derivations, code, or controls where they teach something else.',
                'Watching is exposure, not demonstrated understanding.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--course', required=True, type=Path)
    parser.add_argument('--lesson', required=True, type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(review(json.loads(args.course.read_text()),
                                json.loads(args.lesson.read_text())), indent=2))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
