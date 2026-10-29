import requests
import json
import uuid
import re

sample_rephrased = (
    "Pooling diverse stochastic partitions into a consensus clustering dampens initialization sensitivity and avoids poor local optima. "
    "Aggregating clusterings across random initializations or projected subspaces stabilizes partition boundaries against local minima. "
    "Yet in high dimensions (D >> N), ambient noise undermines this aggregation through two distinct mechanisms. "
    "The first bottleneck is computational: classical consensus functions construct an N x N co-association matrix S where entry S_ij records "
    "the empirical fraction of base partitions assigning observations to the same cluster. "
    "Storing S incurs quadratic memory scaling O(N^2), which becomes prohibitive on large cohorts."
)

# Test PirateXX
space_url = 'https://piratexx-ai-content-detector.hf.space'
session_hash = str(uuid.uuid4())[:8]
r = requests.post(f'{space_url}/queue/join', json={'data': [sample_rephrased], 'fn_index': 0, 'session_hash': session_hash}, timeout=15)
r2 = requests.get(f'{space_url}/queue/data?session_hash={session_hash}', stream=True, timeout=20)
for line in r2.iter_lines():
    if line and 'process_completed' in line.decode('utf-8'):
        payload = json.loads(line.decode('utf-8').replace('data: ', ''))
        print("PirateXX:", payload['output']['data'][0][0])
        break

# Test Liketropy (tr74)
sp = 'tr74-liketropy-llm-detector'
session_hash = str(uuid.uuid4())[:8]
r = requests.post(f'https://{sp}.hf.space/gradio_api/queue/join', json={'data': [sample_rephrased], 'fn_index': 0, 'session_hash': session_hash}, timeout=15)
r2 = requests.get(f'https://{sp}.hf.space/gradio_api/queue/data?session_hash={session_hash}', stream=True, timeout=20)
for line in r2.iter_lines():
    if line and 'process_completed' in line.decode('utf-8'):
        payload = json.loads(line.decode('utf-8').replace('data: ', ''))
        print("Liketropy:", payload['output']['data'][0])
        break
