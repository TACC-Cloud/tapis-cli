import pytest
from time import sleep
from tapis_cli.utils import seconds


@pytest.mark.longrun
def test_jsoncache():
    """Check that Python2/3 lru_cache functions both work w json serializer
    """
    from tapis_cli.hashcache import jsoncache, lru_cache

    @jsoncache.mcache(lru_cache(maxsize=256))
    def timer_function(duration=1):
        sleep(duration)
        return 'function_response'

    delay = 2
    start_01 = seconds()
    resp = timer_function(delay)
    start_02 = seconds()
    resp = timer_function(delay)
    end_01 = seconds()

    delta_1 = round(start_02 - start_01)
    delta_2 = round(end_01 - start_02)

    assert delta_1 == delay
    assert delta_2 < delay


@pytest.mark.longrun
def test_picklecache():
    """Check that Python2/3 lru_cache functions both work w cloudpickle serializer
    """
    from tapis_cli.hashcache import picklecache, lru_cache

    @picklecache.mcache(lru_cache(maxsize=256))
    def timer_function(duration=1):
        sleep(duration)
        return 'function_response'

    delay = 2
    start_01 = seconds()
    resp = timer_function(delay)
    start_02 = seconds()
    resp = timer_function(delay)
    end_01 = seconds()

    delta_1 = round(start_02 - start_01)
    delta_2 = round(end_01 - start_02)

    assert delta_1 == delay
    assert delta_2 < delay
