global_var = 10

def modify_global():
    global global_var
    global_var = 25
    print(f"Global variable modified inside function: {global_var}")

print(f"Global variable before modification: {global_var}")
modify_global()
print(f"Global variable after modification: {global_var}")