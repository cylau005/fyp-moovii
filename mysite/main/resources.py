from import_export import resources
from .models import MovieList, RatingList, PrizeList, Reward_Point

class MovieListResources(resources.ModelResource):
    class meta:
        model = MovieList

class RatingListResources(resources.ModelResource):
    class meta:
        model = MovieList

class PrizeListResources(resources.ModelResource):
    class meta:
        model = PrizeList

class RewardPointResources(resources.ModelResource):
    class meta:
        model = Reward_Point