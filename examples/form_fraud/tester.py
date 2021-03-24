import json
pm = __import__('wrapper')
w = pm.Wrapper()


class Context():
    def get_logger(self):
        return Logger()


class Logger():
    def info(self, message):
        print(message)

    def error(self, message):
        print(message)

    def warning(self, message):
        print(message)

    def debug(self, message):
        print(message)


arr = {
    'email': 'steph_l_jacobs@yahoo.com',
    'ip': '182.54.239.221',
    'timestamp': 582055077
}

r = w.process(arr, Context())
print(r)
