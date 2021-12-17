import os
import sys

SEPARATOR = "\t"


def main():
    corpora_path = sys.argv[1]
    file_name = sys.argv[2]

    annotations = ("LOC", "ORG", "PER")
    for annotation in annotations:
        exclude_annotations = set(annotations).difference({annotation})
        extract_one_entity(
            corpora_path=corpora_path,
            file_name=file_name,
            include_annotation=annotation,
            exclude_annotation=exclude_annotations
        )

    print("Done")


def extract_one_entity(corpora_path: str, file_name: str, include_annotation: str, exclude_annotation: set):
    input_file = os.path.join(corpora_path, f"{file_name}.conll")
    output_file = os.path.join(corpora_path, f"{file_name}_{include_annotation}.conll")

    print("Loading from:", input_file)
    print("Writing to:", output_file)

    with open(input_file, 'r', encoding="utf-8") as in_file_descriptor:
        with open(output_file, 'w', encoding="utf-8") as out_file_descriptor:
            for line in in_file_descriptor:
                line = line.strip()
                if SEPARATOR in line:
                    content, label = line.split(SEPARATOR)

                    for exclude in exclude_annotation:
                        if exclude in label:
                            label = "O"
                            break

                    line = f"{content}\t{label}"

                print(line, file=out_file_descriptor)


if __name__ == "__main__":
    main()
