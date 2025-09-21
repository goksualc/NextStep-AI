import httpx


class CoralClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    async def register_agent(
        self,
        name: str,
        description: str,
        schema: dict,
        endpoint: str,
        pricing: dict | None = None,
    ) -> dict:
        payload = {
            "name": name,
            "description": description,
            "schema": schema,
            "endpoint": endpoint,
            "pricing": pricing or {},
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                f"{self.base_url}/v1/agents", headers=self.headers, json=payload
            )
            r.raise_for_status()
            return r.json()

    async def list_agents(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(f"{self.base_url}/v1/agents", headers=self.headers)
            r.raise_for_status()
            return r.json().get("agents", [])

    async def invoke_agent(self, agent_id: str, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(
                f"{self.base_url}/v1/agents/{agent_id}/invoke",
                headers=self.headers,
                json=payload,
            )
            r.raise_for_status()
            return r.json()
