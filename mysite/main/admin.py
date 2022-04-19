from django.contrib import admin
from .models import MovieList
from import_export.admin import ImportExportActionModelAdmin
from .models import MovieList, RatingList, PrizeList, Reward_Point, CF_List, Interact_List

# Register your models here.
@admin.register(MovieList)
class MovieListAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'movie_name', 'movie_genre', 'overall_rating', 'date_release', 'movie_image_url')

@admin.register(RatingList)
class RatingListAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'user_id', 'date_rating', 'rating_score', 'movie_id', 'action')

@admin.register(PrizeList)
class RatingListAdmin(ImportExportActionModelAdmin):
    list_display = ('item_id', 'item_name', 'require_points')

@admin.register(Reward_Point)
class RatingListAdmin(ImportExportActionModelAdmin):
    list_display = ('user_id', 'point', 'date_modified', 'redeem_item_id')

@admin.register(CF_List)
class RatingListAdmin(ImportExportActionModelAdmin):
    list_display = ('user_id', 'weighted_score', 'movie_id', 'movie_name', 'movie_image_url')

@admin.register(Interact_List)
class RatingListAdmin(ImportExportActionModelAdmin):
    list_display = ('user_id', 'movie_id', 'movie_name', 'movie_image_url')