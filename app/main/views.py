from flask import render_template, request, redirect, url_for, abort
from . import main
from ..request import get_movies, get_movie, search_movie
from ..models import Review, User
from .forms import ReviewForm, UpdateProfile
from flask_login import login_required, login_user, logout_user
from .. import db, photos
# from ..email import mail_message


# views
@main.route("/")
def index():
    """
    View root page function that returns the index page and its data
    """

    # Getting popular movie

    popular_movies = get_movies("popular")
    now_showing_movies = get_movies("now_playing")
    up_coming_movies = get_movies("upcoming")
    # print(popular_movies)

    title = "Home - Best Movie Review Website"

    search_movie = request.args.get('movie_query')
    if search_movie:
        return redirect(url_for('main.search', movie_name=search_movie))
    else:
        return render_template(
        "index.html", title=title, popular=popular_movies, now_showing=now_showing_movies, up_coming=up_coming_movies
    )

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template('profile/profile.html', user=user)


@main.route("/movie/<int:id>")
def movie(id):
    '''
    View movie page function that returns the movie details page and its data
    '''
    movie = get_movie(id)
    title = f'{movie.title}'
    reviews = Review.get_reviews(movie.id)
    return render_template("movie.html", title=title, movie=movie, reviews=reviews)


@main.route('/search/<movie_name>')
def search(movie_name):
    '''
    View function to display the search results
    '''
    movie_name_list = movie_name.split(" ")
    movie_name_format = "+".join(movie_name_list)
    searched_movies = search_movie(movie_name_format)
    title = f'Search results for {movie_name}:'
    return render_template('search.html',movies=searched_movies, title=title)

@main.route('/movie/review/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_review(id):
    form = ReviewForm()
    movie = get_movie(id)

    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data
        new_review = Review(movie.id, title, movie.poster, review)

        new_review.save_review()
        # mail_message('New Movie Review!', 'email/welcome_user', user.email, user=user)
        
        return redirect(url_for('main.movie', id=id))

    title = f'{movie.title} review'
    return render_template('new_review.html', title=title, review_form=form, movie=movie)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))