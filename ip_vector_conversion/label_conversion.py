import os
import sys

def convert(folder):
	for d, ds, fs in os.walk(folder):
		for fname in fs:
			if fname[-4:] != '.PHN':
				continue

			fullname = d + '/' + fname
			fr = open(fullname)
			fw = open(fullname[:-4] + '.lab','w')
			for line in fr:
				[s,e,p] = line.rstrip('\n').split()
				s_ns = str(int(float(s)/16000 * 1000000000))
				e_ns = str(int(float(e)/16000 * 1000000000))
				fw.write(s_ns + ' ' + e_ns + ' ' + p + '\n')
			fr.close()
			fw.close()
			print "Converted", fullname


if __name__ == '__main__':
	folder = '.'
	if len(sys.argv) > 1:
		folder = sys.argv[1]

	print "Converting the .phn (in frames) to .lab(in nanosec) in ", folder
	convert(folder)