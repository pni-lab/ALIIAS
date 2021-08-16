from ALIIAS.namegenerator import generate_n_personal_info
from ALIIAS.encryption import Encryptor
from ALIIAS.utility import norm_str
from Crypto.Random import get_random_bytes
from tqdm import tqdm
from joblib import Parallel, delayed
import numpy as np
from hashlib import sha256

n_subjects = 100
n_runs = 100000
n_cores = -1

pseudokey = get_random_bytes(32)

enc = Encryptor(pseudonym_key=pseudokey)
duplicate_runs = []

def find_sid_duplicates():
    data = generate_n_personal_info(n_subjects)[1]

    short_id = [[], [], [], [], [], [], []]
    duplicate = [[], [], [], [], [], [], []]

    for subject in data:
        long_id = enc.get_long_id(norm_str(subject))

        short_id[0].append(long_id[0:3])
        short_id[1].append(long_id[0:4])
        short_id[2].append(long_id[0:5])
        short_id[3].append(long_id[0:6])
        short_id[4].append(long_id[0:7])
        short_id[5].append(long_id[0:8])
        short_id[6].append(long_id[0:9])

    if n_subjects - len(set(short_id[0])) == 0:
        duplicate[0] = 0
    else:
        duplicate[0] = 1

    if n_subjects - len(set(short_id[1])) == 0:
        duplicate[1] = 0
    else:
        duplicate[1] = 1

    if n_subjects - len(set(short_id[2])) == 0:
        duplicate[2] = 0
    else:
        duplicate[2] = 1

    if n_subjects - len(set(short_id[3])) == 0:
        duplicate[3] = 0
    else:
        duplicate[3] = 1

    if n_subjects - len(set(short_id[4])) == 0:
        duplicate[4] = 0
    else:
        duplicate[4] = 1

    if n_subjects - len(set(short_id[5])) == 0:
        duplicate[5] = 0
    else:
        duplicate[5] = 1

    if n_subjects - len(set(short_id[6])) == 0:
        duplicate[6] = 0
    else:
        duplicate[6] = 1

    return duplicate[0], duplicate[1], duplicate[2], duplicate[3], duplicate[4], duplicate[5], duplicate[6]


result = Parallel(n_jobs=n_cores, verbose=10)(delayed(find_sid_duplicates)() for i in range(n_runs))
duplicates_3, duplicates_4, duplicates_5, duplicates_6, duplicates_7, duplicates_8, duplicates_9 = zip(*result)

print('------------------------------')
print('No participants: ', n_subjects)
print('3 chars: ', sum(duplicates_3), 'duplicates out of ', n_runs)
print('4 chars: ', sum(duplicates_4), 'duplicates out of ', n_runs)
print('5 chars: ', sum(duplicates_5), 'duplicates out of ', n_runs)
print('6 chars: ', sum(duplicates_6), 'duplicates out of ', n_runs)
print('7 chars: ', sum(duplicates_7), 'duplicates out of ', n_runs)
print('8 chars: ', sum(duplicates_8), 'duplicates out of ', n_runs)
print('9 chars: ', sum(duplicates_9), 'duplicates out of ', n_runs)


