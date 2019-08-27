from tapis_cli.search import Argdef, argmod, argtype, optionize

__all__ = ['TapisEntity']


class TapisEntity(object):
    """Base class for any Tapis primitive
    """
    id_display_name = 'ID'
    format_many = False

    SEARCH_ARGS = []
    fields = []

    def add_field(self,
                  param_name,
                  param_type,
                  only_detail,
                  mods_allowed,
                  default_mod,
                  value_choices=None,
                  param_opt=None,
                  searchable=False):
        """Add a searchable field
        """
        arg = Argdef(param_name, param_type, only_detail, mods_allowed,
                     default_mod, value_choices, param_opt, searchable)
        if arg not in self.fields:
            self.fields.append(arg)
        return self

    def add_fields(self, fields):
        """Bulk add multiple searchable fields
        """
        for f in fields:
            self.add_field(*f)
        return self

    def get_args(self, list_only=False):
        pass

    @classmethod
    def optionize(cls, text_string):
        """Render a field name as an option
        """
        return optionize(text_string)

    @classmethod
    def argify(cls, arg_name, arg_type, arg_help=None):
        pass
