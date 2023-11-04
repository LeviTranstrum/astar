import os

# Check current working directory
print("Current working directory:", os.getcwd())

# Check if the file exists
file_path = 'a_star\test.py'
print("Does the file exist?", os.path.exists(file_path))
