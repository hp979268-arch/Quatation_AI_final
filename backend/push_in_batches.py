import subprocess
import time
import os

print('Getting untracked files...')
res = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], capture_output=True, text=True)
files = res.stdout.strip().split('\n')
res2 = subprocess.run(['git', 'diff', '--name-only'], capture_output=True, text=True)
files.extend(res2.stdout.strip().split('\n'))

files = list(set([f for f in files if f]))
print(f'Found {len(files)} files to commit.')

if not files:
    print('Nothing to push.')
    exit(0)

batch_size = 100
for i in range(0, len(files), batch_size):
    batch = files[i:i+batch_size]
    print(f'\n--- Committing batch {i//batch_size + 1} of {(len(files)-1)//batch_size + 1} ---')
    subprocess.run(['git', 'add'] + batch)
    subprocess.run(['git', 'commit', '-m', f'Sync images batch {i//batch_size + 1}'])
    print('Pushing to origin main...')
    # Need to push the current branch (quick_fix) to origin's main branch
    res_push = subprocess.run(['git', 'push', 'origin', 'quick_fix:main'])
    if res_push.returncode != 0:
        print('Push failed! Aborting.')
        break
    time.sleep(2)
print('Done!')
