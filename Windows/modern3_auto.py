import subprocess
import time
import os
import re

# Path to the modern3.exe program
program_path = "modern3.exe"

# Generic input to be provided to the program
generic_input = "Hello, World!"

# Directory path to search for files
directory_path = r"C:\Users\reverser\Desktop\modern3\extracted_functions"

# Search string
search_string = r"\bWhat\b"  # Use regular expression with word boundaries


try:
    # Execute the program
    process = subprocess.Popen(program_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Send the generic input to the program
    process.stdin.write(generic_input.encode())
    process.stdin.flush()

    # Wait for the program to finish
    process.wait()

    # Retrieve the program's output
    output = process.stdout.read().decode()

    # Display the output
    print("Program output:")
    print(output)

    # Search for the string in files after program execution
    def search_and_print_content(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            if re.search(search_string, content):
                print("Found the what's your name? string. Printing the content")
                print("File:", file_path)
                print("Content:")
                print(content)
                print("Found a reference to FUN_004015cb")
                print("----------")

                # Print the content of FUN_004015cb function
                function_path = r"C:\Users\reverser\Desktop\modern3\extracted_functions\FUN_004015cb.txt" 
                try:
                    with open(function_path, "r") as function_file:
                        function_content = function_file.read()
                        print("Content of FUN_004015cb function:")
                        print(function_content)
                        print("----------")
                        print("Found an input buffer of 40. Z seems to increment a counter")
                        
                except FileNotFoundError:
                    print(f"File '{function_path}' not found.")

                # Open the files with Notepad
                try:
                    print("Opening the functions with notepad , windows may spawn on top of each other.")
                    time.sleep(3)
                    subprocess.Popen(["notepad.exe", file_path])
                except OSError:
                    print("Failed to open file with Notepad.")
                
                try:
                    subprocess.Popen(["notepad.exe", function_path])
                except OSError:
                    print("Failed to open function file with Notepad.")

    # Iterate over files in the directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            search_and_print_content(file_path)

    # Run the program again with a payload of 39 "a's" + "z"
    print("Testing for an overflow by sending 39 a's with a z at the end")
    payload = "a" * 39 + "z"
    process = subprocess.Popen(program_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.stdin.write(payload.encode())
    process.stdin.flush()

    # Wait for the program to finish
    process.wait()

    # Retrieve the program's output
    output = process.stdout.read().decode()

    # Display the output
    print("Program output after sending payload:")
    print(output)

except FileNotFoundError:
    print("Error: Program not found at the specified path.")


