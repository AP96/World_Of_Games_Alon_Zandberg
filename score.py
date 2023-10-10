from utils import SCORES_FILE_NAME

POINTS_CALCULATOR = lambda difficulty: (difficulty * 3) + 5


# Add the winning points based on the given difficulty to the scores file.
def add_score(difficulty, file_name=SCORES_FILE_NAME):
    won_points = POINTS_CALCULATOR(difficulty)

    try:
        with open(file_name, 'r') as f:
            current_score = int(f.read().strip())
    except (IOError, ValueError):
        # If there's an error (file doesn't exist or content is not an integer)
        current_score = 0

    new_score = current_score + won_points
    with open(file_name, 'w') as f:
        f.write(str(new_score))
