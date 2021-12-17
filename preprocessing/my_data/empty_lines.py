import sys

import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import os
from os.path import join as p_join
import re


all_corpus = sys.argv[1]
new_corpus = sys.argv[2]

os.makedirs(new_corpus, exist_ok=True)

for file in os.listdir(all_corpus):
    with open(p_join(all_corpus, file), "r", encoding="utf-8") as fp_in:
        with open(p_join(new_corpus, file), "w", encoding="utf-8") as fp_out:
            for line in fp_in:
                punkt_param = PunktParameters()
                abbreviation = [
                    "Tel", "str", "staatl", "gepr", "ggfs", "z.b",
                    "nr", "2", "1", "bzw", "prof", "dr", "med", "sog",
                    "inc", "inkl", "ca", "3", "ggf", "mio", "zzgl",
                    "div", "04", "11", "mrd", "etc", "v.", "7", "co",
                    "u.a", "insb", "31", "30", "21", "J", "Abs", "H",
                    "usw", "h", "u.v.m", "4", "Co", "a", "A",
                    "S", "d.h", "St", "15", "T", "e.V", "vgl",
                    "Std", "z.T", "evtl"
                ]

                punkt_param.abbrev_types = set(abbreviation)
                tokenizer = PunktSentenceTokenizer(punkt_param)
                sentences = tokenizer.tokenize(line)

                for a in sentences:
                    suffix = "str."
                    if a.endswith(suffix):
                        print(a, file=fp_out)
                    else:
                        print(a + "\n", file=fp_out)
