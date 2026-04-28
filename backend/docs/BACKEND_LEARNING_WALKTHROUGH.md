# DeerFlow Backend Learning Walkthrough

This walkthrough turns the 2026 learning plan into a small, verifiable backend track. It is designed for a learner who already knows Python basics, has seen simple LLM chat, and is starting LangGraph and agent backend development.

## Goal

By 2026-06-30, the learner should be able to explain and lightly extend DeerFlow's backend across four high-value areas:

- LangGraph orchestration
- MCP extension
- sandboxed tool execution
- Skills and Memory product behavior

The target deliverable is not a large platform clone. The best outcome is a compact demo that combines one custom skill, one local MCP server, one sandbox/tool-flow explanation, and a clear request-to-response walkthrough.

## Source Reading Order

Use this order for every module:

1. Read the matching deerflow-book chapter for the design idea.
2. Use the DeerFlow 2.0 path appendix only as a path dictionary.
3. Treat local source code as the final authority.

When names differ between 1.x material and local 2.0 source, prefer the local paths and symbols.

## Module Map

| Area | Local source paths | Learning question |
|---|---|---|
| Request flow | `app/gateway/routers/thread_runs.py`, `app/gateway/services.py`, `packages/harness/deerflow/runtime/runs/worker.py` | Which APIs go through Gateway, and which go directly to LangGraph? |
| Lead Agent | `packages/harness/deerflow/agents/lead_agent/agent.py`, `packages/harness/deerflow/agents/thread_state.py` | What runtime config changes the model, tools, prompt, and state schema? |
| Middleware | `packages/harness/deerflow/agents/middlewares/`, `packages/harness/deerflow/sandbox/middleware.py` | What happens when a tool fails, and why should some failures become `ToolMessage`s? |
| Skills | `packages/harness/deerflow/skills/`, `examples/learning_skills/public/repository-reading-assistant/SKILL.md` | Is a skill code, prompt, permission policy, or workflow memory? |
| MCP | `packages/harness/deerflow/mcp/`, `examples/learning_mcp/` | Why does DeerFlow cache MCP tools, and how is an MCP tool different from a configured local tool? |
| Sandbox | `packages/harness/deerflow/sandbox/` | Which paths are virtual, which are physical, and where is the security boundary? |
| Memory | `packages/harness/deerflow/agents/memory/`, `packages/harness/deerflow/agents/middlewares/memory_middleware.py` | Which messages should update memory, and which should be ignored? |

## Milestones

| Weeks | Checkpoint | Repository artifact |
|---|---|---|
| W1-W2 | Explain request flow and ThreadState reducers | `tests/test_learning_thread_state.py` |
| W3-W4 | Explain middleware recovery for failed tools | `tests/test_learning_tool_recovery.py` |
| W5-W6 | Load a repository-reading skill fixture | `examples/learning_skills/`, `tests/test_learning_skill_fixture.py` |
| W7-W8 | Inspect a minimal local MCP integration | `examples/learning_mcp/`, `tests/test_learning_mcp_example.py` |
| W9 | Present the full learning demo and interview story | This document |

## Local Learning MCP

`examples/learning_mcp/repo_reader_server.py` is a read-only MCP server for source navigation practice. It exposes two tools:

- `list_learning_paths`: list files under allowed backend learning roots
- `read_learning_file`: read UTF-8 text files under allowed backend learning roots

The server is intentionally disabled in `examples/learning_mcp/extensions_config.learning.example.json`. Enable it only in a local `extensions_config.json` when you want to practice MCP wiring.

## Practice Prompts

- Trace a single message from HTTP request to streamed response.
- Explain why `merge_artifacts` deduplicates while preserving order.
- Explain why `merge_viewed_images(existing, {})` clears image state.
- Pick one middleware and identify its input state, output state, and failure behavior.
- Compare one MCP tool with one configured DeerFlow sandbox tool.

## Git Rhythm

Use small commits every one or two weeks:

- `test: add thread state learning checks`
- `test: cover tool error recovery behavior`
- `feat: add backend reading skill fixture`
- `feat: add learning mcp integration`
- `docs: add backend learning walkthrough`
