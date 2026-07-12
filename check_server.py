import requests

base_url = "https://devops.extrasolid.com"
token = "10|NKXK0zY6VF6nTrFwU0fVjr7iIlmBVASXSXJqntTl2397d5cd"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(f"{base_url}/api/v1/servers", headers=headers, timeout=10)
servers = response.json()

print("=== Coolify Servers ===")
for s in servers:
    print(f"\nServer: {s.get('name')}")
    print(f"  IP: {s.get('ip')}")
    meta = s.get('server_metadata', {})
    print(f"  CPUs: {meta.get('cpus', '?')}")
    print(f"  Memory: {meta.get('memory_bytes', 0) / 1024**3:.1f} GB")
    print(f"  OS: {meta.get('os', '?')}")
    print(f"  Reachable: {s.get('is_reachable')}")
