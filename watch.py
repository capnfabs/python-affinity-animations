# watch.py

import subprocess
from watchgod import run_process, AllWatcher

def runner():
    subprocess.run(['python', '-m', 'build_pop_n_fade'])

if __name__ == '__main__':
    # by default, WatchGod only watches for changes in .py files;
    # this watches for everything (including SVG files).
    run_process('.', runner, watcher_cls=AllWatcher)
