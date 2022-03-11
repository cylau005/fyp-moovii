from django.contrib import admin
from .models import MovieList
from import_export.admin import ImportExportActionModelAdmin
from .models import MovieList, RatingList, PrizeList

# Register your models here.
# admin.site.register(ToDoList)
# admin.site.register(Item)
#admin.site.register(MovieList)
@admin.register(MovieList)
class MovieListAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'movie_name', 'movie_genre', 'overall_rating', 'date_release', 'movie_image_url')

@admin.register(RatingList)
class RatingListAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'username', 'date_rating', 'rating_score', 'movie_id', 'action')

admin.site.register(PrizeList)