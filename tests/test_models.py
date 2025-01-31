from django.test import TestCase

from todo.models import Tag, Task


class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Test Tag")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "Test Tag")


class TaskModelTest(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="Work")
        self.tag2 = Tag.objects.create(name="Urgent")
        self.task = Task.objects.create(content="Complete the project", is_done=False)

    def test_task_str(self):
        self.assertEqual(str(self.task), "Complete the project")

    def test_get_tag_names(self):
        self.task.tags.add(self.tag1, self.tag2)
        self.assertEqual(self.task.get_tag_names(), "Work, Urgent")

    def test_get_tag_names_no_tags(self):
        task_without_tags = Task.objects.create(content="Simple task", is_done=True)
        self.assertEqual(task_without_tags.get_tag_names(), "")
