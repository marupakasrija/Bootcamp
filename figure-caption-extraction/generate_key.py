import secrets
api_key = secrets.token_urlsafe(32)
print(f"Generated API key: {api_key}")