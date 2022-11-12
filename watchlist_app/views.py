from django.shortcuts import render
from watchlist_app.models import Movie
from django.http import JsonResponse

def movie_list(request):
    movies = Movie.objects.all()
    return JsonResponse({'movies':list(movies.values())})

def movie_detail(request, pk):
    movie = Movie.objects.get(pk=pk) 
    print(movie)
    data = {
        'name': movie.name,
        'description': movie.description,
        'active': movie.active
    }
    return JsonResponse(data)
