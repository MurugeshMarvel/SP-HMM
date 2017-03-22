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

# make vocabulary
index2byte = [0] + list(np.unique(list(itertools.chain(*sents))))  # add <EMP> token
print len(index2byte)
byte2index = {}
for i, b in enumerate(index2byte):
    byte2index[b] = i
voca_size = len(index2byte)
max_len = np.max([len(s) for s in sents])

# save vocabulary
vocabulary_dir = '/home/murugesan/Desktop/' + 'marvel'
if not os.path.exists(os.path.dirname(vocabulary_dir)):
    try:
        os.makedirs(os.path.dirname(vocabulary_dir))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
#vocabulary_file = open(vocabulary_dir + '_vocabulary.txt','w')
#vocabulary_file.write(str(index2byte))
# byte to index label
label = []
for s in sents:
    # save as string for variable-length support.
    label.append(np.asarray([byte2index[ch] for ch in s]).tostring())

#print label, wav_file