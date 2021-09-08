import subprocess
import time
import argparse

'''
Wrapper script that runs a given task and monitors for changes to git remote,
restarting the task if changes are detected and pulled.
'''

parser = argparse.ArgumentParser(description='Run a task while monitoring git for changes. Restart automatically when changes are detected on the current branch')
parser.add_argument('-t', help='Time in seconds between git pull checks. Default is 2.', default=2)
parser.add_argument('arg', nargs='+', help='Task command and arguments.')

args = parser.parse_args()

delay = args.t
task = args.arg

task_p = subprocess.Popen(task, shell=True)

try:
    while True:
        # Blocks until pull is finished
        status_out = subprocess.check_output(['git', 'pull']).decode()
        
        if status_out.strip() != 'Already up to date.':
            # Restart task
            print('CI/CD: Changes detected, restarting...')
            task_p.kill()
            task_p = subprocess.Popen(task, stdout=subprocess.PIPE)

        time.sleep(delay)
finally:
    task_p.kill()