import logging
import os
from shutil import copyfile
dirname = os.path.dirname(__file__)


def start(args):
    if not os.path.exists(args.folder_name):
        logging.debug('Creating folder {args.folder_name}')
        try:
            os.makedirs(args.folder_name)
        except:
            logging.error('Could not create folder.')

    copyfile(os.path.join(dirname, 'assets/runner_template.py'), f"{args.folder_name}/runner.py")
    copyfile(os.path.join(dirname, 'assets/fnc_template.py'), f"{args.folder_name}/fnc.py")
    copyfile(os.path.join(dirname, 'assets/wrapper_template.py'), f"{args.folder_name}/wrapper.py")
    copyfile(os.path.join(dirname, 'assets/config_template.py'), f"{args.folder_name}/config.py")

    print(f"New project created in: `{args.folder_name}`")
    print("")
    print(f"Open {args.folder_name}/fnc.py to begin defining your model.")
    print("")
    print(f"For help creating your function, see existing examples or read the documentation in the README.")
    print("")
