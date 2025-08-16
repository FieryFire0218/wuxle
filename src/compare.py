def compare_guess(guess, answer):
    result = {}

    # Title match
    if guess["title"].lower() == answer["title"].lower():
        result["title"] = "🎉 Correct!"
        return result  # Game over, early return

    # Author
    result["author"] = "✔️" if guess["author"] == answer["author"] else "❌"

    # Translator
    result["translator"] = "✔️" if guess["translator"] == answer["translator"] else "❌"

    # Genre comparison
    guess_genres = set(guess["genres"])
    answer_genres = set(answer["genres"])
    common_genres = guess_genres.intersection(answer_genres)
    result["genres"] = f"{len(common_genres)}/{len(answer_genres)} match"

    # Rating
    if guess["rating"] == answer["rating"]:
        result["rating"] = "✔️"
    elif guess["rating"] > answer["rating"]:
        result["rating"] = "🔽 Lower"
    else:
        result["rating"] = "🔼 Higher"

    # Chapters
    if guess["chapters"] == answer["chapters"]:
        result["chapters"] = "✔️"
    elif guess["chapters"] > answer["chapters"]:
        result["chapters"] = "🔽 Lower"
    else:
        result["chapters"] = "🔼 Higher"

    return result