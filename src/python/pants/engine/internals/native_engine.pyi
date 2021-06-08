# Copyright 2021 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import annotations

from io import RawIOBase
from typing import Any, Sequence, TextIO

from typing_extensions import Protocol

from pants.engine.fs import PathGlobs
from pants.engine.internals.scheduler import Workunit, _PathGlobsAndRootCollection
from pants.engine.internals.session import SessionValues
from pants.engine.process import InteractiveProcess, InteractiveProcessResult

# TODO: black and flake8 disagree about the content of this file:
#   see https://github.com/psf/black/issues/1548
# flake8: noqa: E302

class RawFdRunner(Protocol):
    def __call__(
        self,
        command: str,
        args: tuple[str, ...],
        env: dict[str, str],
        working_directory: bytes,
        cancellation_latch: PySessionCancellationLatch,
        stdin_fileno: int,
        stdout_fileno: int,
        stderr_fileno: int,
    ) -> int: ...

def match_path_globs(path_globs: PathGlobs, paths: tuple[str, ...]) -> str: ...
def capture_snapshots(
    scheduler: PyScheduler,
    session: PySession,
    path_globs_and_root_tuple_wrapper: _PathGlobsAndRootCollection,
) -> tuple[PySnapshot, ...]: ...
def ensure_remote_has_recursive(scheduler: PyScheduler, digests: list[PyDigest]) -> None: ...

# TODO: Should this be a proper FileDigest? Maybe create PyFileDigest.
def single_file_digests_to_bytes(
    scheduler: PyScheduler, digests: list[PyDigest]
) -> list[bytes]: ...
def run_local_interactive_process(
    scheduler: PyScheduler, session: PySession, request: InteractiveProcess
) -> InteractiveProcessResult: ...
def write_digest(
    scheduler: PyScheduler, session: PySession, digest: PyDigest, path_prefix: str
) -> None: ...
def default_cache_path() -> str: ...
def write_log(msg: str, level: int, target: str) -> None: ...
def flush_log() -> None: ...
def set_per_run_log_path(path: str | None) -> None: ...
def maybe_set_panic_handler() -> None: ...
def stdio_initialize(
    level: int,
    show_rust_3rdparty_logs: bool,
    use_color: bool,
    show_target: bool,
    log_levels_by_target: dict[str, int],
    literal_filters: tuple[str, ...],
    regex_filters: tuple[str, ...],
    log_file: str,
) -> tuple[RawIOBase, TextIO, TextIO]: ...
def stdio_thread_get_destination() -> PyStdioDestination: ...
def stdio_thread_set_destination(destination: PyStdioDestination) -> None: ...
def stdio_thread_console_set(stdin_fileno: int, stdout_fileno: int, stderr_fileno: int) -> None: ...
def stdio_thread_console_clear() -> None: ...
def stdio_write_stdout(msg: str) -> None: ...
def stdio_write_stderr(msg: str) -> None: ...
def teardown_dynamic_ui(scheduler: PyScheduler, session: PySession) -> None: ...
def tasks_task_begin(
    tasks: PyTasks,
    func: Any,
    output_type: type,
    can_modify_workunit: bool,
    cacheable: bool,
    name: str,
    desc: str,
    level: int,
) -> None: ...
def tasks_task_end(tasks: PyTasks) -> None: ...
def tasks_add_get(tasks: PyTasks, output: type, input: type) -> None: ...
def tasks_add_select(tasks: PyTasks, selector: type) -> None: ...
def tasks_add_query(tasks: PyTasks, output_type: type, input_type: tuple[type, ...]) -> None: ...
def execution_add_root_select(
    scheduler: PyScheduler,
    execution_request: PyExecutionRequest,
    param_vals: Sequence,
    product: type,
) -> None: ...
def nailgun_client_create(executor: PyExecutor, port: int) -> PyNailgunClient: ...
def nailgun_server_await_shutdown(server: PyNailgunServer) -> None: ...
def nailgun_server_create(
    executor: PyExecutor, port: int, runner: RawFdRunner
) -> PyNailgunServer: ...
def scheduler_create(
    executor: PyExecutor,
    tasks: PyTasks,
    types: PyTypes,
    build_root: str,
    local_execution_root_dir: str,
    named_caches_dir: str,
    ca_certs_path: str | None,
    ignore_patterns: Sequence[str],
    use_gitignore: bool,
    remoting_options: PyRemotingOptions,
    local_store_options: PyLocalStoreOptions,
    exec_strategy_opts: PyExecutionStrategyOptions,
) -> PyScheduler: ...
def scheduler_execute(
    scheduler: PyScheduler, session: PySession, execution_request: PyExecutionRequest
) -> tuple: ...
def scheduler_metrics(scheduler: PyScheduler, session: PySession) -> dict[str, int]: ...
def scheduler_shutdown(scheduler: PyScheduler, timeout_secs: int) -> None: ...
def session_new_run_id(session: PySession) -> None: ...
def session_poll_workunits(
    scheduler: PyScheduler, session: PySession, max_log_verbosity_level: int
) -> tuple[tuple[Workunit, ...], tuple[Workunit, ...]]: ...
def session_get_observation_histograms(scheduler: PyScheduler, session: PySession) -> dict: ...
def session_record_test_observation(
    scheduler: PyScheduler, session: PySession, value: int
) -> None: ...
def session_isolated_shallow_clone(session: PySession, build_id: str) -> PySession: ...
def all_counter_names() -> list[str]: ...
def graph_len(scheduler: PyScheduler) -> int: ...
def graph_visualize(scheduler: PyScheduler, session: PySession, path: str) -> None: ...
def graph_invalidate(scheduler: PyScheduler, paths: Sequence[str]) -> int: ...
def graph_invalidate_all_paths(scheduler: PyScheduler) -> int: ...
def check_invalidation_watcher_liveness(scheduler: PyScheduler) -> None: ...
def validate_reachability(scheduler: PyScheduler) -> None: ...
def rule_graph_consumed_types(
    scheduler: PyScheduler, param_types: Sequence[type], product_type: type
) -> list[type]: ...
def rule_graph_visualize(scheduler: PyScheduler, path: str) -> None: ...
def rule_subgraph_visualize(
    scheduler: PyScheduler, param_types: Sequence[type], product_type: type, path: str
) -> None: ...
def garbage_collect_store(scheduler: PyScheduler, target_size_bytes: int) -> None: ...
def lease_files_in_graph(scheduler: PyScheduler, session: PySession) -> None: ...

class PyDigest:
    def __init__(self, fingerprint: str, serialized_bytes_length: int) -> None: ...
    @property
    def fingerprint(self) -> str: ...
    @property
    def serialized_bytes_length(self) -> int: ...

class PySnapshot:
    def __init__(self) -> None: ...
    @property
    def digest(self) -> PyDigest: ...
    @property
    def dirs(self) -> tuple[str, ...]: ...
    @property
    def files(self) -> tuple[str, ...]: ...

class PyExecutionRequest:
    def __init__(
        self, *, poll: bool, poll_delay_in_ms: int | None, timeout_in_ms: int | None
    ) -> None: ...

class PyExecutionStrategyOptions:
    def __init__(self, **kwargs: Any) -> None: ...

class PyExecutor:
    def __init__(self, *, core_threads: int, max_threads: int) -> None: ...

class PyGeneratorResponseBreak:
    def __init__(self, val: Any) -> None: ...

class PyGeneratorResponseGet:
    def __init__(self, product: type, declared_subject: type, subject: Any) -> None: ...

class PyGeneratorResponseGetMulti:
    def __init__(self, gets: tuple[PyGeneratorResponseGet, ...]) -> None: ...

class PyNailgunServer:
    pass

class PyNailgunClient:
    def execute(self, command: str, args: list[str], env: dict[str, str]) -> int: ...

class PyRemotingOptions:
    def __init__(self, **kwargs: Any) -> None: ...

class PyLocalStoreOptions:
    def __init__(self, **kwargs: Any) -> None: ...

class PyScheduler:
    pass

class PySession:
    def __init__(
        self,
        *,
        scheduler: PyScheduler,
        should_render_ui: bool,
        build_id: str,
        session_values: SessionValues,
        cancellation_latch: PySessionCancellationLatch,
    ) -> None: ...
    def cancel(self) -> None: ...

class PySessionCancellationLatch:
    def __init__(self) -> None: ...

class PyTasks:
    def __init__(self) -> None: ...

class PyTypes:
    def __init__(self, **kwargs: Any) -> None: ...

class PyStdioDestination:
    pass

class PantsdConnectionException(Exception):
    pass

class PantsdClientException(Exception):
    pass

class PollTimeout(Exception):
    pass
