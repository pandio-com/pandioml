#from pandioml.core import Pipeline
from sys import exc_info


class Pipeline:
    _steps = []
    _final_step = None
    _done_step = None

    def __init__(self):
        super().__init__()

    def go(self):
        result = None
        for step in self._steps:
            if result is not None:
                step[2]['_result'] = result
            result = self.try_catch(step[0], *step[1], **step[2])
            print(result)

        if self._final_step is not None and callable(self._final_step[0]):
            if result is not None:
                self._final_step[2]['_result'] = result
            result = self.try_catch(self._final_step[0], *self._final_step[1], **self._final_step[2])

        if self._done_step is not None and callable(self._done_step[0]):
            if result is not None:
                self._done_step[2]['_result'] = result
            return self.try_catch(self._done_step[0], *self._done_step[1], **self._done_step[2])

        return None

    def final(self, fnc, *args, **kwargs):
        self._final_step = [fnc, args, kwargs]
        return self

    def done(self, fnc, *args, **kwargs):
        self._done_step = [fnc, args, kwargs]
        return self

    def then(self, fnc, *args, **kwargs):
        self._steps.append([fnc, args, kwargs])
        return self

    def try_catch(self, handler, *args, **kwargs):
        #try:
        return handler(*args, **kwargs)
        #except Exception as e:
        #    tb = exc_info()[2]
        #    return e, tb


class Tester:
    def hank(self, first, _result=None, name=None):
        print(f"Hello {first}, regards {name}")
        print(f"Results: {_result}")
        return first


def test(first, _result=None, name=None):
    print(f"Hello {first}, regards {name}")
    print(f"Results: {_result}")
    return first


t = Tester()

p = Pipeline()\
    .then(t.hank, 'frank')\
    .then(t.hank, 'Jerrik', name='Chuck')\
    .final(t.hank, 'Amanda', name='Bowe')\
    .done(t.hank, "All done!")


p.go()
