import os
from ghidra.app.decompiler import DecompInterface

# Set the path to the output directory
output_directory = "" 

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Initialize the decompiler interface
decompiler = DecompInterface()
decompiler.openProgram(currentProgram)

# Function to extract decompiled code to a file
def extract_decompiled_code(function):
    # Decompile the function
    results = decompiler.decompileFunction(function, 30, monitor)
    if results.decompileCompleted():
        # Get the decompiled code
        decompiled_code = results.getDecompiledFunction().getC()
        
        # Determine the output file path
        function_name = function.getName()
        output_file = os.path.join(output_directory, function_name + ".txt")
        
        # Write the decompiled code to the output file
        with open(output_file, "w") as file:
            file.write(decompiled_code)
        print("Decompiled code extracted for function: " + function_name)
    else:
        print("Decompilation failed for function: " + function.getName())

# Extract decompiled code for all functions
for function in currentProgram.getFunctionManager().getFunctions(True):
    extract_decompiled_code(function)

# Cleanup
decompiler.dispose()
