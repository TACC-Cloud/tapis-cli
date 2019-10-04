import dateparser
from datetime import datetime
from .searcharg import SearchArg
from .arrowspan import ArrowSpan
from . import argmod, argtype, optionize, propertize, tapisize

__all__ = ['WebParam', 'SearchWebParam', 'SearchWebParamEqualsOnly']


class WebParam(dict):
    pass


class SearchWebParamEqualsOnly(SearchArg):
    """Renders param=value for passing to a web service
    """
    def query_eq(self, value):
        # EQUALS
        if isinstance(value, list):
            value = value[0]
        key = '{}'.format(self.field)
        return WebParam({key: value})


class SearchWebParam(SearchArg):
    """Renders param.mod=value for passing to a web service
    """
    def query_eq(self, value):
        # EQUALS
        if isinstance(value, list):
            value = value[0]
        key = '{}.eq'.format(self.field)
        return WebParam({key: value})

    def query_neq(self, value):
        # NOT_EQUAL
        if isinstance(value, list):
            value = value[0]
        key = '{}.neq'.format(self.field)
        return WebParam({key: value})

    def query_gt(self, value):
        # GREATER_THAN
        if isinstance(value, list):
            value = value[0]
        key = '{}.gt'.format(self.field)
        return WebParam({key: value})

    def query_gte(self, value):
        # GREATER_THAN_OR_EQUAL
        if isinstance(value, list):
            value = value[0]
        key = '{}.gte'.format(self.field)
        return WebParam({key: value})

    def query_lt(self, value):
        # LESS_THAN
        if isinstance(value, list):
            value = value[0]
        key = '{}.lt'.format(self.field)
        return WebParam({key: value})

    def query_lte(self, value):
        # LESS_THAN_OR_EQUAL
        if isinstance(value, list):
            value = value[0]
        key = '{}.lte'.format(self.field)
        return WebParam({key: value})

    def query_in(self, values):
        # IN (array)
        if not isinstance(values, list):
            values = [values]
        qvals = self.to_values(values)
        qvals = ','.join(qvals)
        key = '{}.in'.format(self.field)
        return WebParam({key: qvals})

    def query_nin(self, values):
        # NOT IN (array)
        if not isinstance(values, list):
            values = [values]
        qvals = self.to_values(values)
        qvals = ','.join(qvals)
        key = '{}.nin'.format(self.field)
        return WebParam({key: qvals})

    def query_start(self, value):
        # STARTS WITH
        if isinstance(value, list):
            value = value[0]
        key = '{}.like'.format(self.field)
        val = '{}*'.format(value)
        return WebParam({key: val})

    # def query_nstart(self, value):
    #     # DOESN'T START WITH
    #     if isinstance(value, list):
    #         value = value[0]
    #     key = '{}.nlike'.format(self.field)
    #     val = '{}*'.format(value)
    #     return WebParam({key: val})

    def query_end(self, value):
        # ENDS WITH
        if isinstance(value, list):
            value = value[0]
        key = '{}.like'.format(self.field)
        val = '*{}'.format(value)
        return WebParam({key: val})

    # def query_nend(self, value):
    #     # DOESN'T END WITH
    #     if isinstance(value, list):
    #         value = value[0]
    #     key = '{}.nlike'.format(self.field)
    #     val = '*{}'.format(value)
    #     return WebParam({key: val})

    def query_like(self, value):
        # WILDCARD CONTAINS
        if isinstance(value, list):
            value = value[0]
        key = '{}.like'.format(self.field)
        val = '*{}*'.format(value)
        return WebParam({key: val})

    def query_nlike(self, value):
        # WILDCARD NOT CONTAINS
        if isinstance(value, list):
            value = value[0]
        key = '{}.nlike'.format(self.field)
        val = '*{}*'.format(value)
        return WebParam({key: val})

    def query_on(self, value):
        if self.field_type is not argtype.DATETIME:
            raise TypeError('"on" may only be used for dates and times')
        key = '{}.on'.format(self.field)
        if isinstance(value, list):
            value = value[0]
        val = '{0}'.format(value.format('YYYY-MM-DD'))
        return WebParam({key: val})

    def query_after(self, value):
        if self.field_type is not argtype.DATETIME:
            raise TypeError('"after" may only be used for dates and times')
        key = '{}.after'.format(self.field)
        if isinstance(value, list):
            value = value[0]
        val = '{0}'.format(value.format('YYYY-MM-DD'))
        return WebParam({key: val})

    def query_before(self, value):
        if self.field_type is not argtype.DATETIME:
            raise TypeError('"before" may only be used for dates and times')
        key = '{}.before'.format(self.field)
        if isinstance(value, list):
            value = value[0]
        val = '{0}'.format(value.format('YYYY-MM-DD'))
        return WebParam({key: val})
