from django.test import TestCase

from todo.models import Task
from todo.model_utils import TaskContext, StateErrorException


class TaskStatePatternTestCase(TestCase):
    
    def setUp(self):
        self.new_task = Task.objects.create(
            title="Hello Friend.",
            description="This is a new Task used for testing"
        )
        self.new_task_context = TaskContext(self.new_task)
        self.inprogress_task = Task.objects.create(
            title="Hello Friend.",
            description="This is an in-progress Task used for testing",
            state=Task.IN_PROGRESS
        )
        self.inprogress_task_context = TaskContext(self.inprogress_task)
        self.done_task = Task.objects.create(
            title="Hello Friend.",
            description="This is a done Task used for testing",
            state=Task.DONE
        )
        self.done_task_context = TaskContext(self.done_task)

    def test_new_task_can_be_edited(self):
        task = self.new_task_context.update(
            title="New Task Update",
            description="This is the new task update man."
        )
        self.assertEqual(task.pk, self.new_task.pk)
        self.new_task.refresh_from_db()
        self.assertEqual(self.new_task.title, "New Task Update")
        self.assertEqual(self.new_task.description, "This is the new task update man.")

    def test_new_task_can_not_be_linked(self):
        with self.assertRaises(StateErrorException) as e:
            task = self.new_task_context.link(self.inprogress_task)
        
        self.assertEqual(e.exception._msg, "New tasks can not be linked.")

    def test_new_task_change_state_to_in_progress(self):
        self.new_task_context.change_state()
        self.assertEqual(self.new_task_context._task.state, Task.IN_PROGRESS)
        self.new_task.refresh_from_db()
        self.assertEqual(self.new_task.state, Task.IN_PROGRESS)

    def test_in_progress_task_can_not_be_edited(self):
        with self.assertRaises(StateErrorException) as e:
            task = self.inprogress_task_context.update(
                title="In progress task Update",
                description="This is the inprogress task update man."
            )
        self.assertEqual(e.exception._msg, "Tasks In Progress can not be edited.")

    def test_in_progress_task_can_be_linked(self):
        task = self.inprogress_task_context.link(self.new_task)

        self.assertEqual(task.pk, self.inprogress_task.pk)
        self.assertIn(self.new_task, self.inprogress_task.children.all())

    def test_in_progress_task_can_not_be_linked_to_done_tasks(self):
        with self.assertRaises(StateErrorException) as e:
            task = self.inprogress_task_context.link(self.done_task)
        
        self.assertEqual(e.exception._msg, "In-progress task can't be linked to a done task.")
    
    def test_linking_changes_linked_tasks_state_to_in_progress(self):
        task = Task.objects.create(title="Temp new task", description="Nothing Fancy")
        self.assertEqual(task.state, Task.NEW)
        self.inprogress_task_context.link(task)
        self.assertIn(task, self.inprogress_task.children.all())
        task.refresh_from_db()
        self.assertEqual(task.state, Task.IN_PROGRESS)

    def test_in_progress_task_change_state_to_done(self):
        self.inprogress_task_context.change_state()
        self.assertEqual(self.inprogress_task_context._task.state, Task.DONE)
        self.inprogress_task.refresh_from_db()
        self.assertEqual(self.inprogress_task.state, Task.DONE)

    def test_done_task_can_not_be_edited(self):
        with self.assertRaises(StateErrorException) as e:
            task = self.done_task_context.update(
                title="Done task Update",
                description="This is the done task update man."
            )
        self.assertEqual(e.exception._msg, "Done Tasks can not be edited.")

    def test_done_task_can_not_be_linked(self):
        with self.assertRaises(StateErrorException) as e:
            task = self.done_task_context.link(self.inprogress_task)
        
        self.assertEqual(e.exception._msg, "Done Tasks can not be linked.")

    def test_done_task_change_state_to_in_progress(self):
        self.done_task_context.change_state()
        self.assertEqual(self.done_task_context._task.state, Task.IN_PROGRESS)
        self.done_task.refresh_from_db()
        self.assertEqual(self.done_task.state, Task.IN_PROGRESS)