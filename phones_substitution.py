import os
import cPickle
import sys
import signal
import json


def process(folder, sentences=False, foldings = {},startend_sil=False):