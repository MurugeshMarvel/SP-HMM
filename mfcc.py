
import numpy
import scipy.io.wavfile
from scipy.fftpack import dct
import matplotlib.pyplot as plt
from scipy import signal
import scipy.io.wavfile




def mfcc_generate(wav_file, length=None):

	sample_rate , signal_ = scipy.io.wavfile.read('hello1.wav')
	if length != 'None':
		signal_ = signal_[0:int(3.5 * sample_rate)]

	scipy.io.wavfile.write('mfcc_test1.wav',sample_rate,signal_)
	print len(signal_)
	y = range(len(signal_))
	NFFT = 512
	nfilt = 40
	num_ceps = 12
	cep_lifter = 22

	pre_emphasis = 0.97
	emphasized_signal = numpy.append(signal_[0], signal_[1:] - pre_emphasis * signal_[:-1])
	print emphasized_signal
	frame_size = 0.025
	frame_stride = 0.01
	frame_length, frame_step = frame_size * sample_rate, frame_stride * sample_rate
	signal_length = len(emphasized_signal)
	frame_length = int(round(frame_length))
	frame_step = int(round(frame_step))
	num_frames = int(numpy.ceil(float(numpy.abs(signal_length - frame_length))/ frame_step))
	pad_signal_length = num_frames * frame_step + frame_length
	z = numpy.zeros((pad_signal_length - signal_length))
	pad_signal = numpy.append(emphasized_signal, z)
	indices = numpy.tile(numpy.arange(0,frame_length), (num_frames, 1)) + numpy.tile(numpy.arange(0, num_frames * frame_step, frame_step), (frame_length,1)). T
	frames = pad_signal[indices.astype(numpy.int32,copy=False)]
	frames *= numpy.hamming(frame_length)

	mag_frames = numpy.absolute(numpy.fft.rfft(frames, NFFT))
	pow_frames = ((1.0/NFFT) * ((mag_frames) ** 2))

	low_freq_mel = 0
	high_freq_mel = (2595 * numpy.log10(1 + (sample_rate / 2) / 700))  # Convert Hz to Mel
	mel_points = numpy.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # Equally spaced in Mel scale
	hz_points = (700 * (10**(mel_points / 2595) - 1))  # Convert Mel to Hz
	bin = numpy.floor((NFFT + 1) * hz_points / sample_rate)

	fbank = numpy.zeros((nfilt, int(numpy.floor(NFFT / 2 + 1))))
	for m in range(1, nfilt + 1):
	    f_m_minus = int(bin[m - 1])   # left
	    f_m = int(bin[m])             # center
	    f_m_plus = int(bin[m + 1])    # right

	    for k in range(f_m_minus, f_m):
	        fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
	    for k in range(f_m, f_m_plus):
	        fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
	filter_banks = numpy.dot(pow_frames, fbank.T)
	filter_banks = numpy.where(filter_banks == 0, numpy.finfo(float).eps, filter_banks)  # Numerical Stability
	filter_banks = 20 * numpy.log10(filter_banks)  # dB
	mfcc = dct(filter_banks, type=2, axis=1, norm='ortho')[:, 1 : (num_ceps + 1)] # Keep 2-13
	(nframes, ncoeff) = mfcc.shape
	n = numpy.arange(ncoeff)
	lift = 1 + (cep_lifter / 2) * numpy.sin(numpy.pi * n / cep_lifter)
	mfcc *= lift  #*
	return mfcc