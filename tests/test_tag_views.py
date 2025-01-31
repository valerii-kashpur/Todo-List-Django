from django.test import TestCase
from django.urls import reverse

from todo.models import Tag


class TestTagViews(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="Work")
        self.tag2 = Tag.objects.create(name="Home")
        self.tag3 = Tag.objects.create(name="Shop")
        self.tags = Tag.objects.all()

    def test_tag_list_view_status_code(self):
        response = self.client.get(reverse("todo:tag-list"))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_tags_list(self):
        response = self.client.get(reverse("todo:tag-list"))
        self.assertIn("tag_list", response.context)
        self.assertEqual(len(response.context["tag_list"]), len(self.tags))
