import numpy as np
import pandas as pd
import os
import glob
import mfcc




def mfcc_feature(data_path):
	df = pd.read_table(data_path + 'speaker-info.txt', usecols=['ID','AGE','GENDER','ACCENTS'],
                     index_col= False, delim_whitespace=True)
	file_ids = []
	for d in [data_path + 'txt/p%d/' % uid for uid in df.ID.values]:
		file_ids.extend([f[-12:-4] for f in sorted(glob.glob(d + '*.txt'))])

	wav_files = [data_path + 'wav48/%s/' %f[:4] + f + '.wav' for f in file_ids]
	return wav_files
feature_array = np.array([])
if __name__ == '__main__':
	feature = mfcc_feature('/home/murugesan/VCTK-Corpus/')
	for i in feature:
		np.append(feature_array, mfcc.mfcc_generate(i))