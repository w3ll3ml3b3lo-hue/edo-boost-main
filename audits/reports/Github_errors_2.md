Run ruff:

Run ruff check app/ tests/ --output-format=github
Error: app/api/services/diagnostic_benchmark_service.py:218:31: F821 Undefined name `Any`
Error: app/api/services/diagnostic_benchmark_service.py:285:29: F821 Undefined name `Any`
Error: app/api/services/lesson_service.py:12:24: F401 `sqlalchemy.text` imported but unused
  help: Remove unused import: `sqlalchemy.text`
Error: tests/integration/conftest.py:1:8: F401 `pytest` imported but unused
  help: Remove unused import: `pytest`
Error: tests/unit/test_study_plan_service.py:14:47: F401 `app.api.judiciary.provider_router.ProviderRouter` imported but unused
  help: Remove unused import: `app.api.judiciary.provider_router.ProviderRouter`
Error: tests/unit/test_study_plan_service.py:15:38: F401 `app.api.judiciary.client.JudiciaryClient` imported but unused
  help: Remove unused import: `app.api.judiciary.client.JudiciaryClient`
Error: Process completed with exit code 1.

*********************************************************************************************************************

Unit Tests

Run pytest tests/unit/ \
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-8.2.1, pluggy-1.6.0 -- /opt/hostedtoolcache/Python/3.11.15/x64/bin/python
cachedir: .pytest_cache
rootdir: /home/runner/work/edo-boost-main/edo-boost-main
configfile: pytest.ini
plugins: mock-3.14.0, timeout-2.3.1, cov-5.0.0, anyio-4.13.0, asyncio-0.23.7, Faker-25.2.0
asyncio: mode=Mode.AUTO
collecting ... collected 186 items

tests/unit/test_constitutional_schema.py::TestConstitutionalRule::test_rule_is_immutable PASSED [  0%]
tests/unit/test_constitutional_schema.py::TestConstitutionalRule::test_popia_01_is_critical PASSED [  1%]
tests/unit/test_constitutional_schema.py::TestConstitutionalRule::test_pii_01_is_critical PASSED [  1%]
tests/unit/test_constitutional_schema.py::TestConstitutionalRule::test_child_01_is_critical PASSED [  2%]
tests/unit/test_constitutional_schema.py::TestConstitutionalRule::test_caps_01_applies_to_lesson PASSED [  2%]
tests/unit/test_constitutional_schema.py::TestConstitutionalRule::test_popia_03_applies_to_all_actions PASSED [  3%]
tests/unit/test_constitutional_schema.py::TestConstitutionalRule::test_corpus_has_minimum_rules PASSED [  3%]
tests/unit/test_constitutional_schema.py::TestConstitutionalRule::test_all_rules_have_check_prompts PASSED [  4%]
tests/unit/test_constitutional_schema.py::TestConstitutionalRule::test_all_rules_have_sources PASSED [  4%]
tests/unit/test_constitutional_schema.py::TestRuleRetrieval::test_get_rules_for_lesson_generation PASSED [  5%]
tests/unit/test_constitutional_schema.py::TestRuleRetrieval::test_get_critical_rules_lesson PASSED [  5%]
tests/unit/test_constitutional_schema.py::TestRuleRetrieval::test_get_rules_for_diagnostic PASSED [  6%]
tests/unit/test_constitutional_schema.py::TestRuleRetrieval::test_inactive_rules_excluded PASSED [  6%]
tests/unit/test_constitutional_schema.py::TestRuleRetrieval::test_unknown_action_returns_empty PASSED [  7%]
tests/unit/test_constitutional_schema.py::TestExecutiveAction::test_valid_action_created PASSED [  8%]
tests/unit/test_constitutional_schema.py::TestExecutiveAction::test_learner_id_rejected_in_params PASSED [  8%]
tests/unit/test_constitutional_schema.py::TestExecutiveAction::test_guardian_email_rejected_in_params PASSED [  9%]
tests/unit/test_constitutional_schema.py::TestExecutiveAction::test_grade_range_validated PASSED [  9%]
tests/unit/test_constitutional_schema.py::TestExecutiveAction::test_action_id_is_uuid_string PASSED [ 10%]
tests/unit/test_constitutional_schema.py::TestJudiciaryStamp::test_approved_stamp PASSED [ 10%]
tests/unit/test_constitutional_schema.py::TestJudiciaryStamp::test_rejected_stamp_has_violations PASSED [ 11%]
tests/unit/test_constitutional_schema.py::TestJudiciaryStamp::test_stamp_is_immutable PASSED [ 11%]
tests/unit/test_constitutional_schema.py::TestAuditEvent::test_audit_event_creation PASSED [ 12%]
tests/unit/test_constitutional_schema.py::TestAuditEvent::test_audit_event_is_immutable PASSED [ 12%]
tests/unit/test_constitutional_schema.py::TestEtherProfile::test_prompt_modifier_contains_archetype PASSED [ 13%]
tests/unit/test_constitutional_schema.py::TestEtherProfile::test_all_archetypes_have_prompt_modifiers PASSED [ 13%]
tests/unit/test_constitutional_schema.py::TestEtherProfile::test_ether_tone_params_defaults_valid PASSED [ 14%]
tests/unit/test_constitutional_schema.py::TestOperationResult::test_success_result PASSED [ 15%]
tests/unit/test_constitutional_schema.py::TestOperationResult::test_failure_result PASSED [ 15%]
tests/unit/test_five_pillars.py::TestConstitutionalRuleImmutability::test_hash_is_computed_on_construction PASSED [ 16%]
tests/unit/test_five_pillars.py::TestConstitutionalRuleImmutability::test_hash_is_deterministic PASSED [ 16%]
tests/unit/test_five_pillars.py::TestConstitutionalRuleImmutability::test_verify_returns_true_for_unmodified_rule PASSED [ 17%]
tests/unit/test_five_pillars.py::TestConstitutionalRuleImmutability::test_pydantic_frozen_prevents_mutation PASSED [ 17%]
tests/unit/test_five_pillars.py::TestConstitutionalRuleImmutability::test_different_text_produces_different_hash PASSED [ 18%]
tests/unit/test_five_pillars.py::TestConstitutionalRuleImmutability::test_orm_update_event_raises PASSED [ 18%]
tests/unit/test_five_pillars.py::TestConstitutionalRuleImmutability::test_orm_delete_event_raises PASSED [ 19%]
tests/unit/test_five_pillars.py::TestPIIScrubber::test_clean_text_passes PASSED [ 19%]
tests/unit/test_five_pillars.py::TestPIIScrubber::test_sa_id_number_detected PASSED [ 20%]
tests/unit/test_five_pillars.py::TestPIIScrubber::test_email_detected PASSED [ 20%]
tests/unit/test_five_pillars.py::TestPIIScrubber::test_sa_mobile_detected PASSED [ 21%]
tests/unit/test_five_pillars.py::TestPIIScrubber::test_assert_pii_clean_raises_on_pii PASSED [ 22%]
tests/unit/test_five_pillars.py::TestPIIScrubber::test_assert_pii_clean_passes_clean_text PASSED [ 22%]
tests/unit/test_five_pillars.py::TestPIIScrubber::test_multiple_pii_types_detected PASSED [ 23%]
tests/unit/test_five_pillars.py::TestWorkerAgentStampGate::test_approved_stamp_unblocks_execution PASSED [ 23%]
tests/unit/test_five_pillars.py::TestWorkerAgentStampGate::test_rejected_stamp_raises_unauthorized PASSED [ 24%]
tests/unit/test_five_pillars.py::TestWorkerAgentStampGate::test_assert_stamped_raises_without_prior_stamp PASSED [ 24%]
tests/unit/test_five_pillars.py::TestWorkerAgentStampGate::test_hmac_signature_verification PASSED [ 25%]
tests/unit/test_five_pillars.py::TestWorkerAgentStampGate::test_tampered_signature_fails_verification PASSED [ 25%]
tests/unit/test_five_pillars.py::TestJudiciaryFastPath::test_sa_id_number_triggers_fast_rejection PASSED [ 26%]
tests/unit/test_five_pillars.py::TestJudiciaryFastPath::test_email_in_params_triggers_fast_rejection PASSED [ 26%]
tests/unit/test_five_pillars.py::TestJudiciaryFastPath::test_clean_action_passes_fast_path PASSED [ 27%]
tests/unit/test_five_pillars.py::TestConsentGate::test_active_consent_passes PASSED [ 27%]
tests/unit/test_five_pillars.py::TestConsentGate::test_no_consent_raises_permission_error PASSED [ 28%]
tests/unit/test_five_pillars.py::TestConsentGate::test_revoked_consent_raises_permission_error PASSED [ 29%]
tests/unit/test_five_pillars.py::TestSessionOrchestrator::test_valid_transition_succeeds PASSED [ 29%]
tests/unit/test_five_pillars.py::TestSessionOrchestrator::test_invalid_transition_raises PASSED [ 30%]
tests/unit/test_five_pillars.py::TestSessionOrchestrator::test_suspended_learner_cannot_transition_except_to_archived PASSED [ 30%]
tests/unit/test_five_pillars.py::TestIRTEngine::test_parameter_update_creates_new_version PASSED [ 31%]
tests/unit/test_five_pillars.py::TestIRTEngine::test_irt_3pl_probability_bounds PASSED [ 31%]
tests/unit/test_five_pillars.py::TestIRTEngine::test_eap_update_increases_theta_on_correct PASSED [ 32%]
tests/unit/test_five_pillars.py::TestIRTEngine::test_eap_update_decreases_theta_on_incorrect PASSED [ 32%]
tests/unit/test_five_pillars.py::TestEtherProfiler::test_build_profile_returns_valid_sephira PASSED [ 33%]
tests/unit/test_five_pillars.py::TestEtherProfiler::test_profile_decay_toward_neutral PASSED [ 33%]
tests/unit/test_five_pillars.py::TestEtherProfiler::test_decay_zero_days_unchanged PASSED [ 34%]
tests/unit/test_fourth_estate.py::TestEventPublishing::test_publish_increments_event_count PASSED [ 34%]
tests/unit/test_fourth_estate.py::TestEventPublishing::test_published_event_in_buffer PASSED [ 35%]
tests/unit/test_fourth_estate.py::TestEventPublishing::test_publish_action_submitted PASSED [ 36%]
tests/unit/test_fourth_estate.py::TestEventPublishing::test_publish_approved_stamp PASSED [ 36%]
tests/unit/test_fourth_estate.py::TestEventPublishing::test_publish_rejected_stamp_creates_violation_event PASSED [ 37%]
tests/unit/test_fourth_estate.py::TestEventPublishing::test_violation_increments_violation_count PASSED [ 37%]
tests/unit/test_fourth_estate.py::TestEventPublishing::test_publish_llm_success PASSED [ 38%]
tests/unit/test_fourth_estate.py::TestEventPublishing::test_publish_llm_failure PASSED [ 38%]
tests/unit/test_fourth_estate.py::TestEventPublishing::test_publish_ether_cache_hit PASSED [ 39%]
tests/unit/test_fourth_estate.py::TestEventPublishing::test_publish_ether_cache_miss PASSED [ 39%]
tests/unit/test_fourth_estate.py::TestBufferBehaviour::test_buffer_caps_at_1000_events PASSED [ 40%]
tests/unit/test_fourth_estate.py::TestBufferBehaviour::test_get_recent_events_returns_n PASSED [ 40%]
tests/unit/test_fourth_estate.py::TestBufferBehaviour::test_most_recent_events_returned_last PASSED [ 41%]
tests/unit/test_fourth_estate.py::TestStats::test_initial_stats_zero PASSED [ 41%]
tests/unit/test_fourth_estate.py::TestStats::test_stats_contains_stream_key PASSED [ 42%]
tests/unit/test_fourth_estate.py::TestRedisDegradation::test_publishes_without_redis PASSED [ 43%]
tests/unit/test_fourth_estate.py::TestFourthEstateSingleton::test_singleton PASSED [ 43%]
tests/unit/test_fourth_estate_circuit_breaker.py::test_fourth_estate_circuit_breaker_flow PASSED [ 44%]
tests/unit/test_fourth_estate_circuit_breaker.py::test_fourth_estate_circuit_breaker_reopen PASSED [ 44%]
tests/unit/test_gamification.py::test_streak_grace_period PASSED         [ 45%]
tests/unit/test_gamification.py::test_mastery_badge_award PASSED         [ 45%]
tests/unit/test_gamification_service.py::TestGamificationXPCalculation::test_calculate_level_from_xp PASSED [ 46%]
tests/unit/test_gamification_service.py::TestGamificationXPCalculation::test_xp_to_next_level_calculation PASSED [ 46%]
tests/unit/test_gamification_service.py::TestGamificationXPCalculation::test_level_min_is_one PASSED [ 47%]
tests/unit/test_gamification_service.py::TestGamificationXPCalculation::test_award_xp_lesson_complete PASSED [ 47%]
tests/unit/test_gamification_service.py::TestGamificationXPCalculation::test_award_xp_with_streak_bonus PASSED [ 48%]
tests/unit/test_gamification_service.py::TestGamificationXPCalculation::test_level_up_detection PASSED [ 48%]
tests/unit/test_gamification_service.py::TestGamificationBadges::test_available_badges_for_grade_r3 PASSED [ 49%]
tests/unit/test_gamification_service.py::TestGamificationBadges::test_available_badges_for_grade_4plus PASSED [ 50%]
tests/unit/test_gamification_service.py::TestGamificationBadges::test_badge_thresholds_are_realistic PASSED [ 50%]
tests/unit/test_gamification_service.py::TestGamificationBadges::test_streaks_badges_exist PASSED [ 51%]
tests/unit/test_gamification_service.py::TestGamificationProfileGeneration::test_get_learner_profile_junior PASSED [ 51%]
tests/unit/test_gamification_service.py::TestGamificationProfileGeneration::test_get_learner_profile_senior PASSED [ 52%]
tests/unit/test_gamification_service.py::TestGamificationProfileGeneration::test_learner_not_found_raises_error PASSED [ 52%]
tests/unit/test_gamification_service.py::TestGamificationProfileGeneration::test_earned_badges_are_included_in_profile PASSED [ 53%]
tests/unit/test_gamification_service.py::TestGamificationStreakLogic::test_streak_bonus_increases_with_days PASSED [ 53%]
tests/unit/test_gamification_service.py::TestGamificationStreakLogic::test_streak_thresholds_are_ordered PASSED [ 54%]
tests/unit/test_gamification_service.py::TestGamificationXPConfig::test_xp_config_is_complete PASSED [ 54%]
tests/unit/test_gamification_service.py::TestGamificationXPConfig::test_xp_values_are_reasonable PASSED [ 55%]
tests/unit/test_gamification_service.py::TestGamificationXPConfig::test_grade_band_config_complete PASSED [ 55%]
tests/unit/test_gamification_service.py::TestGamificationMetrics::test_xp_awarded_metric PASSED [ 56%]
tests/unit/test_gamification_service.py::TestGamificationMetrics::test_badge_awarded_metric PASSED [ 56%]
tests/unit/test_irt_benchmarks.py::test_irt_convergence PASSED           [ 57%]
tests/unit/test_irt_engine.py::TestIRTCore::test_p_correct_at_matching_difficulty PASSED [ 58%]
tests/unit/test_irt_engine.py::TestIRTCore::test_p_correct_increases_with_theta PASSED [ 58%]
tests/unit/test_irt_engine.py::TestIRTCore::test_fisher_information_peaks_at_difficulty PASSED [ 59%]
tests/unit/test_irt_engine.py::TestIRTCore::test_compute_mastery_score_range PASSED [ 59%]
tests/unit/test_irt_engine.py::TestIRTCore::test_compute_mastery_score_midpoint PASSED [ 60%]
tests/unit/test_irt_engine.py::TestThetaUpdate::test_theta_increases_after_correct_answers PASSED [ 60%]
tests/unit/test_irt_engine.py::TestThetaUpdate::test_sem_decreases_with_more_responses PASSED [ 61%]
tests/unit/test_irt_engine.py::TestThetaUpdate::test_empty_responses_returns_defaults PASSED [ 61%]
tests/unit/test_irt_engine.py::TestAdaptiveSelection::test_selects_item_for_current_grade PASSED [ 62%]
tests/unit/test_irt_engine.py::TestAdaptiveSelection::test_excludes_administered_items PASSED [ 62%]
tests/unit/test_irt_engine.py::TestStoppingRules::test_stops_when_max_questions_reached PASSED [ 63%]
tests/unit/test_irt_engine.py::TestStoppingRules::test_stops_when_sem_low PASSED [ 63%]
tests/unit/test_irt_engine.py::TestStoppingRules::test_continues_when_sem_high PASSED [ 64%]
tests/unit/test_irt_engine.py::TestGapProbe::test_triggers_when_theta_below_floor PASSED [ 65%]
tests/unit/test_irt_engine.py::TestGapProbe::test_does_not_trigger_above_floor PASSED [ 65%]
tests/unit/test_irt_engine.py::TestGapProbe::test_probe_decrements_grade PASSED [ 66%]
tests/unit/test_irt_engine.py::TestGapProbe::test_probe_stops_at_grade_r PASSED [ 66%]
tests/unit/test_irt_engine.py::TestGapReport::test_report_has_required_fields PASSED [ 67%]
tests/unit/test_irt_engine.py::TestGapReport::test_low_mastery_flagged_as_gap PASSED [ 67%]
tests/unit/test_judiciary.py::TestPIIScanning::test_uuid_in_system_prompt_rejected PASSED [ 68%]
tests/unit/test_judiciary.py::TestPIIScanning::test_uuid_in_user_prompt_rejected PASSED [ 68%]
tests/unit/test_judiciary.py::TestPIIScanning::test_email_in_prompt_rejected PASSED [ 69%]
tests/unit/test_judiciary.py::TestPIIScanning::test_sa_id_number_in_prompt_rejected PASSED [ 69%]
tests/unit/test_judiciary.py::TestPIIScanning::test_clean_prompts_pass_pii_scan PASSED [ 70%]
tests/unit/test_judiciary.py::TestPIIScanning::test_no_prompts_passes_pii_scan PASSED [ 70%]
tests/unit/test_judiciary.py::TestStructuralValidation::test_has_gap_without_gap_grade_rejected PASSED [ 71%]
tests/unit/test_judiciary.py::TestStructuralValidation::test_gap_grade_equal_to_grade_rejected PASSED [ 72%]
tests/unit/test_judiciary.py::TestStructuralValidation::test_valid_gap_grade_passes PASSED [ 72%]
tests/unit/test_judiciary.py::TestStructuralValidation::test_unexpected_param_keys_flagged PASSED [ 73%]
tests/unit/test_judiciary.py::TestStructuralValidation::test_clean_lesson_params_approved PASSED [ 73%]
tests/unit/test_judiciary.py::TestStampProperties::test_stamp_records_rules_evaluated PASSED [ 74%]
tests/unit/test_judiciary.py::TestStampProperties::test_stamp_has_latency PASSED [ 74%]
tests/unit/test_judiciary.py::TestStampProperties::test_stamp_has_reasoning PASSED [ 75%]
tests/unit/test_judiciary.py::TestStampProperties::test_rejection_increments_counter PASSED [ 75%]
tests/unit/test_judiciary.py::TestStampProperties::test_approval_increments_stamp_count PASSED [ 76%]
tests/unit/test_judiciary.py::TestJudiciarySingleton::test_singleton_returns_same_instance PASSED [ 76%]
tests/unit/test_judiciary.py::TestJudiciarySingleton::test_stats_structure PASSED [ 77%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_removes_sa_id_number PASSED [ 77%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_removes_email_address PASSED [ 78%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_removes_sa_mobile_number PASSED [ 79%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_preserves_non_pii_content PASSED [ 79%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_scrubs_dict_recursively PASSED [ 80%]
tests/unit/test_pii_scrubber.py::TestPIIScrubber::test_does_not_alter_lesson_content PASSED [ 80%]
tests/unit/test_profiler.py::TestSignalExtraction::test_empty_events_returns_defaults PASSED [ 81%]
tests/unit/test_profiler.py::TestSignalExtraction::test_all_correct_accuracy_is_1 PASSED [ 81%]
tests/unit/test_profiler.py::TestSignalExtraction::test_all_wrong_accuracy_is_0 PASSED [ 82%]
tests/unit/test_profiler.py::TestSignalExtraction::test_fast_response_speed_norm_high PASSED [ 82%]
tests/unit/test_profiler.py::TestSignalExtraction::test_slow_response_speed_norm_low PASSED [ 83%]
tests/unit/test_profiler.py::TestSignalExtraction::test_hint_rate_computed_correctly PASSED [ 83%]
tests/unit/test_profiler.py::TestArchetypeClassification::test_high_ability_fast_maps_to_keter_region PASSED [ 84%]
tests/unit/test_profiler.py::TestArchetypeClassification::test_struggling_learner_maps_to_foundation_archetype PASSED [ 84%]
tests/unit/test_profiler.py::TestArchetypeClassification::test_empty_events_returns_default_archetype PASSED [ 85%]
tests/unit/test_profiler.py::TestArchetypeClassification::test_confidence_in_valid_range PASSED [ 86%]
tests/unit/test_profiler.py::TestArchetypeClassification::test_all_archetypes_are_classifiable PASSED [ 86%]
tests/unit/test_profiler.py::TestParameterTuning::test_high_hint_rate_increases_encouragement PASSED [ 87%]
tests/unit/test_profiler.py::TestParameterTuning::test_low_accuracy_slows_pacing PASSED [ 87%]
tests/unit/test_profiler.py::TestParameterTuning::test_high_ability_speeds_up_pacing PASSED [ 88%]
tests/unit/test_profiler.py::TestColdStart::test_cold_start_returns_tiferet PASSED [ 88%]
tests/unit/test_profiler.py::TestColdStart::test_cold_start_has_expires_at PASSED [ 89%]
tests/unit/test_profiler.py::TestColdStart::test_learner_hash_is_not_learner_id PASSED [ 89%]
tests/unit/test_profiler.py::TestComputeAndCache::test_compute_profile_from_events PASSED [ 90%]
tests/unit/test_profiler.py::TestComputeAndCache::test_profile_tone_params_valid PASSED [ 90%]
tests/unit/test_profiler.py::TestArchetypeDefaults::test_all_archetypes_have_defaults PASSED [ 91%]
tests/unit/test_profiler.py::TestArchetypeDefaults::test_all_defaults_have_valid_tone_params PASSED [ 91%]
tests/unit/test_profiler.py::TestProfilerSingleton::test_singleton_returns_same_instance PASSED [ 92%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_plan_with_valid_learner SKIPPED [ 93%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_plan_learner_not_found PASSED [ 93%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_prioritize_subjects_high_gap_first PASSED [ 94%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_remediation_tasks_creates_gap_specific_tasks PASSED [ 94%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_grade_tasks_creates_advancement_tasks PASSED [ 95%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_weekly_schedule_distribution PASSED [ 95%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_gap_ratio_affects_remediation_distribution PASSED [ 96%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_grade_band_determines_focus_areas PASSED [ 96%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_determine_week_focus_from_gaps PASSED [ 97%]
tests/unit/test_study_plan_service.py::TestStudyPlanValidation::test_gap_ratio_validation_bounds PASSED [ 97%]
tests/unit/test_study_plan_service.py::TestStudyPlanValidation::test_schedule_has_all_days PASSED [ 98%]
tests/unit/test_study_plan_service.py::TestStudyPlanAlgorithmQuality::test_consistent_task_distribution PASSED [ 98%]
tests/unit/test_study_plan_service.py::TestStudyPlanAlgorithmQuality::test_no_empty_schedules PASSED [ 99%]
tests/unit/test_study_plan_service.py::TestStudyPlanAlgorithmQuality::test_prioritization_ranks_subjects_logically PASSED [100%]

=============================== warnings summary ===============================
tests/unit/test_gamification_service.py::TestGamificationMetrics::test_badge_awarded_metric
  /home/runner/work/edo-boost-main/edo-boost-main/app/api/services/gamification_service.py:388: RuntimeWarning: coroutine 'AsyncMockMixin._execute_mock_call' was never awaited
    self.session.add(learner_badge)
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

---------- coverage: platform linux, python 3.11.15-final-0 ----------
Name                                               Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------
app/__init__.py                                        0      0   100%
app/api/__init__.py                                    0      0   100%
app/api/constitutional_schema/__init__.py              3      0   100%
app/api/constitutional_schema/schema.py               25      4    84%   152-155
app/api/constitutional_schema/types.py               138      2    99%   112, 115
app/api/core/__init__.py                               0      0   100%
app/api/core/audit_helpers.py                         26     26     0%   7-170
app/api/core/celery_app.py                            23     23     0%   11-137
app/api/core/config.py                                95     13    86%   129, 137-172
app/api/core/database.py                              34     15    56%   22, 43-57, 66
app/api/core/metrics.py                               54     35    35%   119-163
app/api/core/pii_patterns.py                          36     16    56%   30, 32, 43-47, 51-59
app/api/fourth_estate.py                             111     19    83%   55, 196, 208, 212-217, 234-236, 244, 247-253
app/api/judiciary/__init__.py                          5      0   100%
app/api/judiciary/agent.py                           102    102     0%   6-260
app/api/judiciary/audit_agent.py                     110    110     0%   8-278
app/api/judiciary/base.py                             77      3    96%   124, 157, 177
app/api/judiciary/client.py                           26     15    42%   26-37, 47-56
app/api/judiciary/compliance.py                       89     44    51%   106-125, 129-140, 145-147, 176, 183-214, 218-242, 245-247
app/api/judiciary/engine.py                          104     54    48%   83-95, 152-163, 166-175, 185-212, 225, 228-231, 234-259, 262-281, 285-319
app/api/judiciary/legacy.py                           91     25    73%   73, 124-157
app/api/judiciary/main.py                             53     53     0%   7-138
app/api/judiciary/models.py                          147      1    99%   105
app/api/judiciary/profiler.py                         70     19    73%   192-193, 201-208, 212-226, 238-248
app/api/judiciary/provider_router.py                  92     63    32%   43, 46-48, 55-59, 63-71, 75-84, 92-99, 107-114, 127-157, 162-198, 206-208, 221
app/api/judiciary/service.py                         117     71    39%   77-109, 112-120, 141-143, 148, 156-167, 176-221, 234-251, 260-270, 276, 281-306, 318-328, 334-346
app/api/judiciary/services.py                         88     88     0%   6-276
app/api/judiciary/state_machine.py                    74     24    68%   84-86, 94-111, 132, 159-163, 175-195, 204-216
app/api/judiciary/streams.py                          86     86     0%   7-190
app/api/main.py                                       82     82     0%   5-189
app/api/ml/__init__.py                                 0      0   100%
app/api/ml/irt_engine.py                              93      2    98%   83, 116
app/api/models/__init__.py                             0      0   100%
app/api/models/api_models.py                         154    154     0%   3-228
app/api/models/db_models.py                          294      0   100%
app/api/orchestrator.py                               37     37     0%   6-86
app/api/profiler.py                                   83      2    98%   169-170
app/api/routers/__init__.py                            0      0   100%
app/api/routers/assessments.py                       121    121     0%   7-367
app/api/routers/audit.py                              75     75     0%   7-184
app/api/routers/auth.py                              187    187     0%   3-430
app/api/routers/diagnostic.py                        195    195     0%   3-731
app/api/routers/gamification.py                       72     72     0%   3-116
app/api/routers/health.py                              9      9     0%   1-18
app/api/routers/learners.py                           99     99     0%   3-375
app/api/routers/lessons.py                           101    101     0%   3-327
app/api/routers/parent.py                            184    184     0%   3-332
app/api/routers/study_plans.py                        74     74     0%   3-206
app/api/routers/system.py                            154    154     0%   3-421
app/api/services/__init__.py                           0      0   100%
app/api/services/audit_query_service.py              119    119     0%   8-370
app/api/services/diagnostic_benchmark_service.py     130    130     0%   11-346
app/api/services/dummy_data_service.py                78     78     0%   9-176
app/api/services/gamification_service.py             178     59    67%   55, 65-70, 86-87, 213, 217, 255-256, 276-291, 341-374, 403-412, 423-441, 447, 458, 464-473, 490-495
app/api/services/inference_gateway.py                145    103    29%   90-101, 105-113, 119-135, 149-200, 205, 219-290, 295-303
app/api/services/lesson_service.py                   118    118     0%   6-266
app/api/services/parent_portal_service.py             79     79     0%   6-274
app/api/services/popia_deletion_service.py           126    126     0%   11-433
app/api/services/prompt_manager.py                    25     14    44%   20-33, 38
app/api/services/study_plan_service.py               108     56    48%   48, 66-101, 104-120, 123-134, 158-164, 169-185, 194-197, 211-225, 236-238, 243, 282-283
app/api/tasks/__init__.py                              0      0   100%
app/api/tasks/plan_tasks.py                           68     68     0%   3-171
app/api/tasks/report_tasks.py                         35     35     0%   3-70
--------------------------------------------------------------------------------
TOTAL                                               5099   3444    32%
Coverage HTML written to dir coverage_html
Coverage XML written to file coverage.xml

FAIL Required test coverage of 80% not reached. Total coverage: 32.46%
================== 185 passed, 1 skipped, 1 warning in 7.64s ===================
Error: Process completed with exit code 1.


********************************************************************************************************************************************


Integration tests errors:

================= 31 failed, 61 passed, 91 warnings in 12.45s ==================


********************************************************************************************************************************************


Schema tests errors:

Run alembic upgrade head
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.11.15/x64/bin/alembic", line 6, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/alembic/config.py", line 641, in main
    CommandLine(prog=prog).main(argv=argv)
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/alembic/config.py", line 631, in main
    self.run_cmd(cfg, options)
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/alembic/config.py", line 608, in run_cmd
    fn(
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/alembic/command.py", line 403, in upgrade
    script.run_env()
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/alembic/script/base.py", line 583, in run_env
    util.load_python_file(self.dir, "env.py")
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/alembic/util/pyfiles.py", line 95, in load_python_file
    module = load_module_py(module_id, path)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/alembic/util/pyfiles.py", line 113, in load_module_py
    spec.loader.exec_module(module)  # type: ignore
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/runner/work/edo-boost-main/edo-boost-main/alembic/env.py", line 10, in <module>
    from app.api.core.config import settings
  File "/home/runner/work/edo-boost-main/edo-boost-main/app/api/core/config.py", line 180, in <module>
    settings = get_settings()
               ^^^^^^^^^^^^^^
  File "/home/runner/work/edo-boost-main/edo-boost-main/app/api/core/config.py", line 177, in get_settings
    return Settings()
           ^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/pydantic_settings/main.py", line 84, in __init__
    super().__init__(
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/pydantic/main.py", line 176, in __init__
    self.__pydantic_validator__.validate_python(data, self_instance=self)
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
  Value error, JWT_SECRET must be set outside test environments [type=value_error, input_value={'DATABASE_URL': 'postgre...ost:5432/eduboost_test'}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.7/v/value_error
Error: Process completed with exit code 1.

********************************************************************************************************************************************


POPIA compliance tests errors:

Run pytest tests/popia/ -v --tb=short -k "pii or consent or erasure"
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-8.2.1, pluggy-1.6.0 -- /opt/hostedtoolcache/Python/3.11.15/x64/bin/python
cachedir: .pytest_cache
rootdir: /home/runner/work/edo-boost-main/edo-boost-main
configfile: pytest.ini
plugins: mock-3.14.0, timeout-2.3.1, cov-5.0.0, anyio-4.13.0, asyncio-0.23.7, Faker-25.2.0
asyncio: mode=Mode.AUTO
collecting ... collected 1 item / 1 deselected / 0 selected


---------- coverage: platform linux, python 3.11.15-final-0 ----------
Name                                               Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------
app/__init__.py                                        0      0   100%
app/api/__init__.py                                    0      0   100%
app/api/constitutional_schema/__init__.py              3      0   100%
app/api/constitutional_schema/schema.py               25      6    76%   138, 144, 152-155
app/api/constitutional_schema/types.py               138     12    91%   106-116, 165
app/api/core/__init__.py                               0      0   100%
app/api/core/audit_helpers.py                         26     26     0%   7-170
app/api/core/celery_app.py                            23     23     0%   11-137
app/api/core/config.py                                95     13    86%   129, 137-172
app/api/core/database.py                              34     19    44%   22, 43-57, 65-72
app/api/core/metrics.py                               54     35    35%   119-163
app/api/core/pii_patterns.py                          36     26    28%   29-63
app/api/fourth_estate.py                             111    111     0%   1-265
app/api/judiciary/__init__.py                          5      0   100%
app/api/judiciary/agent.py                           102    102     0%   6-260
app/api/judiciary/audit_agent.py                     110    110     0%   8-278
app/api/judiciary/base.py                             77     35    55%   54-55, 58-59, 62-66, 95-99, 120-138, 145-160, 173-180, 187-188
app/api/judiciary/client.py                           26     26     0%   5-56
app/api/judiciary/compliance.py                       89     89     0%   5-247
app/api/judiciary/engine.py                          104    104     0%   8-319
app/api/judiciary/legacy.py                           91     69    24%   45-51, 54-57, 66-76, 79-91, 99-166, 178-180
app/api/judiciary/main.py                             53     53     0%   7-138
app/api/judiciary/models.py                          147      9    94%   55, 63, 88-90, 93-97, 101, 105
app/api/judiciary/profiler.py                         70     70     0%   7-248
app/api/judiciary/provider_router.py                  92     63    32%   43, 46-48, 55-59, 63-71, 75-84, 92-99, 107-114, 127-157, 162-198, 206-208, 221
app/api/judiciary/service.py                         117    117     0%   9-346
app/api/judiciary/services.py                         88     88     0%   6-276
app/api/judiciary/state_machine.py                    74     74     0%   7-216
app/api/judiciary/streams.py                          86     86     0%   7-190
app/api/main.py                                       82     82     0%   5-189
app/api/ml/__init__.py                                 0      0   100%
app/api/ml/irt_engine.py                              93     93     0%   7-304
app/api/models/__init__.py                             0      0   100%
app/api/models/api_models.py                         154      0   100%
app/api/models/db_models.py                          294      0   100%
app/api/orchestrator.py                               37     37     0%   6-86
app/api/profiler.py                                   83     83     0%   3-221
app/api/routers/__init__.py                            0      0   100%
app/api/routers/assessments.py                       121    121     0%   7-367
app/api/routers/audit.py                              75     75     0%   7-184
app/api/routers/auth.py                              187    137    27%   40-45, 50-57, 64-81, 87-95, 102-129, 133-140, 171-204, 217-257, 268-298, 308-329, 335-336, 349-386, 399-430
app/api/routers/diagnostic.py                        195    195     0%   3-731
app/api/routers/gamification.py                       72     72     0%   3-116
app/api/routers/health.py                              9      9     0%   1-18
app/api/routers/learners.py                           99     99     0%   3-375
app/api/routers/lessons.py                           101    101     0%   3-327
app/api/routers/parent.py                            184    138    25%   28-32, 48-51, 55-62, 75-90, 102, 114-127, 136-149, 162-178, 192-219, 228-239, 248-259, 268-280, 289-301, 308-332
app/api/routers/study_plans.py                        74     74     0%   3-206
app/api/routers/system.py                            154    154     0%   3-421
app/api/services/__init__.py                           0      0   100%
app/api/services/audit_query_service.py              119    119     0%   8-370
app/api/services/diagnostic_benchmark_service.py     130    130     0%   11-346
app/api/services/dummy_data_service.py                78     78     0%   9-176
app/api/services/gamification_service.py             178    178     0%   8-495
app/api/services/inference_gateway.py                145    116    20%   59-73, 78-80, 90-101, 105-113, 119-135, 149-200, 205, 219-290, 295-303
app/api/services/lesson_service.py                   118    118     0%   6-266
app/api/services/parent_portal_service.py             79     53    33%   39-44, 47-56, 76-105, 108-126, 129-146, 152, 155-162, 167-174, 193-200, 220-228, 238-240, 257-259, 273-274
app/api/services/popia_deletion_service.py           126    111    12%   39, 47-63, 76-228, 241-267, 283-373, 400-433
app/api/services/prompt_manager.py                    25     14    44%   20-33, 38
app/api/services/study_plan_service.py               108    108     0%   6-283
app/api/tasks/__init__.py                              0      0   100%
app/api/tasks/plan_tasks.py                           68     68     0%   3-171
app/api/tasks/report_tasks.py                         35     35     0%   3-70
app/api/util/encryption.py                            21     12    43%   9-10, 14-16, 20-28, 32, 36
--------------------------------------------------------------------------------
TOTAL                                               5120   3976    22%
Coverage HTML written to dir coverage_html

============================ 1 deselected in 4.59s =============================
Error: Process completed with exit code 5.




********************************************************************************************************************************************


Upload scan results errors:

Run github/codeql-action/upload-sarif@v3
Warning: CodeQL Action v3 will be deprecated in December 2026. Please update all occurrences of the CodeQL Action in your workflow files to v4. For more information, see https://github.blog/changelog/2025-10-28-upcoming-deprecation-of-codeql-action-v3/
Warning: This run of the CodeQL Action does not have permission to access the CodeQL Action API endpoints. This could be because the Action is running on a pull request from a fork. If not, please ensure the workflow has at least the 'security-events: read' permission. Details: Resource not accessible by integration - https://docs.github.com/rest
Post-processing sarif files: ["trivy-results.sarif"]
Validating trivy-results.sarif
Adding fingerprints to SARIF file. See https://docs.github.com/en/code-security/reference/code-scanning/sarif-support-for-code-scanning#data-for-preventing-duplicated-alerts for more information.
Uploading code scanning results
  Uploading results
  Warning: Resource not accessible by integration - https://docs.github.com/rest
  Error: Resource not accessible by integration - https://docs.github.com/rest
  Warning: This run of the CodeQL Action does not have permission to access the CodeQL Action API endpoints. This could be because the Action is running on a pull request from a fork. If not, please ensure the workflow has at least the 'security-events: read' permission. Details: Resource not accessible by integration - https://docs.github.com/rest