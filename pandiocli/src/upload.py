import logging


def start(args):
    print('in upload')
    print(args)
    logging.debug(
        'The lowest level. Used for small details. Usually you care about these messages only when diagnosing problems.')
    logging.info('Used to record information on general events in your program or confirm that things are working at their point in the program.')
    logging.warning(
        'Used to indicate a potential problem that doesn’t prevent the program from working but might do so in the future.')
    logging.error(
        'Used to record an error that caused the program to fail to do something')
    logging.critical(
        'The highest level. Used to indicate a fatal error that has caused or is about to cause the program to stop running entirely.')

    print(args.url)