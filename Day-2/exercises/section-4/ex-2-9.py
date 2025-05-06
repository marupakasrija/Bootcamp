import functools
import time
def validate_args(*expected_arg_types, **expected_kwarg_types):
    """
    Decorator to validate argument types for a class method or function.
    `expected_arg_types` are for positional arguments.
    `expected_kwarg_types` are for keyword arguments.
    """
    def decorator(method):
        @functools.wraps(method)
        def wrapper(self_or_arg1, *args, **kwargs): # self_or_arg1 handles both instance methods and static/class methods
            # Determine if it's a method (has 'self') or a regular function
            actual_args = args
            first_arg_offset = 0
            if hasattr(self_or_arg1, method.__name__): # Likely an instance method call
                 actual_args = (self_or_arg1,) + args # Prepend self for arg matching if needed, but we usually validate from *args
                 first_arg_offset = 1 # 'self' is the first arg to the method, but not in *args passed here

            # Validate positional arguments (skipping 'self' if it's an instance method)
            method_args_to_validate = args # These are the *args passed to wrapper
            for i, (arg, expected_type) in enumerate(zip(method_args_to_validate, expected_arg_types)):
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"Argument {i+1} of '{method.__name__}' expected type {expected_type.__name__}, but got {type(arg).__name__}"
                    )

            # Validate keyword arguments
            for name, expected_type in expected_kwarg_types.items():
                if name in kwargs:
                    if not isinstance(kwargs[name], expected_type):
                        raise TypeError(
                            f"Keyword argument '{name}' of '{method.__name__}' expected type {expected_type.__name__}, but got {type(kwargs[name]).__name__}"
                        )
            return method(self_or_arg1, *args, **kwargs)
        return wrapper
    return decorator

class UserProfile:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    @validate_args(str, int) # Expects message (str), priority (int)
    def add_notification(self, message, priority):
        print(f"User {self.username}: Adding notification '{message}' with priority {priority}.")

    @validate_args(new_username=str) # Expects new_username (str)
    def update_username(self, new_username):
        print(f"User {self.username}: Updating username to '{new_username}'.")
        self.username = new_username

    @classmethod
    @validate_args(str) # Expects group_name (str)
    def create_user_group(cls, group_name):
        print(f"Creating user group: {group_name}")
        return f"Group '{group_name}' created."

    @staticmethod
    @validate_args(str, str) # Expects prefix (str), suffix (str)
    def generate_id_string(prefix, suffix):
        return f"{prefix}-{int(time.time())}-{suffix}"


user = UserProfile(1, "john_doe")
user.add_notification("New message received", 1)
# Output: User john_doe: Adding notification 'New message received' with priority 1.

user.update_username(new_username="john_d_updated")
# Output: User john_doe: Updating username to 'john_d_updated'.

UserProfile.create_user_group("Admins")
# Output: Creating user group: Admins

print(UserProfile.generate_id_string("ID", "END"))
# Output: ID-1715010333-END (timestamp will vary)


try:
    user.add_notification("Error test", "high") # 'high' is not an int
except TypeError as e:
    print(f"Error: {e}")
# Output: Error: Argument 2 of 'add_notification' expected type int, but got str

try:
    user.update_username(new_username=123) # 123 is not a str
except TypeError as e:
    print(f"Error: {e}")
# Output: Error: Keyword argument 'new_username' of 'update_username' expected type str, but got int