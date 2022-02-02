import os
def get_initial_directory(cache_dir):
    if os.path.isfile(cache_dir):
        initial_dir = open(cache_dir, 'r').read()
        if not os.path.isdir(initial_dir):
            initial_dir = os.getcwd()
        return initial_dir
    else:
        return os.getcwd()