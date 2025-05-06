import functools

# Simulated user roles (in a real app, this would come from a user session or database)
CURRENT_USER_ROLE = "admin"
# CURRENT_USER_ROLE = "guest"


def role_required(required_role):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      if CURRENT_USER_ROLE == required_role:
        print(f"User has role '{CURRENT_USER_ROLE}'. Access granted to '{func.__name__}'.")
        return func(*args, **kwargs)
      else:
        print(f"Access denied for '{func.__name__}'. User role '{CURRENT_USER_ROLE}' does not match required role '{required_role}'.")
        # Optionally, raise an exception:
        # raise PermissionError(f"User role '{CURRENT_USER_ROLE}' not authorized.")
        return None # Or some other indication of failure
    return wrapper
  return decorator

@role_required("admin")
def admin_task(task_description):
  print(f"Performing admin task: {task_description}")
  return "Admin task completed"

@role_required("editor")
def editor_task(document_id):
  print(f"Editing document: {document_id}")
  return "Document saved"

# Test with CURRENT_USER_ROLE = "admin"
admin_result = admin_task("System backup")
print(f"Admin task result: {admin_result}\n")

editor_result = editor_task("doc123")
print(f"Editor task result: {editor_result}\n")

# To test with a different role, change CURRENT_USER_ROLE above and rerun.
# For example, if CURRENT_USER_ROLE = "guest":
# admin_task("System backup") would print:
# Access denied for 'admin_task'. User role 'guest' does not match required role 'admin'.
# Admin task result: None