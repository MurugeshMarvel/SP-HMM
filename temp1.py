import tensorflow as tf
from data import VCTK

data = VCTK(batch_size = 20)

sess = tf.InteractiveSession()
x = data.mfcc


u = x.eval()
print u