import datetime
import calendar

# --- Current Time ---
# Using the provided current time context for consistency in examples
# In a live script, you'd just use datetime.datetime.now()
current_dt_context = datetime.datetime(2025, 5, 6, 22, 15, 45) # As per user context
# For actual current time:
# current_dt_actual = datetime.datetime.now()

print(f"Current Date and Time (from context): {current_dt_context}")

# --- Time Delta Arithmetic ---
today_context = current_dt_context.date()
seven_days_later = today_context + datetime.timedelta(days=7)
print(f"Today (from context): {today_context}")
print(f"7 days from today: {seven_days_later}")

# --- Format Dates ---
formatted_date = today_context.strftime("%Y-%m-%d")
print(f"Today formatted as 'YYYY-MM-DD': {formatted_date}")
formatted_datetime = current_dt_context.strftime("%A, %B %d, %Y %I:%M:%S %p")
print(f"Current datetime formatted: {formatted_datetime}")


# --- Parse Date String ---
date_string = "2024-01-01"
parsed_date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
print(f"Parsed '{date_string}' into date object: {parsed_date_obj}")

datetime_string = "2025-07-15 14:30:00"
parsed_datetime_obj = datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
print(f"Parsed '{datetime_string}' into datetime object: {parsed_datetime_obj}")

# --- Get Weekday Name ---
# Using today_context (May 6, 2025, which is a Tuesday)
weekday_index = today_context.weekday() # Monday is 0 and Sunday is 6
weekday_name = calendar.day_name[weekday_index]
print(f"The date {today_context} is a {weekday_name} (index: {weekday_index})")

# --- Date Comparison ---
date1 = datetime.date(2025, 5, 1)
date2 = today_context # 2025, 5, 6

print(f"\nComparing dates: {date1} and {date2}")
if date1 < date2:
    print(f"{date1} is earlier than {date2}")
elif date2 < date1:
    print(f"{date2} is earlier than {date1}")
else:
    print(f"{date1} and {date2} are the same date")

# --- Generate Calendar Month ---
year_to_show = 2025
month_to_show = 5
print(f"\nCalendar for {calendar.month_name[month_to_show]} {year_to_show}:")
print(calendar.month(year_to_show, month_to_show))

# --- Round Time to Nearest Hour ---
# Given datetime.now(), round it to the top of the hour.
# Using current_dt_context = datetime.datetime(2025, 5, 6, 22, 15, 45)

dt_to_round = current_dt_context
rounded_dt = dt_to_round.replace(minute=0, second=0, microsecond=0)
if dt_to_round.minute >= 30: # If minute is 30 or more, round up to the next hour
    rounded_dt += datetime.timedelta(hours=1)

print(f"\nRounding time:")
print(f"Original datetime: {dt_to_round}")
print(f"Rounded to nearest hour (top of the hour): {rounded_dt}")

dt_early_in_hour = datetime.datetime(2025, 5, 6, 22, 10, 0) # Example: 22:10
rounded_early = dt_early_in_hour.replace(minute=0, second=0, microsecond=0)
if dt_early_in_hour.minute >=30:
    rounded_early += datetime.timedelta(hours=1)
print(f"Original datetime (22:10): {dt_early_in_hour}, Rounded: {rounded_early}")

dt_late_in_hour = datetime.datetime(2025, 5, 6, 22, 50, 0) # Example: 22:50
rounded_late = dt_late_in_hour.replace(minute=0, second=0, microsecond=0)
if dt_late_in_hour.minute >=30:
    rounded_late += datetime.timedelta(hours=1)
print(f"Original datetime (22:50): {dt_late_in_hour}, Rounded: {rounded_late}")