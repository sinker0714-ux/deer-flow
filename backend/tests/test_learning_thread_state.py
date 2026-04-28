from deerflow.agents.thread_state import merge_artifacts, merge_viewed_images


def test_learning_artifacts_reducer_preserves_order_and_deduplicates():
    merged = merge_artifacts(["workspace/report.md", "outputs/chart.png"], ["outputs/chart.png", "outputs/summary.md"])

    assert merged == ["workspace/report.md", "outputs/chart.png", "outputs/summary.md"]


def test_learning_artifacts_reducer_handles_missing_sides():
    assert merge_artifacts(None, ["outputs/summary.md"]) == ["outputs/summary.md"]
    assert merge_artifacts(["workspace/report.md"], None) == ["workspace/report.md"]


def test_learning_viewed_images_reducer_merges_and_overrides_by_path():
    existing = {
        "/mnt/user-data/uploads/chart.png": {
            "base64": "old-image",
            "mime_type": "image/png",
        }
    }
    new = {
        "/mnt/user-data/uploads/chart.png": {
            "base64": "new-image",
            "mime_type": "image/png",
        },
        "/mnt/user-data/uploads/diagram.jpg": {
            "base64": "diagram-image",
            "mime_type": "image/jpeg",
        },
    }

    merged = merge_viewed_images(existing, new)

    assert merged["/mnt/user-data/uploads/chart.png"]["base64"] == "new-image"
    assert merged["/mnt/user-data/uploads/diagram.jpg"]["mime_type"] == "image/jpeg"


def test_learning_viewed_images_reducer_empty_dict_clears_state():
    existing = {
        "/mnt/user-data/uploads/chart.png": {
            "base64": "image-data",
            "mime_type": "image/png",
        }
    }

    assert merge_viewed_images(existing, {}) == {}
