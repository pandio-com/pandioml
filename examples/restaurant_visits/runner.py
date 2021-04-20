from pandioml.function import Context
import matplotlib.pyplot as plt
import signal
import argparse
import tracemalloc
import wrapper as wr
import fnc as pm
import numpy as np

shutdown = False
tracemalloc.start(10)


def run(dataset_name, loops, artifact_pipeline_id=None):
    import time
    try:
        generator = getattr(__import__('pandioml.data', fromlist=[dataset_name]), dataset_name)()
    except:
        raise Exception(f"Could not find the dataset specified at ({dataset_name}).")

    fnc_id = 'example.model'

    w = wr.Wrapper()
    correctness_dist = []

    avg = 0

    index = 0
    while True:
        start = time.time()
        c = Context()
        # TODO, simulate a user setting, remove it
        c.set_user_config_value('pipeline', 'inference')

        if shutdown or (index >= loops and loops != -1):
            w.fnc.shutdown()
            break

        event = generator.next()

        print('event')
        print(event)

        result = w.process(pm.Fnc.input_schema.encode(event).decode('UTF-8'), c, fnc_id)

        print('result')
        print(result)

        print(f"Actual: {w.output[c.get_user_config_value('pipeline')]['labels'][0]}")
        print(f"Prediction: {w.output[c.get_user_config_value('pipeline')]['prediction']}")

        if w.output[c.get_user_config_value('pipeline')]['labels'] == \
                w.output[c.get_user_config_value('pipeline')]['prediction']:
            correctness_dist.append(1)
            print('CORRECT')
        else:
            correctness_dist.append(0)
            print('WRONG')

        print("")

        end = time.time()
        print(f"Runtime ({index}) of the program is {round(end - start, 3)}")

        w.output = None

        index += 1

    time = [i for i in range(1, index)]
    accuracy = [sum(correctness_dist[:i])/len(correctness_dist[:i]) for i in range(1, index)]
    plt.plot(time, accuracy)
    plt.show()


def shutdown_callback(signalNumber, frame):
    global shutdown
    shutdown = True


signal.signal(signal.SIGINT, shutdown_callback)
signal.signal(signal.SIGTERM, shutdown_callback)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test your PandioML project')
    parser.add_argument('--dataset_name', type=str, help='The name of the data set inside of pandioml.data')
    parser.add_argument('--loops', type=str, help='The number of events to process before finishing the test.',
                        required=False)

    args = parser.parse_args()
    loops = -1
    if 'loops' in args:
        loops = int(args.loops)

    run(args.dataset_name, loops)

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')[:10]
    for stat in top_stats:
        print(stat)
