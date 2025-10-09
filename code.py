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
"""
dogsite_job['dogsite_info'] ->Points to the summary analysis object for the entire protein — not individual pockets.
Contains quantitative pocket data for all detected pockets — things like:
Volume
Depth
Enclosure
Hydrophobicity
Aromaticity
Donor/acceptor counts
etc.
////////////////////////////////////////////////////////
dogsite_job['output_pockets']->
Comes directly from the job submission result (DOGSITE_JOBS).
Contains IDs of each detected pocket.
Each ID refers to a single pocket entry that you can query from
---------------------------------------------------------------------------
These endpoints focus on 3D structural details — like:
Residues forming the pocket
Atom coordinates
Pocket geometry
Visualization references








"""
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


scores_pocket={}
the_info=dogsite_info["info"]

for key in dogsite_info:
    print("k is ",key,end="\n")
print(dogsite_job.keys())
print(dogsite_job['output_pockets'])



the_info = dogsite_info["info"]
pocket_ids = dogsite_job["output_pockets"]

for pocket_data, pocket_id in zip(the_info, pocket_ids):
    print(f"{pocket_data['name']} → {pocket_id}")
    scores_pocket[pocket_id] = (
    0.3 * float(pocket_data['volume']) +
    0.2 * float(pocket_data['depth']) +
    0.2 * float(pocket_data['enclosure']) * 100 +
    0.1 * float(pocket_data['hydrophobicity']) * 100 +
    0.1 * float(pocket_data['aromat']) +
    0.1 * float(pocket_data['accept'] + pocket_data['donor']))




sorted_scores = sorted(scores_pocket.items(), key=lambda x: x[1], reverse=True)

# Print sorted pockets with their scores


min_score = min(scores_pocket.values())
max_score = max(scores_pocket.values())

# Normalize to 0–1
if max_score == min_score:
    normalized_scores = {pid: 1.0 for pid in scores_pocket}
else:
    normalized_scores = {
        pid: (score - min_score) / (max_score - min_score)
        for pid, score in scores_pocket.items()
    }

# Sort by normalized score (descending)
sorted_norm = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)

# Print normalized scores
for pid, score in sorted_norm:
    print(f"{pid}: {score:.3f}")