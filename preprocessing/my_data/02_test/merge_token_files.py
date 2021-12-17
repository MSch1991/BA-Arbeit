import os
from dataclasses import dataclass

#SOURCE_FOLDER_1 = os.path.join("source", "left")
SOURCE_FOLDER_1 = "/home/melle/Schreibtisch/dev_data_newline/csv_unanno"
#SOURCE_FOLDER_2 = os.path.join("source", "right")
SOURCE_FOLDER_2 = "/home/melle/Schreibtisch/concat/concat_dev"
#TARGET_FOLDER = os.path.join("target", "merge")
TARGET_FOLDER = "/home/melle/Schreibtisch/concat/merge/dev_data"

@dataclass
class Directories:
    source_folder_1: str
    source_folder_2: str
    target_folder: str


def main():
    os.makedirs(TARGET_FOLDER, exist_ok=True)
    directories = Directories(SOURCE_FOLDER_1, SOURCE_FOLDER_2, TARGET_FOLDER)

    file_names = preprocessing(directories)
    processing(file_names, directories)


def preprocessing(directories: Directories) -> list:
    file_names_1 = set(os.listdir(directories.source_folder_1))
    file_names_2 = set(os.listdir(directories.source_folder_2))
    result = file_names_1.intersection(file_names_2)
    print(sorted(list(result)))
    return sorted(list(result))


def processing(file_names: list, directories: Directories) -> None:
    for file_name in file_names:
        process_single_file(file_name, directories)


def process_single_file(file_name: str, directories: Directories):
    lines_path = os.path.join(directories.source_folder_1, file_name)
    entity_lines_path = os.path.join(directories.source_folder_2, file_name)
    result_path = os.path.join(directories.target_folder, file_name)

    lines = read_all_lines(lines_path)

    entity_lines = read_all_lines(entity_lines_path)

    result = transfer_line_breaks(lines, entity_lines)
    

    write_all_lines(result_path, result)


def read_all_lines(path: str) -> list:
    with open(path, 'r', encoding="utf-8") as file_descriptor:
        return [line.strip() for line in file_descriptor]


def transfer_line_breaks(lines: list, entity_lines: list) -> list:
    if len(lines) < len(entity_lines):
        raise ValueError("Lines must be longer than entity lines, since they should contain empty lines.")

    result = list()
    position = 0

    for line in lines:
        if len(line.strip()) == 0:
            result.append(line)
        else:
            ensure_equality(line, entity_lines[position].split("\t")[0])
            result.append(entity_lines[position])
            position += 1

    return result


def ensure_equality(content_left: str, content_right: str) -> None:          
    if content_left != content_right:
        raise ValueError(f"'{content_left}' != '{content_right}'")


def write_all_lines(path: str, lines: list) -> None:
    with open(path, 'w', encoding="utf-8") as file_descriptor:
        for line in lines:
            print(line, file=file_descriptor)


if __name__ == "__main__":
    main()
