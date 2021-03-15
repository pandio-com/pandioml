import logging

def start(args):
    print(f"You have successfully registered at Pandio.com!")
    print("")
    print(f"Please check your email ({args.email}) to verify your registration.")
    print("")
    print(f"Once you have verified your email, all functionality will be enabled.")
    print("")
    logging.debug(f'Sending a registration email to ({args.email})')
