from . import BaseSchema


class Schema(BaseSchema):
    PROPERTIES = [('name', '', str, 'Tapis actor name'),
                  ('description', '', str, 'Tapis actor name description'),
                  ('alias', '', str, 'Tapis actor alias'),
                  ('stateless', True, bool, 'Whether actor is stateless'),
                  ('hint', '', str, 'Scaling hint for actor'),
                  ('privileged', False, bool,
                   'Whether actor runs with advanced capabilities'),
                  ('use_uid', True, bool,
                   'Whether actor should run as the owner UNIX ID'),
                  ('workers', 1, int,
                   'Default number of workers for the actor')]
