import logging, os, zipfile, hashlib

def start(args):
    print('in function')
    print(args)

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
            if 'test' not in file:
                ziph.write(os.path.join(root, file))
