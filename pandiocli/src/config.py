import pathlib, os
from goodconf import GoodConf, Value


class PandioConf(GoodConf):
    @classmethod
    def set_value(cls, key, value):
        if hasattr(cls, key):
            return setattr(cls, key, value)

        return False


class Conf(PandioConf):
    "Configuration for pandiocli"
    DEBUG = Value(default=False, help="Toggle debugging.")
    PANDIO_CLUSTER = Value(
        default='NOT_CONFIGURED',
        help="Pandio cluster url")
    PANDIO_TENANT = Value(
        default='NOT_CONFIGURED',
        help="Pandio cluster tenant")
    PANDIO_NAMESPACE = Value(
        default='NOT_CONFIGURED',
        help="Pandio cluster namespace")
    PANDIO_CLUSTER_TOKEN = Value(
        default='NOT_CONFIGURED',
        help="Pandio cluster authorization token")
    PANDIO_DATA_TOKEN = Value(
        default='NOT_CONFIGURED',
        help="Pandio data authorization token")
    PANDIO_REGISTER_TOKEN = Value(
        default=None,
        help="Pandio register authorization token")
    PANDIO_EMAIL = Value(
        default='NOT_CONFIGURED',
        help="Pandio account email")


config = Conf()
if os.path.exists(str(pathlib.Path(__file__).parent.absolute())+'/config.json'):
    config.load(str(pathlib.Path(__file__).parent.absolute())+'/config.json')


def start(args):
    if args.command == 'set' and 'key' in args and 'value' in args:
        if config.set_value(args.key, args.value) is not False:
            print(f"Setting {args.key} to {args.value}")
            f = open(str(pathlib.Path(__file__).parent.absolute()) + '/config.json', "w")
            f.write(config.generate_json())
            f.close()
        else:
            print(f"Could not set {args.key} to {args.value}, {args.key} does not exist.")

    elif args.command == 'show':
        print("PANDIO SETTINGS")
        print("")
        for k in config._values:
            print(k, '=', getattr(config, k))
    else:
        print(f"Action ({args.action}) not found.")

    print("")
