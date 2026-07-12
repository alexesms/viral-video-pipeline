import requests

base_url = "https://devops.extrasolid.com"
token = "10|NKXK0zY6VF6nTrFwU0fVjr7iIlmBVASXSXJqntTl2397d5cd"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

app_uuid = "r1397tqxzytjtu5g60vs1rv8"

# Create scheduled task for daily pipeline run
payload = {
    "name": "daily-video-pipeline",
    "command": "cd /app && python3 workflow_orchestrator.py --mode=daily >> /app/pipeline.log 2>&1",
    "expression": "0 8 * * *",
    "container_id": app_uuid
}

print("Creating scheduled task...")
response = requests.post(
    f"{base_url}/api/v1/applications/{app_uuid}/scheduled",
    headers=headers,
    json=payload,
    timeout=30
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:300]}")
