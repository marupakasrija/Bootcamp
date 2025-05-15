def calculate_score(user_data):
    """Calculates the final score for a user based on their data."""
    base_score = user_data.get('base', 0)
    bonus = user_data.get('bonus', 0)
    penalty = user_data.get('penalty', 0)
    final_score = base_score + bonus - penalty
    return final_score

if __name__ == "__main__":
    user_info = {'base': 100, 'bonus': 20, 'penalty': 5}
    score = calculate_score(user_info)
    print(f"The final score is: {score}")

# Original unclear function name:
# def do_it(d):
#     bs = d.get('b', 0)
#     bn = d.get('bo', 0)
#     p = d.get('p', 0)
#     fs = bs + bn - p
#     return fs