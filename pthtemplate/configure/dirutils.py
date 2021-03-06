import os
import datetime

def get_exper_id(exper_name):
    dt = datetime.datetime.now()
    exper_id = '{}_{:02d}-{:02d}-{:02d}'.format(dt.date(), dt.hour, dt.minute, dt.second)
    if exper_name is not None:
        exper_id = '{}_{}'.format(exper_id, exper_name)
    return exper_id

def get_dir(exper_name, subroot, subdir=None):
    """
    Return $subroot/$exper_name/$subdir
    """
    if subdir is None:
        return os.path.join(os.getenv('HISTORY'), os.getenv('PROGRAM'), subroot, exper_name)
    else:
        return os.path.join(os.getenv('HISTORY'), os.getenv('PROGRAM'), subroot, exper_name, subdir)
