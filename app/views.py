from flask import render_template

from app import app

# views
@app.route("/")
def index():
    message = "Hellooo Macy"
    title = "Home - Best Movie Review Website"
    return render_template("index.html", text=message, title=title)


@app.route("/movie/<movie_id>")
def movie(movie_id):
    return render_template("movie.html", id=movie_id)
