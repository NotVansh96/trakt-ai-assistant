from groq import Groq

from config import GROQ_API_KEY

from database import (
    get_recent_history,
    get_top_ratings,
    get_watchlist_items,
    get_all_watchlist,
    get_taste_profile,
    save_taste_profile
)

client = Groq(
    api_key=GROQ_API_KEY
)


# ==================================================
# AI CHAT
# ==================================================

def ask_gemini(prompt):

    history = get_recent_history(50)
    ratings = get_top_ratings(100)
    watchlist = get_watchlist_items(200)
    taste_profile = get_taste_profile()

    history_text = "\n".join(
        [
            f"{title} ({media_type}) watched at {watched_at}"
            for title, media_type, watched_at in history
        ]
    )

    ratings_text = "\n".join(
        [
            f"{title}: {rating}/10"
            for title, rating in ratings
        ]
    )

    watchlist_text = "\n".join(
        [
            f"{title} ({media_type})"
            for title, media_type in watchlist
        ]
    )

    system_prompt = f"""
You are Vansh's personal entertainment AI assistant.

USER TASTE PROFILE:

{taste_profile}

RECENT WATCH HISTORY:

{history_text}

TOP RATINGS:

{ratings_text}

WATCHLIST:

{watchlist_text}

Rules:

- Use the taste profile as the primary source of truth.
- Use ratings as evidence.
- Use watch history as context.
- Give personalized answers.
- Avoid generic recommendations.
- When recommending titles, prioritize items already present in the watchlist.
- Keep answers practical and concise.
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Groq Error: {str(e)}"


# ==================================================
# WATCH NEXT
# ==================================================

def rank_watchlist():

    profile = get_taste_profile()

    ratings = get_top_ratings(50)

    watchlist = get_all_watchlist()

    ratings_text = "\n".join(
        [
            f"{title}: {rating}/10"
            for title, rating in ratings
        ]
    )

    watchlist_text = "\n".join(
        [
            f"{title} ({media_type})"
            for title, media_type in watchlist
        ]
    )

    prompt = f"""
You are an elite recommendation engine.

USER TASTE PROFILE:

{profile}

USER'S HIGHEST RATED TITLES:

{ratings_text}

WATCHLIST:

{watchlist_text}

TASK:

Rank ONLY the 10 BEST titles from the watchlist.

Rules:

- Be highly selective.
- Quality is more important than quantity.
- Use the user's highest-rated titles as evidence.
- Explain WHY each recommendation matches.
- Reference specific titles the user rated highly.
- Focus on:
    - themes
    - emotional impact
    - character arcs
    - storytelling style
    - mythology
    - inspiration
    - family dynamics
    - world-building
    - humor
    - adventure

Avoid:

- "popular"
- "critically acclaimed"
- "highly rated"
- "fan favorite"
- generic praise

For every recommendation provide:

Rank
Title
Match Score (1-100)
Similar To
Why It Matches

Format:

#1 Title

Match Score: 98

Similar To:
- Title A
- Title B

Why It Matches:
Detailed explanation

#2 Title

Match Score: 95

Similar To:
- Title A
- Title B

Why It Matches:
Detailed explanation
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Groq Error: {str(e)}"

# ==================================================
# DASHBOARD RECOMMENDATIONS
# ==================================================

def get_top_recommendations():

    profile = get_taste_profile()

    watchlist = get_all_watchlist()

    watchlist_text = "\n".join(
        [
            f"{title} ({media_type})"
            for title, media_type in watchlist
        ]
    )

    prompt = f"""
You are a recommendation engine.

USER TASTE PROFILE:

{profile}

WATCHLIST:

{watchlist_text}

TASK:

Select the 5 BEST titles from the watchlist.

Important:

- Consider both movies and shows.
- Do not favor movies over shows.
- If a show is a stronger match than a movie, select the show.
- Return the best overall matches regardless of format.

Rules:

- Return ONLY titles already present in the watchlist.
- No explanations.
- No rankings.
- No scores.
- No bullet points.
- No markdown.
- No intro text.
- One title per line.

Example:

Spider-Man: Beyond the Spider-Verse
The Amazing Spider-Man
The Mandalorian and Grogu
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        recommendations = (
            response
            .choices[0]
            .message
            .content
            .strip()
            .split("\n")
        )

        recommendations = [
            item.strip()
            for item in recommendations
            if item.strip()
        ]

        # Remove accidental explanation lines
        recommendations = [
            item
            for item in recommendations
            if len(item) < 80
        ]

        return recommendations[:5]

    except Exception as e:

        print(e)

        return []

# ==================================================
# TASTE PROFILE
# ==================================================

def generate_taste_profile():

    ratings = get_top_ratings(124)

    ratings_text = "\n".join(
        [
            f"{title}: {rating}/10"
            for title, rating in ratings
        ]
    )

    prompt = f"""
Analyze the user's ratings.

Only make conclusions supported by evidence.

Do not write paragraphs.

Return EXACTLY this format:

Return EXACTLY this format:

GENRES: Fantasy, Adventure, Animation, Superhero

THEMES: Friendship, Heroism, Family, Self-Discovery

STYLES: Fast-Paced, Character-Driven, World-Building

CONTENT: Movies, TV Shows, Animation

DISLIKES: Slow-Paced, Weak Characters, Poor Writing

RECOMMENDATION STRATEGY: Fantasy, Superheroes, Character-Driven Stories

Ratings:

{ratings_text}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        profile = response.choices[0].message.content

        save_taste_profile(profile)

        return profile

    except Exception as e:
        return f"Groq Error: {str(e)}"