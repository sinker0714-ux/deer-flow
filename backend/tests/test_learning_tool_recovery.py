from types import SimpleNamespace

from langchain_core.messages import ToolMessage

from deerflow.agents.middlewares.tool_error_handling_middleware import ToolErrorHandlingMiddleware


def test_learning_tool_exception_becomes_recoverable_tool_message():
    middleware = ToolErrorHandlingMiddleware()
    request = SimpleNamespace(tool_call={"id": "call-1", "name": "learning_repo_reader"})

    def failing_tool(_request):
        raise RuntimeError("file is outside the allowed learning roots")

    result = middleware.wrap_tool_call(request, failing_tool)

    assert isinstance(result, ToolMessage)
    assert result.tool_call_id == "call-1"
    assert result.name == "learning_repo_reader"
    assert result.status == "error"
    assert "Tool 'learning_repo_reader' failed" in result.text
    assert "outside the allowed learning roots" in result.text
