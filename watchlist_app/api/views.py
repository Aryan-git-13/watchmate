from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
# from rest_framework.decorators import api_view
from watchlist_app.models import WatchList, StreamPlatform, Reviews
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import AdminOrReadOnly, ReviewUserOrReadOnly


class StreamPlatformVS(viewsets.ViewSet):
    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        platform = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def create(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        print(pk)
        queryset = StreamPlatform.objects.get(pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformListAV(APIView):
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(APIView):
    def get(self, request, id):
        try:
            platform = StreamPlatform.objects.get(pk=id)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, id):
        platform = StreamPlatform.objects.get(pk=id)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        platform = StreamPlatform.objects.get(pk=id)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# WatchList starts here
class WatchListAV(APIView):
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetailAV(APIView):

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ReviewsListAV(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetailAV(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

class ReviewCreateAV(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        Reviews.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_query = Reviews.objects.filter(watchlist=movie, review_user=review_user)
        if review_query.exists():
            raise ValidationError("You already reviewed this movie!")

        if movie.number_of_ratings == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            current_rating = serializer.validated_data['rating']
            movie.avg_rating = (movie.avg_rating + current_rating)/2

        movie.number_of_ratings = movie.number_of_ratings + 1
        movie.save()
        serializer.save(watchlist=movie, review_user=review_user)


class ReviewsListAV(generics.ListAPIView):
    # queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reviews.objects.filter(watchlist=pk)


class ReviewDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
