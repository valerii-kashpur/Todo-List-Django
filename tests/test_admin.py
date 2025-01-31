from django.contrib.admin.sites import site
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from todo.admin import TagAdmin, TaskAdmin
from todo.models import Tag, Task


class AdminSiteTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin", password="admin"
        )
        self.client.login(username="admin", password="admin")

        self.tag = Tag.objects.create(name="Work")
        self.task = Task.objects.create(content="Test Task", is_done=False)
        self.task.tags.add(self.tag)

    def test_tag_admin_search_fields(self):
        admin = TagAdmin(self.tag, site)
        self.assertIn("name", admin.search_fields)

    def test_task_admin_list_display(self):
        admin = TaskAdmin(self.task, site)
        expected_fields = (
        "content", "created_at", "deadline", "is_done", "display_tags")
        self.assertEqual(admin.list_display, expected_fields)

    def test_task_admin_search_fields(self):
        admin = TaskAdmin(self.task, site)
        self.assertIn("content", admin.search_fields)

    def test_task_admin_filter_horizontal(self):
        admin = TaskAdmin(self.task, site)
        self.assertIn("tags", admin.filter_horizontal)

    def test_task_admin_display_tags(self):
        admin = TaskAdmin(self.task, site)
        self.assertEqual(admin.display_tags(self.task), "Work")
