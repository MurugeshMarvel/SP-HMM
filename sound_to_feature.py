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
            rawfname= bdir + '/' + fname[:-4]+'.rawaudio'
            wavfname = bdir + '/'+ fname
            tempfname = bdir + '/' + fname[:-4] + '_temp.wav'
            mfccfname = bdir + '/' + fname[:-4] + mfc_extension
            if sox:
                shutil.move(wavfname, tempfname)
                call(['sox',tempfname,wavfname])
                shutil.move(tempfname,wavfname)

            if htk_mfcc:
                call(['HCopy','-C','wav_config',wavfname,mfccfname])
                srate, sound = wavfile.read(wavfname)
            if stereo_wave and len(sound.shape == 2):
                sound = sound[:,0]+ sound[:,1]
            if gammatones:
                gammatonefname = bdir + '/' + fname[:-4] + '_gamma.npy'
                tmp_snd = loadsound(wavfname)
                gamma_cf = erbspace(20*Hz, 20*kHz, n_gmammatones_filters)
                gamma_fb = Gammatone(tmp_snd, gamma_cf)
                with open(gammatonefname,'w') as o_f:
                    npsave(o_f, gamma_fb.process())

            if spectograms:
                powersspec, _,_,_ = specgram(sound, NFFT=int(srate * specgram_window), Fs=srate,noverlap=int(srate*specgram_window))
                specgramfname = bdir + '/' + fname[:-4]+'_specgram.npy'
                with open(specgramfname,'w') as o_f:
                    npsave(o_f , powerspec.T)
                if filterbanks:
                    if fbanks ==None:
                        fbanks = Spectral(nfilt = n_fbanks, alpha=0.97,do_dct=False, fs=srate, frate=fbanks_rate, wlen=fbanks_window,nfft=1024,do_deltas=False,do_deltasdeltas=False)
                    fbank = fbanks.transform()