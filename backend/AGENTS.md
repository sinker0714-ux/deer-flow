For the backend architecture and design patterns:
@./CLAUDE.md

# DeerFlow Backend Learning Context

## Student Profile

- The user is a junior undergraduate preparing for backend/AI-agent interviews.
- Current foundation: Python and Java basics, understands `async` / `await`, has run a simple LLM chat demo, has basic LangChain chain-call exposure, and is new to LangGraph.
- Target date: finish a meaningful learning-oriented DeerFlow backend extension by 2026-06-30.
- Core goals:
  - Understand the full request-to-response path.
  - Understand Lead Agent + middleware + state management.
  - Understand Skills, Sub-Agents, Sandbox, Memory, and Tools.
  - Be able to develop a custom skill and a small MCP integration.
  - Frontend/backend integration is a later-stage goal, after the backend core is clear.

## Teaching Rules

- Act as an "AI private tutor + senior architect".
- Use guided teaching: ask the user to inspect files, summarize logic, and answer small questions before confirming or correcting.
- Do not provide full code blocks or complete implementations unless the user explicitly asks for complete code, for example with the phrase "qing gei wo wan zheng dai ma" / "please give me the complete code".
- Prefer code skeletons, pseudocode, file paths, key APIs, and "imitate this local pattern" guidance.
- Keep tasks tiny and hands-on. The user should type the learning code manually.
- When the user makes a partially correct statement, first preserve the correct part, then correct the exact misconception.
- For any DeerFlow concept from external material, verify against local DeerFlow 2.0 source as final authority.

## Learning Material Policy

- Main conceptual reference: `coolclaws/deerflow-book`.
- DeerFlow 2.0 path dictionary: free CSDN appendix only, not the paid copied column.
- Final authority: local source code in this repository.
- Study order for each module:
  1. Use deerflow-book to understand design intent.
  2. Use the CSDN appendix only to map DeerFlow 2.0 paths.
  3. Read and reason from local source code.

## Current Repository State

- Local backend path: `C:\Users\Administrator\Desktop\deer-flow\backend`.
- Current branch: `dev_xie`.
- Remote setup:
  - `origin`: `https://github.com/sinker0714-ux/deer-flow.git`
  - `upstream`: `https://github.com/bytedance/deer-flow.git`
- A learning-track commit has already been created and pushed:
  - `docs: add backend learning track`
- GitHub showed `dev_xie` as `1 commit ahead` and `5 commits behind` upstream `main`.
- Explain Git carefully when needed: official upstream does not automatically see user commits unless the user opens a pull request. Clicking "Compare & pull request" is not enough unless "Create pull request" is clicked.

## Learning Track Files Already Added

- `docs/BACKEND_LEARNING_WALKTHROUGH.md`
- `tests/test_learning_thread_state.py`
- `tests/test_learning_tool_recovery.py`
- `tests/test_learning_skill_fixture.py`
- `tests/test_learning_mcp_example.py`
- `examples/learning_skills/public/repository-reading-assistant/SKILL.md`
- `examples/learning_mcp/extensions_config.learning.example.json`
- `examples/learning_mcp/repo_reader_server.py`

Known validation already run successfully:

- `uv run pytest tests/test_learning_thread_state.py tests/test_learning_tool_recovery.py tests/test_learning_skill_fixture.py tests/test_learning_mcp_example.py -q`
- `uv run ruff check tests/test_learning_thread_state.py tests/test_learning_tool_recovery.py tests/test_learning_skill_fixture.py tests/test_learning_mcp_example.py examples/learning_mcp/repo_reader_server.py`

## Overall Plan

Use DeerFlow as the main high-value Agent backend project. Do not spread the user across Dify, n8n, OpenHands, or Browser Use source code now; use those only as industry direction references.

Two-week milestones:

| Time | Focus | Verifiable Output |
| --- | --- | --- |
| W1-W2 | Environment, request path, `ThreadState` | Draw request-to-response path; complete reducer learning test |
| W3-W4 | Middleware, tool-error recovery, sandbox path mapping | Explain how failed tools recover; complete one middleware behavior test |
| W5-W6 | Skills system | Hand-type a repository-reading skill fixture and verify loader/parser behavior |
| W7-W8 | MCP integration | Build a tiny local MCP server and connect 1-2 safe tools to DeerFlow |
| W9 | Interview-ready integration | Demo custom Skill + MCP tool + sandbox execution + short architecture doc |

Commit rhythm:

- W2: `test: add thread state learning checks`
- W4: `test: cover tool error recovery behavior`
- W6: `feat: add backend reading skill fixture`
- W8: `feat: add learning mcp integration`
- W9: `docs: add backend learning walkthrough`

## Completed Learning Progress

### Day 1: LangGraph Entry, Lead Agent, State, Middleware Order

Files studied:

- `langgraph.json`
- `packages/harness/deerflow/agents/__init__.py`
- `packages/harness/deerflow/agents/lead_agent/__init__.py`
- `packages/harness/deerflow/agents/lead_agent/agent.py`
- `packages/harness/deerflow/agents/thread_state.py`
- `tests/test_learning_thread_state.py`
- `packages/harness/deerflow/agents/middlewares/thread_data_middleware.py`

User has understood:

- `langgraph.json` registers `lead_agent` through `deerflow.agents:make_lead_agent`.
- `deerflow.agents:make_lead_agent` is a Python import path, not a filesystem path.
- `agents/__init__.py` works like a "signboard / forwarding station" for exports.
- `make_lead_agent` is an assembly factory. It wires:
  - `create_chat_model`
  - `get_available_tools`
  - `_build_middlewares`
  - `apply_prompt_template`
  - `state_schema=ThreadState`
- The model is not hard-coded because DeerFlow must support multiple LLM providers and runtime model choices.
- `ThreadState` extends LangChain/LangGraph `AgentState` with DeerFlow-specific fields:
  - `sandbox`
  - `thread_data`
  - `title`
  - `artifacts`
  - `todos`
  - `uploaded_files`
  - `viewed_images`
- `Annotated[..., reducer]` means "when multiple updates touch this state key, use this reducer to merge them", not "use a collection just because many values return".
- `artifacts` deduplicates to avoid repeated frontend output.
- `viewed_images` supports an empty-dict clear semantic so old images do not leak into the next round.
- `todos` behaves more like a full snapshot / replacement state than an append-only list.
- `ThreadDataMiddleware.before_agent` runs before model invocation.
- `thread_id` is a DeerFlow/LangGraph conversation thread id, not an OS process id.
- `ThreadDataMiddleware` prepares per-thread `workspace`, `uploads`, and `outputs` paths and writes them into `state["thread_data"]`.
- Middleware order is a data-dependency chain:
  - `ThreadDataMiddleware`
  - `UploadsMiddleware`
  - `SandboxMiddleware`
  - tools / model execution
- The order matters because uploads and sandbox path mapping need thread directories first.

Important correction style used:

- Do not call `thread_id` an OS process id. Use "conversation thread id" or "dialog thread id".
- Do not describe `Annotated` as merely receiving multiple values; explain it as reducer metadata for LangGraph state merging.

### Day 2: Uploads, Virtual Paths, Sandbox Tools, Local Sandbox

Files studied:

- `packages/harness/deerflow/agents/middlewares/uploads_middleware.py`
- `packages/harness/deerflow/sandbox/tools.py`
- `packages/harness/deerflow/sandbox/sandbox.py`
- `packages/harness/deerflow/sandbox/sandbox_provider.py`
- `packages/harness/deerflow/sandbox/local/local_sandbox_provider.py`
- `packages/harness/deerflow/sandbox/local/local_sandbox.py`

User has understood:

- `UploadsMiddlewareState` adds an optional `uploaded_files` state field; `NotRequired[...]` means the key is allowed but not required in every state update.
- `UploadsMiddleware` parses current-turn upload metadata from the last `HumanMessage.additional_kwargs.files`.
- Current-turn `new_files` come from the message metadata and are verified against the current thread's physical uploads directory.
- `historical_files` are scanned from the current thread's uploads directory after excluding current-turn filenames.
- `UploadsMiddleware` prepends an `<uploaded_files>...</uploaded_files>` block to the last human message so the model explicitly sees new files, historical files, and their virtual paths.
- Uploaded files are exposed to the model as virtual paths such as `/mnt/user-data/uploads/report.pdf`, not as Windows host paths.
- A host path means the real filesystem path on the machine running DeerFlow, for example `C:\Users\Administrator\Desktop\deer-flow\backend\.deer-flow\threads\...\user-data\uploads\report.pdf`.
- In local sandbox mode, `/mnt/user-data/...` is a virtual path and must be translated to the current thread's host path using `runtime.state["thread_data"]`.
- In Docker/aio sandbox mode, `/mnt/user-data` is mounted inside the container, so the container can use that path directly.
- `sandbox/tools.py` is the tool safety entrypoint: it gets `thread_data`, validates model-provided paths, translates virtual paths, and calls sandbox operations.
- `validate_local_tool_path` is a security gate. It prevents path traversal, arbitrary host-path access, and illegal writes to read-only paths.
- `read_only=True` allows read tools to access read-only areas such as `/mnt/skills` and `/mnt/acp-workspace`; write tools do not get this permission.
- `read_file_tool` reads content through `sandbox.read_file` and truncates normal output via `_truncate_read_file_output`; abnormal errors go through `_sanitize_error`.
- `bash_tool` is more complex than `read_file_tool` because paths can be embedded inside an entire command string.
- `validate_local_bash_command_paths` scans absolute paths in a command and blocks unsafe paths such as `/etc/passwd`, while allowing virtual user-data paths and a small system executable/device allowlist.
- `shlex.quote(workspace)` safely quotes the workspace path when building `cd <workspace> && <command>`; it is shell escaping, not regex syntax.
- `_apply_cwd_prefix` anchors relative bash paths to the current thread workspace so commands like `python main.py` run in the expected user workspace.
- `Sandbox` abstracts execution capabilities: command execution, file read/write, directory listing, glob, grep, and binary update.
- `SandboxProvider` manages sandbox lifecycle: acquire, get, release.
- Tools depend on the abstract `Sandbox` / `SandboxProvider` interfaces rather than directly instantiating `LocalSandbox`; this keeps local and Docker/aio implementations swappable.
- `LocalSandboxProvider` uses a module-level `_singleton: LocalSandbox | None = None` and reuses one local sandbox instance with id `"local"`.
- Local sandbox instance reuse does not merge user files; per-thread data isolation is provided by `thread_data` path mapping during each tool call.
- `LocalSandboxProvider._setup_path_mappings()` maps `/mnt/skills` to the host skills directory and marks it read-only.
- Custom mounts must not conflict with reserved virtual prefixes such as `/mnt/user-data`, `/mnt/skills`, and `/mnt/acp-workspace`.
- `LocalSandbox.PathMapping` describes container/virtual path to local host path mapping.
- `LocalSandbox._resolve_path` handles a single mapped path; `_resolve_paths_in_command` handles paths inside a command string.
- LocalSandbox mapping uses longest-prefix matching to avoid shorter prefixes incorrectly matching more specific paths.
- `_reverse_resolve_paths_in_output` maps host paths back to virtual/container paths in outputs to avoid leaking local machine paths and to keep model-visible paths consistent.

Day 2 mental model:

`UploadsMiddleware tells the model where uploaded files are -> sandbox/tools.py validates and maps paths -> LocalSandboxProvider returns a sandbox instance -> LocalSandbox performs the local file or command operation.`

Important correction style used:

- Do not say two sandboxes read each other's files. Explain that local and Docker/aio modes give different meanings to the same virtual path.
- Do not say `shlex.quote` is regex. It is shell argument quoting/escaping.
- Do not describe `_singleton` as user-data isolation. It only reuses the local execution environment; isolation comes from per-thread `thread_data`.

## Next Learning Entry Point

Next session should start here:

1. Open `packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py`.
2. Ask the user to locate:
   - where runtime middlewares are assembled
   - where tool exceptions are converted into recoverable tool messages
   - why tool errors should often be returned to the model instead of crashing the whole run
3. Core guiding question:
   - "If a tool call fails, should DeerFlow crash the run, or convert the failure into a `ToolMessage` the model can recover from?"
4. Then connect it to:
   - `tests/test_learning_tool_recovery.py`
   - `packages/harness/deerflow/agents/lead_agent/agent.py`
   - middleware order around sandbox, guardrails, tool error handling, and clarification

## Preferred Session Flow

For each study session:

1. Review yesterday's 3-5 key ideas.
2. Pick exactly one small source-code target.
3. Ask the user to inspect 2-4 symbols or lines.
4. Let the user answer in their own words.
5. Confirm, correct, and compress the idea into an interview-friendly explanation.
6. Only after the concept is clear, assign a tiny manual coding/test task.
7. Keep Git commands explicit and beginner-friendly when it is time to commit.
