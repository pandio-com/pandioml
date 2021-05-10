from sys import exc_info
import traceback


class Pipelines:
    _pipelines = {}
    _output = {}
    _error_content = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._pipelines = {}
        self._output = {}
        self._error_content = None

    def get_keys(self):
        return list(self._pipelines.keys())

    def builder(self):
        pass

    def add(self, name, pipeline):
        self._pipelines[name] = [pipeline]
        return self

    def go(self, name=None, fnc=None):
        if name is not None:
            try:
                self._output[name] = self.try_catch(self._pipelines[name][0], fnc)
            except Exception as e:
                raise Exception(f"Could not execute pipeline: {e}")
        else:
            for name in self._pipelines:
                try:
                    self._output[name] = self.try_catch(self._pipelines[name][0])
                except Exception as e:
                    raise Exception(f"Could not execute pipeline: {e}")

        return self._output

    def try_catch(self, handler, fnc):
        #try:
        return handler.go(fnc)
        #except Exception as e:
        #    tb = traceback.extract_tb(exc_info()[2])
        #    self._error_content = e, tb
        #    return self._error_content


class Pipeline:
    _steps = []
    _final_step = None
    _done_step = None
    _error_step = None
    _error_content = None
    _fnc = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._steps = []
        self._final_step = None
        self._done_step = None
        self._error_step = None
        self._error_content = None

    def go(self, fnc=None):
        self._fnc = fnc
        result = None
        for step in self._steps:
            if self._error_content is not None:
                break
            if result is not None:
                step[2]['result'] = result
            result = self.try_catch(step[0], *step[1], **step[2])
            if self._fnc is not None:
                self._fnc.set_result(result)

        if self._error_content is None:
            if self._final_step is not None and callable(self._final_step[0]):
                if result is not None:
                    self._final_step[2]['result'] = result
                result = self.try_catch(self._final_step[0], *self._final_step[1], **self._final_step[2])
                if self._fnc is not None:
                    self._fnc.set_result(result)

            if self._done_step is not None and callable(self._done_step[0]):
                if result is not None:
                    self._done_step[2]['result'] = result
                return self.try_catch(self._done_step[0], *self._done_step[1], **self._done_step[2])

        if self._error_content is not None:
            self._error_step[2]['result'] = self._error_content
            return self.try_catch(self._error_step[0], *self._error_step[1], **self._error_step[2])

        return None

    def final(self, fnc, *args, **kwargs):
        self._final_step = [fnc, args, kwargs]
        return self

    def done(self, fnc, *args, **kwargs):
        self._done_step = [fnc, args, kwargs]
        return self

    def catch(self, fnc, *args, **kwargs):
        self._error_step = [fnc, args, kwargs]
        return self

    def then(self, fnc, *args, **kwargs):
        self._steps.append([fnc, args, kwargs])
        return self

    def try_catch(self, handler, *args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except Exception as e:
            tb = traceback.extract_tb(exc_info()[2])
            self._error_content = e, tb
            return self._error_content
