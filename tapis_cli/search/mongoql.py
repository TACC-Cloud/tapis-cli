import arrow
import dateparser
from bson import Regex
from datetime import datetime
from .searcharg import SearchArg
from .arrowspan import ArrowSpan
from . import argmod, argtype, optionize, propertize, tapisize

__all__ = ['MongoQuery', 'SearchMongoQuery']


class MongoQuery(dict):
    pass


class SearchMongoQuery(SearchArg):
    def query_eq(self, value):
        # EQUALS
        if isinstance(value, list):
            value = value[0]
        if self.field_type is argtype.DATETIME:
            return MongoQuery({
                self.field: {
                    '$gte': value.smart_floor().isoformat(),
                    '$lt': value.smart_ceil().isoformat()
                }
            })
        else:
            return MongoQuery({self.field: value})

    def query_neq(self, value):
        # NOT_EQUAL
        if isinstance(value, list):
            value = value[0]
        if self.field_type is argtype.DATETIME:
            return MongoQuery({
                self.field: {
                    '$not': {
                        '$gte': value.smart_floor().isoformat(),
                        '$lt': value.smart_ceil().isoformat()
                    }
                }
            })
        else:
            return MongoQuery({self.field: {'$ne': value}})

    def query_gt(self, value):
        # GREATER_THAN
        if isinstance(value, list):
            value = value[0]
        if self.field_type is argtype.DATETIME:
            value = value.datetime.isoformat()
        return MongoQuery({self.field: {'$gt': value}})

    def query_gte(self, value):
        # GREATER_THAN_OR_EQUAL
        if isinstance(value, list):
            value = value[0]
        if self.field_type is argtype.DATETIME:
            value = value.datetime.isoformat()
        return MongoQuery({self.field: {'$gte': value}})

    def query_lt(self, value):
        # LESS_THAN
        if isinstance(value, list):
            value = value[0]
        if self.field_type is argtype.DATETIME:
            value = value.datetime.isoformat()
        return MongoQuery({self.field: {'$lt': value}})

    def query_lte(self, value):
        # LESS_THAN_OR_EQUAL
        if isinstance(value, list):
            value = value[0]
        if self.field_type is argtype.DATETIME:
            value = value.datetime.isoformat()
        return MongoQuery({self.field: {'$lte': value}})

    def query_in(self, values):
        # IN (array)
        if not isinstance(values, list):
            values = [values]
        qvals = self.to_values(values)
        return MongoQuery({self.field: {'$in': qvals}})

    def query_nin(self, values):
        # NOT IN (array)
        if not isinstance(values, list):
            values = [values]
        qvals = self.to_values(values)
        return MongoQuery({self.field: {'$nin': qvals}})

    def query_start(self, value):
        # STARTS WITH
        if isinstance(value, list):
            value = value[0]
        return MongoQuery({self.field: Regex('^' + value + '.*', 'i')})

    def query_nstart(self, value):
        # DOESN'T START WITH
        if isinstance(value, list):
            value = value[0]
        return MongoQuery(
            {self.field: {
                '$not': Regex('^' + value + '.*', 'i')
            }})

    def query_end(self, value):
        # ENDS WITH
        if isinstance(value, list):
            value = value[0]
        return MongoQuery({self.field: Regex('*.' + value + '$', 'i')})

    def query_nend(self, value):
        # DOESN'T END WITH
        if isinstance(value, list):
            value = value[0]
        return MongoQuery(
            {self.field: {
                '$not': Regex('*.' + value + '$', 'i')
            }})

    def query_like(self, value):
        # WILDCARD CONTAINS
        if isinstance(value, list):
            value = value[0]
        return MongoQuery({self.field: Regex('.*' + value + '.*', 'i')})

    def query_nlike(self, value):
        # WILDCARD NOT CONTAINS
        if isinstance(value, list):
            value = value[0]
        return MongoQuery(
            {self.field: {
                '$not': Regex('.*' + value + '.*', 'i')
            }})

    def query_on(self, value):
        if self.field_type is not argtype.DATETIME:
            raise TypeError('"on" may only be used for dates and times')
        return self.query_eq(value)

    def query_after(self, value):
        if self.field_type is not argtype.DATETIME:
            raise TypeError('"after" may only be used for dates and times')
        return self.query_gt(value)

    def query_before(self, value):
        if self.field_type is not argtype.DATETIME:
            raise TypeError('"before" may only be used for dates and times')
        return self.query_lt(value)
