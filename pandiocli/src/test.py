import pathlib
import os
import sys
import signal
import time
from .config import Conf
from pandioml.function import Context


config = Conf()
if os.path.exists(str(pathlib.Path(__file__).parent.absolute())+'/config.json'):
    config.load(str(pathlib.Path(__file__).parent.absolute())+'/config.json')

shutdown = False


def start(args):
    try:
        FormSubmissionGenerator = getattr(__import__('pandioml.dataset', fromlist=[args.dataset_name]),
                                          args.dataset_name)
    except:
        raise Exception(f"Could not find the dataset specified at ({args.dataset_name}).")

    try:
        sys.path.insert(1, os.path.join(os.getcwd(), args.project_folder_name))
        pm = __import__('wrapper')
    except:
        raise Exception(f"Could not find the project specified at ({os.path.join(os.getcwd(), args.project_folder_name)}).")

    w = pm.Wrapper()

    generator = FormSubmissionGenerator(0, 10000)

    while generator.has_more_samples():
        for event in generator.next_sample():
            r = w.process(event, Context())
            print(r)
            if shutdown:
                w.fnc.shutdown()
                exit()

    arr = {
        'email': 'steph_l_jacobs@yahoo.com',
        'ip': '182.54.239.221',
        'timestamp': 582055077
    }

    r = w.process(arr, Context())
    print(r)

    print("")


def shutdown_callback(signalNumber, frame):
    global shutdown
    shutdown = True


signal.signal(signal.SIGINT, shutdown_callback)
signal.signal(signal.SIGTERM, shutdown_callback)
