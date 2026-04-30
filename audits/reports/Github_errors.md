mypy errors:

Run mypy app/ --ignore-missing-imports --strict-optional
app/api/judiciary/models.py:78: error: Argument "default_factory" to "Field" has incompatible type "type[ScopeModel]"; expected "Callable[[], Never] | Callable[[dict[str, Any]], Never]"  [arg-type]
app/api/judiciary/service.py:90: error: "JudiciaryStamp" has no attribute "_replace"  [attr-defined]
app/api/util/encryption.py:36: error: Incompatible return value type (got "str | None", expected "str")  [return-value]
app/api/judiciary/main.py:76: error: The return type of an async generator function should be "AsyncGenerator" or one of its supertypes  [misc]
app/api/services/gamification_service.py:277: error: Unsupported operand types for > ("int" and "object")  [operator]
app/api/services/gamification_service.py:279: error: Unsupported operand types for - ("object" and "int")  [operator]
app/api/services/gamification_service.py:324: error: Unsupported operand types for > ("int" and "object")  [operator]
app/api/services/diagnostic_benchmark_service.py:218: error: Need type annotation for "by_subject" (hint: "by_subject: dict[<type>, <type>] = ...")  [var-annotated]
app/api/services/diagnostic_benchmark_service.py:285: error: Need type annotation for "by_grade" (hint: "by_grade: dict[<type>, <type>] = ...")  [var-annotated]
app/api/services/audit_query_service.py:219: error: Need type annotation for "categorized"  [var-annotated]
app/api/services/audit_query_service.py:285: error: Need type annotation for "event_counts" (hint: "event_counts: dict[<type>, <type>] = ...")  [var-annotated]
app/api/services/audit_query_service.py:290: error: Need type annotation for "pillar_counts" (hint: "pillar_counts: dict[<type>, <type>] = ...")  [var-annotated]
app/api/fourth_estate.py:61: error: Incompatible types in assignment (expression has type "Redis[Any]", variable has type "None")  [assignment]
app/api/fourth_estate.py:63: error: "None" has no attribute "xadd"  [attr-defined]
app/api/routers/auth.py:74: error: "Redis[Any]" has no attribute "aclose"; maybe "close"?  [attr-defined]
app/api/routers/auth.py:375: error: "Redis[Any]" has no attribute "aclose"; maybe "close"?  [attr-defined]
app/api/routers/auth.py:420: error: "Redis[Any]" has no attribute "aclose"; maybe "close"?  [attr-defined]
app/api/routers/system.py:133: error: "FourthEstate" has no attribute "get_sequence"; maybe "_sequence"?  [attr-defined]
app/api/judiciary/provider_router.py:130: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
app/api/services/lesson_service.py:17: error: Module "app.api.judiciary.profiler" has no attribute "EtherPromptModifier"  [attr-defined]
app/api/orchestrator.py:46: error: Incompatible types in assignment (expression has type "StudyPlanService", variable has type "LessonService")  [assignment]
app/api/orchestrator.py:54: error: Incompatible types in assignment (expression has type "ParentReportService", variable has type "LessonService")  [assignment]
app/api/tasks/plan_tasks.py:90: error: Item "None" of "Any | None" has no attribute "get"  [union-attr]
app/api/tasks/plan_tasks.py:91: error: Item "None" of "Any | None" has no attribute "get"  [union-attr]
app/api/routers/lessons.py:137: error: Argument "lesson" to "LessonGenerationResponse" has incompatible type "Any | None"; expected "dict[str, Any]"  [arg-type]
app/api/routers/lessons.py:160: error: "Redis[Any]" has no attribute "aclose"; maybe "close"?  [attr-defined]
app/api/routers/diagnostic.py:158: error: Item "None" of "Any | None" has no attribute "get"  [union-attr]
app/api/routers/diagnostic.py:159: error: Item "None" of "Any | None" has no attribute "get"  [union-attr]
app/api/routers/diagnostic.py:257: error: Item "None" of "Any | None" has no attribute "get"  [union-attr]
app/api/routers/diagnostic.py:258: error: Item "None" of "Any | None" has no attribute "get"  [union-attr]
app/api/routers/diagnostic.py:287: error: Argument "item_id" to "DiagnosticItem" has incompatible type "Any | None"; expected "str"  [arg-type]
app/api/routers/diagnostic.py:290: error: Argument "question_text" to "DiagnosticItem" has incompatible type "Any | None"; expected "str"  [arg-type]
app/api/routers/diagnostic.py:293: error: Argument "options" to "DiagnosticItem" has incompatible type "Any | None"; expected "list[str]"  [arg-type]
app/api/routers/diagnostic.py:383: error: Value of type "Any | None" is not indexable  [index]
app/api/routers/diagnostic.py:409: error: Value of type "Any | None" is not indexable  [index]
app/api/routers/diagnostic.py:410: error: Value of type "Any | None" is not indexable  [index]
app/api/routers/diagnostic.py:425: error: Value of type "Any | None" is not indexable  [index]
app/api/routers/diagnostic.py:426: error: Value of type "Any | None" is not indexable  [index]
app/api/routers/diagnostic.py:434: error: Value of type "Any | None" is not indexable  [index]
app/api/routers/diagnostic.py:435: error: Value of type "Any | None" is not indexable  [index]
app/api/routers/diagnostic.py:437: error: Argument "item_id" to "DiagnosticItem" has incompatible type "Any | None"; expected "str"  [arg-type]
app/api/routers/diagnostic.py:438: error: Argument "question_text" to "DiagnosticItem" has incompatible type "Any | None"; expected "str"  [arg-type]
app/api/routers/diagnostic.py:441: error: Argument "options" to "DiagnosticItem" has incompatible type "Any | None"; expected "list[str]"  [arg-type]
app/api/routers/diagnostic.py:450: error: Value of type "Any | None" is not indexable  [index]
app/api/routers/diagnostic.py:457: error: Value of type "Any | None" is not indexable  [index]
app/api/routers/diagnostic.py:459: error: Value of type "Any | None" is not indexable  [index]
Found 45 errors in 15 files (checked 63 source files)
Error: Process completed with exit code 1.

*****************************************************************************************

Unit tests errors:

tests/unit/test_profiler.py::TestProfilerSingleton::test_singleton_returns_same_instance PASSED [ 92%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_plan_with_valid_learner FAILED [ 93%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_plan_learner_not_found FAILED [ 93%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_prioritize_subjects_high_gap_first FAILED [ 94%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_remediation_tasks_creates_gap_specific_tasks FAILED [ 94%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_grade_tasks_creates_advancement_tasks FAILED [ 95%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_weekly_schedule_distribution FAILED [ 95%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_gap_ratio_affects_remediation_distribution FAILED [ 96%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_grade_band_determines_focus_areas FAILED [ 96%]
tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_determine_week_focus_from_gaps FAILED [ 97%]
tests/unit/test_study_plan_service.py::TestStudyPlanValidation::test_gap_ratio_validation_bounds FAILED [ 97%]
tests/unit/test_study_plan_service.py::TestStudyPlanValidation::test_schedule_has_all_days FAILED [ 98%]
tests/unit/test_study_plan_service.py::TestStudyPlanAlgorithmQuality::test_consistent_task_distribution FAILED [ 98%]
tests/unit/test_study_plan_service.py::TestStudyPlanAlgorithmQuality::test_no_empty_schedules FAILED [ 99%]
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/ast.py:50: RuntimeWarning: coroutine 'AsyncMockMixin._execute_mock_call' was never awaited
  return compile(source, filename, mode, flags,
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
tests/unit/test_study_plan_service.py::TestStudyPlanAlgorithmQuality::test_prioritization_ranks_subjects_logically FAILED [100%]

=================================== FAILURES ===================================
__________________ TestConsentGate.test_active_consent_passes __________________
tests/unit/test_five_pillars.py:300: in test_active_consent_passes
    await gate.assert_active("PSEUDO-123")  # should not raise
app/api/judiciary/compliance.py:97: in assert_active
    raise PermissionError(
E   PermissionError: Learner PSEUDO-123 does not have ACTIVE parental consent. Processing blocked under POPIA Section 35.
___________________________ test_streak_grace_period ___________________________
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:1967: in _exec_single_context
    self.dialect.do_execute(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/default.py:924: in do_execute
    cursor.execute(statement, parameters)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:146: in execute
    self._adapt_connection._handle_exception(error)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:298: in _handle_exception
    raise error
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:128: in execute
    self.await_(_cursor.execute(operation, parameters))
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:131: in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/cursor.py:48: in execute
    await self._execute(self._cursor.execute, sql, parameters)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/cursor.py:40: in _execute
    return await self._conn._execute(fn, *args, **kwargs)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/core.py:132: in _execute
    return await future
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/core.py:115: in run
    result = function()
E   sqlite3.OperationalError: no such table: learners

The above exception was the direct cause of the following exception:
tests/unit/test_gamification.py:22: in test_streak_grace_period
    await session.commit()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/session.py:1009: in commit
    await greenlet_spawn(self.sync_session.commit)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:203: in greenlet_spawn
    result = context.switch(value)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:2017: in commit
    trans.commit(_to_root=True)
<string>:2: in commit
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1302: in commit
    self._prepare_impl()
<string>:2: in _prepare_impl
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1277: in _prepare_impl
    self.session.flush()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:4341: in flush
    self._flush(objects)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:4476: in _flush
    with util.safe_reraise():
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py:146: in __exit__
    raise exc_value.with_traceback(exc_tb)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:4437: in _flush
    flush_context.execute()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/unitofwork.py:466: in execute
    rec.execute(self)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/unitofwork.py:642: in execute
    util.preloaded.orm_persistence.save_obj(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py:93: in save_obj
    _emit_insert_statements(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py:1233: in _emit_insert_statements
    result = connection.execute(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:1418: in execute
    return meth(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/sql/elements.py:515: in _execute_on_connection
    return connection._execute_clauseelement(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:1640: in _execute_clauseelement
    ret = self._execute_context(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:1846: in _execute_context
    return self._exec_single_context(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:1986: in _exec_single_context
    self._handle_dbapi_exception(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:2353: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:1967: in _exec_single_context
    self.dialect.do_execute(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/default.py:924: in do_execute
    cursor.execute(statement, parameters)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:146: in execute
    self._adapt_connection._handle_exception(error)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:298: in _handle_exception
    raise error
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:128: in execute
    self.await_(_cursor.execute(operation, parameters))
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:131: in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/cursor.py:48: in execute
    await self._execute(self._cursor.execute, sql, parameters)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/cursor.py:40: in _execute
    return await self._conn._execute(fn, *args, **kwargs)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/core.py:132: in _execute
    return await future
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/core.py:115: in run
    result = function()
E   sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: learners
E   [SQL: INSERT INTO learners (learner_id, grade, home_language, avatar_id, learning_style, overall_mastery, streak_days, total_xp, last_active_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING created_at]
E   [parameters: ('9e64c644a6944fbe8b4f6ef024f140bc', 3, 'eng', 0, '{"visual": 0.6, "auditory": 0.2, "kinesthetic": 0.2}', 0.0, 5, 100, '2026-04-28 13:49:23.828034')]
E   (Background on this error at: https://sqlalche.me/e/20/e3q8)
___________________________ test_mastery_badge_award ___________________________
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:1967: in _exec_single_context
    self.dialect.do_execute(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/default.py:924: in do_execute
    cursor.execute(statement, parameters)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:146: in execute
    self._adapt_connection._handle_exception(error)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:298: in _handle_exception
    raise error
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:128: in execute
    self.await_(_cursor.execute(operation, parameters))
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:131: in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/cursor.py:48: in execute
    await self._execute(self._cursor.execute, sql, parameters)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/cursor.py:40: in _execute
    return await self._conn._execute(fn, *args, **kwargs)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/core.py:132: in _execute
    return await future
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/core.py:115: in run
    result = function()
E   sqlite3.OperationalError: no such table: learners

The above exception was the direct cause of the following exception:
tests/unit/test_gamification.py:54: in test_mastery_badge_award
    await session.commit()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/session.py:1009: in commit
    await greenlet_spawn(self.sync_session.commit)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:203: in greenlet_spawn
    result = context.switch(value)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:2017: in commit
    trans.commit(_to_root=True)
<string>:2: in commit
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1302: in commit
    self._prepare_impl()
<string>:2: in _prepare_impl
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1277: in _prepare_impl
    self.session.flush()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:4341: in flush
    self._flush(objects)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:4476: in _flush
    with util.safe_reraise():
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py:146: in __exit__
    raise exc_value.with_traceback(exc_tb)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:4437: in _flush
    flush_context.execute()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/unitofwork.py:466: in execute
    rec.execute(self)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/unitofwork.py:642: in execute
    util.preloaded.orm_persistence.save_obj(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py:93: in save_obj
    _emit_insert_statements(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py:1233: in _emit_insert_statements
    result = connection.execute(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:1418: in execute
    return meth(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/sql/elements.py:515: in _execute_on_connection
    return connection._execute_clauseelement(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:1640: in _execute_clauseelement
    ret = self._execute_context(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:1846: in _execute_context
    return self._exec_single_context(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:1986: in _exec_single_context
    self._handle_dbapi_exception(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:2353: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:1967: in _exec_single_context
    self.dialect.do_execute(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/default.py:924: in do_execute
    cursor.execute(statement, parameters)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:146: in execute
    self._adapt_connection._handle_exception(error)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:298: in _handle_exception
    raise error
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:128: in execute
    self.await_(_cursor.execute(operation, parameters))
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:131: in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/cursor.py:48: in execute
    await self._execute(self._cursor.execute, sql, parameters)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/cursor.py:40: in _execute
    return await self._conn._execute(fn, *args, **kwargs)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/core.py:132: in _execute
    return await future
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/aiosqlite/core.py:115: in run
    result = function()
E   sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: learners
E   [SQL: INSERT INTO learners (learner_id, grade, home_language, avatar_id, learning_style, overall_mastery, streak_days, total_xp) VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING created_at, last_active_at]
E   [parameters: ('fa6f65c25fa84d21afc2819ff3a32e16', 4, 'eng', 0, '{"visual": 0.6, "auditory": 0.2, "kinesthetic": 0.2}', 0.0, 0, 500)]
E   (Background on this error at: https://sqlalche.me/e/20/e3q8)
________ TestStudyPlanGeneration.test_generate_plan_with_valid_learner _________
tests/unit/test_study_plan_service.py:61: in test_generate_plan_with_valid_learner
    result = await study_plan_service.generate_plan(
app/api/services/study_plan_service.py:144: in generate_plan
    return await self.run(
app/api/judiciary/base.py:172: in run
    action = await self._build_action(**kwargs)
app/api/services/study_plan_service.py:46: in _build_action
    await self._assert_consent(learner_pseudonym, self._session)
app/api/judiciary/base.py:158: in _assert_consent
    if row is None or row[0] != "consent_granted":
E   TypeError: 'coroutine' object is not subscriptable
_________ TestStudyPlanGeneration.test_generate_plan_learner_not_found _________
tests/unit/test_study_plan_service.py:87: in test_generate_plan_learner_not_found
    await study_plan_service.generate_plan(
app/api/services/study_plan_service.py:144: in generate_plan
    return await self.run(
app/api/judiciary/base.py:172: in run
    action = await self._build_action(**kwargs)
app/api/services/study_plan_service.py:46: in _build_action
    await self._assert_consent(learner_pseudonym, self._session)
app/api/judiciary/base.py:158: in _assert_consent
    if row is None or row[0] != "consent_granted":
E   TypeError: 'coroutine' object is not subscriptable
_______ TestStudyPlanGeneration.test_prioritize_subjects_high_gap_first ________
tests/unit/test_study_plan_service.py:103: in test_prioritize_subjects_high_gap_first
    prioritized = study_plan_service._prioritize_subjects(subjects_mastery)
E   AttributeError: 'StudyPlanService' object has no attribute '_prioritize_subjects'
_ TestStudyPlanGeneration.test_generate_remediation_tasks_creates_gap_specific_tasks _
tests/unit/test_study_plan_service.py:116: in test_generate_remediation_tasks_creates_gap_specific_tasks
    remediation_tasks = study_plan_service._generate_remediation_tasks(
E   AttributeError: 'StudyPlanService' object has no attribute '_generate_remediation_tasks'
_ TestStudyPlanGeneration.test_generate_grade_tasks_creates_advancement_tasks __
tests/unit/test_study_plan_service.py:133: in test_generate_grade_tasks_creates_advancement_tasks
    grade_tasks = study_plan_service._generate_grade_tasks(
E   AttributeError: 'StudyPlanService' object has no attribute '_generate_grade_tasks'
______ TestStudyPlanGeneration.test_generate_weekly_schedule_distribution ______
tests/unit/test_study_plan_service.py:151: in test_generate_weekly_schedule_distribution
    schedule = study_plan_service._generate_weekly_schedule(
E   AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
___ TestStudyPlanGeneration.test_gap_ratio_affects_remediation_distribution ____
tests/unit/test_study_plan_service.py:178: in test_gap_ratio_affects_remediation_distribution
    schedule_high_gap = study_plan_service._generate_weekly_schedule(
E   AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
________ TestStudyPlanGeneration.test_grade_band_determines_focus_areas ________
tests/unit/test_study_plan_service.py:206: in test_grade_band_determines_focus_areas
    junior_schedule = study_plan_service._generate_weekly_schedule(
E   AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
_________ TestStudyPlanGeneration.test_determine_week_focus_from_gaps __________
tests/unit/test_study_plan_service.py:233: in test_determine_week_focus_from_gaps
    week_focus = study_plan_service._determine_week_focus(
E   AttributeError: 'StudyPlanService' object has no attribute '_determine_week_focus'
___________ TestStudyPlanValidation.test_gap_ratio_validation_bounds ___________
tests/unit/test_study_plan_service.py:260: in test_gap_ratio_validation_bounds
    schedule = study_plan_service._generate_weekly_schedule(
E   AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
______________ TestStudyPlanValidation.test_schedule_has_all_days ______________
tests/unit/test_study_plan_service.py:271: in test_schedule_has_all_days
    schedule = study_plan_service._generate_weekly_schedule(
E   AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
_______ TestStudyPlanAlgorithmQuality.test_consistent_task_distribution ________
tests/unit/test_study_plan_service.py:294: in test_consistent_task_distribution
    schedule = study_plan_service._generate_weekly_schedule(
E   AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
____________ TestStudyPlanAlgorithmQuality.test_no_empty_schedules _____________
tests/unit/test_study_plan_service.py:316: in test_no_empty_schedules
    schedule = study_plan_service._generate_weekly_schedule(
E   AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
__ TestStudyPlanAlgorithmQuality.test_prioritization_ranks_subjects_logically __
tests/unit/test_study_plan_service.py:335: in test_prioritization_ranks_subjects_logically
    prioritized = study_plan_service._prioritize_subjects(subjects_mastery)
E   AttributeError: 'StudyPlanService' object has no attribute '_prioritize_subjects'
=============================== warnings summary ===============================
tests/unit/test_gamification_service.py::TestGamificationMetrics::test_badge_awarded_metric
  /home/runner/work/edo-boost-main/edo-boost-main/app/api/services/gamification_service.py:391: RuntimeWarning: coroutine 'AsyncMockMixin._execute_mock_call' was never awaited
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
app/api/core/database.py                              34     19    44%   22, 43-57, 65-72
app/api/core/metrics.py                               54     35    35%   119-163
app/api/core/pii_patterns.py                          36     16    56%   30, 32, 43-47, 51-59
app/api/fourth_estate.py                             109     18    83%   192, 204, 208-213, 230-232, 240, 243-249
app/api/judiciary.py                                  91     25    73%   73, 124-157
app/api/judiciary/__init__.py                         12      1    92%   16
app/api/judiciary/agent.py                           102    102     0%   6-260
app/api/judiciary/audit_agent.py                     110    110     0%   8-278
app/api/judiciary/base.py                             74      3    96%   124, 159, 176
app/api/judiciary/client.py                           26     15    42%   26-37, 47-56
app/api/judiciary/compliance.py                       89     44    51%   106-125, 129-140, 145-147, 176, 183-214, 218-242, 245-247
app/api/judiciary/engine.py                          104     54    48%   83-95, 152-163, 166-175, 185-212, 225, 228-231, 234-259, 262-281, 285-319
app/api/judiciary/main.py                             52     52     0%   7-137
app/api/judiciary/models.py                          147      1    99%   105
app/api/judiciary/profiler.py                         45      0   100%
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
app/api/models/db_models.py                          283      0   100%
app/api/orchestrator.py                               37     37     0%   6-85
app/api/profiler.py                                   83      3    96%   136, 169-170
app/api/routers/__init__.py                            0      0   100%
app/api/routers/assessments.py                       121    121     0%   7-367
app/api/routers/audit.py                              75     75     0%   7-184
app/api/routers/auth.py                              187    187     0%   3-430
app/api/routers/diagnostic.py                        187    187     0%   3-720
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
app/api/services/gamification_service.py             178     75    58%   55, 65-70, 86-87, 213, 217, 255-256, 266, 279-294, 344-377, 406-415, 426-444, 448-485, 493-498
app/api/services/inference_gateway.py                145    103    29%   90-101, 105-113, 119-135, 149-200, 205, 219-290, 295-303
app/api/services/lesson_service.py                   105    105     0%   6-246
app/api/services/parent_portal_service.py             79     79     0%   6-274
app/api/services/popia_deletion_service.py           126    126     0%   11-433
app/api/services/prompt_manager.py                    25     14    44%   20-33, 38
app/api/services/study_plan_service.py                88     55    38%   48, 66-101, 104-120, 123-134, 153-159, 164-180, 189-192, 206-220, 231-233, 243-244
app/api/tasks/__init__.py                              0      0   100%
app/api/tasks/plan_tasks.py                           65     65     0%   3-168
app/api/tasks/report_tasks.py                         35     35     0%   3-70
--------------------------------------------------------------------------------
TOTAL                                               5020   3420    32%
Coverage HTML written to dir coverage_html
Coverage XML written to file coverage.xml

FAIL Required test coverage of 80% not reached. Total coverage: 31.87%
=========================== short test summary info ============================
FAILED tests/unit/test_five_pillars.py::TestConsentGate::test_active_consent_passes - PermissionError: Learner PSEUDO-123 does not have ACTIVE parental consent. Processing blocked under POPIA Section 35.
FAILED tests/unit/test_gamification.py::test_streak_grace_period - sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: learners
[SQL: INSERT INTO learners (learner_id, grade, home_language, avatar_id, learning_style, overall_mastery, streak_days, total_xp, last_active_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING created_at]
[parameters: ('9e64c644a6944fbe8b4f6ef024f140bc', 3, 'eng', 0, '{"visual": 0.6, "auditory": 0.2, "kinesthetic": 0.2}', 0.0, 5, 100, '2026-04-28 13:49:23.828034')]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
FAILED tests/unit/test_gamification.py::test_mastery_badge_award - sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: learners
[SQL: INSERT INTO learners (learner_id, grade, home_language, avatar_id, learning_style, overall_mastery, streak_days, total_xp) VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING created_at, last_active_at]
[parameters: ('fa6f65c25fa84d21afc2819ff3a32e16', 4, 'eng', 0, '{"visual": 0.6, "auditory": 0.2, "kinesthetic": 0.2}', 0.0, 0, 500)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_plan_with_valid_learner - TypeError: 'coroutine' object is not subscriptable
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_plan_learner_not_found - TypeError: 'coroutine' object is not subscriptable
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_prioritize_subjects_high_gap_first - AttributeError: 'StudyPlanService' object has no attribute '_prioritize_subjects'
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_remediation_tasks_creates_gap_specific_tasks - AttributeError: 'StudyPlanService' object has no attribute '_generate_remediation_tasks'
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_grade_tasks_creates_advancement_tasks - AttributeError: 'StudyPlanService' object has no attribute '_generate_grade_tasks'
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_generate_weekly_schedule_distribution - AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_gap_ratio_affects_remediation_distribution - AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_grade_band_determines_focus_areas - AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanGeneration::test_determine_week_focus_from_gaps - AttributeError: 'StudyPlanService' object has no attribute '_determine_week_focus'
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanValidation::test_gap_ratio_validation_bounds - AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanValidation::test_schedule_has_all_days - AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanAlgorithmQuality::test_consistent_task_distribution - AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanAlgorithmQuality::test_no_empty_schedules - AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
FAILED tests/unit/test_study_plan_service.py::TestStudyPlanAlgorithmQuality::test_prioritization_ranks_subjects_logically - AttributeError: 'StudyPlanService' object has no attribute '_prioritize_subjects'
================== 17 failed, 169 passed, 1 warning in 9.78s ===================
Error: Process completed with exit code 1.

****************************************************************************************************************

Integration test errors:

Run pytest tests/integration/ -v --tb=short \
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-8.2.1, pluggy-1.6.0 -- /opt/hostedtoolcache/Python/3.11.15/x64/bin/python
cachedir: .pytest_cache
rootdir: /home/runner/work/edo-boost-main/edo-boost-main
configfile: pytest.ini
plugins: mock-3.14.0, timeout-2.3.1, cov-5.0.0, anyio-4.13.0, asyncio-0.23.7, Faker-25.2.0
timeout: 60.0s
timeout method: signal
timeout func_only: False
asyncio: mode=Mode.AUTO
collecting ... collected 92 items

tests/integration/test_api_contracts.py::test_create_learner_rejects_unknown_fields PASSED [  1%]
tests/integration/test_api_contracts.py::test_diagnostic_invalid_subject_returns_structured_error FAILED [  2%]
tests/integration/test_api_contracts.py::test_diagnostic_run_returns_valid_response FAILED [  3%]
tests/integration/test_api_contracts.py::test_diagnostic_history_endpoint PASSED [  4%]
tests/integration/test_api_contracts.py::test_right_to_access_endpoint PASSED [  5%]
tests/integration/test_api_contracts.py::test_audit_search_endpoint PASSED [  6%]
tests/integration/test_auth_lifecycle.py::test_guardian_login_invalid_credentials FAILED [  7%]
tests/integration/test_auth_lifecycle.py::test_learner_session_creation PASSED [  8%]
tests/integration/test_celery_study_plan.py::TestCeleryStudyPlanTasks::test_refresh_study_plan_task_success PASSED [  9%]
tests/integration/test_celery_study_plan.py::TestCeleryStudyPlanTasks::test_refresh_study_plan_task_no_diagnostic PASSED [ 10%]
tests/integration/test_celery_study_plan.py::TestCeleryStudyPlanTasks::test_daily_plan_refresh_multiple_learners PASSED [ 11%]
tests/integration/test_celery_study_plan.py::TestCeleryStudyPlanTasks::test_daily_plan_refresh_empty PASSED [ 13%]
tests/integration/test_celery_study_plan.py::TestCeleryStudyPlanTasks::test_orchestrator_mocked_for_plan_generation FAILED [ 14%]
tests/integration/test_celery_study_plan.py::TestCeleryStudyPlanTasks::test_refresh_task_has_retry_config PASSED [ 15%]
tests/integration/test_celery_study_plan.py::TestCeleryStudyPlanTasks::test_daily_refresh_task_has_retry_config PASSED [ 16%]
tests/integration/test_celery_study_plan.py::TestCeleryStudyPlanTasks::test_beat_schedule_has_daily_plan_refresh PASSED [ 17%]
tests/integration/test_celery_study_plan.py::TestCeleryStudyPlanTasks::test_beat_schedule_has_weekly_parent_reports PASSED [ 18%]
tests/integration/test_five_pillar_pipeline.py::TestLessonPipelineEndToEnd::test_full_pipeline_success FAILED [ 19%]
tests/integration/test_five_pillar_pipeline.py::TestLessonPipelineEndToEnd::test_learner_id_never_reaches_llm FAILED [ 20%]
tests/integration/test_five_pillar_pipeline.py::TestLessonPipelineEndToEnd::test_llm_failure_returns_503 FAILED [ 21%]
tests/integration/test_five_pillar_pipeline.py::TestLessonPipelineEndToEnd::test_missing_required_fields_returns_422 PASSED [ 22%]
tests/integration/test_five_pillar_pipeline.py::TestLessonPipelineEndToEnd::test_invalid_grade_returns_422 PASSED [ 23%]
tests/integration/test_five_pillar_pipeline.py::TestConstitutionalMetadata::test_response_includes_stamp_status FAILED [ 25%]
tests/integration/test_five_pillar_pipeline.py::TestConstitutionalMetadata::test_constitutional_health_between_0_and_1 FAILED [ 26%]
tests/integration/test_five_pillar_pipeline.py::TestFourthEstateIntegration::test_audit_events_emitted_on_success FAILED [ 27%]
tests/integration/test_five_pillar_pipeline.py::TestFourthEstateIntegration::test_no_violations_on_clean_request FAILED [ 28%]
tests/integration/test_five_pillar_pipeline.py::TestHealthEndpoint::test_health_returns_ok PASSED [ 29%]
tests/integration/test_five_pillar_pipeline.py::TestPOPIACompliance::test_response_contains_no_learner_pii FAILED [ 30%]
tests/integration/test_five_pillar_pipeline.py::TestPOPIACompliance::test_study_plan_endpoint_exists PASSED [ 31%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_award_xp_lesson_complete_flow PASSED [ 32%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_award_xp_level_up_detection PASSED [ 33%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_award_xp_invalid_type_raises_error PASSED [ 34%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_award_xp_learner_not_found PASSED [ 35%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_update_streak_continues_streak PASSED [ 36%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_update_streak_breaks_streak PASSED [ 38%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_update_streak_same_day_no_change PASSED [ 39%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_grade_r3_max_daily_xp PASSED [ 40%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_grade_47_max_daily_xp PASSED [ 41%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_discovery_badges_available_for_grade_47 PASSED [ 42%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_no_discovery_badges_for_grade_r3 PASSED [ 43%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_get_leaderboard_returns_top_learners PASSED [ 44%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_get_leaderboard_respects_limit PASSED [ 45%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_badge_award_for_streak_threshold PASSED [ 46%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_xp_config_has_all_required_types PASSED [ 47%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_xp_values_are_reasonable PASSED [ 48%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_profile_includes_grade_band PASSED [ 50%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_profile_includes_level_calculations PASSED [ 51%]
tests/integration/test_gamification_integration.py::TestGamificationIntegration::test_profile_includes_available_badges PASSED [ 52%]
tests/integration/test_lesson_api.py::TestLessonGeneration::test_generate_lesson_success FAILED [ 53%]
tests/integration/test_lesson_api.py::TestLessonGeneration::test_learner_id_never_in_llm_call FAILED [ 54%]
tests/integration/test_lesson_api.py::TestLessonGeneration::test_generate_lesson_llm_failure_returns_503 FAILED [ 55%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_learner_progress_summary_success FAILED [ 56%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_learner_progress_summary_no_consent FAILED [ 57%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_learner_progress_summary_consent_revoked FAILED [ 58%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_learner_progress_summary_learner_not_found PASSED [ 59%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_diagnostic_trends_success FAILED [ 60%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_diagnostic_trends_no_sessions FAILED [ 61%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_study_plan_adherence_success FAILED [ 63%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_study_plan_adherence_no_plan FAILED [ 64%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_generate_parent_report_success FAILED [ 65%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_export_data_success FAILED [ 66%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_unauthorized_access_different_guardian PASSED [ 67%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_consent_check_order_matters FAILED [ 68%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_progress_summary_empty_subjects FAILED [ 69%]
tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_diagnostic_trends_custom_days FAILED [ 70%]
tests/integration/test_parent_reporting.py::test_parent_report_loop FAILED [ 71%]
tests/integration/test_parent_reporting.py::test_parent_access_revoked FAILED [ 72%]
tests/integration/test_phase1_contracts_extended.py::test_guardian_login_rejects_unknown_fields PASSED [ 73%]
tests/integration/test_phase1_contracts_extended.py::test_parent_report_rejects_unknown_fields FAILED [ 75%]
tests/integration/test_phase1_contracts_extended.py::test_study_plan_rejects_unknown_fields PASSED [ 76%]
tests/integration/test_phase1_contracts_extended.py::test_learner_session_creation PASSED [ 77%]
tests/integration/test_phase1_contracts_extended.py::test_learner_session_rejects_empty_learner_id PASSED [ 78%]
tests/integration/test_phase1_contracts_extended.py::test_guardian_login_rejects_invalid_email PASSED [ 79%]
tests/integration/test_phase1_contracts_extended.py::test_protected_endpoint_without_token PASSED [ 80%]
tests/integration/test_privacy_compliance.py::test_record_consent_returns_created FAILED [ 81%]
tests/integration/test_privacy_compliance.py::test_execute_deletion_contract FAILED [ 82%]
tests/integration/test_privacy_compliance.py::test_right_to_access_contract FAILED [ 83%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_generate_save_fetch_cycle FAILED [ 84%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_fetch_current_plan PASSED [ 85%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_fetch_no_plan_returns_none PASSED [ 86%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_refresh_plan_creates_new_plan FAILED [ 88%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_refresh_nonexistent_plan_raises_error PASSED [ 89%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_sparse_data_no_mastery_records FAILED [ 90%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_sparse_data_no_knowledge_gaps FAILED [ 91%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_overload_many_knowledge_gaps FAILED [ 92%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_conflict_gap_ratio_bounds FAILED [ 93%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_diagnostic_linkage_integration FAILED [ 94%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_grade_band_diagnostic_integration FAILED [ 95%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_plan_with_rationale_includes_explanations FAILED [ 96%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_grade_0_grade_r_handling FAILED [ 97%]
tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_empty_schedule_fallback FAILED [ 98%]
tests/integration/test_study_plan_mastery.py::test_study_plan_mastery_prioritization FAILED [100%]

=================================== FAILURES ===================================
___________ test_diagnostic_invalid_subject_returns_structured_error ___________
tests/integration/test_api_contracts.py:30: in test_diagnostic_invalid_subject_returns_structured_error
    response = await client.post(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1892: in post
    return await self.request(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1574: in request
    return await self.send(request, auth=auth, follow_redirects=follow_redirects)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1661: in send
    response = await self._send_handling_auth(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1689: in _send_handling_auth
    response = await self._send_handling_redirects(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1726: in _send_handling_redirects
    response = await self._send_single_request(request)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1763: in _send_single_request
    response = await transport.handle_async_request(request)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_transports/asgi.py:164: in handle_async_request
    await self.app(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/applications.py:123: in __call__
    await self.middleware_stack(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/errors.py:186: in __call__
    raise exc
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/errors.py:164: in __call__
    await self.app(scope, receive, _send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/prometheus_fastapi_instrumentator/middleware.py:169: in __call__
    raise exc
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/prometheus_fastapi_instrumentator/middleware.py:167: in __call__
    await self.app(scope, receive, send_wrapper)
app/api/main.py:88: in __call__
    await self.app(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/gzip.py:24: in __call__
    await responder(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/gzip.py:44: in __call__
    await self.app(scope, receive, self.send_with_gzip)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/exceptions.py:65: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/_exception_handler.py:64: in wrapped_app
    raise exc
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    await app(scope, receive, sender)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:756: in __call__
    await self.middleware_stack(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:776: in app
    await route.handle(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:297: in handle
    await self.app(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:77: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/_exception_handler.py:64: in wrapped_app
    raise exc
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    await app(scope, receive, sender)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:72: in app
    response = await func(request)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/routing.py:278: in app
    raw_response = await run_endpoint_function(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/routing.py:191: in run_endpoint_function
    return await dependant.call(**values)
app/api/routers/diagnostic.py:115: in run_diagnostic
    from app.api.orchestrator import OrchestratorRequest, get_orchestrator
app/api/orchestrator.py:14: in <module>
    from app.api.services.lesson_service import LessonService
app/api/services/lesson_service.py:17: in <module>
    from app.api.judiciary.profiler import EtherPromptModifier
E   ImportError: cannot import name 'EtherPromptModifier' from 'app.api.judiciary.profiler' (/home/runner/work/edo-boost-main/edo-boost-main/app/api/judiciary/profiler.py)
__________________ test_diagnostic_run_returns_valid_response __________________
tests/integration/test_api_contracts.py:53: in test_diagnostic_run_returns_valid_response
    response = await client.post(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1892: in post
    return await self.request(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1574: in request
    return await self.send(request, auth=auth, follow_redirects=follow_redirects)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1661: in send
    response = await self._send_handling_auth(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1689: in _send_handling_auth
    response = await self._send_handling_redirects(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1726: in _send_handling_redirects
    response = await self._send_single_request(request)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1763: in _send_single_request
    response = await transport.handle_async_request(request)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_transports/asgi.py:164: in handle_async_request
    await self.app(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/applications.py:123: in __call__
    await self.middleware_stack(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/errors.py:186: in __call__
    raise exc
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/errors.py:164: in __call__
    await self.app(scope, receive, _send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/prometheus_fastapi_instrumentator/middleware.py:169: in __call__
    raise exc
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/prometheus_fastapi_instrumentator/middleware.py:167: in __call__
    await self.app(scope, receive, send_wrapper)
app/api/main.py:88: in __call__
    await self.app(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/gzip.py:24: in __call__
    await responder(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/gzip.py:44: in __call__
    await self.app(scope, receive, self.send_with_gzip)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/exceptions.py:65: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/_exception_handler.py:64: in wrapped_app
    raise exc
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    await app(scope, receive, sender)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:756: in __call__
    await self.middleware_stack(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:776: in app
    await route.handle(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:297: in handle
    await self.app(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:77: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/_exception_handler.py:64: in wrapped_app
    raise exc
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    await app(scope, receive, sender)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:72: in app
    response = await func(request)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/routing.py:278: in app
    raw_response = await run_endpoint_function(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/routing.py:191: in run_endpoint_function
    return await dependant.call(**values)
app/api/routers/diagnostic.py:115: in run_diagnostic
    from app.api.orchestrator import OrchestratorRequest, get_orchestrator
app/api/orchestrator.py:14: in <module>
    from app.api.services.lesson_service import LessonService
app/api/services/lesson_service.py:17: in <module>
    from app.api.judiciary.profiler import EtherPromptModifier
E   ImportError: cannot import name 'EtherPromptModifier' from 'app.api.judiciary.profiler' (/home/runner/work/edo-boost-main/edo-boost-main/app/api/judiciary/profiler.py)
___________________ test_guardian_login_invalid_credentials ____________________
tests/integration/test_auth_lifecycle.py:15: in test_guardian_login_invalid_credentials
    response = await client.post(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1892: in post
    return await self.request(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1574: in request
    return await self.send(request, auth=auth, follow_redirects=follow_redirects)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1661: in send
    response = await self._send_handling_auth(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1689: in _send_handling_auth
    response = await self._send_handling_redirects(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1726: in _send_handling_redirects
    response = await self._send_single_request(request)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_client.py:1763: in _send_single_request
    response = await transport.handle_async_request(request)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/httpx/_transports/asgi.py:164: in handle_async_request
    await self.app(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/applications.py:123: in __call__
    await self.middleware_stack(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/errors.py:186: in __call__
    raise exc
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/errors.py:164: in __call__
    await self.app(scope, receive, _send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/prometheus_fastapi_instrumentator/middleware.py:169: in __call__
    raise exc
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/prometheus_fastapi_instrumentator/middleware.py:167: in __call__
    await self.app(scope, receive, send_wrapper)
app/api/main.py:88: in __call__
    await self.app(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/gzip.py:24: in __call__
    await responder(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/gzip.py:44: in __call__
    await self.app(scope, receive, self.send_with_gzip)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/middleware/exceptions.py:65: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/_exception_handler.py:64: in wrapped_app
    raise exc
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    await app(scope, receive, sender)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:756: in __call__
    await self.middleware_stack(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:776: in app
    await route.handle(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:297: in handle
    await self.app(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:77: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/_exception_handler.py:64: in wrapped_app
    raise exc
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    await app(scope, receive, sender)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/starlette/routing.py:72: in app
    response = await func(request)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/routing.py:278: in app
    raw_response = await run_endpoint_function(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/routing.py:191: in run_endpoint_function
    return await dependant.call(**values)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/slowapi/extension.py:734: in async_wrapper
    response = await func(*args, **kwargs)  # type: ignore
app/api/routers/auth.py:221: in guardian_login
    parent = await _find_parent_by_email(session, email_lower)
app/api/routers/auth.py:133: in _find_parent_by_email
    result = await session.execute(select(ParentAccount))
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/session.py:461: in execute
    result = await greenlet_spawn(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:2351: in execute
    return self._execute_internal(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:2226: in _execute_internal
    conn = self._connection_for_bind(bind)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:2095: in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
<string>:2: in _connection_for_bind
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1189: in _connection_for_bind
    conn = bind.connect()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:3276: in connect
    return self._connection_cls(self)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:146: in __init__
    self._dbapi_connection = engine.raw_connection()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:3300: in raw_connection
    return self.pool.connect()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/pool/base.py:449: in connect
    return _ConnectionFairy._checkout(self)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/pool/base.py:1362: in _checkout
    with util.safe_reraise():
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py:146: in __exit__
    raise exc_value.with_traceback(exc_tb)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/pool/base.py:1300: in _checkout
    result = pool._dialect._do_ping_w_event(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/default.py:715: in _do_ping_w_event
    return self.do_ping(dbapi_connection)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:1138: in do_ping
    dbapi_connection.ping()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:810: in ping
    self._handle_exception(error)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:791: in _handle_exception
    raise error
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:808: in ping
    _ = self.await_(self._async_ping())
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:131: in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:817: in _async_ping
    await tr.start()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/asyncpg/connection.py:350: in execute
    result = await self._protocol.query(query, timeout)
asyncpg/protocol/protocol.pyx:374: in query
    ???
E   RuntimeError: Task <Task pending name='Task-11' coro=<test_guardian_login_invalid_credentials() running at /home/runner/work/edo-boost-main/edo-boost-main/tests/integration/test_auth_lifecycle.py:15> cb=[_run_until_complete_cb() at /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/asyncio/base_events.py:181]> got Future <Future pending cb=[Protocol._on_waiter_completed()]> attached to a different loop
------------------------------ Captured log call -------------------------------
ERROR    sqlalchemy.pool.impl.AsyncAdaptedQueuePool:base.py:378 Exception terminating connection <AdaptedConnection <asyncpg.connection.Connection object at 0x7fb528fa7100>>
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 374, in _close_connection
    self._dialect.do_terminate(connection)
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 1105, in do_terminate
    dbapi_connection.terminate()
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 884, in terminate
    self.await_(self._connection.close(timeout=2))
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 131, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/asyncpg/connection.py", line 1467, in close
    await self._protocol.close(timeout)
  File "asyncpg/protocol/protocol.pyx", line 626, in close
  File "asyncpg/protocol/protocol.pyx", line 659, in asyncpg.protocol.protocol.BaseProtocol._request_cancel
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/asyncpg/connection.py", line 1611, in _cancel_current_command
    self._cancellations.add(self._loop.create_task(self._cancel(waiter)))
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/asyncio/base_events.py", line 435, in create_task
    self._check_closed()
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/asyncio/base_events.py", line 520, in _check_closed
Error:     raise RuntimeError('Event loop is closed')
RuntimeError: Event loop is closed
____ TestCeleryStudyPlanTasks.test_orchestrator_mocked_for_plan_generation _____
tests/integration/test_celery_study_plan.py:170: in test_orchestrator_mocked_for_plan_generation
    with patch(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:1430: in __enter__
    self.target = self.getter()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pkgutil.py:715: in resolve_name
    result = getattr(result, p)
E   AttributeError: module 'app.api' has no attribute 'orchestrator'
____________ TestLessonPipelineEndToEnd.test_full_pipeline_success _____________
tests/integration/test_five_pillar_pipeline.py:74: in test_full_pipeline_success
    with patch("app.api.services.lesson_service.call_llm", new_callable=AsyncMock) as mock_llm:
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:1430: in __enter__
    self.target = self.getter()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pkgutil.py:715: in resolve_name
    result = getattr(result, p)
E   AttributeError: module 'app.api.services' has no attribute 'lesson_service'
_________ TestLessonPipelineEndToEnd.test_learner_id_never_reaches_llm _________
tests/integration/test_five_pillar_pipeline.py:94: in test_learner_id_never_reaches_llm
    with patch("app.api.services.lesson_service.call_llm", side_effect=capture):
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:1430: in __enter__
    self.target = self.getter()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pkgutil.py:715: in resolve_name
    result = getattr(result, p)
E   AttributeError: module 'app.api.services' has no attribute 'lesson_service'
___________ TestLessonPipelineEndToEnd.test_llm_failure_returns_503 ____________
tests/integration/test_five_pillar_pipeline.py:106: in test_llm_failure_returns_503
    with patch("app.api.services.lesson_service.call_llm", new_callable=AsyncMock) as mock_llm:
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:1430: in __enter__
    self.target = self.getter()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pkgutil.py:715: in resolve_name
    result = getattr(result, p)
E   AttributeError: module 'app.api.services' has no attribute 'lesson_service'
________ TestConstitutionalMetadata.test_response_includes_stamp_status ________
tests/integration/test_five_pillar_pipeline.py:139: in test_response_includes_stamp_status
    with patch("app.api.services.lesson_service.call_llm", new_callable=AsyncMock) as mock_llm:
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:1430: in __enter__
    self.target = self.getter()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pkgutil.py:715: in resolve_name
    result = getattr(result, p)
E   AttributeError: module 'app.api.services' has no attribute 'lesson_service'
____ TestConstitutionalMetadata.test_constitutional_health_between_0_and_1 _____
tests/integration/test_five_pillar_pipeline.py:151: in test_constitutional_health_between_0_and_1
    with patch("app.api.services.lesson_service.call_llm", new_callable=AsyncMock) as mock_llm:
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:1430: in __enter__
    self.target = self.getter()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pkgutil.py:715: in resolve_name
    result = getattr(result, p)
E   AttributeError: module 'app.api.services' has no attribute 'lesson_service'
_______ TestFourthEstateIntegration.test_audit_events_emitted_on_success _______
tests/integration/test_five_pillar_pipeline.py:177: in test_audit_events_emitted_on_success
    with patch("app.api.services.lesson_service.call_llm", new_callable=AsyncMock) as mock_llm:
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:1430: in __enter__
    self.target = self.getter()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pkgutil.py:715: in resolve_name
    result = getattr(result, p)
E   AttributeError: module 'app.api.services' has no attribute 'lesson_service'
_______ TestFourthEstateIntegration.test_no_violations_on_clean_request ________
tests/integration/test_five_pillar_pipeline.py:193: in test_no_violations_on_clean_request
    with patch("app.api.services.lesson_service.call_llm", new_callable=AsyncMock) as mock_llm:
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:1430: in __enter__
    self.target = self.getter()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pkgutil.py:715: in resolve_name
    result = getattr(result, p)
E   AttributeError: module 'app.api.services' has no attribute 'lesson_service'
__________ TestPOPIACompliance.test_response_contains_no_learner_pii ___________
tests/integration/test_five_pillar_pipeline.py:225: in test_response_contains_no_learner_pii
    with patch("app.api.services.lesson_service.call_llm", new_callable=AsyncMock) as mock_llm:
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:1430: in __enter__
    self.target = self.getter()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pkgutil.py:715: in resolve_name
    result = getattr(result, p)
E   AttributeError: module 'app.api.services' has no attribute 'lesson_service'
______________ TestLessonGeneration.test_generate_lesson_success _______________
tests/integration/test_lesson_api.py:15: in test_generate_lesson_success
    with patch("app.api.services.lesson_service.call_llm", new_callable=AsyncMock) as mock_llm:
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:1430: in __enter__
    self.target = self.getter()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pkgutil.py:715: in resolve_name
    result = getattr(result, p)
E   AttributeError: module 'app.api.services' has no attribute 'lesson_service'
____________ TestLessonGeneration.test_learner_id_never_in_llm_call ____________
tests/integration/test_lesson_api.py:46: in test_learner_id_never_in_llm_call
    with patch("app.api.services.lesson_service.call_llm", side_effect=capture_prompt):
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:1430: in __enter__
    self.target = self.getter()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pkgutil.py:715: in resolve_name
    result = getattr(result, p)
E   AttributeError: module 'app.api.services' has no attribute 'lesson_service'
______ TestLessonGeneration.test_generate_lesson_llm_failure_returns_503 _______
tests/integration/test_lesson_api.py:61: in test_generate_lesson_llm_failure_returns_503
    with patch("app.api.services.lesson_service.call_llm", new_callable=AsyncMock) as mock_llm:
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:1430: in __enter__
    self.target = self.getter()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/pkgutil.py:715: in resolve_name
    result = getattr(result, p)
E   AttributeError: module 'app.api.services' has no attribute 'lesson_service'
____ TestParentPortalIntegration.test_get_learner_progress_summary_success _____
tests/integration/test_parent_portal_integration.py:98: in test_get_learner_progress_summary_success
    assert result["guardian_id"] == str(mock_guardian_id)
E   KeyError: 'guardian_id'
___ TestParentPortalIntegration.test_get_learner_progress_summary_no_consent ___
tests/integration/test_parent_portal_integration.py:120: in test_get_learner_progress_summary_no_consent
    assert "consent" in str(exc_info.value).lower()
E   AssertionError: assert 'consent' in 'guardian is not linked to this learner'
E    +  where 'guardian is not linked to this learner' = <built-in method lower of str object at 0x7fb52a822df0>()
E    +    where <built-in method lower of str object at 0x7fb52a822df0> = 'Guardian is not linked to this learner'.lower
E    +      where 'Guardian is not linked to this learner' = str(ValueError('Guardian is not linked to this learner'))
E    +        where ValueError('Guardian is not linked to this learner') = <ExceptionInfo ValueError('Guardian is not linked to this learner') tblen=3>.value
_ TestParentPortalIntegration.test_get_learner_progress_summary_consent_revoked _
tests/integration/test_parent_portal_integration.py:148: in test_get_learner_progress_summary_consent_revoked
    with pytest.raises(ValueError) as exc_info:
E   Failed: DID NOT RAISE <class 'ValueError'>
________ TestParentPortalIntegration.test_get_diagnostic_trends_success ________
tests/integration/test_parent_portal_integration.py:217: in test_get_diagnostic_trends_success
    assert len(result["trends"]) == 1
E   KeyError: 'trends'
______ TestParentPortalIntegration.test_get_diagnostic_trends_no_sessions ______
tests/integration/test_parent_portal_integration.py:249: in test_get_diagnostic_trends_no_sessions
    assert len(result["trends"]) == 0
E   KeyError: 'trends'
______ TestParentPortalIntegration.test_get_study_plan_adherence_success _______
tests/integration/test_parent_portal_integration.py:286: in test_get_study_plan_adherence_success
    assert result["adherence_percentage"] == 75.0
E   KeyError: 'adherence_percentage'
______ TestParentPortalIntegration.test_get_study_plan_adherence_no_plan _______
tests/integration/test_parent_portal_integration.py:309: in test_get_study_plan_adherence_no_plan
    result = await service.get_study_plan_adherence(learner_id, mock_guardian_id)
app/api/services/parent_portal_service.py:220: in get_study_plan_adherence
    await self._assert_link(learner_id, guardian_id)
app/api/services/parent_portal_service.py:162: in _assert_link
    raise ValueError("Guardian is not linked to this learner")
E   ValueError: Guardian is not linked to this learner
_______ TestParentPortalIntegration.test_generate_parent_report_success ________
tests/integration/test_parent_portal_integration.py:347: in test_generate_parent_report_success
    result = await service.generate_parent_report(learner_id, mock_guardian_id)
app/api/services/parent_portal_service.py:240: in generate_parent_report
    return await service.run(
app/api/judiciary/base.py:172: in run
    action = await self._build_action(**kwargs)
app/api/services/parent_portal_service.py:54: in _build_action
    await self._assert_consent(learner_pseudonym, self._session)
app/api/judiciary/base.py:159: in _assert_consent
    raise ConsentViolationError(
E   app.api.judiciary.base.ConsentViolationError: Learner a40fb630-5df0-4a6d-af58-5774e650bea2 does not have ACTIVE parental consent. Processing is blocked until consent is granted.
_____________ TestParentPortalIntegration.test_export_data_success _____________
tests/integration/test_parent_portal_integration.py:423: in test_export_data_success
    result = await service.export_data(learner_id, mock_guardian_id)
app/api/services/parent_portal_service.py:259: in export_data
    return await PopiaDeletionService(self._session).export_data(
app/api/services/popia_deletion_service.py:283: in export_data
    await self._verify_guardian_consent(learner_id, guardian_id)
app/api/services/popia_deletion_service.py:432: in _verify_guardian_consent
    if revoked and revoked.occurred_at > consent.occurred_at:
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/unittest/mock.py:653: in __getattr__
    raise AttributeError("Mock object has no attribute %r" % name)
E   AttributeError: Mock object has no attribute 'occurred_at'
_________ TestParentPortalIntegration.test_consent_check_order_matters _________
tests/integration/test_parent_portal_integration.py:498: in test_consent_check_order_matters
    with pytest.raises(ValueError) as exc_info:
E   Failed: DID NOT RAISE <class 'ValueError'>
_______ TestParentPortalIntegration.test_progress_summary_empty_subjects _______
tests/integration/test_parent_portal_integration.py:532: in test_progress_summary_empty_subjects
    assert result["average_subject_mastery"] == 0
E   KeyError: 'average_subject_mastery'
________ TestParentPortalIntegration.test_diagnostic_trends_custom_days ________
tests/integration/test_parent_portal_integration.py:557: in test_diagnostic_trends_custom_days
    assert len(result["trends"]) == 0
E   KeyError: 'trends'
___________________________ test_parent_report_loop ____________________________
tests/integration/test_parent_reporting.py:34: in test_parent_report_loop
    await session.commit()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/session.py:1009: in commit
    await greenlet_spawn(self.sync_session.commit)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:2017: in commit
    trans.commit(_to_root=True)
<string>:2: in commit
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1302: in commit
    self._prepare_impl()
<string>:2: in _prepare_impl
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1277: in _prepare_impl
    self.session.flush()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:4341: in flush
    self._flush(objects)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:4476: in _flush
    with util.safe_reraise():
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py:146: in __exit__
    raise exc_value.with_traceback(exc_tb)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:4437: in _flush
    flush_context.execute()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/unitofwork.py:466: in execute
    rec.execute(self)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/unitofwork.py:642: in execute
    util.preloaded.orm_persistence.save_obj(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py:60: in save_obj
    for (
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py:223: in _organize_states_for_save
    for state, dict_, mapper, connection in _connections_for_states(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py:1753: in _connections_for_states
    connection = uowtransaction.transaction.connection(base_mapper)
<string>:2: in connection
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1039: in connection
    return self._connection_for_bind(bind, execution_options)
<string>:2: in _connection_for_bind
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1175: in _connection_for_bind
    conn = self._parent._connection_for_bind(
<string>:2: in _connection_for_bind
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1189: in _connection_for_bind
    conn = bind.connect()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:3276: in connect
    return self._connection_cls(self)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:146: in __init__
    self._dbapi_connection = engine.raw_connection()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:3300: in raw_connection
    return self.pool.connect()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/pool/base.py:449: in connect
    return _ConnectionFairy._checkout(self)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/pool/base.py:1362: in _checkout
    with util.safe_reraise():
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py:146: in __exit__
    raise exc_value.with_traceback(exc_tb)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/pool/base.py:1300: in _checkout
    result = pool._dialect._do_ping_w_event(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/default.py:715: in _do_ping_w_event
    return self.do_ping(dbapi_connection)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:1138: in do_ping
    dbapi_connection.ping()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:810: in ping
    self._handle_exception(error)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:791: in _handle_exception
    raise error
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:808: in ping
    _ = self.await_(self._async_ping())
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:131: in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:817: in _async_ping
    await tr.start()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/asyncpg/connection.py:350: in execute
    result = await self._protocol.query(query, timeout)
asyncpg/protocol/protocol.pyx:374: in query
    ???
E   RuntimeError: Task <Task pending name='Task-85' coro=<test_parent_report_loop() running at /home/runner/work/edo-boost-main/edo-boost-main/tests/integration/test_parent_reporting.py:34> cb=[_run_until_complete_cb() at /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/asyncio/base_events.py:181]> got Future <Future pending cb=[Protocol._on_waiter_completed()]> attached to a different loop
------------------------------ Captured log call -------------------------------
ERROR    sqlalchemy.pool.impl.AsyncAdaptedQueuePool:base.py:378 Exception terminating connection <AdaptedConnection <asyncpg.connection.Connection object at 0x7fb528fa7790>>
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 374, in _close_connection
    self._dialect.do_terminate(connection)
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 1105, in do_terminate
    dbapi_connection.terminate()
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 884, in terminate
    self.await_(self._connection.close(timeout=2))
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 131, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/asyncpg/connection.py", line 1467, in close
    await self._protocol.close(timeout)
  File "asyncpg/protocol/protocol.pyx", line 626, in close
  File "asyncpg/protocol/protocol.pyx", line 659, in asyncpg.protocol.protocol.BaseProtocol._request_cancel
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/asyncpg/connection.py", line 1611, in _cancel_current_command
    self._cancellations.add(self._loop.create_task(self._cancel(waiter)))
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/asyncio/base_events.py", line 435, in create_task
    self._check_closed()
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/asyncio/base_events.py", line 520, in _check_closed
Error:     raise RuntimeError('Event loop is closed')
RuntimeError: Event loop is closed
__________________________ test_parent_access_revoked __________________________
tests/integration/test_parent_reporting.py:80: in test_parent_access_revoked
    await service.generate_parent_report(learner_id, guardian_id)
app/api/services/parent_portal_service.py:238: in generate_parent_report
    progress = await self.get_learner_progress_summary(learner_id, guardian_id)
app/api/services/parent_portal_service.py:167: in get_learner_progress_summary
    await self._assert_link(learner_id, guardian_id)
app/api/services/parent_portal_service.py:162: in _assert_link
    raise ValueError("Guardian is not linked to this learner")
E   ValueError: Guardian is not linked to this learner

During handling of the above exception, another exception occurred:
tests/integration/test_parent_reporting.py:79: in test_parent_access_revoked
    with pytest.raises(ValueError, match="Guardian consent has been revoked"):
E   AssertionError: Regex pattern did not match.
E    Regex: 'Guardian consent has been revoked'
E    Input: 'Guardian is not linked to this learner'
__________________ test_parent_report_rejects_unknown_fields ___________________
tests/integration/test_phase1_contracts_extended.py:39: in test_parent_report_rejects_unknown_fields
    assert response.status_code == 422
E   assert 401 == 422
E    +  where 401 = <Response [401 Unauthorized]>.status_code
_____________________ test_record_consent_returns_created ______________________
tests/integration/test_privacy_compliance.py:28: in test_record_consent_returns_created
    assert response.status_code in [201, 500]
E   assert 401 in [201, 500]
E    +  where 401 = <Response [401 Unauthorized]>.status_code
________________________ test_execute_deletion_contract ________________________
tests/integration/test_privacy_compliance.py:52: in test_execute_deletion_contract
    assert response.status_code in [404, 200]
E   assert 401 in [404, 200]
E    +  where 401 = <Response [401 Unauthorized]>.status_code
________________________ test_right_to_access_contract _________________________
tests/integration/test_privacy_compliance.py:69: in test_right_to_access_contract
    assert response.status_code in [404, 200]
E   assert 401 in [404, 200]
E    +  where 401 = <Response [401 Unauthorized]>.status_code
___________ TestStudyPlanIntegration.test_generate_save_fetch_cycle ____________
tests/integration/test_study_plan_integration.py:93: in test_generate_save_fetch_cycle
    plan = await service.generate_plan(
E   TypeError: StudyPlanService.generate_plan() missing 2 required positional arguments: 'knowledge_gaps' and 'subjects_mastery'
_________ TestStudyPlanIntegration.test_refresh_plan_creates_new_plan __________
tests/integration/test_study_plan_integration.py:182: in test_refresh_plan_creates_new_plan
    new_plan = await service.refresh_plan(learner_id=learner_id, gap_ratio=0.5)
app/api/services/study_plan_service.py:180: in refresh_plan
    return await self.generate_plan(
app/api/services/study_plan_service.py:144: in generate_plan
    return await self.run(
app/api/judiciary/base.py:172: in run
    action = await self._build_action(**kwargs)
app/api/services/study_plan_service.py:46: in _build_action
    await self._assert_consent(learner_pseudonym, self._session)
app/api/judiciary/base.py:159: in _assert_consent
    raise ConsentViolationError(
E   app.api.judiciary.base.ConsentViolationError: Learner d22221d6-0716-4d82-b5e7-c007980e3b33 does not have ACTIVE parental consent. Processing is blocked until consent is granted.
_________ TestStudyPlanIntegration.test_sparse_data_no_mastery_records _________
tests/integration/test_study_plan_integration.py:222: in test_sparse_data_no_mastery_records
    plan = await service.generate_plan(
E   TypeError: StudyPlanService.generate_plan() missing 2 required positional arguments: 'knowledge_gaps' and 'subjects_mastery'
_________ TestStudyPlanIntegration.test_sparse_data_no_knowledge_gaps __________
tests/integration/test_study_plan_integration.py:254: in test_sparse_data_no_knowledge_gaps
    plan = await service.generate_plan(
E   TypeError: StudyPlanService.generate_plan() missing 2 required positional arguments: 'knowledge_gaps' and 'subjects_mastery'
__________ TestStudyPlanIntegration.test_overload_many_knowledge_gaps __________
tests/integration/test_study_plan_integration.py:287: in test_overload_many_knowledge_gaps
    plan = await service.generate_plan(
E   TypeError: StudyPlanService.generate_plan() missing 2 required positional arguments: 'knowledge_gaps' and 'subjects_mastery'
___________ TestStudyPlanIntegration.test_conflict_gap_ratio_bounds ____________
tests/integration/test_study_plan_integration.py:312: in test_conflict_gap_ratio_bounds
    plan = await service.generate_plan(
E   TypeError: StudyPlanService.generate_plan() missing 2 required positional arguments: 'knowledge_gaps' and 'subjects_mastery'
_________ TestStudyPlanIntegration.test_diagnostic_linkage_integration _________
tests/integration/test_study_plan_integration.py:355: in test_diagnostic_linkage_integration
    plan = await service.generate_plan(
E   TypeError: StudyPlanService.generate_plan() missing 1 required positional argument: 'subjects_mastery'
_______ TestStudyPlanIntegration.test_grade_band_diagnostic_integration ________
tests/integration/test_study_plan_integration.py:383: in test_grade_band_diagnostic_integration
    schedule_r3 = service._generate_weekly_schedule(
E   AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
___ TestStudyPlanIntegration.test_plan_with_rationale_includes_explanations ____
tests/integration/test_study_plan_integration.py:458: in test_plan_with_rationale_includes_explanations
    assert "schedule_with_rationale" in plan_with_rationale
E   AssertionError: assert 'schedule_with_rationale' in {'created_at': '2026-04-30T13:50:02.996796', 'days': {'monday': [{'concept': 'fractions', 'subject': 'MATH', 'task_id': '92fce700-a8fb-4132-901c-c032c63165e8', 'title': 'Review: Fractions', ...}], 'tuesday': []}, 'gap_ratio': 0.4, 'generated_by': 'ALGORITHM', ...}
____________ TestStudyPlanIntegration.test_grade_0_grade_r_handling ____________
tests/integration/test_study_plan_integration.py:485: in test_grade_0_grade_r_handling
    plan = await service.generate_plan(
E   TypeError: StudyPlanService.generate_plan() missing 2 required positional arguments: 'knowledge_gaps' and 'subjects_mastery'
____________ TestStudyPlanIntegration.test_empty_schedule_fallback _____________
tests/integration/test_study_plan_integration.py:508: in test_empty_schedule_fallback
    plan = await service.generate_plan(
app/api/services/study_plan_service.py:144: in generate_plan
    return await self.run(
app/api/judiciary/base.py:172: in run
    action = await self._build_action(**kwargs)
app/api/services/study_plan_service.py:46: in _build_action
    await self._assert_consent(learner_pseudonym, self._session)
app/api/judiciary/base.py:159: in _assert_consent
    raise ConsentViolationError(
E   app.api.judiciary.base.ConsentViolationError: Learner 3eeac199-d644-4560-901a-5aa9e4d599eb does not have ACTIVE parental consent. Processing is blocked until consent is granted.
____________________ test_study_plan_mastery_prioritization ____________________
tests/integration/test_study_plan_mastery.py:35: in test_study_plan_mastery_prioritization
    await session.commit()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/session.py:1009: in commit
    await greenlet_spawn(self.sync_session.commit)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:2017: in commit
    trans.commit(_to_root=True)
<string>:2: in commit
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1302: in commit
    self._prepare_impl()
<string>:2: in _prepare_impl
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1277: in _prepare_impl
    self.session.flush()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:4341: in flush
    self._flush(objects)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:4476: in _flush
    with util.safe_reraise():
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py:146: in __exit__
    raise exc_value.with_traceback(exc_tb)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:4437: in _flush
    flush_context.execute()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/unitofwork.py:466: in execute
    rec.execute(self)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/unitofwork.py:642: in execute
    util.preloaded.orm_persistence.save_obj(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py:60: in save_obj
    for (
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py:223: in _organize_states_for_save
    for state, dict_, mapper, connection in _connections_for_states(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py:1753: in _connections_for_states
    connection = uowtransaction.transaction.connection(base_mapper)
<string>:2: in connection
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1039: in connection
    return self._connection_for_bind(bind, execution_options)
<string>:2: in _connection_for_bind
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1175: in _connection_for_bind
    conn = self._parent._connection_for_bind(
<string>:2: in _connection_for_bind
    ???
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py:139: in _go
    ret_value = fn(self, *arg, **kw)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/orm/session.py:1189: in _connection_for_bind
    conn = bind.connect()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:3276: in connect
    return self._connection_cls(self)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:146: in __init__
    self._dbapi_connection = engine.raw_connection()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/base.py:3300: in raw_connection
    return self.pool.connect()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/pool/base.py:449: in connect
    return _ConnectionFairy._checkout(self)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/pool/base.py:1362: in _checkout
    with util.safe_reraise():
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py:146: in __exit__
    raise exc_value.with_traceback(exc_tb)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/pool/base.py:1300: in _checkout
    result = pool._dialect._do_ping_w_event(
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/engine/default.py:715: in _do_ping_w_event
    return self.do_ping(dbapi_connection)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:1138: in do_ping
    dbapi_connection.ping()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:810: in ping
    self._handle_exception(error)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:791: in _handle_exception
    raise error
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:808: in ping
    _ = self.await_(self._async_ping())
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:131: in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:817: in _async_ping
    await tr.start()
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/asyncpg/connection.py:350: in execute
    result = await self._protocol.query(query, timeout)
asyncpg/protocol/protocol.pyx:374: in query
    ???
E   RuntimeError: Task <Task pending name='Task-127' coro=<test_study_plan_mastery_prioritization() running at /home/runner/work/edo-boost-main/edo-boost-main/tests/integration/test_study_plan_mastery.py:35> cb=[_run_until_complete_cb() at /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/asyncio/base_events.py:181]> got Future <Future pending cb=[Protocol._on_waiter_completed()]> attached to a different loop
------------------------------ Captured log call -------------------------------
ERROR    sqlalchemy.pool.impl.AsyncAdaptedQueuePool:base.py:378 Exception terminating connection <AdaptedConnection <asyncpg.connection.Connection object at 0x7fb528fa66b0>>
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 374, in _close_connection
    self._dialect.do_terminate(connection)
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 1105, in do_terminate
    dbapi_connection.terminate()
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 884, in terminate
    self.await_(self._connection.close(timeout=2))
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 131, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/asyncpg/connection.py", line 1467, in close
    await self._protocol.close(timeout)
  File "asyncpg/protocol/protocol.pyx", line 626, in close
  File "asyncpg/protocol/protocol.pyx", line 659, in asyncpg.protocol.protocol.BaseProtocol._request_cancel
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/asyncpg/connection.py", line 1611, in _cancel_current_command
    self._cancellations.add(self._loop.create_task(self._cancel(waiter)))
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/asyncio/base_events.py", line 435, in create_task
    self._check_closed()
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/asyncio/base_events.py", line 520, in _check_closed
Error:     raise RuntimeError('Event loop is closed')
RuntimeError: Event loop is closed
=============================== warnings summary ===============================
tests/integration/test_api_contracts.py::test_right_to_access_endpoint
tests/integration/test_auth_lifecycle.py::test_guardian_login_invalid_credentials
tests/integration/test_parent_reporting.py::test_parent_report_loop
tests/integration/test_study_plan_mastery.py::test_study_plan_mastery_prioritization
  /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/_pytest/stash.py:108: RuntimeWarning: coroutine 'Connection._cancel' was never awaited
    del self._storage[key]
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

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
app/api/core/celery_app.py                            23      5    78%   91, 102, 114, 124, 137
app/api/core/config.py                                95     13    86%   129, 137-172
app/api/core/database.py                              34     13    62%   16, 44-47, 53-55, 65-72
app/api/core/metrics.py                               54     35    35%   119-163
app/api/core/pii_patterns.py                          36     26    28%   29-63
app/api/fourth_estate.py                             109     67    39%   54-72, 75-109, 112, 125-144, 151-152, 165-166, 179-180, 192, 203-205, 208-213, 230-232, 240, 243-249
app/api/judiciary.py                                  91     69    24%   45-51, 54-57, 66-76, 79-91, 99-166, 178-180
app/api/judiciary/__init__.py                         12      1    92%   16
app/api/judiciary/agent.py                           102    102     0%   6-260
app/api/judiciary/audit_agent.py                     110    110     0%   8-278
app/api/judiciary/base.py                             74     22    70%   54-55, 58-59, 62-66, 120-138, 175-179, 186-187
app/api/judiciary/client.py                           26     26     0%   5-56
app/api/judiciary/compliance.py                       89     89     0%   5-247
app/api/judiciary/engine.py                          104    104     0%   8-319
app/api/judiciary/main.py                             52     52     0%   7-137
app/api/judiciary/models.py                          147      9    94%   55, 63, 88-90, 93-97, 101, 105
app/api/judiciary/profiler.py                         45     31    31%   86-93, 110-116, 130-138, 141-144, 147-159, 162-165, 168-180
app/api/judiciary/provider_router.py                  92     63    32%   43, 46-48, 55-59, 63-71, 75-84, 92-99, 107-114, 127-157, 162-198, 206-208, 221
app/api/judiciary/service.py                         117    117     0%   9-346
app/api/judiciary/services.py                         88     88     0%   6-276
app/api/judiciary/state_machine.py                    74     74     0%   7-216
app/api/judiciary/streams.py                          86     86     0%   7-190
app/api/main.py                                       82     21    74%   52-53, 74-83, 93-108, 113-115, 148, 166-170
app/api/ml/__init__.py                                 0      0   100%
app/api/ml/irt_engine.py                              93     93     0%   7-304
app/api/models/__init__.py                             0      0   100%
app/api/models/api_models.py                         154      0   100%
app/api/models/db_models.py                          283      0   100%
app/api/orchestrator.py                               37     30    19%   15-85
app/api/profiler.py                                   83     83     0%   3-221
app/api/routers/__init__.py                            0      0   100%
app/api/routers/assessments.py                       121     84    31%   66-96, 126-164, 175-193, 215-296, 324-367
app/api/routers/audit.py                              75     43    43%   54-68, 78-88, 102-111, 126-132, 140-163, 171-184
app/api/routers/auth.py                              187    126    33%   50-57, 66-81, 87-95, 102-129, 134-140, 171-204, 223-257, 268-298, 308-329, 349-386, 399-430
app/api/routers/diagnostic.py                        187    152    19%   38-65, 73-100, 117-198, 211-304, 314-455, 469-494, 516-536, 542-559, 568-584, 606-645, 658-670, 682-695, 707-720
app/api/routers/gamification.py                       72     34    53%   52-67, 75-86, 94-102, 110-116
app/api/routers/health.py                              9      1    89%   18
app/api/routers/learners.py                           99     78    21%   32-62, 68-81, 93-111, 121-131, 141-147, 164-265, 287-375
app/api/routers/lessons.py                           101     79    22%   22, 45-134, 152-167, 184, 188-217, 223-227, 233-237, 262-300, 311-327
app/api/routers/parent.py                            184    138    25%   28-32, 48-51, 55-62, 75-90, 102, 114-127, 136-149, 162-178, 192-219, 228-239, 248-259, 268-280, 289-301, 308-332
app/api/routers/study_plans.py                        74     46    38%   47-66, 74-87, 107-129, 142-152, 167-206
app/api/routers/system.py                            154     76    51%   47-52, 70-115, 127-136, 141-155, 160, 202-217, 227-287, 316, 366, 370, 372, 389-399, 411-421
app/api/services/__init__.py                           0      0   100%
app/api/services/audit_query_service.py              119     87    27%   49, 76-118, 149-179, 206-250, 273-312, 348-370
app/api/services/diagnostic_benchmark_service.py     130    130     0%   11-346
app/api/services/dummy_data_service.py                78     60    23%   29, 37-47, 50-123, 133-173
app/api/services/gamification_service.py             178     57    68%   55, 65-70, 75, 251, 255-256, 259, 266, 279-294, 344-377, 385-397, 406-415, 426-444, 450, 465-466, 476
app/api/services/inference_gateway.py                145    116    20%   59-73, 78-80, 90-101, 105-113, 119-135, 149-200, 205, 219-290, 295-303
app/api/services/lesson_service.py                   105     96     9%   18-246
app/api/services/parent_portal_service.py             79     22    72%   56, 76-105, 108-126, 129-146, 273-274
app/api/services/popia_deletion_service.py           126    101    20%   47-63, 76-228, 241-267, 285-373, 407, 420, 433
app/api/services/prompt_manager.py                    25     14    44%   20-33, 38
app/api/services/study_plan_service.py                88     42    52%   48, 66-101, 104-120, 123-134, 191, 206-220, 231-233, 243-244
app/api/tasks/__init__.py                              0      0   100%
app/api/tasks/plan_tasks.py                           65     40    38%   36-97, 112-124, 138-148, 167-168
app/api/tasks/report_tasks.py                         35     35     0%   3-70
app/api/util/encryption.py                            21      6    71%   20-28, 36
--------------------------------------------------------------------------------
TOTAL                                               5041   3136    38%
Coverage HTML written to dir coverage_html

=========================== short test summary info ============================
FAILED tests/integration/test_api_contracts.py::test_diagnostic_invalid_subject_returns_structured_error - ImportError: cannot import name 'EtherPromptModifier' from 'app.api.judiciary.profiler' (/home/runner/work/edo-boost-main/edo-boost-main/app/api/judiciary/profiler.py)
FAILED tests/integration/test_api_contracts.py::test_diagnostic_run_returns_valid_response - ImportError: cannot import name 'EtherPromptModifier' from 'app.api.judiciary.profiler' (/home/runner/work/edo-boost-main/edo-boost-main/app/api/judiciary/profiler.py)
FAILED tests/integration/test_auth_lifecycle.py::test_guardian_login_invalid_credentials - RuntimeError: Task <Task pending name='Task-11' coro=<test_guardian_login_invalid_credentials() running at /home/runner/work/edo-boost-main/edo-boost-main/tests/integration/test_auth_lifecycle.py:15> cb=[_run_until_complete_cb() at /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/asyncio/base_events.py:181]> got Future <Future pending cb=[Protocol._on_waiter_completed()]> attached to a different loop
FAILED tests/integration/test_celery_study_plan.py::TestCeleryStudyPlanTasks::test_orchestrator_mocked_for_plan_generation - AttributeError: module 'app.api' has no attribute 'orchestrator'
FAILED tests/integration/test_five_pillar_pipeline.py::TestLessonPipelineEndToEnd::test_full_pipeline_success - AttributeError: module 'app.api.services' has no attribute 'lesson_service'
FAILED tests/integration/test_five_pillar_pipeline.py::TestLessonPipelineEndToEnd::test_learner_id_never_reaches_llm - AttributeError: module 'app.api.services' has no attribute 'lesson_service'
FAILED tests/integration/test_five_pillar_pipeline.py::TestLessonPipelineEndToEnd::test_llm_failure_returns_503 - AttributeError: module 'app.api.services' has no attribute 'lesson_service'
FAILED tests/integration/test_five_pillar_pipeline.py::TestConstitutionalMetadata::test_response_includes_stamp_status - AttributeError: module 'app.api.services' has no attribute 'lesson_service'
FAILED tests/integration/test_five_pillar_pipeline.py::TestConstitutionalMetadata::test_constitutional_health_between_0_and_1 - AttributeError: module 'app.api.services' has no attribute 'lesson_service'
FAILED tests/integration/test_five_pillar_pipeline.py::TestFourthEstateIntegration::test_audit_events_emitted_on_success - AttributeError: module 'app.api.services' has no attribute 'lesson_service'
FAILED tests/integration/test_five_pillar_pipeline.py::TestFourthEstateIntegration::test_no_violations_on_clean_request - AttributeError: module 'app.api.services' has no attribute 'lesson_service'
FAILED tests/integration/test_five_pillar_pipeline.py::TestPOPIACompliance::test_response_contains_no_learner_pii - AttributeError: module 'app.api.services' has no attribute 'lesson_service'
FAILED tests/integration/test_lesson_api.py::TestLessonGeneration::test_generate_lesson_success - AttributeError: module 'app.api.services' has no attribute 'lesson_service'
FAILED tests/integration/test_lesson_api.py::TestLessonGeneration::test_learner_id_never_in_llm_call - AttributeError: module 'app.api.services' has no attribute 'lesson_service'
FAILED tests/integration/test_lesson_api.py::TestLessonGeneration::test_generate_lesson_llm_failure_returns_503 - AttributeError: module 'app.api.services' has no attribute 'lesson_service'
FAILED tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_learner_progress_summary_success - KeyError: 'guardian_id'
FAILED tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_learner_progress_summary_no_consent - AssertionError: assert 'consent' in 'guardian is not linked to this learner'
 +  where 'guardian is not linked to this learner' = <built-in method lower of str object at 0x7fb52a822df0>()
 +    where <built-in method lower of str object at 0x7fb52a822df0> = 'Guardian is not linked to this learner'.lower
 +      where 'Guardian is not linked to this learner' = str(ValueError('Guardian is not linked to this learner'))
 +        where ValueError('Guardian is not linked to this learner') = <ExceptionInfo ValueError('Guardian is not linked to this learner') tblen=3>.value
FAILED tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_learner_progress_summary_consent_revoked - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_diagnostic_trends_success - KeyError: 'trends'
FAILED tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_diagnostic_trends_no_sessions - KeyError: 'trends'
FAILED tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_study_plan_adherence_success - KeyError: 'adherence_percentage'
FAILED tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_get_study_plan_adherence_no_plan - ValueError: Guardian is not linked to this learner
FAILED tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_generate_parent_report_success - app.api.judiciary.base.ConsentViolationError: Learner a40fb630-5df0-4a6d-af58-5774e650bea2 does not have ACTIVE parental consent. Processing is blocked until consent is granted.
FAILED tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_export_data_success - AttributeError: Mock object has no attribute 'occurred_at'
FAILED tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_consent_check_order_matters - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_progress_summary_empty_subjects - KeyError: 'average_subject_mastery'
FAILED tests/integration/test_parent_portal_integration.py::TestParentPortalIntegration::test_diagnostic_trends_custom_days - KeyError: 'trends'
FAILED tests/integration/test_parent_reporting.py::test_parent_report_loop - RuntimeError: Task <Task pending name='Task-85' coro=<test_parent_report_loop() running at /home/runner/work/edo-boost-main/edo-boost-main/tests/integration/test_parent_reporting.py:34> cb=[_run_until_complete_cb() at /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/asyncio/base_events.py:181]> got Future <Future pending cb=[Protocol._on_waiter_completed()]> attached to a different loop
FAILED tests/integration/test_parent_reporting.py::test_parent_access_revoked - AssertionError: Regex pattern did not match.
 Regex: 'Guardian consent has been revoked'
 Input: 'Guardian is not linked to this learner'
FAILED tests/integration/test_phase1_contracts_extended.py::test_parent_report_rejects_unknown_fields - assert 401 == 422
 +  where 401 = <Response [401 Unauthorized]>.status_code
FAILED tests/integration/test_privacy_compliance.py::test_record_consent_returns_created - assert 401 in [201, 500]
 +  where 401 = <Response [401 Unauthorized]>.status_code
FAILED tests/integration/test_privacy_compliance.py::test_execute_deletion_contract - assert 401 in [404, 200]
 +  where 401 = <Response [401 Unauthorized]>.status_code
FAILED tests/integration/test_privacy_compliance.py::test_right_to_access_contract - assert 401 in [404, 200]
 +  where 401 = <Response [401 Unauthorized]>.status_code
FAILED tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_generate_save_fetch_cycle - TypeError: StudyPlanService.generate_plan() missing 2 required positional arguments: 'knowledge_gaps' and 'subjects_mastery'
FAILED tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_refresh_plan_creates_new_plan - app.api.judiciary.base.ConsentViolationError: Learner d22221d6-0716-4d82-b5e7-c007980e3b33 does not have ACTIVE parental consent. Processing is blocked until consent is granted.
FAILED tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_sparse_data_no_mastery_records - TypeError: StudyPlanService.generate_plan() missing 2 required positional arguments: 'knowledge_gaps' and 'subjects_mastery'
FAILED tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_sparse_data_no_knowledge_gaps - TypeError: StudyPlanService.generate_plan() missing 2 required positional arguments: 'knowledge_gaps' and 'subjects_mastery'
FAILED tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_overload_many_knowledge_gaps - TypeError: StudyPlanService.generate_plan() missing 2 required positional arguments: 'knowledge_gaps' and 'subjects_mastery'
FAILED tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_conflict_gap_ratio_bounds - TypeError: StudyPlanService.generate_plan() missing 2 required positional arguments: 'knowledge_gaps' and 'subjects_mastery'
FAILED tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_diagnostic_linkage_integration - TypeError: StudyPlanService.generate_plan() missing 1 required positional argument: 'subjects_mastery'
FAILED tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_grade_band_diagnostic_integration - AttributeError: 'StudyPlanService' object has no attribute '_generate_weekly_schedule'
FAILED tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_plan_with_rationale_includes_explanations - AssertionError: assert 'schedule_with_rationale' in {'created_at': '2026-04-30T13:50:02.996796', 'days': {'monday': [{'concept': 'fractions', 'subject': 'MATH', 'task_id': '92fce700-a8fb-4132-901c-c032c63165e8', 'title': 'Review: Fractions', ...}], 'tuesday': []}, 'gap_ratio': 0.4, 'generated_by': 'ALGORITHM', ...}
FAILED tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_grade_0_grade_r_handling - TypeError: StudyPlanService.generate_plan() missing 2 required positional arguments: 'knowledge_gaps' and 'subjects_mastery'
FAILED tests/integration/test_study_plan_integration.py::TestStudyPlanIntegration::test_empty_schedule_fallback - app.api.judiciary.base.ConsentViolationError: Learner 3eeac199-d644-4560-901a-5aa9e4d599eb does not have ACTIVE parental consent. Processing is blocked until consent is granted.
FAILED tests/integration/test_study_plan_mastery.py::test_study_plan_mastery_prioritization - RuntimeError: Task <Task pending name='Task-127' coro=<test_study_plan_mastery_prioritization() running at /home/runner/work/edo-boost-main/edo-boost-main/tests/integration/test_study_plan_mastery.py:35> cb=[_run_until_complete_cb() at /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/asyncio/base_events.py:181]> got Future <Future pending cb=[Protocol._on_waiter_completed()]> attached to a different loop
================== 45 failed, 47 passed, 4 warnings in 12.18s ==================
Error: Process completed with exit code 1.

**************************************************************************************************************************

Bootstrap schema errors:

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

***********************************************************************************

POPIA compliance test errors:

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
app/api/fourth_estate.py                             109    109     0%   1-261
app/api/judiciary.py                                  91     69    24%   45-51, 54-57, 66-76, 79-91, 99-166, 178-180
app/api/judiciary/__init__.py                         12      1    92%   16
app/api/judiciary/agent.py                           102    102     0%   6-260
app/api/judiciary/audit_agent.py                     110    110     0%   8-278
app/api/judiciary/base.py                             74     32    57%   54-55, 58-59, 62-66, 95-99, 120-138, 145-159, 172-179, 186-187
app/api/judiciary/client.py                           26     26     0%   5-56
app/api/judiciary/compliance.py                       89     89     0%   5-247
app/api/judiciary/engine.py                          104    104     0%   8-319
app/api/judiciary/main.py                             52     52     0%   7-137
app/api/judiciary/models.py                          147    147     0%   1-252
app/api/judiciary/profiler.py                         45     45     0%   7-180
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
app/api/models/db_models.py                          283      0   100%
app/api/orchestrator.py                               37     37     0%   6-85
app/api/profiler.py                                   83     83     0%   3-221
app/api/routers/__init__.py                            0      0   100%
app/api/routers/assessments.py                       121    121     0%   7-367
app/api/routers/audit.py                              75     75     0%   7-184
app/api/routers/auth.py                              187    137    27%   40-45, 50-57, 64-81, 87-95, 102-129, 133-140, 171-204, 217-257, 268-298, 308-329, 335-336, 349-386, 399-430
app/api/routers/diagnostic.py                        187    187     0%   3-720
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
app/api/services/gamification_service.py             178    178     0%   8-498
app/api/services/inference_gateway.py                145    116    20%   59-73, 78-80, 90-101, 105-113, 119-135, 149-200, 205, 219-290, 295-303
app/api/services/lesson_service.py                   105    105     0%   6-246
app/api/services/parent_portal_service.py             79     53    33%   39-44, 47-56, 76-105, 108-126, 129-146, 152, 155-162, 167-174, 193-200, 220-228, 238-240, 257-259, 273-274
app/api/services/popia_deletion_service.py           126    111    12%   39, 47-63, 76-228, 241-267, 283-373, 400-433
app/api/services/prompt_manager.py                    25     14    44%   20-33, 38
app/api/services/study_plan_service.py                88     88     0%   6-244
app/api/tasks/__init__.py                              0      0   100%
app/api/tasks/plan_tasks.py                           65     65     0%   3-168
app/api/tasks/report_tasks.py                         35     35     0%   3-70
app/api/util/encryption.py                            21     12    43%   9-10, 14-16, 20-28, 32, 36
--------------------------------------------------------------------------------
TOTAL                                               5041   4040    20%
Coverage HTML written to dir coverage_html

============================ 1 deselected in 5.15s =============================
Error: Process completed with exit code 5.

******************************************************************************

Docker Image Security Scan errors:

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

