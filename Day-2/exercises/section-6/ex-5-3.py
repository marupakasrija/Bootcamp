def is_valid_user(user_id):
    """Checks if the given user ID is valid."""
    # Simulate a database check
    valid_ids = [1, 5, 10, 15]
    return user_id in valid_ids

def has_permission(user_role, action):
    """Checks if a user role has permission to perform a specific action."""
    permissions = {
        "admin": ["read", "write", "delete"],
        "editor": ["read", "write"],
        "viewer": ["read"]
    }
    return action in permissions.get(user_role, [])

def can_access_resource(user_role, resource_id):
    """Checks if a user role can access a specific resource."""
    # Simulate resource access rules
    if user_role == "viewer" and resource_id > 100:
        return False
    return True

if __name__ == "__main__":
    print(f"Is user 5 valid? {is_valid_user(5)}")
    print(f"Does admin have write permission? {has_permission('admin', 'write')}")
    print(f"Can viewer access resource 50? {can_access_resource('viewer', 50)}")