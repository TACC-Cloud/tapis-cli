from . import BaseSchema


class Schema(BaseSchema):
    PROPERTIES = [
        ('name', '', str, 'Tapis app name'),
        ('version', '', str, 'Tapis app semantic version'),
        ('bundle', '', str, 'Local path containing app assets'),
        ('deployment_path', '', str, 'Remote path holding app assets'),
        ('deployment_system', '', str, 'Storage system holding app assets'),
        ('execution_system', '', str, 'Execution system for Tapis app')
    ]
