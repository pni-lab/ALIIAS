from pseudoID.namegenerator import generate_n_personal_info
from pseudoID.encryption import Encryptor
from pseudoID.utility import norm_str
from tqdm import tqdm
from joblib import Parallel, delayed
import xlsxwriter


n_subjects = 500
n_runs = 100000
n_cores = -1


def parfor_subject_sweep():
    data = generate_n_personal_info(n_subjects)
    enc = Encryptor()
    short_id = []
    duplicate_runs = []
    for subject in data:
        ciphertext = ""

        first = True
        for element in subject:
            if first:
                ciphertext = ciphertext + norm_str(element)
                first = False
            else:
                ciphertext = ciphertext + ' ' + norm_str(element)

        long_id = enc.long_id(ciphertext)
        short_id.append(enc.short_id(long_id))

        if n_subjects - len(set(short_id)) == 0:
            duplicate = 0
        else:
            duplicate = 1

    return duplicate

result = Parallel(n_jobs=n_cores, verbose=10)(delayed(parfor_subject_sweep)() for i in range(n_runs))
print(sum(result))





