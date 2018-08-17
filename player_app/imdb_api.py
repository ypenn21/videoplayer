# imports
import json
import pdb
import logging
from imdbpie import Imdb
from imdb import IMDb

# models
from .models import Movie

# setup logger
# usage: logger.info("hello info!")
logger = logging.getLogger(__name__)

# movies count for placeholder movies
MOVIES_COUNT = 30

# initialize imdb instance 
imdb = Imdb()
ia = IMDb()

# gets popular titles from imdb
# example model is in docs/movie.json
# should return models.Movie
def get_popular_titles():
    return _unpack_and_parse_movies(imdb.get_popular_titles())

# gets popular movies from imdb
# example model is in docs/movie.json
# should return models.Movie
def get_popular_movies():
    return _unpack_and_parse_movies(imdb.get_popular_movies())

# gets popular shows from imdb
# example model is in docs/movie.json
# should return models.Movie
def get_popular_shows():
    return _unpack_and_parse_movies(imdb.get_popular_shows())

# gets one movie from imdb
# example model is in docs/movie-details.json
# should return models.MovieDetails
def get_movie_details_by_id(id):
    movie_details = ia.get_movie(id[2:])
    return _parse_movie_details(movie_details)

# def _parse_title(title):

#     image_url = title.poster_url
#     trailer_url = title.trailers[0]['url']

#     movie_details_model = MovieDetails.create(
#         title.imdb_id, 
#         title.title, 
#         title.year,
#         title.plot_outline,
#         title.rating,
#         image_url,
#         trailer_url)

#     return movie_details_model

def _unpack_and_parse_movies(movies):
    unpacked_movies = _unpack_movies(movies)

    return list(map(lambda m: _parse_movie(m), unpacked_movies))

def _unpack_movies(movies):
    return movies['ranks']

def _parse_movie(movie):

    movie_id            = _try_get_attribute(movie, 'id').replace('/', '').replace('title', '')
    movie_title         = _try_get_attribute(movie, 'title')
    movie_image         = _try_get_attribute(movie, 'image')
    movie_image_url     = _try_get_attribute(movie_image, 'url')

    movie_model = Movie.create(
        movie_id, 
        movie_title, 
        movie_image_url)

    return movie_model

def _parse_movie_details(movie):

    # base details attributes 
    movie_id            = movie.getID()
    movie_title         = ""
    movie_image         = ""
    movie_image_url     = ""
    year                = ""
    
    # other movie details attributes
    plot_text           = ""

    # videos
    trailer_url         = ""
    
    movie_model = Movie.create(
        movie_id, 
        movie_title, 
        movie_image_url,
        year,
        plot_text,
        trailer_url)

    return movie_model

def _try_get_attribute(obj, attribute):

    if type(obj) is dict and len(obj.keys()) > 0 and attribute in obj:
        return obj[attribute]

    return ""

# creates a number of placeholder movies using test data. 
# returns a list of models.Movie
def _get_placeholder_movies(count):

    movies = []

    for i in range(1, count+1):
        movie_id = "id"
        movie_title = "Movie " + str(i)
        movie_image_url = "http://via.placeholder.com/125x175"

        movie = Movie.create(
            movie_id,
            movie_title,
            movie_image_url
        )

        movies.append(movie)
    
    return movies

# creates a placeholder movie detail object
# returns models.MovieDetails
# def _get_placeholder_movie_details():
    
#     image_url = "http://via.placeholder.com/125x175"
#     trailer_url = "https://github.com/bower-media-samples/big-buck-bunny-1080p-30s/blob/master/video.mp4?raw=true"

#     movie_details_model = MovieDetails.create(
#         "id", 
#         "Movie title", 
#         "2017",
#         "Some plot",
#         8.2,
#         image_url,
#         trailer_url)

#     return movie_details_model