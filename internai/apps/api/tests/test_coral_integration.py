"""
Tests for Coral integration and agent registry.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.agents_registry import (
    ensure_agents_registered,
    get_agent_metadata,
    list_agent_names,
)
from app.coral_client import CoralClient


def test_coral_client_initialization():
    """Test CoralClient initialization with parameters."""
    client = CoralClient("http://test-coral:8080", "test-api-key")
    assert client.base_url == "http://test-coral:8080"
    assert client.headers["Authorization"] == "Bearer test-api-key"


@pytest.mark.asyncio
async def test_register_agent():
    """Test agent registration returns expected structure."""
    client = CoralClient("http://test-coral:8080", "test-key")

    # Mock the httpx response
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "agent_id": "agent_test_123",
            "name": "test_agent",
            "status": "registered",
        }
        mock_response.raise_for_status.return_value = None

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        result = await client.register_agent(
            name="test_agent",
            description="Test agent",
            schema={"input": {}, "output": {}},
            endpoint="/test",
        )

        assert "agent_id" in result
        assert result["name"] == "test_agent"


@pytest.mark.asyncio
async def test_invoke_agent():
    """Test agent invocation returns expected structure."""
    client = CoralClient("http://test-coral:8080", "test-key")

    # Mock the httpx response
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "agent_id": "test_agent_id",
            "status": "completed",
            "result": {"test": "payload"},
        }
        mock_response.raise_for_status.return_value = None

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        result = await client.invoke_agent("test_agent_id", {"test": "payload"})

        assert "agent_id" in result
        assert result["status"] == "completed"


@pytest.mark.asyncio
async def test_list_agents():
    """Test listing agents returns expected structure."""
    client = CoralClient("http://test-coral:8080", "test-key")

    # Mock the httpx response
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "agents": [
                {"agent_id": "agent_1", "name": "test1"},
                {"agent_id": "agent_2", "name": "test2"},
            ]
        }
        mock_response.raise_for_status.return_value = None

        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )

        agents = await client.list_agents()

        assert isinstance(agents, list)
        assert len(agents) == 2
        assert all("agent_id" in agent for agent in agents)


def test_agent_metadata():
    """Test agent metadata retrieval."""
    # Test getting specific agent metadata
    metadata = get_agent_metadata("cv_analyzer")
    assert metadata["name"] == "cv_analyzer"
    assert "input_schema" in metadata
    assert "output_schema" in metadata

    # Test getting non-existent agent
    try:
        get_agent_metadata("non_existent_agent")
        raise AssertionError("Should have raised KeyError")
    except KeyError:
        pass


def test_list_agent_names():
    """Test listing all agent names."""
    names = list_agent_names()
    expected_names = ["cv_analyzer", "job_scout", "matcher", "app_writer", "coach"]

    assert len(names) == 5
    assert all(name in expected_names for name in names)


@pytest.mark.asyncio
@patch("app.agents_registry.os.path.exists")
@patch("app.agents_registry.open")
async def test_ensure_agents_registered(mock_open, mock_exists):
    """Test agent registration with caching."""
    # Mock file operations
    mock_exists.return_value = False
    mock_file = Mock()
    mock_file.__enter__.return_value = mock_file
    mock_open.return_value = mock_file

    client = CoralClient("http://test-coral:8080", "test-key")

    # Mock the register_agent method
    with patch.object(client, "register_agent") as mock_register:
        mock_register.return_value = {
            "agent_id": "test_agent_id",
            "name": "test_agent",
            "status": "registered",
        }

        agent_ids = await ensure_agents_registered(client)

        # Should have registered all 5 agents
        assert len(agent_ids) == 5
        assert all("agent_id" in str(agent_id) for agent_id in agent_ids.values())

        # Should have called register_agent 5 times
        assert mock_register.call_count == 5
