import logging, pathlib, os
from .config import Conf

config = Conf()
if os.path.exists(str(pathlib.Path(__file__).parent.absolute())+'/config.json'):
    config.load(str(pathlib.Path(__file__).parent.absolute())+'/config.json')


def start(args):
    print(f"You have successfully registered at Pandio.com!")
    print("")
    print(f"Please check your email ({args.email}) to verify your registration.")
    print("")
    print(f"Once you have verified your email, all functionality will be enabled.")
    print("")
    logging.debug(f'Sending a registration email to ({args.email})')
    config.set_value('PANDIO_EMAIL', args.email)
    f = open(str(pathlib.Path(__file__).parent.absolute())+'/config.json', "w")
    f.write(config.generate_json())
    f.close()
