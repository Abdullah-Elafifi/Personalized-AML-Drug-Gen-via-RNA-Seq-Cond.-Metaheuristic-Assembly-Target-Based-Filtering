import requests
import time
import json
import os
import io
from urllib.parse import urljoin
import sys
import time
import urllib.request
from Bio.PDB import PDBParser
import nglview as nv
import pandas as pd
#from sklearn.preprocessing import MinMaxScaler
import numpy as np

PROTEINS_PLUS_URL = 'https://proteins.plus/api/v2/'
UPLOAD = urljoin(PROTEINS_PLUS_URL, 'molecule_handler/upload/')
UPLOAD_JOBS = urljoin(PROTEINS_PLUS_URL, 'molecule_handler/upload/jobs/')
PROTEINS = urljoin(PROTEINS_PLUS_URL, 'molecule_handler/proteins/')
PROTEINSITES = urljoin(PROTEINS_PLUS_URL, 'molecule_handler/protein_sites/')
ELECTRONDENSITYMAP = urljoin(PROTEINS_PLUS_URL, 'molecule_handler/electron_density_maps/')
LIGANDS = urljoin(PROTEINS_PLUS_URL, 'molecule_handler/ligands/')
DOGSITE = urljoin(PROTEINS_PLUS_URL, 'dogsite/')
DOGSITE_INFO = urljoin(DOGSITE, 'info/')
DOGSITE_JOBS = urljoin(DOGSITE, 'jobs/')
try:
    response = requests.get(PROTEINS_PLUS_URL + '/')
    print(response)
except requests.ConnectionError as error:
    if 'Connection refused' in str(error):
        print('WARNING: could not establish a connection to the server', file=sys.stderr)
    raise



def poll_job(job_id, poll_url, poll_interval=1, max_polls=10):
    """Poll the progress of a job

    Continously polls the server in regular intervals and updates the job information, especially the status.

    :param job_id: UUID of the job to poll
    :type job_id: str
    :param poll_url: URl to send the polling request to
    :type poll_url: str
    :param poll_interval: time interval between polls in seconds
    :type poll_interval: int
    :param max_polls: maximum number of times to poll before exiting
    :type max_polls: int
    :return: polled job
    :rtype: dict
    """
    job = requests.get(poll_url + job_id + '/').json()
    status = job['status']
    current_poll = 0
    while status == 'pending' or status == 'running':
        print(f'Job {job_id} is {status}')
        current_poll += 1
        if current_poll >= max_polls:
            #print(f'Job {job_id} has not completed after {max_polls} polling requests' \
                  #f' and {poll_interval * max_polls} seconds')
            return job
        time.sleep(poll_interval)
        job = requests.get(poll_url + job_id + '/').json()
        status = job['status']
    #print(f'Job {job_id} completed with {status}')
    return job

pdb_path = 'Y:\\proteins_pdb\\A0AV96.pdb'
with open(pdb_path, 'rb') as upload_file:
    query = {'protein_file': upload_file}
    job_submission = requests.post(DOGSITE, files=query).json()
    dogsite_job = poll_job(job_submission['job_id'], DOGSITE_JOBS)


while(True):
    if(dogsite_job['status']=="success"):
        #print("completed",dogsite_job,"\n")
        break




#print("\n_we_got_here")


dogsite_info = requests.get(DOGSITE_INFO + dogsite_job['dogsite_info'] + '/').json()
c=1


scores=[]
the_info=dogsite_info["info"]
for key in dogsite_info:
    print("k is ",key,end="\n")
print(dogsite_job.keys())
print(dogsite_job['output_pockets'])


first_pocket=dogsite_job['output_pockets'][0]
site = requests.get(PROTEINSITES + first_pocket + '/').json()
residues_first_pocket = site['site_description']['residue_ids']
for i in residues_first_pocket:
    print(i)


for pocket in the_info:
    print(f"{c}",pocket, end='\n')
    scores.append((
    0.3 * float(pocket['volume']) +
    0.2 * float(pocket['depth']) +
    0.2 * float(pocket['enclosure']) * 100 +
    0.1 * float(pocket['hydrophobicity']) * 100 +
    0.1 * float(pocket['aromat']) +
    0.1 * float(pocket['accept'] + pocket['donor'])
    ))


min_score = min(scores)
max_score = max(scores)

normalized_scores = [(s - min_score) / (max_score - min_score) for s in scores]
normalized_scores.sort(reverse=True)
