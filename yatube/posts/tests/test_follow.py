from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Follow

User = get_user_model()


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(
            username='Author'
        )
        cls.follower = User.objects.create(
            username='User'
        )

    def test_create_follow_from_follower_to_author(self):
        """Проверка создания подписки."""
        self.assertEqual(Follow.objects.count(), 0)
        client_follower = Client()
        client_follower.force_login(FollowTest.follower)
        client_follower.get(
            reverse(
                'posts:profile_follow',
                args=(FollowTest.author.username,)
            )
        )
        self.assertEqual(Follow.objects.count(), 1)
        follow_obj = Follow.objects.first()
        self.assertEqual(follow_obj.author, FollowTest.author)
        self.assertEqual(follow_obj.user, FollowTest.follower)
        client_follower.get(
            reverse(
                'posts:profile_follow',
                args=(FollowTest.author.username,)
            )
        )
        self.assertEqual(Follow.objects.count(), 1)
        follows = Follow.objects.filter(
            author=FollowTest.author,
            user=FollowTest.follower)
        self.assertEqual(len(follows), 1)

    def test_delete_follow_from_follower_to_author(self):
        """Проверка удаления подписки."""
        self.assertEqual(Follow.objects.count(), 0)
        Follow.objects.create(
            author=FollowTest.author,
            user=FollowTest.follower
        )
        self.assertEqual(Follow.objects.count(), 1)
        client_follower = Client()
        client_follower.force_login(FollowTest.follower)
        client_follower.get(
            reverse(
                'posts:profile_unfollow',
                args=(FollowTest.author.username,)
            )
        )
        self.assertEqual(Follow.objects.count(), 0)
        follows = Follow.objects.filter(
            author=FollowTest.author,
            user=FollowTest.follower)
        self.assertFalse(follows)
