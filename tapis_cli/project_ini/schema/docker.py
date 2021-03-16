from . import BaseSchema


class Schema(BaseSchema):
    PROPERTIES = [('dockerfile', 'Dockerfile', str,
                   'Dockerfile to build current project'),
                  ('username', '', str, 'Container registry username'),
                  ('group', '', str, 'Container registry group'),
                  ('registry', '', str, 'Container registry URL'),
                  ('repo', '', str, 'Container repo name'),
                  ('tag', '', str, 'Container repo tag'),
                  ('build_args', '', str, 'Container build arguments'),
                  ('use_commit_hash', True, bool,
                   'Use commit hash for tag if available')]
