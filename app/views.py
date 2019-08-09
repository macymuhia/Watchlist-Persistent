from flask import render_template

from app import app

from .request import get_movies

# views
@app.route("/")
def index():
    """
    View root page function that returns the index page and its data
    """

    # Getting popular movie

    popular_movies = get_movies("popular")
    now_showing_movies = get_movies("now_playing")
    up_coming_movies = get_movies("upcoming")
    print(popular_movies)

    message = "Hellooo Macy"
    title = "Home - Best Movie Review Website"
    return render_template(
        "index.html", text=message, title=title, popular=popular_movies, now_showing=now_showing_movies, up_coming=up_coming_movies
    )


@app.route("/movie/<movie_id>")
def movie(movie_id):
    return render_template("movie.html", id=movie_id)
