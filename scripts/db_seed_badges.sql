-- EduBoost SA — Badge Definitions Seed
-- Seeds the `badges` table with all standard badge definitions.
-- Run: docker exec -i eduboost-postgres psql -U eduboost_user -d eduboost < scripts/db_seed_badges.sql

BEGIN;

INSERT INTO badges (badge_id, badge_key, name, description, badge_type, icon_url, grade_band) VALUES

-- ── Streak Badges ────────────────────────────────────────────────────────────
(gen_random_uuid(), 'streak_3',   '3-Day Streak',   'Complete lessons for 3 consecutive days',   'streak', '/badges/streak_3.png',   'all'),
(gen_random_uuid(), 'streak_7',   '7-Day Streak',   'Complete lessons for 7 consecutive days',   'streak', '/badges/streak_7.png',   'all'),
(gen_random_uuid(), 'streak_14',  '14-Day Streak',  'Complete lessons for 14 consecutive days',  'streak', '/badges/streak_14.png',  'all'),
(gen_random_uuid(), 'streak_30',  '30-Day Streak',  'Complete lessons for 30 consecutive days',  'streak', '/badges/streak_30.png',  'all'),
(gen_random_uuid(), 'streak_60',  '60-Day Streak',  'Complete lessons for 60 consecutive days',  'streak', '/badges/streak_60.png',  'all'),
(gen_random_uuid(), 'streak_100', '100-Day Streak', 'Complete lessons for 100 consecutive days', 'streak', '/badges/streak_100.png', 'all'),

-- ── Mastery Badges ───────────────────────────────────────────────────────────
(gen_random_uuid(), 'mastery_5',  'Quick Learner',    'Master 5 concepts',  'mastery', '/badges/mastery_5.png',  'all'),
(gen_random_uuid(), 'mastery_10', 'Knowledge Seeker', 'Master 10 concepts', 'mastery', '/badges/mastery_10.png', 'all'),
(gen_random_uuid(), 'mastery_25', 'Subject Expert',   'Master 25 concepts', 'mastery', '/badges/mastery_25.png', 'all'),

-- ── Milestone Badges (Grade R-3) ─────────────────────────────────────────────
(gen_random_uuid(), 'first_lesson', 'First Steps',       'Complete your first lesson', 'milestone', '/badges/first_lesson.png', 'R-3'),
(gen_random_uuid(), 'lessons_10',   'Dedicated Learner', 'Complete 10 lessons',        'milestone', '/badges/lessons_10.png',   'R-3'),
(gen_random_uuid(), 'lessons_50',   'Scholar',           'Complete 50 lessons',        'milestone', '/badges/lessons_50.png',   'R-3'),

-- ── Discovery Badges (Grade 4-7) ─────────────────────────────────────────────
(gen_random_uuid(), 'discovery_math',    'Math Explorer',       'Explore 5 different math topics',     'discovery', '/badges/discovery_math.png',    '4-7'),
(gen_random_uuid(), 'discovery_science', 'Science Explorer',    'Explore 5 different science topics',  'discovery', '/badges/discovery_science.png', '4-7'),
(gen_random_uuid(), 'discovery_english', 'Language Explorer',   'Explore 5 different language topics', 'discovery', '/badges/discovery_english.png', '4-7'),
(gen_random_uuid(), 'discovery_10',      'Curious Mind',        'Explore 10 different topics',         'discovery', '/badges/discovery_10.png',      '4-7'),
(gen_random_uuid(), 'discovery_25',      'Renaissance Learner', 'Explore 25 different topics',         'discovery', '/badges/discovery_25.png',      '4-7'),

-- ── Assessment Badges ────────────────────────────────────────────────────────
(gen_random_uuid(), 'perfect_score',    'Perfect Score',     'Achieve 100% on any assessment',    'assessment', '/badges/perfect_score.png',    'all'),
(gen_random_uuid(), 'assessments_5',    'Assessment Ace',    'Complete 5 assessments',            'assessment', '/badges/assessments_5.png',    'all'),
(gen_random_uuid(), 'assessments_20',   'Assessment Master', 'Complete 20 assessments',           'assessment', '/badges/assessments_20.png',   'all'),
(gen_random_uuid(), 'first_diagnostic', 'Brain Scanner',     'Complete your first diagnostic',    'assessment', '/badges/first_diagnostic.png', 'all')

ON CONFLICT (badge_key) DO NOTHING;

COMMIT;
