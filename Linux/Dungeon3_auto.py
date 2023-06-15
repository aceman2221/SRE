from pwn import *
import angr

# Set up pwntools for the correct architecture
exe = './dungeon3'
print("Running checksec")
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=True)

# Set up state with symbolic input
proj = angr.Project(exe)
state = proj.factory.entry_state(stdin=angr.SimFile)

# Explore the binary using angr
sm = proj.factory.simulation_manager(state)
sm.explore(find=elf.symbols.vault)

# Retrieve the successful path
found = sm.found[0]
input_payload = found.posix.stdin.load(0)
input_payload_str = input_payload.decode().strip()

print("Payload found:", input_payload_str)

# Send the payload
p = process(exe)
p.recvline()
print("Sending Payload")
print("Payload:", input_payload_str.encode())
p.sendline(input_payload_str.encode())
result = p.recv()
print("Result:", result.decode())
