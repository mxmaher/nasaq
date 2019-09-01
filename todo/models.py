import abc

from django.db import models
from django.utils.translation import gettext as _


class Task(models.Model):
    """
    A Stateful Task that contains a title and a description. 
    and can be linked to other tasks in a on-to relation,
    """
    NEW = 0
    IN_PROGRESS = 1
    DONE = 2

    STATES = [
        (NEW, _('New')),
        (IN_PROGRESS, _('In Progress')),
        (DONE, _('Done'))
    ]

    title = models.CharField(_('Title'), max_length=100)
    description = models.TextField(_('Description'))
    state = models.SmallIntegerField(choices=STATES, default=NEW)
    children = models.ManyToManyField('self')

    def __str__(self):
        return f"Task: {self.id} - {self.STATES[self.state][1]}"