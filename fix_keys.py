import re

# Read the file
with open('/Users/alexcheung/viral-video-lab-workflow/workflow_orchestrator.py', 'r') as f:
    content = f.read()

# Replace hardcoded keys with environment variables
content = content.replace(
    'COOLIFY_TOKEN=*** \"10|NKXK0zY6VF6nTrFwU0fVjr7iIlmBVASXSXJqntTl2397d5cd\")',
    'COOLIFY_TOKEN=*** "")'
)

# Write back
with open('/Users/alexcheung/viral-video-lab-workflow/workflow_orchestrator.py', 'w') as f:
    f.write(content)

print("✅ Fixed API key references")
