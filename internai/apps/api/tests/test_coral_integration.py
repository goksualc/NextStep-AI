"""
Tests for Coral integration and agent registry.
"""

from unittest.mock import Mock, patch
from app.coral_client import CoralClient
from app.agents_registry import ensure_agents_registered, get_agent_metadata, list_agent_names


def test_coral_client_initialization():
    """Test CoralClient initialization with environment variables."""
    with patch.dict('os.environ', {
        'CORAL_SERVER_URL': 'http://test-coral:8080',
        'CORAL_API_KEY': 'test-api-key'
    }):
        client = CoralClient()
        assert client.server_url == 'http://test-coral:8080'
        assert client.api_key == 'test-api-key'


def test_coral_client_missing_api_key():
    """Test CoralClient raises error when API key is missing."""
    with patch.dict('os.environ', {}, clear=True):
        try:
            CoralClient()
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "CORAL_API_KEY" in str(e)


def test_register_agent():
    """Test agent registration returns expected structure."""
    with patch.dict('os.environ', {
        'CORAL_API_KEY': 'test-key'
    }):
        client = CoralClient()
        result = client.register_agent(
            name="test_agent",
            description="Test agent",
            schema={"input": {}, "output": {}},
            endpoint="/test"
        )
        
        assert "agent_id" in result
        assert result["name"] == "test_agent"
        assert result["status"] == "registered"


def test_invoke_agent():
    """Test agent invocation returns expected structure."""
    with patch.dict('os.environ', {
        'CORAL_API_KEY': 'test-key'
    }):
        client = CoralClient()
        result = client.invoke_agent("test_agent_id", {"test": "payload"})
        
        assert "agent_id" in result
        assert result["status"] == "completed"
        assert "result" in result


def test_list_agents():
    """Test listing agents returns expected structure."""
    with patch.dict('os.environ', {
        'CORAL_API_KEY': 'test-key'
    }):
        client = CoralClient()
        agents = client.list_agents()
        
        assert isinstance(agents, list)
        assert len(agents) == 5  # We have 5 predefined agents
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
        assert False, "Should have raised KeyError"
    except KeyError:
        pass


def test_list_agent_names():
    """Test listing all agent names."""
    names = list_agent_names()
    expected_names = ["cv_analyzer", "job_scout", "matcher", "app_writer", "coach"]
    
    assert len(names) == 5
    assert all(name in expected_names for name in names)


@patch('app.agents_registry.os.path.exists')
@patch('app.agents_registry.open')
def test_ensure_agents_registered(mock_open, mock_exists):
    """Test agent registration with caching."""
    # Mock file operations
    mock_exists.return_value = False
    mock_file = Mock()
    mock_file.__enter__.return_value = mock_file
    mock_open.return_value = mock_file
    
    with patch.dict('os.environ', {
        'CORAL_API_KEY': 'test-key'
    }):
        client = CoralClient()
        
        # Mock the register_agent method
        with patch.object(client, 'register_agent') as mock_register:
            mock_register.return_value = {
                "agent_id": "test_agent_id",
                "name": "test_agent",
                "status": "registered"
            }
            
            agent_ids = ensure_agents_registered(client)
            
            # Should have registered all 5 agents
            assert len(agent_ids) == 5
            assert all("agent_id" in str(agent_id) for agent_id in agent_ids.values())
            
            # Should have called register_agent 5 times
            assert mock_register.call_count == 5
