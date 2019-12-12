__all__ = ['BaseSchema']


class BaseSchema:
    section = 'DEFAULT'
    PROPERTIES = [('field', 'default', str, 'Field description')]

    def parser_args(self):
        pass

    def get_section(self):
        return self.section

    def get_keys(self):
        key_dict = {}
        for field, default, field_type, description in self.PROPERTIES:
            key_dict[field] = default
        return key_dict
