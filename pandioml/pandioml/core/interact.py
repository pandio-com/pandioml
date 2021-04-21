import code


# local=locals() or local=globals()
def interact(banner=None, local=locals(), exitmsg=None):
    return code.interact(banner='Start PandioML Interactive Session' + (' | ' + banner if banner is not None else ''),
                         readfunc=None, local=local, exitmsg='Exit PandioML Interactive Session' +
                                                             (' | ' + exitmsg if exitmsg is not None else ''))
