from . import BaseSchema


class Schema(BaseSchema):
    PROPERTIES = [('branch', 'master', str, 'Current git branch'),
                  ('remote', '', str, 'Current git remote')]
