import os
import shutil
import tempfile
from pathlib import Path

# Create a temporary directory for these operations to keep things clean
temp_dir_for_fs = Path(tempfile.mkdtemp(prefix="std_lib_mastery_"))
print(f"Created temporary directory: {temp_dir_for_fs}")

# --- Read a File with pathlib ---
my_file_path = temp_dir_for_fs / "myfile.txt"
my_file_path.write_text("Hello from pathlib!\nSecond line.")
file_content = my_file_path.read_text()
print(f"\nRead a File with pathlib (content of {my_file_path.name}):\n{file_content}")

# --- List Files in a Directory ---
(temp_dir_for_fs / "script1.py").touch()
(temp_dir_for_fs / "script2.py").touch()
(temp_dir_for_fs / "another_file.txt").touch()

print("\nList Files in a Directory (Python files in temp dir):")
python_files = list(temp_dir_for_fs.glob("*.py"))
for py_file in python_files:
    print(py_file.name)

# --- Write to a File (using pathlib was shown above, here's with open) ---
output_file_path = temp_dir_for_fs / "output.txt"
with open(output_file_path, "w") as f:
    f.write("Hello from open()!")
print(f"\nWrite to a File: Created {output_file_path.name} with content: '{output_file_path.read_text()}'")

# --- Create and Delete File/Directory ---
# Create directory
new_dir_path = temp_dir_for_fs / "my_new_directory"
os.makedirs(new_dir_path, exist_ok=True) # exist_ok=True prevents error if it already exists
print(f"\nCreate Directory: Created {new_dir_path}")
print(f"Does new directory exist? {new_dir_path.exists() and new_dir_path.is_dir()}")

# Create a file inside it
file_in_new_dir = new_dir_path / "temp.data"
file_in_new_dir.write_text("some data")
print(f"Created file {file_in_new_dir.name} in new directory.")

# Delete directory and its contents
shutil.rmtree(new_dir_path)
print(f"Delete Directory: Deleted {new_dir_path}")
print(f"Does new directory exist after deletion? {new_dir_path.exists()}")

# --- Temp File Usage ---
print("\nTemp File Usage:")
with tempfile.NamedTemporaryFile(mode="w+", delete=False, dir=temp_dir_for_fs, suffix=".tmp", prefix="app_") as tmp_file:
    tmp_file_name = tmp_file.name
    tmp_file.write("This is some temporary data.")
    tmp_file.seek(0) # Go to the beginning to read
    print(f"NamedTemporaryFile created at: {tmp_file_name}")
    print(f"Content of temporary file: '{tmp_file.read()}'")
# The file is not deleted on close because delete=False. We'll clean it up with the temp_dir.
print(f"Does temp file {Path(tmp_file_name).name} exist after close? {Path(tmp_file_name).exists()}")


# --- Copy Files with shutil ---
source_file_for_copy = temp_dir_for_fs / "source.txt"
source_file_for_copy.write_text("Content to be copied.")
destination_file_for_copy = temp_dir_for_fs / "destination.txt"
shutil.copy(source_file_for_copy, destination_file_for_copy)
print("\nCopy Files with shutil:")
print(f"Copied '{source_file_for_copy.name}' to '{destination_file_for_copy.name}'")
print(f"Content of destination file: '{destination_file_for_copy.read_text()}'")
print(f"Does destination file exist? {destination_file_for_copy.exists()}")

# --- Absolute vs Relative Paths ---
relative_path = Path("myfile.txt") # Relative to current working directory
# For this example, let's consider it relative to our temp_dir_for_fs
path_in_temp = temp_dir_for_fs / "example.txt"
path_in_temp.touch()

print("\nAbsolute vs Relative Paths:")
print(f"Path object (potentially relative): {path_in_temp.name} inside {temp_dir_for_fs.name}")
print(f"Resolved (absolute) path: {path_in_temp.resolve()}")

# --- Check File Existence ---
existing_file = temp_dir_for_fs / "myfile.txt" # We created this earlier
non_existing_file = temp_dir_for_fs / "ghost.txt"
a_directory = temp_dir_for_fs

print("\nCheck File Existence:")
print(f"Does '{existing_file.name}' exist? {existing_file.exists()}")
print(f"Is '{existing_file.name}' a file? {existing_file.is_file()}")
print(f"Is '{existing_file.name}' a directory? {existing_file.is_dir()}")

print(f"Does '{non_existing_file.name}' exist? {non_existing_file.exists()}")

print(f"Does '{a_directory.name}' exist? {a_directory.exists()}")
print(f"Is '{a_directory.name}' a file? {a_directory.is_file()}")
print(f"Is '{a_directory.name}' a directory? {a_directory.is_dir()}")


# --- Clean up the temporary directory ---
try:
    shutil.rmtree(temp_dir_for_fs)
    print(f"\nCleaned up temporary directory: {temp_dir_for_fs}")
except Exception as e:
    print(f"Error cleaning up temp directory {temp_dir_for_fs}: {e}")