def delete_user(user_id):
    print(f"Deleting user with ID: {user_id}")
    return True  # Simulate successful deletion

is_admin = True
user_to_delete = 123
is_admin and delete_user(user_to_delete)

is_admin = False
is_admin and delete_user(456) # This part is not executed