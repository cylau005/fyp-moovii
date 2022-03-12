from import_export import resources
from .models import MovieList, RatingList, PrizeList

class MovieListResources(resources.ModelResource):
    class meta:
        model = MovieList

class RatingListResources(resources.ModelResource):
    class meta:
        model = MovieList

class PrizeListResources(resources.ModelResource):
    class meta:
        model = PrizeList