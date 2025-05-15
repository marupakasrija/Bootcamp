import functools

# Original print: print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)

# Step 1: Fix the separator to '---'
print_with_custom_sep = functools.partial(print, sep='---')
print_with_custom_sep("Hello", "world", "Python")
# Output: Hello---world---Python

# Step 2: Fix the end character to '<<<\n' based on the previous partial
print_custom_sep_and_end = functools.partial(print_with_custom_sep, end='<<<\n')
print_custom_sep_and_end("Chained", "partials", "rock")
# Output: Chained---partials---rock<<<

# Step 3: Prepend a fixed prefix argument (objects are passed first)
# This requires a bit more care as 'print' takes *objects first.
# We can create a helper or use lambda if we want to fix arguments that are not the first few.
# However, to fix the first argument for `print`:
def prefixed_print_func(prefix, *args, **kwargs):
    print(prefix, *args, **kwargs)

# Now use partial on our helper
log_print = functools.partial(prefixed_print_func, "[LOG]")
log_print_custom = functools.partial(log_print, sep=' | ', end=' EOL\n')

log_print("This is a log message.")
# Output: [LOG] This is a log message.

log_print_custom("Event", "UserLoggedIn", "UserID:123")
# Output: [LOG] Event | UserLoggedIn | UserID:123 EOL