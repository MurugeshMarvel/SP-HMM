import os
import shutil
import sys
from numpy import call
from numpy import save as npsave
import scipy
from scipy.io import wavfile


specgram_window = 0.020
specgram_overlap =0.010
fbanks_window  = 0.025
fbanks_rate = 100
n_fbanks = 40
n_gmammatones_filters = 1000

def process(folder,debug=False,htk_mfcc=False,forcemfcext=False,stereo_wave=False,gammatones=False,spectograms=False,filterbanks=False,sox=True):
    mfc_extension = '.mfc_unnorm'
    wcfg = open('wav_config','r')
    for line in wcfg:
        if "ENORMALISE" in line:
            mfc_extension = '.mfc'

    if forcemfcext:
        mfc_extension = '.mfc'
    print "MFC Extension is", mfc_extension
    if gammatones:
        try:
            from brian import Hz, kHz
            from brian.hears import loadsound, erbspace, Gammatone

        except ImportError:
            print >> sys.stderr, "You need Brian Hears"

            sys.exit(-1)

        if spectograms:
            try:
                from pylab import specgram

            except ImportError:
                print >> sys.stderr,'You need Pylab'
                sys.exit(-1)

        fbanks = None
        if filterbanks:
            try:
                sys.path.append('../spectral')
                from spectral import Spectral

            except ImportError:
                print >> sys.stderr, 'you need spectral (in the parent folder)'

        for bdir, _ , files in  os.walk(folder):
            for fname in files:
                if fname[-4:] != '.WAV':
                    continue
                rawfname= bdir + '/' + fname[:4]+'.rawaudio'
                wavfname = bdir + '/'+ fname[:4]
                tempfname = bdir + '/' + fname[:4] + '_temp.wav'
                mfccfname = bdir + '/' + fname[:-4] + mfc_extension
                if sox:
                    shutil.move(wavfname, tempfname)
                    call(['sox',tempfname,wavfname])
                    shutil.move(tempfname,wavfname)

                if htk_mfcc:
                    call(['HCopy','-C','wav_config',wavfname,mfccfname])
                    srate, sound = wavfile.read(wavfname)
                    
