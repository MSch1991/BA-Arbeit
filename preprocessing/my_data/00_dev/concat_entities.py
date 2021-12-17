import os
import sys

CATEGORIES = ("loc", "org", "per")


def utf_open(file_name: str):
    return open(file_name, 'r', encoding="utf-8")


class ParallelOpen:
    def __init__(self, loc_file: str, org_file: str, per_file: str):
        self._loc_file = loc_file
        self._org_file = org_file
        self._per_file = per_file

        self._loc_file_descriptor = None
        self._org_file_descriptor = None
        self._per_file_descriptor = None

    def __enter__(self):
        self._loc_file_descriptor = utf_open(self._loc_file)
        self._org_file_descriptor = utf_open(self._org_file)
        self._per_file_descriptor = utf_open(self._per_file)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._loc_file_descriptor.close()
        self._org_file_descriptor.close()
        self._per_file_descriptor.close()

    def __iter__(self):
        return self

    def __next__(self):
        result = (self._loc_file_descriptor, self._org_file_descriptor, self._per_file_descriptor)
        result = map(next, result)
        result = map(str.strip, result)

        result = tuple(result)
        if len(result) == 0:
            raise StopIteration

        return result


def main():
    source_dir = sys.argv[1]
    target_dir = sys.argv[2]

    os.makedirs(target_dir, exist_ok=True)
    for file in os.listdir(target_dir):
        os.remove(os.path.join(target_dir, file))
    indices = find_all_indices(source_dir)

    for index in indices:
        files = [os.path.join(source_dir, category, f"{category}_data_{index}.txt") for category in CATEGORIES]
        with ParallelOpen(*files) as source_files:
            result_lines, error_count = analyze_lines(index, source_files)

            if error_count > 0:
                print(f"Too much errors ({error_count}) in file {index}. Skip ...\n")
                continue

        with open(os.path.join(target_dir, f"data_{index}.txt"), 'w', encoding="utf-8") as file_descriptor:
            for line in result_lines:
                print(line, file=file_descriptor)


def find_all_indices(source_directory: str) -> list:
    def extract_index(file_name: str) -> int:
        index_with_extension = file_name.split('_')[-1]
        index = index_with_extension.split('.')[0]
        return int(index)

    directories = {category: os.path.join(source_directory, category) for category in CATEGORIES}
    files = {category: os.listdir(directories[category]) for category in CATEGORIES}
    indices = [set(map(extract_index, value)) for key, value in files.items()]
    indices = set.intersection(*indices)

    return sorted(list(indices))


def analyze_lines(index: int, source_files) -> tuple:
    error_count = 0
    result_lines = list()

    for i, lines in enumerate(source_files):
        words, entity = zip(*map(lambda s: s.split('\t'), lines))
        unique_words = set(words)

        if len(unique_words) != 1:
            print(f"Error in file: {index} at line {i}: Words do not align, {words}")
            error_count += 1
            break

        o_count = entity.count('O')
        if o_count < 2:
            print(f"Error in file: {index} at line {i}: Entity do not align, {entity}")
            error_count += 1
            continue
        elif o_count == 2:
            entity = [e for e in entity if e != 'O'][0]
        else:
            entity = 'O'

        result_lines.append(f"{tuple(unique_words)[0]}\t{entity}")

    return result_lines, error_count


if __name__ == "__main__":
    main()
