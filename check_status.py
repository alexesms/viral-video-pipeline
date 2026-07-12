import requests

base_url = "https://devops.extrasolid.com"
token = "10|NKXK0zY6VF6nTrFwU0fVjr7iIlmBVASXSXJqntTl2397d5cd"
headers = {"Authorization": f"Bearer {token}"}

app_uuid = "r1397tqxzytjtu5g60vs1rv8"

response = requests.get(
    f"{base_url}/api/v1/applications/{app_uuid}",
    headers=headers,
    timeout=10
)

app = response.json()
print(f"Application: {app.get('name')}")
print(f"Status: {app.get('status')}")
print(f"FQDN: {app.get('fqdn')}")
