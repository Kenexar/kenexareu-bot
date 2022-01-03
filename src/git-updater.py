import os
import subprocess
import time
from datetime import datetime


def update_check(result=subprocess.run(['git', 'pull'], stdout=subprocess.PIPE, check=True)):
    return result.stdout.decode('utf-8')


rounds = 0
runs = 0

if __name__ == '__main__':
    while True:
        runs += 1
        print('run through', runs)
        if datetime.now().strftime('%H') in ['12', '0']:
            if 'already up to date.' in update_check().lower():
                continue

            time.sleep(120)
            os.system('./restart.sh')
            rounds += 1
            print(f'restart {rounds}')

        time.sleep(3600)
