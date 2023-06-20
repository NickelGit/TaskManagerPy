from django_fsm import FSMField, transition
from django.db import models
from .base_model import BaseModel
from .user import User
from .tag import Tag


class Task(BaseModel):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=600)
    planned_delivery_date = models.DateField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tasks"
    )
    assignee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_tasks"
    )
    tags = models.ManyToManyField(Tag)

    class States(models.TextChoices):
        NEW_TASK = "new_task"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    state = FSMField(choices=States.choices, default=States.NEW_TASK, protected=True)

    @transition(field=state, source=States.NEW_TASK, target=States.IN_DEVELOPMENT)
    def start_development(self):
        pass

    @transition(field=state, source=States.IN_DEVELOPMENT, target=States.IN_QA)
    def send_to_qa(self):
        pass

    @transition(field=state, source=States.IN_QA, target=States.IN_DEVELOPMENT)
    def reject(self):
        pass

    @transition(field=state, source=States.IN_QA, target=States.IN_CODE_REVIEW)
    def send_to_code_review(self):
        pass

    @transition(field=state, source=States.IN_CODE_REVIEW, target=States.IN_DEVELOPMENT)
    def request_changes(self):
        pass

    @transition(
        field=state, source=States.IN_CODE_REVIEW, target=States.READY_FOR_RELEASE
    )
    def approve(self):
        pass

    @transition(field=state, source=States.READY_FOR_RELEASE, target=States.RELEASED)
    def release(self):
        pass

    @transition(
        field=state, source=[States.RELEASED, States.NEW_TASK], target=States.ARCHIVED
    )
    def archive(self):
        pass

    class PrioritiyLevels(models.TextChoices):
        HIGH = "high"
        NORMAL = "normal"
        LOW = "low"

    priority = models.CharField(
        max_length=255, default=PrioritiyLevels.NORMAL, choices=PrioritiyLevels.choices
    )
