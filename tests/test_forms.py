from datetime import datetime, timedelta

from django.test import TestCase

from todo.forms import TaskForm, TagForm
from todo.models import Tag


class TaskFormTest(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="Work")
        self.tag2 = Tag.objects.create(name="Urgent")

    def test_task_form_valid(self):
        form_data = {
            "content": "Finish the Django project",
            "deadline": (datetime.now() + timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M"),
            "is_done": False,
            "tags": [self.tag1.id, self.tag2.id],
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_without_content(self):
        form_data = {
            "content": "",
            "deadline": (datetime.now() + timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M"),
            "is_done": False,
            "tags": [self.tag1.id, self.tag2.id],
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_task_form_invalid_deadline_format(self):
        form_data = {
            "content": "Task with wrong deadline",
            "deadline": "incorrect-format",
            "is_done": False,
            "tags": [self.tag1.id],
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)
        

class TagFormTest(TestCase):
    def test_tag_form_valid(self):
        form_data = {"name": "New Tag"}
        form = TagForm(data=form_data)
        self.assertTrue(form.is_valid())
