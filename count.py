import os


def count_lines_in_py_files(directory):
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    total_lines += sum(1 for line in f)
    return total_lines


repository_path = "./"  # Change this to your repository path
lines_count = count_lines_in_py_files(repository_path)
print(f"Total lines in .py files: {lines_count}")
