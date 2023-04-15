from django.urls import path, include
from watchlist_app.api.views import (WatchListAV, WatchDetailAV, StreamPlatformListAV, StreamPlatformDetailAV,
                                     ReviewsListAV, ReviewDetailAV, ReviewCreateAV, UserReview, WatchListLAV)
from rest_framework.routers import DefaultRouter                                     


# router = DefaultRouter()
# router.register('stream', StreamPlatformVS, basename='streamplatform')


urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='movie-details'),
    path('list2/', WatchListLAV.as_view(), name='watch-list-2'),
    
    # path('', include(router.urls)),
    path('stream/', StreamPlatformListAV.as_view(), name="stream"),
    path('stream/<int:id>/', StreamPlatformDetailAV.as_view(), name="stream"),

    # path('reviews/', ReviewsListAV.as_view(), name="review-list"),
    # path('reviews/<int:pk>/', ReviewDetailAV.as_view(), name="review-detail")
    path('<int:pk>/review-create/', ReviewCreateAV.as_view(), name="review-create"),
    path('<int:pk>/reviews/', ReviewsListAV.as_view(), name="review-detail"),
    path('reviews/<int:pk>', ReviewDetailAV.as_view(), name="review-list"),
    path('reviews/', UserReview.as_view(), name="user-review-detail"),
]