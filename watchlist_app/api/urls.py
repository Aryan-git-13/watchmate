from django.urls import path, include
from watchlist_app.api.views import WatchListAV, WatchDetailAV, StreamPlatformListAV, StreamPlatformDetailAV
urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>', WatchDetailAV.as_view(), name='movie_details'),
    path('stream/', StreamPlatformListAV.as_view(), name="stream"),
    path('stream/<int:id>/', StreamPlatformDetailAV.as_view(), name="stream")
]