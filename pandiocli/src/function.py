import logging, os, zipfile, hashlib, pathlib
from .config import Conf

config = Conf()
if os.path.exists(str(pathlib.Path(__file__).parent.absolute())+'/config.json'):
    config.load(str(pathlib.Path(__file__).parent.absolute())+'/config.json')


def start(args):
    print('in function')
    print(args)
    if args.command == 'upload':
        if 'project_folder' in args:
            root_path = os.getcwd()
            tmp_path = '/tmp/'
            path = root_path + '/' + args.project_folder
            if os.path.isdir(path):
                # TODO, remove this when pandioml is available via PIP
                os.system(f"cp -rf {path}/../../pandioml/dist/pandioml-1.0.0-py3-none-any.whl {path}/deps/pandioml-1.0.0-py3-none-any.whl")
                os.system(f"pip download \
                            --only-binary :all: \
                            --platform manylinux1_x86_64 \
                            --python-version 38 -r {path}/requirements.txt -d {path}/deps")
                print('it worked')
                hash = hashlib.md5(bytes(args.project_folder, 'utf-8'))
                tmp_file = hash.hexdigest() + '.zip'
                zipf = zipfile.ZipFile(tmp_path + tmp_file, 'w', zipfile.ZIP_DEFLATED)
                zipdir(path, zipf)
                zipf.close()
                print(f"File located at {tmp_path}{tmp_file}")
                # TODO, make the post request to upload the function
                #response = requests.post(f"https://{config.PANDIO_CONNECTION_STRING}/admin/v3/functions/{config.PANDIO_TENANT}/{config.PANDIO_TENANT}/{hash}",
                # data={
                #   "inputs": persistent://public/default/input-topic,
                #   "parallelism": 1
                #   "output": persistent://public/default/output-topic
                #   "log-topic": persistent://public/default/log-topic
                #   "classname": org.example.test.ExclamationFunction
                #   "py": tmp_path + tmp_file
                # })
            else:
                raise Exception(f"Path ({path}) could not be found.")
        else:
            raise Exception('--folder-name must be specified')
    else:
        raise Exception('Nothing matched the action: {0}'.format(args.command))


def package(args):
    print(args)
    if args.action == 'create':
        if 'folder_name' in args:
            root_path = os.path.dirname(os.path.realpath(__file__))
            tmp_path = root_path + '/../'
            path = root_path + '/../functions/' + args.folder_name
            if os.path.isdir(path):
                print('it worked')
                hash = hashlib.md5(bytes(args.folder_name, 'utf-8'))
                zipf = zipfile.ZipFile(tmp_path + hash.hexdigest()+'.zip', 'w', zipfile.ZIP_DEFLATED)
                zipdir(path, zipf)
                zipf.close()
        else:
            raise Exception('--path must be specified')

    raise Exception('Nothing matched the action: {0}'.format(args.action))


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            if 'test' not in file and 'runner.py' not in file and 'requirements.txt' not in file:
                rel_dir = os.path.relpath(root, path)
                rel_file = os.path.join(rel_dir, file)
                if 'pycache' not in rel_file:
                    ziph.write(os.path.join(root, file), rel_file)
