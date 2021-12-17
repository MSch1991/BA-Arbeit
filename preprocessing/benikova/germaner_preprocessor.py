import os
import sys

import re


def main():
    conll_directory = sys.argv[1]
    prefix = sys.argv[2]

    for data_set in ("dev", "test", "train"):
        normalize_file(conll_directory, prefix, data_set)

    print("Done")


def normalize_file(conll_directory: str, prefix: str, data_set: str):
    input_file = os.path.join(conll_directory, f"{prefix}_{data_set}.conll")
    output_file = os.path.join(conll_directory, f"{prefix}_{data_set}.conll")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    separator = "\t"

    print("Loading from:", input_file)
    print("Writing to:", output_file)

    with open(input_file, 'r', encoding="utf-8") as in_file_descriptor:
        with open(output_file, 'w', encoding="utf-8") as out_file_descriptor:
            for line in in_file_descriptor:
                line = line.strip()
                if separator in line:
                    content, label = line.split(separator)

                    if label.endswith("OTH"):
                        label = "O"
                    elif label.endswith("part"):
                        label = label.replace("part", "")
                    elif label.endswith("deriv"):
                        label = label.replace("deriv", "")

                    line = f"{content}\t{label}"

                print(line, file=out_file_descriptor)


if __name__ == "__main__":
    main()
