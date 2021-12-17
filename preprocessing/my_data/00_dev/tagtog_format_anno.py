import os
import re
import sys

import nltk

PHONE_REGEX = r"\+\d{2}\s?(?:\(\d+\))?\s?\d+-?\s?\d+-?\d+"
PHONE_PLACEHOLDER = "PHONENUMBERPLACEHOLDERPYTHON"
ABBREVIATIONS = ["Tel.", "str.", "staatl.", "gepr.", "ggfs.", "z.b.",
                 "nr.", "2.", "1.", "bzw.", "prof.", "dr.", "med.", "sog.",
                 "inc.", "inkl.", "ca.", "3.", "ggf.", "mio.", "zzgl.",
                 "div.", "04.", "11.", "mrd.", "etc.", "v.", "7.", "co.",
                 "u.a.", "z.B.", "Str.", "Nr.", "Prof.", "Dr.", "Med.",
                 "Mio.", "Mrd.", "insb.", "21.", "31.", "J.", "30.",
                 "Abs.", "H.", "usw.", "h.", "u.v.m.", "4.", "Co.", "a.",
                 "A.", "S.", "d.h.", "St.", "15.", "T.", "e.V.", "vgl.",
                 "Std.", "z.T.", "evtl."]

ABBREVIATIONS = [entry.replace(".", "\\.") for entry in ABBREVIATIONS]
ABBREV_PLACEHOLDER = " ABBREVPLACEHOLDER "


def main():
    source_dir = sys.argv[1]
    target_dir = sys.argv[2]

    files = [file_name for file_name in os.listdir(source_dir) if file_name.endswith("tsv")]
    for file in files:
        generate_os_file(file, source_dir, target_dir)


def generate_os_file(file, source_dir, target_dir):
    if source_dir == target_dir:
        return ValueError("Source and Target directory can't be the same")

    os.makedirs(target_dir, exist_ok=True)

    in_file = os.path.join(source_dir, file)
    out_file = os.path.join(target_dir, file)

    tsv_file = read_tsv(in_file)
    normalized_tsv = normalize_tsv(tsv_file)
    write_tsv(out_file, normalized_tsv)


def read_tsv(in_file):
    lines = list()
    with open(in_file, 'r', encoding="utf-8") as fp:
        for i, line in enumerate(fp):
            lines.append(line)
        if lines[0].startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0")):
            lines.pop(0)

    return lines


def normalize_tsv(tsv_file):
    blocks = group_blocks(tsv_file)

    result_blocks = list()

    for block in blocks:
        if len(block) == 1:
            block = block[0], 'O'

        phone_numbers = re.findall(PHONE_REGEX, block[0])
        block = re.sub(PHONE_REGEX, PHONE_PLACEHOLDER, block[0]), block[1]
        abbrevs = re.findall(r"(?<=\W)(" + '|'.join(ABBREVIATIONS) + r")(?=\W)", block[0])
        block = re.sub(r"(?<=\W)(" + '|'.join(ABBREVIATIONS) + r")(?=\W)", ABBREV_PLACEHOLDER, block[0]), block[1]

        new_blocks = process_block(block)

        j = 0
        for i, (content, identifier) in enumerate(new_blocks):
            if PHONE_PLACEHOLDER in content:
                new_blocks[i] = phone_numbers[j], identifier
                j += 1

        j = 0
        for i, (content, identifier) in enumerate(new_blocks):
            if ABBREV_PLACEHOLDER.strip() in content:
                new_blocks[i] = abbrevs[j], identifier
                j += 1

        result_blocks.extend(new_blocks)

    return convert_blocks_to_tsv(result_blocks)


def group_blocks(tsv_file) -> list:
    blocks = list()
    buffer = ""
    for line in tsv_file:
        buffer += line
        if "\t" in line:
            blocks.append(buffer)
            buffer = ""

    if buffer != "":
        blocks.append(buffer)

    return [block.split('\t') for block in blocks]


def process_block(block: tuple) -> list:
    content, indicator = block

    return [(token, indicator) for token in nltk.word_tokenize(content, language='german')]


def convert_blocks_to_tsv(blocks):
    return [f"{content}\t{indicator}" for content, indicator in blocks]


def write_tsv(out_file, normalized_tsv):
    with open(out_file, 'w', encoding="utf-8") as fp:
        for line in normalized_tsv:
            print(line, file=fp, end="")


if __name__ == "__main__":
    main()
