import arrow

__all__ = ['ArrowSpan']


class ArrowSpan(arrow.Arrow):
    """Subclass of Arrow with upgraded span() capability used to generate MongoDB date ranges for queries
    """
    YEAR = 'year'
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    HOUR = 'hour'
    MINUTE = 'minute'
    SPANS = [YEAR, MONTH, WEEK, DAY, HOUR, MINUTE]
    default_span = DAY
    original_value = None

    def setup(self, value):
        setattr(self, 'original_value', value)
        return self

    def smart_span(self, span_value=None):
        orig = getattr(self, 'original_value', '').lower()
        span = self.default_span
        if span_value is None:
            # Iterate thru last X, this X, next X, etc
            for s in [self.YEAR, self.MONTH, self.WEEK, self.DAY]:
                if s in orig:
                    span = s
                    break
        # We are able to call Arrow's span() since this is a subclass
        return self.span(span)

    def smart_floor(self, span_value=None):
        orig = getattr(self, 'original_value', '').lower()
        span = self.default_span
        if span_value is None:
            # Iterate thru last X, this X, next X, etc
            for s in [self.YEAR, self.MONTH, self.WEEK, self.DAY]:
                if s in orig:
                    span = s
                    break
        # We are able to call Arrow's floor() since this is a subclass
        return self.floor(span).datetime

    def smart_ceil(self, span_value=None):
        orig = getattr(self, 'original_value', '').lower()
        span = self.default_span
        if span_value is None:
            # Iterate thru last X, this X, next X, etc
            for s in [self.YEAR, self.MONTH, self.WEEK, self.DAY]:
                if s in orig:
                    span = s
                    break
        # We are able to call Arrow's ceil()) since this is a subclass
        return self.ceil(span).datetime
