from tapis_cli.display import Verbosity
from tapis_cli.search import Argdef, argmod, argtype, optionize

__all__ = ['TapisModel']


class TapisModel(object):
    """Base class for Tapis models
    """

    SEARCH_ARGS = []
    ARGS_ORDERED = []
    service_id_type = 'Unknown'

    format_many = False
    payload = {}
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

    def add_fields(self, fields, ordered=[]):
        """Bulk add multiple searchable fields
        """
        fnames = [f[0] for f in fields]
        # Add ordered
        for o in ordered:
            for f in fields:
                if f[0] == o:
                    self.add_field(*f)
                    fields.remove(f)
        # Add remaining, ordered as sent in fields
        for f in fields:
            self.add_field(*f)
        return self

    def _add_fields(self, fields, ordererd=[]):
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

    def __init__(self):
        self.add_fields(self.SEARCH_ARGS, self.ARGS_ORDERED)

    def get_headers(self, verbosity_level=None, formatter='table'):
        if verbosity_level is None:
            verbosity_level = Verbosity.LISTING
        headers = list()
        for f in self.fields:
            # print('{}: {}> = {}'.format(f, verbosity_level, f.verbosity))
            if verbosity_level >= f.verbosity:
                if argtype.format_allows_param_type(f, formatter):
                    headers.append(f.param_name)
        return headers

    @classmethod
    def render_key_value(cls, key, value):
        """Overridable function to how JSON key/values should be transformed
        """
        return key, value

    @classmethod
    def transform_response(cls, response_json):
        """Apply an intermediate transform to a JSON document
        """
        transformed = dict()
        for k, v in response_json.items():
            k1, v1 = cls.render_key_value(k, v)
            transformed[k1] = v1
        return transformed

    def validate(self, entity, permissive=True):
        return True
