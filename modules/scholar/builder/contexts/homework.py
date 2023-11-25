import datetime
from schema import And, Optional

from core.utilities.schema import Schema
from .hierarchy import ContextIssue, ContextIssueSub, ContextIssueSubSub
from .buildable import ContextIssueBase


class HomeworkMixin:
    _target = 'homework'
    _subdir = 'homework'


class ContextHomeworkSubproblem(HomeworkMixin, ContextIssueSubSub):
    _schema = Schema({
        'id': And(str, len),
        'name': And(str, len),
        Optional('bonus'): bool,
    })


class ContextHomeworkProblem(HomeworkMixin, ContextIssueSub):
    _subcontext_key = 'subproblems'
    _subcontext_class = ContextHomeworkSubproblem
    _schema = Schema({
        'id': And(str, len),
        'name': And(str, len),
        Optional('bonus'): bool,
    })


class ContextHomeworkIssue(HomeworkMixin, ContextIssue):
    _subcontext_key = 'problems'
    _subcontext_class = ContextHomeworkProblem
    _schema = Schema({
        'deadline': datetime.date,
        'id': And(str, len),
        'number': int,
    })


class ContextHomework(HomeworkMixin, ContextIssueBase):
    _issue_context_class = ContextHomeworkIssue
    _schema = Schema({})
