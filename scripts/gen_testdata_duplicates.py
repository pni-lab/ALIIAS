from pseudoID.namegenerator import generate_n_personal_info
from pseudoID.encryption import Encryptor
from pseudoID.utility import norm_str
from tqdm import tqdm
import xlsxwriter


n_subjects = 10000000
target_path = '../../data_test/duplicates.xlsx'

data = generate_n_personal_info(n_subjects)

enc = Encryptor()

short_id = []
ciphers = []

# encrypt all the participants
for subject in tqdm(data):
    ciphertext = ""

    first = True
    for element in subject:
        if first:
            ciphertext = ciphertext + norm_str(element)
            first = False
        else:
            ciphertext = ciphertext + ' ' + norm_str(element)
    ciphers.append(ciphertext)
    long_id = enc.long_id(ciphertext)
    short_id.append(enc.short_id(long_id))

# find all the duplicates, based on SID
helper = set()

duplicate_idx = []
duplicate_val = []
for idx, val in enumerate(short_id):
    if val not in helper:
        helper.add(val)
    else:
        duplicate_val.append(val)
        duplicate_idx.append(idx)

# locate all the "names" based on the duplicate short ids
duplicate_names = []
for idx, dup in enumerate(duplicate_val):
    for idx_sid, sid in enumerate(short_id):
        if sid == dup:
            duplicate_names.append(data[idx_sid])


print(duplicate_names)

workbook = xlsxwriter.Workbook(target_path)
worksheet = workbook.add_worksheet()

for row, sub in enumerate(duplicate_names):
    for col, info in enumerate(sub):
        worksheet.write(row, col, info)
workbook.close()

print('Number of duplicates: ', n_subjects - len(set(short_id)))
