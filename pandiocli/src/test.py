import pathlib
import os
import os.path
import signal
import subprocess
import sys
from .config import Conf
import hashlib
from pandioml.core.artifacts import artifact


config = Conf()
if os.path.exists(str(pathlib.Path(__file__).parent.absolute())+'/config.json'):
    config.load(str(pathlib.Path(__file__).parent.absolute())+'/config.json')

shutdown = False


def start(args):
    BUF_SIZE = 65536

    loops = -1
    if args.loops is not None:
        loops = int(args.loops)

    workers = 1
    if args.workers is not None:
        workers = int(args.workers)

    if not os.path.isfile(f"{args.project_folder}/fnc.py"):
        print(f"{args.project_folder} is invalid.")
        exit()

    val = input("Would you like to store artifacts (dataset, pipeline, model, etc.)? If no, only the model will be saved. (y,n): ")
    store = True if val.lower() == 'y' or val.lower() == 'yes' else False
    if store:
        print("Artifacts will be saved!")

        print("")

        name_id = input("Would you like to name this run? Leave blank for no name: ")

        print("")

        print("Generating artifact identifiers.")

        os.system(
            f"cd {args.project_folder} && rm -rf dist && rm -rf build && rm -rf fnc.spec && rm -rf __pycache__ && "
            f"PYTHONHASHSEED=1 && export "
            "PYTHONHASHSEED && pyinstaller -F --exclude-module scikit-learn "
            "--exclude-module river --exclude-module pandioml --exclude-module scikit-multiflow --exclude-module "
            "pulsar-client --exclude-module Faker --exclude-module scipy --exclude-module numpy --exclude-module "
            "pandas --exclude-module python-dateutil --exclude-module six --exclude-module test-unidecode "
            "--exclude-module ratelimit --exclude-module fastavro --exclude-module grpcio --exclude-module certifi "
            "--exclude-module prometheus-client --exclude-module apache-bookkeeper-client --exclude-module protobuf "
            "--exclude-module pytz --exclude-module sortedcontainers --exclude-module matplotlib --exclude-module "
            "requests --exclude-module pymmh3 --exclude-module setuptools --exclude-module pyparsing --exclude-module"
            " pillow --exclude-module cycler --exclude-module kiwisolver --exclude-module idna --exclude-module "
            "chardet --exclude-module urllib3 --exclude-module threadpoolctl --exclude-module sklearn "
            "--exclude-module pytest --exclude-module pickle fnc.py >/dev/null 2>&1 && unset PYTHONHASHSEED")

        md5 = hashlib.md5()

        with open(f"{args.project_folder}/dist/fnc", 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)

        os.system(f"cd {args.project_folder} && rm -rf dist && rm -rf build && rm -rf fnc.spec && rm -rf __pycache__")

        if len(name_id) > 0:
            artifact.set_name_id(name_id)

        artifact.set_pipeline_id(md5.hexdigest())

        print(f"Artifact pipeline id is: {artifact.get_pipeline_id()}")

        print(f"Artifact name id is: {artifact.get_name_id()}")
    else:
        print("NOT SAVING any artifacts!")

    # programs = [f"python {args.project_folder}/runner.py --dataset_name {args.dataset_name} --loops {loops}"]

    # start all programs
    #processes = [subprocess.Popen(program) for program in programs]
    # wait
    #for process in processes:
    #    process.wait()

    body = ''
    with open(f"{args.project_folder}/fnc.py", 'r') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            body += data

    artifact.add('fnc.py', body)

    print("Starting execution of pipeline(s).")

    sys.path.insert(1, os.path.join(os.getcwd(), args.project_folder))
    pm = __import__('runner')
    pm.run(args.dataset_name, loops)

    print("")


def shutdown_callback(signalNumber, frame):
    global shutdown
    shutdown = True


signal.signal(signal.SIGINT, shutdown_callback)
signal.signal(signal.SIGTERM, shutdown_callback)
