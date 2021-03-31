import pathlib
import os
import signal
import subprocess
from .config import Conf


config = Conf()
if os.path.exists(str(pathlib.Path(__file__).parent.absolute())+'/config.json'):
    config.load(str(pathlib.Path(__file__).parent.absolute())+'/config.json')

shutdown = False


def start(args):
    loops = -1
    if args.loops is not None:
        loops = int(args.loops)

    workers = 1
    if args.workers is not None:
        workers = int(args.workers)

    programs = [f"python {args.project_folder}/runner.py --dataset_name {args.dataset_name} --loops {loops}"]
    programs = ["which python"]

    # start all programs
    #processes = [subprocess.Popen(program) for program in programs]
    # wait
    #for process in processes:
    #    process.wait()

    #sys.path.insert(1, os.path.join(os.getcwd(), args.project_folder_name))
    #pm = __import__('runner')
    #pm.run(args.dataset_name, loops)

    print("")


def shutdown_callback(signalNumber, frame):
    global shutdown
    shutdown = True


signal.signal(signal.SIGINT, shutdown_callback)
signal.signal(signal.SIGTERM, shutdown_callback)
