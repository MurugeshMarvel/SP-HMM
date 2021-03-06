import numpy as np
import pandas as pd
import glob
import os
import string
import itertools
import mfcc
import theano
import sugartensor as tf

class data(object):
    def __init__(self, batch_size = 16, data_path = '/home/murugesan/VCTK-Corpus/', vocabulary_loading= False):
        if vocabulary_loading:
            vocabulary_file = 'muru_works' + self.__class__.__name__ + 'vocabulary.npy'
            if os.path.exists(vocabulary_file):
                self.index2byte = np.load(vocabulary_file)
                self.byte2index  = {}
                for i, b in enumerate(self.index2byte):
                    self.byte2index[b]  = i
                self.voca_size = len(self.index2byte)
                tf.sg_info('Vocabulary loaded')
                return
        labels, wave_files = self.load_corpus(data_path)
        
        label = theano.tensor.as_tensor_variable(labels)
        wave_file = theano.tensor.as_tensor_variable(wave_file)
        label, wave_file = tf.train.slice_input_producer([labels, wave_file], shuffle = True)
        def load_mfcc(self, source):
            lable, wav = source
            lab = np.fromstring(lable, np.int)
            mfcc = mfcc.mfcc_generate(wav)
            return lab, mfcc
    def load_corpus(self,data_path):
        df = pd.read_table(data_path + 'speaker-info.txt', usecols=['ID','AGE','GENDER','ACCENTS'],
                     index_col= False, delim_whitespace=True)
        file_ids = []
        for d in [data_path + 'txt/p%d/' % uid for uid in df.ID.values]:
            file_ids.extend([f[-12:-4] for f in sorted(glob.glob(d + '*.txt'))])
            
            
        wav_files = [data_path + 'wav48/%s/' %f[:4] + f + '.wav' for f in file_ids]
        
        file_id, wav_file = [] , []
        for i,w in zip(file_ids, wav_files):
            if os.stat(w).st_size > 120000:
                file_id.append(i)
                wav_file.append(w)
                
        sents = []
        for f in file_id:
            s = ' '.join(open(data_path + '/txt/%s/' % f[:4] + f + '.txt').read().
                                translate(None, string.punctuation).lower().split())
            sents.append([ord(ch) for ch in s])
        self.index2byte = [0] + list(np.unique(list(itertools.chain(*sents))))
        self.byte2index = {}
        for i,b in enumerate(self.index2byte):
            self.byte2index[b] = i
        self.voca_size = len(self.index2byte)
        self.max_len = np.max(len(s) for s in sents)
        #saving vocabulary
        vocabulary_dir = 'muru_work'  + self.__class__.__name__
        if not os.path.exists(os.path.dirname(vocabulary_dir)):
            try:
                os.makedirs(os.path.dirname(vocabulary_dir))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        vocabulary_file = vocabulary_dir + '_vocabulary.npy'
        if not os.path.exists(vocabulary_file):
            np.save(vocabulary_file, self.index2byte)
        label = []
        for s in sents:
            label.append(np.asarray([self.byte2index[ch] for ch in s]).tostring())
        return label, wav_file
if __name__ == "__main__":
    obj = data()
    ids , wav = obj.load_corpus('/home/murugesan/VCTK-Corpus/')
    print ids