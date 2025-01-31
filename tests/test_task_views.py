from django.test import TestCase
from django.urls import reverse

from todo.models import Tag, Task


class TaskListViewTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Work")
        self.task1 = Task.objects.create(content="First Task", is_done=False)
        self.task2 = Task.objects.create(content="Second Task", is_done=True)
        self.task3 = Task.objects.create(content="Third Task", is_done=False)
        self.task1.tags.add(self.tag)
        self.tasks = Task.objects.all()

    def test_task_list_view_status_code(self):
        response = self.client.get(reverse("todo:task-list"))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_tasks_list(self):
        response = self.client.get(reverse("todo:task-list"))
        self.assertIn("task_list", response.context)
        self.assertEqual(len(response.context["task_list"]), len(self.tasks))

    def test_task_list_view_ordering(self):
        response = self.client.get(reverse("todo:task-list"))
        tasks = list(response.context["task_list"])

        expected_order = sorted(
            [self.task1, self.task2, self.task3],
            key=lambda t: (t.is_done, -t.created_at.timestamp()),
        )

        self.assertEqual(tasks, expected_order)


class ToggleTaskStatusTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(content="Test Task", is_done=False)

    def test_toggle_task_status(self):
        url = reverse("todo:toggle-task-status", kwargs={"pk": self.task.pk})
        self.client.post(url)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_done)

        self.client.post(url)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_done)

    def test_toggle_task_status_redirects(self):
        url = reverse("todo:toggle-task-status", kwargs={"pk": self.task.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse("todo:task-list"))
