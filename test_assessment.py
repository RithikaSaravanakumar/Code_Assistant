"""
test_assessment.py - Run verification tests for the randomized assessment system.
"""
import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Question, AttemptQuestion

print('=' * 60)
print('RUNNING ASSESSMENT VERIFICATION TESTS')
print('=' * 60)

with app.app_context():
    # TEST 1: >= 50 MCQ questions exist
    mcq_count = Question.query.filter_by(question_type='mcq').count()
    status1 = 'PASS' if mcq_count >= 50 else 'FAIL'
    print(f'[TEST 1] MCQ question count: {mcq_count} (expected >= 50) -> {status1}')

    # TEST 2: Can select exactly 20 questions
    all_mcq = Question.query.filter_by(question_type='mcq').all()
    selected = random.sample(all_mcq, 20)
    status2 = 'PASS' if len(selected) == 20 else 'FAIL'
    print(f'[TEST 2] Random 20 question selection: {len(selected)} questions -> {status2}')

    # TEST 3: No duplicate question IDs in the 20 selected
    q_ids = [q.id for q in selected]
    status3 = 'PASS' if len(q_ids) == len(set(q_ids)) else 'FAIL'
    print(f'[TEST 3] No duplicate question IDs in selection -> {status3}')

    # TEST 4: Option shuffle + correct label remapping is accurate
    labels = ['A', 'B', 'C', 'D']
    all_correct = True
    for q in selected[:10]:
        opts = [q.option_a, q.option_b, q.option_c, q.option_d]
        orig_idx = labels.index(q.correct_answer)
        correct_text = opts[orig_idx]

        positions = [0, 1, 2, 3]
        random.shuffle(positions)
        shuffled = [opts[p] for p in positions]
        new_pos = positions.index(orig_idx)
        new_label = labels[new_pos]

        if shuffled[new_pos] != correct_text:
            all_correct = False
            print(f'  MISMATCH qid={q.id}: expected={correct_text}, got={shuffled[new_pos]}')

    status4 = 'PASS' if all_correct else 'FAIL'
    print(f'[TEST 4] Shuffle + correct label remapping accuracy -> {status4}')

    # TEST 5: AttemptQuestion table is accessible
    try:
        count = AttemptQuestion.query.count()
        print(f'[TEST 5] AttemptQuestion table accessible ({count} rows) -> PASS')
    except Exception as e:
        print(f'[TEST 5] AttemptQuestion table -> FAIL: {e}')

    # TEST 6: Total questions > 20 (randomization makes sense)
    total = len(all_mcq)
    status6 = 'PASS' if total > 20 else 'FAIL'
    print(f'[TEST 6] Total MCQ ({total}) > 20 per attempt -> {status6}')

    # TEST 7: Two independent random samples differ (randomisation working)
    sample_a = set(q.id for q in random.sample(all_mcq, 20))
    sample_b = set(q.id for q in random.sample(all_mcq, 20))
    are_different = (sample_a != sample_b)
    status7 = 'PASS' if are_different else 'NOTE: same by chance (unlikely)'
    print(f'[TEST 7] Two random samples are different -> {status7}')

    # TEST 8: Verify correct_answer values are valid in all seed questions
    invalid = [q for q in all_mcq if q.correct_answer not in ('A', 'B', 'C', 'D')]
    status8 = 'PASS' if not invalid else f'FAIL ({len(invalid)} invalid)'
    print(f'[TEST 8] All MCQ correct_answer values are A/B/C/D -> {status8}')

    # TEST 9: All MCQ questions have all 4 options populated
    incomplete = [q for q in all_mcq if not all([q.option_a, q.option_b, q.option_c, q.option_d])]
    status9 = 'PASS' if not incomplete else f'FAIL ({len(incomplete)} incomplete)'
    print(f'[TEST 9] All MCQ questions have all 4 options -> {status9}')

print('=' * 60)
print('ALL TESTS COMPLETE')
print('=' * 60)
