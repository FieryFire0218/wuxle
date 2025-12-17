def _normalize_rating_5(v):
    if v is None:
        return None

    s = None
    if isinstance(v, str):
        s = v.strip()
        import re
        m = re.search(r"[-+]?\d*\.?\d+", s)
        if not m:
            return None
        try:
            num = float(m.group(0))
        except (TypeError, ValueError):
            return None
    else:
        try:
            num = float(v)
        except (TypeError, ValueError):
            return None
        s = str(v)

    s_lower = s.lower()

    if "%" in s_lower:
        val = num / 20.0
    elif "/10" in s_lower or (5.0 < num <= 10.0):
        val = num / 2.0
    elif "/5" in s_lower or num <= 5.0:
        val = num
    else:
        val = num / 20.0 if num > 10.0 else num

    return val

def _round_to_half(v: float) -> float:
    return round(v * 2) / 2

def _render_stars(v: float) -> str:
    if v is None:
        return ""
    v = max(0.0, min(5.0, v))
    full = int(v)  # number of full stars
    half = 1 if (v - full) >= 0.5 else 0
    return "★" * full + ("½" if half else "")

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
    result["genres"] = {
        "summary": f"{len(common_genres)}/{len(answer_genres)} match",
        "matched": list(common_genres)
    }
    # Rating
    g_r_raw = _normalize_rating_5(guess.get("rating"))
    a_r_raw = _normalize_rating_5(answer.get("rating"))
    if g_r_raw is None or a_r_raw is None:
        result["rating"] = {
            "summary": "Rating unknown",
            "higher_or_lower": None,
        }
    else:
        g_r = _round_to_half(g_r_raw)
        a_r = _round_to_half(a_r_raw)
        g_r = max(0.0, min(5.0, g_r))
        a_r = max(0.0, min(5.0, a_r))

        g_stars = _render_stars(g_r)
        a_stars = _render_stars(a_r)
        diff = round(g_r - a_r, 2)
        result["rating"] = {
            "summary": f"{g_stars} vs {a_stars} (Δ {diff})",
            "higher_or_lower": "higher" if g_r > a_r else ("lower" if g_r < a_r else "equal"),
        }

    # Chapters
    if guess["chapters"] == answer["chapters"]:
        result["chapters"] = "✔️"
    elif guess["chapters"] > answer["chapters"]:
        result["chapters"] = "🔽 Lower"
    else:
        result["chapters"] = "🔼 Higher"

    return result