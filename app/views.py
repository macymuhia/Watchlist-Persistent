from flask import render_template, request, redirect, url_for

from app import app

from .request import get_movies, get_movie, search_movie

from .models import reviews

from .forms import ReviewForm

Review = reviews.Review

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
    # print(popular_movies)

    message = "Hellooo Macy"
    title = "Home - Best Movie Review Website"

    search_movie = request.args.get('movie_query')
    if search_movie:
        return redirect(url_for('search', movie_name=search_movie))
    else:
        return render_template(
        "index.html", text=message, title=title, popular=popular_movies, now_showing=now_showing_movies, up_coming=up_coming_movies
    )


@app.route("/movie/<int:id>")
def movie(id):
    '''
    View movie page function that returns the movie details page and its data
    '''
    movie = get_movie(id)
    title = f'{movie.title}'
    reviews = Review.get_reviews(movie.id)
    return render_template("movie.html", title=title, movie=movie, reviews=reviews)


@app.route('/search/<movie_name>')
def search(movie_name):
    '''
    View function to display the search results
    '''
    movie_name_list = movie_name.split(" ")
    movie_name_format = "+".join(movie_name_list)
    searched_movies = search_movie(movie_name_format)
    title = f'Search results for {movie_name}:'
    return render_template('search.html',movies=searched_movies, title=title)

@app.route('/movie/review/new/<int:id>', methods=['GET', 'POST'])
def new_review(id):
    form = ReviewForm()
    movie = get_movie(id)

    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data
        new_review = Review(movie.id, title, movie.poster, review)

        new_review.save_review()
        
        return redirect(url_for('movie', id=id))

    title = f'{movie.title} review'
    return render_template('new_review.html', title=title, review_form=form, movie=movie)
