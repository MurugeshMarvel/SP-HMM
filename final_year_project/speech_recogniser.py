import sugartensor as tf
import numpy as np
import librosa
from tensor_model import *
import input_vector as data

tf.sg_verbosity(10)

batch_size = 1     
voca_size = data.voca_size

x = tf.placeholder(dtype=tf.sg_floatx, shape=(batch_size, None, 20))

seq_len = tf.not_equal(x.sg_sum(axis=2), 0.).sg_int().sg_sum(axis=1)

logit = get_logit(x, voca_size=voca_size)

decoded, _ = tf.nn.ctc_beam_search_decoder(logit.sg_transpose(perm=[1, 0, 2]), seq_len, merge_repeated=False)

y = tf.sparse_to_dense(decoded[0].indices, decoded[0].dense_shape, decoded[0].values) + 1

tf.sg_arg_def(file=('', 'speech wave file to recognize.'))

wav, _ = librosa.load(tf.sg_arg().file, mono=True, sr=16000)

mfcc = np.transpose(np.expand_dims(librosa.feature.mfcc(wav, 16000), axis=0), [0, 2, 1])

with tf.Session() as sess:

    tf.sg_init(sess)
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint('saved_model/20_03/'))
    label = sess.run(y, feed_dict={x: mfcc})
data.print_index(label)