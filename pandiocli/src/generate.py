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
    copyfile(os.path.join(dirname, 'assets/function_template.py'), f"{args.folder_name}/function.py")

    print(f"New project created in: `{args.folder_name}`")
    print("")
    print(f"Open {args.folder_name}/function.py to begin defining your model.")
    print("")
    print(f"Execute `python {args.folder_name}/runner.py` to test your newly created function.")
    print("")
    print(f"When ready, deploy to Pandio with `pandiocli function upload {args.folder_name}`")
    print("")
