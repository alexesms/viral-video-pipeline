import requests

base_url = "https://devops.extrasolid.com"
token = "10|NKXK0zY6VF6nTrFwU0fVjr7iIlmBVASXSXJqntTl2397d5cd"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Create app
payload = {
    "name": "viral-video-pipeline",
    "description": "Automated video dubbing pipeline",
    "project_uuid": "u5qefkqsr86yqidyn5iua00p",
    "server_uuid": "lz7ibnotv4psf9gxv3mpyq7x",
    "environment_name": "production",
    "git_repository": "https://github.com/alexesms/viral-video-pipeline",
    "git_branch": "main",
    "build_pack": "dockerfile",
    "ports_exposes": "8080"
}

print("Creating application...")
response = requests.post(
    f"{base_url}/api/v1/applications/public",
    headers=headers,
    json=payload,
    timeout=30
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:300]}")

if response.status_code in [200, 201]:
    result = response.json()
    app_uuid = result.get('uuid')
    print(f"\n✅ Created: {app_uuid}")
    
    # Set domain
    requests.patch(
        f"{base_url}/api/v1/applications/{app_uuid}",
        headers=headers,
        json={"domains": "https://pipeline.extrasolid.com"},
        timeout=30
    )
    
    # Disable health check
    requests.patch(
        f"{base_url}/api/v1/applications/{app_uuid}",
        headers=headers,
        json={"health_check_enabled": False},
        timeout=30
    )
    
    # Start
    start = requests.post(
        f"{base_url}/api/v1/applications/{app_uuid}/start",
        headers=headers,
        timeout=30
    )
    print(f"Start: {start.status_code}")
