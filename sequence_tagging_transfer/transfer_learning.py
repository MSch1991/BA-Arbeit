#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 13:52:43 2017

@author: riedlmn
"""

import sys
from model.ner_model import NERModel
from model.config import Config
from model.data_utils import CoNLLDataset

import subprocess


def conv(n):
    n = n.decode("utf-8")
    n = n.replace(";","")
    n = n.replace(":","")
    n = n.replace("%","")
    return n

def readResults(f):
    cmd = ["sh","./evaluate_conll.sh",f]
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in result.stdout.readlines():
        ls = line.strip().split()
        if b'accuracy:' in ls:
            p = conv(ls[3])
            r = conv(ls[5])
            f = conv(ls[7])
            return [p,r,f]

if len(sys.argv)< 4:
    sys.stderr.write("No arguments have been specified to execute the script:\n")
    sys.stderr.write("python %s configuration transfer_training.conll transfer_test.conll\n" %(sys.argv[0]))
    sys.exit(0)
config_file = sys.argv[1]
filename_train2 = sys.argv[2]
filename_dev2 = sys.argv[3]

config = Config(config_file)

# load model
model = NERModel(config)
model.build()
model.restore_session(config.dir_model)


train2  = CoNLLDataset(filename_train2, config.processing_word,
                     config.processing_tag, config.max_iter)
dev2  = CoNLLDataset(filename_dev2, config.processing_word,
                     config.processing_tag, config.max_iter)

#continue training!
model.train(train2,dev2)

