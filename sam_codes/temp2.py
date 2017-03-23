import numpy as np
import pandas as pd
import os
import glob
import mfcc
import string
import itertools

data_path = '/home/murugesan/VCTK-Corpus/'
df = pd.read_table(data_path + 'speaker-info.txt', usecols=['ID', 'AGE', 'GENDER', 'ACCENTS'],
                           index_col=False, delim_whitespace=True)

# make file ID
file_ids = []
for d in [data_path + 'txt/p%d/' % uid for uid in df.ID.values]:
    file_ids.extend([f[-12:-4] for f in sorted(glob.glob(d + '*.txt'))])

# make wave file list
wav_files = [data_path + 'wav48/%s/' % f[:4] + f + '.wav' for f in file_ids]

# exclude extremely short wave files
file_id, wav_file = [], []
for i, w in zip(file_ids, wav_files):
    if os.stat(w).st_size > 240000:  # at least 5 seconds
        file_id.append(i)
        wav_file.append(w)

# read label sentence
sents = []

for f in file_id:
    # remove punctuation, to lower, clean white space
    s = ' '.join(open(data_path + 'txt/%s/' % f[:4] + f + '.txt').read()
                 .translate(None, string.punctuation).lower().split())
    # append byte code
    sents.append([ord(ch) for ch in s])

in2by = []
in2by = [0] + list(np.unique(list(itertools.chain(*sents))))
by2in = {}
for i, b in enumerate(in2by):
    by2in[b] = i

voca_size = len(in2by)
print voca_size
max_len = np.max([len(s) for s in sents])
print max_len