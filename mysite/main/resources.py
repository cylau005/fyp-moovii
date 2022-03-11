from import_export import resources
from .models import MovieList, RatingList

class MovieListResources(resources.ModelResource):
    class meta:
        model = MovieList

class RatingListResources(resources.ModelResource):
    class meta:
        model = MovieList
