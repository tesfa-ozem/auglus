# -*- coding: utf-8 -*-
from . import BaseEnum


class Priority(BaseEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Status(BaseEnum):
    NEW = "New"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    OVERDUE = "Overdue"
