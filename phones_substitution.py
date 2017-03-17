import os
import cPickle
import sys
import signal
import json


def process(folder, sentences=False, foldings = {},startend_sil=False):
	c_before = {}
	c_after = {}
	for d, ds, fs in os.walk(folder):
		for fname in fs:
			if fname[-4:] != '.lab':
				continue
			fullname = d.rstrip('/') + '/' + fname
			print fullname
			phones_before = []
			phones_after = []
			os.rename(fullname, fullname +'~')
			fr = open(fullname+'~','r')
			fw = open(fullname,'w')
			text_buffer = []
			for line in fr:
				phones_before.append(line.split()[-1])
				tmpline = line
				tmpline = tmpline.replace('-','')
				tmp = tmpline.split()
				for k, v in foldings.iteritems():
					if tmp[-1] = = k :
						tmp[-1] = v
						tmpline = ' '.join(tmp)

				text_buffer.append(tmpline.split())
			first_phone = text_buffer[0][-1].strip()
			last_phone = text_buffer[-1][-1].strip()
			if sentences:
				if first_phone == 'h#' or first_phone == 'sil' or first_phone == '<s>' or first_phone == '{B_TRANS}':
					text_buffer[0] = text_buffer[0][:-1] + ['!ENTER']

				if last_phone == 'h#' or last_phone == 'sil' or last_phone == '</s>' or last_phone == '{E_TRANS}':
					text_buffer[0] = text_buffer[-1][:-1] + ['!EXIT']

			if startend_sil:
				text_buffer[0] = text_buffer[0][:-1] + ['sil']
				text_buffer[-1] = text_buffer[-1][:-1] + ['sil']

			for buffer_line in text_buffer:
				phones_after.append(buffer_line[-1])
				fw.write(' '.join(buffer_line)  + '\n')
			fw.close()
			os.remove(fullname + '~')
			for tmp_phn in phones_before:
				