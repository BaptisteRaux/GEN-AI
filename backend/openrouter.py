"""Local LLM client for making requests to distributed council members.

This version replaces OpenRouter with calls to local / remote REST services
(one per model), as defined in backend/config.py::MODEL_ENDPOINTS.
"""

import httpx
from typing import List, Dict, Any, Optional
from .config import MODEL_ENDPOINTS


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via its REST endpoint.

    Args:
        model: Logical model identifier (e.g., "member1", "chairman")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed.
        The shape matches what council.py expects from the original OpenRouter client.
    """
    endpoint_cfg = MODEL_ENDPOINTS.get(model)
    if endpoint_cfg is None:
        print(f"Unknown model identifier in MODEL_ENDPOINTS: {model}")
        return None

    url = endpoint_cfg["url"].rstrip("/") + "/chat"

    payload = {
        "messages": messages
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()

            data = response.json()

            content = data.get("content") or data.get("answer")
            if content is None:
                print(f"Model {model} returned no 'content' field: {data}")
                return None

            return {
                "content": content,
                "reasoning_details": data.get("reasoning_details")
            }

    except Exception as e:
        print(f"Error querying model {model} at {url}: {e}")
        return None

async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of logical model identifiers (e.g. ['member1', 'member2'])
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    tasks = [query_model(model, messages) for model in models]

    responses = await asyncio.gather(*tasks)

    return {model: response for model, response in zip(models, responses)}
