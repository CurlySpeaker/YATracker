from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from project_manager.models import Project, Task
from user_manager.models import Student, Instructor


class ProjectTestCase(TestCase):
    def setUp(self):
        Student.objects.create(name="Student", surname="", user_type="stu", email="ex@ex.com", password="pass")
        Instructor.objects.create(name="Instructor", surname="", user_type="ins", email="ex2@ex.com", password="pass2")

        proj = Project(title="Project",
                       description="Text",
                       instructor=Instructor.objects.get(name="Instructor"))
        proj.save()
        proj.students.add(Student.objects.get(name="Student"))
        proj.save()

    def test_task_creation(self):
        task = Task(title="Task",
                    description="Text",
                    status="todo",
                    project=Project.objects.get(title="Project"))
        task.save()
        task.members.add(Student.objects.get(name="Student"))
        task.save()

        try:
            Task.objects.get(title="Task")
        except ObjectDoesNotExist:
            self.fail("Test failed!")
