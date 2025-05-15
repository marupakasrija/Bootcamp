def show_settings(**kwargs):
    print("Settings:")
    for key, value in kwargs.items():
        print(f"{key}: {value}")

show_settings(theme="dark", font_size=12)
# Output:
# Settings:
# theme: dark
# font_size: 12

show_settings(language="English", notifications=True, timeout=30)
# Output:
# Settings:
# language: English
# notifications: True
# timeout: 30