import pytest
import os
import subprocess
from unittest.mock import patch, MagicMock, AsyncMock
from sbtumcp.main import get_status, run_adb_command, ask_local_ollama

def test_get_status():
    status = get_status()
    assert "SBTUMCP Core is Online" in status
    assert "Status: Master Ball is in control" in status

@pytest.mark.asyncio
async def test_run_adb_command_success():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=["adb", "devices"],
            returncode=0,
            stdout="List of devices attached\ndevice123\tdevice\n",
            stderr=""
        )
        res = await run_adb_command("devices")
        assert "device123" in res

@pytest.mark.asyncio
async def test_run_adb_command_error():
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = Exception("ADB not found")
        res = await run_adb_command("devices")
        assert "ADB Error: ADB not found" in res

@pytest.mark.asyncio
async def test_ask_local_ollama_api_success():
    # Test httpx.AsyncClient post success
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json = MagicMock(return_value={"response": "Hello world!"})
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        res = await ask_local_ollama("test prompt", "llama3")
        assert "Ollama (llama3) Response:\nHello world!" in res

@pytest.mark.asyncio
async def test_ask_local_ollama_fallback_success():
    # Test httpx error but subprocess fallback success
    with patch("httpx.AsyncClient.post", side_effect=Exception("HTTP Connection refused")), \
         patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=["ollama", "run", "llama3", "test prompt"],
            returncode=0,
            stdout="Fallback Response",
            stderr=""
        )
        res = await ask_local_ollama("test prompt", "llama3")
        assert "Fallback Response" in res
