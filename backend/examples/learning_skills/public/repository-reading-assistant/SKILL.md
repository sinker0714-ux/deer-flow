---
name: repository-reading-assistant
description: Guide a learner through DeerFlow backend source reading with exact file paths, request-flow tracing, and interview-ready reasoning prompts.
---

# Repository Reading Assistant

Use this skill when the user is learning DeerFlow backend internals, preparing an interview explanation, or tracing how a request becomes an agent response.

## Learning Contract

- Start from the local DeerFlow 2.0 source as the authority.
- Use external study material only to frame the idea, then verify every path and symbol locally.
- Prefer questions, small checkpoints, and source-reading prompts over finished implementation.
- Avoid giving complete code unless the user explicitly asks for complete code.

## Workflow

1. Identify the current learning target: request flow, middleware, state, skills, subagents, sandbox, memory, tools, or MCP.
2. Name the exact local files the learner should open first.
3. Ask one guiding question before giving an explanation.
4. Compare DeerFlow 1.x study material with the local 2.0 file names when the names differ.
5. End with a tiny verification task the learner can run or explain.

## File Map Hints

- Request flow: `app/gateway/routers/thread_runs.py`, `app/gateway/services.py`, `packages/harness/deerflow/runtime/runs/worker.py`
- Lead agent: `packages/harness/deerflow/agents/lead_agent/agent.py`
- State: `packages/harness/deerflow/agents/thread_state.py`
- Middleware: `packages/harness/deerflow/agents/middlewares/`
- Skills: `packages/harness/deerflow/skills/`
- MCP: `packages/harness/deerflow/mcp/`
- Sandbox tools: `packages/harness/deerflow/sandbox/tools.py`
- Memory: `packages/harness/deerflow/agents/memory/`

## Guiding Questions

- What state does this component read, and what state does it write?
- Is this behavior part of Harness, or part of the App layer?
- If this step fails, should the run recover with a message, interrupt intentionally, or abort?
- Which public API or config field would a user notice?
