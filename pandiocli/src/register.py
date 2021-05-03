import logging, pathlib, os
from .config import Conf
import requests
import faker
import time
from appdirs import user_config_dir

config = Conf()
if os.path.exists(user_config_dir('PandioCLI', 'Pandio')+'/config.json'):
    config.load(user_config_dir('PandioCLI', 'Pandio')+'/config.json')


def save_config():
    f = open(user_config_dir('PandioCLI', 'Pandio') + '/config.json', "w")
    f.write(config.generate_json())
    f.close()


def register(email):
    fake = faker.Faker('en_US')
    response = requests.post(
        "https://app.staging.pandio.com/api/v1/starter/create-user",
        json={'email': email, 'first_name': getattr(fake, 'first_name_nonbinary')(),
              'last_name': getattr(fake, 'last_name_nonbinary')()}
    )

    if response.status_code != 201:
        return None

    return response.json()


def get_details(token):
    response = requests.get(
        "https://app.staging.pandio.com/api/v1/starter/tenant-details",
        headers={'Authorization': f"Bearer {token}", 'Accept': 'application/json'}
    )

    if response.status_code != 200:
        print(response.json()['error'])
        exit()

    if response.json()['status'] != 'HEALTH_OK':
        print("")
        print("Retrieving...")
        return None

    return response.json()


def start(args):
    print(f"Creating an account with email {args.email}.")
    print("")
    existing_token = getattr(config, 'PANDIO_REGISTER_TOKEN')
    if existing_token is False:
        token = register(args.email)
        if token is None:
            print("")
            print("An error occurred. Please try again.")
            exit()

        config.set_value('PANDIO_REGISTER_TOKEN', token)

        save_config()
    else:
        token = existing_token

    input("Please verify your email and then return to this prompt and hit enter:")

    print("")

    print("Retrieving your account details.")

    time.sleep(10)

    for i in range(0, 3):
        details = get_details(token)
        if details is None:
            time.sleep(20)
            continue
        else:
            break

    if details is None:
        print("")
        print("Something went wrong with account activation. "
              "Please try again or reach out to customer support at support@pandio.com.")
        exit()

    config.set_value('PANDIO_CLUSTER', details['data']['cluster'])
    config.set_value('PANDIO_TENANT', details['data']['tenant'])
    config.set_value('PANDIO_NAMESPACE', details['data']['namespace'])
    config.set_value('PANDIO_CLUSTER_TOKEN', details['data']['cluster_token'])
    config.set_value('PANDIO_DATA_TOKEN', details['data']['training_data_token'])
    config.set_value('PANDIO_EMAIL', args.email)

    print("")
    print("Your account is now active, cheers!")
    print("")

    save_config()
