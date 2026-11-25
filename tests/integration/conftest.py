import pytest


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark everything under tests/integration/ as an integration test."""
    for item in items:
        if "tests/integration/" in item.path.as_posix():
            item.add_marker(pytest.mark.integration)
