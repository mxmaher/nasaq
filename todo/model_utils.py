import abc
from rest_framework.exceptions import APIException

from todo.models import Task


class StateErrorException(APIException):
    status_code = 400
    default_detail = 'Error Handeling Task state.'


class State(metaclass=abc.ABCMeta):
    """
    Abstract class serving as the interface implemented by different states.
    
    All methods defined here as abstractmtheods should be implmented by subclasses
    or an exception will be raised on state initiation.

    This is an implmentation of the state design pattern.

    Refrence: 
        - https://airbrake.io/blog/design-patterns/behavioral-design-patterns-state 
    """
    @abc.abstractmethod
    def change_state(self, instance):
        pass

    @abc.abstractmethod
    def update(self, instance, **kwargs):
        pass

    @abc.abstractmethod
    def link(self, instance, children):
        pass


class TaskIsNewState(State):
    """
    In this state a task's title and description can be edited.
    but it can not be linked to another task.
    """
    def change_state(self, instance):
        """
        Froward change the state of the task to in-progress

        params:
            - instance: a Task model insatance.
        """
        instance.state = instance.IN_PROGRESS
        instance.save()
        return instance

    def update(self, instance, **kwargs):
        """
        Only update the title and desription of a task.

        params:
            - instance: a Task model instance.
            - kwargs: a dict of Task model fields and values.
        """
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        instance.save(update_fields=['title', 'description'])
        return instance

    def link(self, instance, children):
        """
        Only tasks with an in-progress states can have other tasks linked to them.
        """
        raise StateErrorException(detail="New tasks can not be linked.")


class TaskIsInProgressState(State):
    """
    In this state a task can be linked to other tasks but can not be edited.
    """
    def change_state(self, instance):
        """
        Forward Change the state of the task to Done.

        params:
            - instance: a Task model insatance.
        """
        instance.state = instance.DONE
        instance.save()
        return instance

    def update(self, instance, **kwargs):
        """
        Only Task with a new state can be edited or updated.
        
        params:
            - instance: a Task model insatance.
            - kwargs: a dict of Task model fields and values.
        """
        raise StateErrorException(detail="Tasks In Progress can not be edited.")

    def link(self, instance, child):
        """
        Link two tasks togther by adding the child to the intance
        children many-to-many set.

        params:
            - instance: a Task model insatance.
            - children: a list of Task model instaces.
        """
        if child.state not in [Task.NEW, Task.IN_PROGRESS]:
            raise StateErrorException(detail="In-progress task can't be linked to a done task.")

        if instance == child:
            raise StateErrorException(detail="Tasks Can not be linked to themselves.")

        instance.children.add(child)
        
        # update child task state to in-progress after being added to instance children.
        if child.state != Task.IN_PROGRESS:
            child.state = Task.IN_PROGRESS
            child.save()
        
        return instance


class TaskIsDoneState(State):
    """
    In this state a task can not be edited or linked.
    """
    def change_state(self, instance):
        """
        Roll back the state of the to In-progress
        """
        instance.state = instance.IN_PROGRESS
        instance.save()
        return instance

    def update(self, instance, **kwargs):
        raise StateErrorException(detail="Done Tasks can not be edited.")
    
    def link(self, instance, children):
        raise StateErrorException(detail="Done Tasks can not be linked.")


class TaskContext:
    """
    This class serves as the glue that ties a task to it's
    behavioural state, and provides the client api for the state pattern.  
    """
    STATES_MAPPING = {
        Task.NEW: TaskIsNewState(),
        Task.IN_PROGRESS: TaskIsInProgressState(),
        Task.DONE: TaskIsDoneState()
    }

    def __init__(self, task):
        self._task = task
        self._state = self.STATES_MAPPING[task.state]

    def update(self, **kwargs):
        return self._state.update(self._task, **kwargs)

    def link(self, child):
        return self._state.link(self._task, child)
    
    def change_state(self):
        self._task = self._state.change_state(self._task)
        self._state = self.STATES_MAPPING[self._task.state]
