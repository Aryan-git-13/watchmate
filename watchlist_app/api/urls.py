from django.urls import path, include
from watchlist_app.api.views import (WatchListAV, WatchDetailAV, StreamPlatformListAV, StreamPlatformDetailAV,
                                     ReviewsListAV, ReviewDetailAV, ReviewCreateAV, StreamPlatformVS)
from rest_framework.routers import DefaultRouter                                     


router = DefaultRouter()  
router.register('stream', StreamPlatformVS, basename='streamplatform')


urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>', WatchDetailAV.as_view(), name='movie-details'),
    
    path('', include(router.urls)),
    # path('stream/', StreamPlatformListAV.as_view(), name="stream"),
    # path('stream/<int:id>/', StreamPlatformDetailAV.as_view(), name="stream"),

    # path('reviews/', ReviewsListAV.as_view(), name="review-list"),
    # path('reviews/<int:pk>/', ReviewDetailAV.as_view(), name="review-detail")
    path('stream/<int:pk>/review-create', ReviewCreateAV.as_view(), name="review-create"),
    path('stream/<int:pk>/reviews', ReviewsListAV.as_view(), name="review-detail"),
    path('stream/reviews/<int:pk>', ReviewDetailAV.as_view(), name="review-list"),
]