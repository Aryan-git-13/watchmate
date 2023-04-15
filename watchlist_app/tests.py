from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import StreamPlatform, WatchList, Reviews


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="AryanTesting", password="1313")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = StreamPlatform.objects.create(
             name="Youtube",
            about="Reels on google",
            website="https://www.youtube.com"
        )

    def test_streamPlatformCreate(self):
        data = {
            "name": "Youtube",
            "about": "Reels on google",
            "website": "https://www.youtube.com"
        }

        response = self.client.post(reverse('stream-platform'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, 'Stream create failing')

    def test_StreamList(self):
        response = self.client.get(reverse('stream-platform'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_StreamDetail(self):
        response = self.client.get(reverse('stream', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="AryanTesting", password="1313")
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(
            name="Youtube",
            about="Reels on google",
            website="https://www.youtube.com"
        )
        self.watchlist = WatchList.objects.create(
            platform=self.stream,
            title="Example",
            storyline="My story",
            active=True
        )

    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "MyMovie",
            "storyline": "Such a great movie it was",
            "active": True
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_StreamList(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response = self.client.get(reverse('movie-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="AryanTesting", password="1313")
        self.token = Token.objects.get(user=self.user)
        self.stream = StreamPlatform.objects.create(
            name="Youtube",
            about="Reels on google",
            website="https://www.youtube.com"
        )
        self.watchlist = WatchList.objects.create(
            platform=self.stream,
            title="Example",
            storyline="My story",
            active=True
        )
        self.watchlist2 = WatchList.objects.create(
            platform=self.stream,
            title="Example 2",
            storyline="My story 2",
            active=True
        )
        self.review = Reviews.objects.create(
            rating=3,
            description="good movie",
            active=True,
            watchlist=self.watchlist2,
            review_user=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_review_create(self):
        data = {
            "rating": 3,
            "description": "good movie",
            "active": True,
            "watchlist": self.watchlist,
            "review_user": self.user
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_review_update(self):
        data = {
            "rating": 5,
            "description": "good movies always has some point",
            "active": False,
            "watchlist": self.watchlist2,
            "review_user": self.user
        }
        response = self.client.put(reverse('review-list', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_review_list(self):
        response = self.client.get(reverse('review-detail', args=(self.watchlist2.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_detail(self):
        response = self.client.get(reverse('review-list', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username=' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
