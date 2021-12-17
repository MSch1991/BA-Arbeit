#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 21:15:04 2021

@author: melle
"""

import re

import nltk
import os

PHONE_REGEX = r"\+\d{2}\s?(?:\(\d+\))?\s?\d+-?\s?\d+-?\d+"

PHONE_PLACEHOLDER = "PHONENUMBERPLACEHOLDERPYTHON"

ABBREVIATIONS = ["Tel.", "str.", "staatl.", "gepr.", "ggfs.", "z.b.",
                 "nr.", "2.", "1.", "bzw.", "prof.", "dr.", "med.", "sog.",
                 "inc.", "inkl.", "ca.", "3.", "ggf.", "mio.", "zzgl.",
                 "div.", "04.", "11.", "mrd.", "etc.", "v.", "7.", "co.",
                 "u.a.", "z.B.", "Str.", "Nr.", "Prof.", "Dr.", "Med.",
                 "Mio.", "Mrd.", "insb.", "J.", "21.", "30.", "31.",
                 "Abs.", "H.", "usw.", "h.", "u.v.m.", "4.", "Co.", "a.",
                 "A.", "S.", "d.h.", "St.", "15.", "T.", "e.V.", "vgl.",
                 "Std.", "z.T.", "evtl."]

ABBREVIATIONS = [entry.replace(".", "\\.") for entry in ABBREVIATIONS]
ABBREV_REGEX = r"(?<=\W)(" + '|'.join(ABBREVIATIONS) + r")(?=\W)"

ABBREV_PLACEHOLDER = "ABBREVPLACEHOLDER"

SOURCE_DIR = "/home/melle/Schreibtisch/dev_data_newline/with_newline"
TARGET_DIR = "/home/melle/Schreibtisch/dev_data_newline/csv_unanno"


def main():
    files = [file_name for file_name in os.listdir(SOURCE_DIR) if file_name.endswith("txt")]
    for file in files:
        generate_os_file(file)


def generate_os_file(file):
    if SOURCE_DIR == TARGET_DIR:
        return ValueError("Source and Target directory can't be the same")

    os.makedirs(TARGET_DIR, exist_ok=True)

    in_file = os.path.join(SOURCE_DIR, file)
    out_file = os.path.join(TARGET_DIR, file)

    lines = read_txt(in_file)
    lines = convert_to_blocks(lines)
    write_txt(out_file, lines)


def read_txt(in_file: str) -> list:
    lines = list()
    with open(in_file, "r", encoding="utf-8") as fp_in:
        for line in fp_in:
            lines.append(line)
    return lines


def convert_to_blocks(lines: list) -> list:
    result = list()

    for line in lines:
        line = " " + line
        line, phone_numbers = insert_placeholders(line, PHONE_REGEX, PHONE_PLACEHOLDER)
        line, abbrevs = insert_placeholders(line, ABBREV_REGEX, ABBREV_PLACEHOLDER)
        line = line[1:]

        tokens = [token for token in nltk.word_tokenize(line, language='german')]

        restore_originals(tokens, phone_numbers, PHONE_PLACEHOLDER)
        restore_originals(tokens, abbrevs, ABBREV_PLACEHOLDER)

        if not tokens:
            tokens = ['']

        result += tokens

    return result


def insert_placeholders(line: str, regex: str, placeholder: str) -> tuple:
    originals = re.findall(regex, line)
    line = re.sub(regex, placeholder, line)

    return line, originals


def restore_originals(tokens: list, originals: list, placeholder: str):
    j = 0
    for i, token in enumerate(tokens):
        if token == placeholder:
            tokens[i] = originals[j]
            j += 1


def write_txt(out_file: str, lines: list):
    with open(out_file, 'w', encoding="utf-8") as file_descriptor:
        for line in lines:
            print(line, file=file_descriptor)


if __name__ == "__main__":
    main()
