import nbformat
import ast
import argparse
import importlib.util
import inspect
import sys
from io import StringIO
from contextlib import redirect_stdout
import importlib
import json 

class ImportsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = {}

    def visit_Import(self, node):
        for alias in node.names:
            # Import the module using importlib
            module = importlib.import_module(alias.name)
            self.imports[alias.asname or alias.name] = module  # Store the module reference
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module_name = node.module
        for alias in node.names:
            name = alias.asname or alias.name
            full_name = f"{module_name}.{name}" if module_name else name
            # Import the specific module member
            module_member = importlib.import_module(full_name)
            self.imports[name] = module_member  # Store the member reference
        self.generic_visit(node)


def extract_variables_from_cell(cell_content, symbol_table, cell_num, cell_vars, cell_imports):
    parsed_code = ast.parse(cell_content)
    visitor = ImportsVisitor()
    visitor.visit(parsed_code)
    cell_imports[cell_num] = visitor.imports    
    for node in parsed_code.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    symbol_table[target.id] = None

def execute_cell_function(cell_num, symbol_table, fun_dir, cell_vars, imports):
    print(f'----------exec cell {cell_num}--------\nsymbol table:',symbol_table)
    module_name = f"func_{cell_num}"
    module_path = f"{fun_dir}/func_{cell_num}.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    function_name = f"func_{cell_num}"
    cell_function = getattr(module, function_name)
    parameters = inspect.signature(cell_function).parameters.keys()

    arguments = {
        param: imports.get(param, symbol_table.get(param, None))  # Check imports first, then symbol_table
        for param in parameters
    }

    original_stdout = sys.stdout
    captured_output = StringIO()
    # print(symbol_table['df'])

    try:
        with redirect_stdout(captured_output):
            ret = cell_function(**arguments)
            for i, var in enumerate(cell_vars[str(cell_num+1)]):
                print(var)
                symbol_table[var] = ret[i]

    finally:
        print(captured_output.getvalue())
        sys.stdout = original_stdout
        print(f"Execution of cell {cell_num} completed.")
    



# Load the Jupyter notebook
parser = argparse.ArgumentParser(description="Run the existing compiled binary for a specific cell in a Jupyter notebook.")
parser.add_argument("--notebook_path", help="Path to the Jupyter notebook")
parser.add_argument("--functions_dir", help="dir to functions")
args = parser.parse_args()

with open(args.notebook_path, 'r', encoding='utf-8') as notebook_file:
    notebook_content = nbformat.read(notebook_file, as_version=4)

# Initialize the symbol table
symbol_table = {}
with open(f'{args.functions_dir}/cell_vars.json', 'r') as f:
  cell_vars = json.load(f)

print(cell_vars)
cell_imports = {}
imports = {}
# Extract variables from each code cell
for i, cell in enumerate(notebook_content.cells):
    if cell.cell_type == 'code':
        extract_variables_from_cell(cell.source, symbol_table, i+1, cell_vars, cell_imports)
# print(symbol_table)
# print(cell_vars)

# Run an interactive loop to execute cells dynamically
while True:
    command = input("Enter command (e.g., 'exec 1', 'exit'): ")

    if command.startswith('exec'):
        cell_num = int(command[5:])
        
        if cell_num in range(1, len(notebook_content.cells)):
            execute_cell_function(cell_num, symbol_table, args.functions_dir, cell_vars, imports)
            imports.update(cell_imports[cell_num + 1])
            print(imports)
        else:
            print(f"Cell {cell_num} does not exist.")
    
    elif command == 'exit':
        break
    else:
        print("Invalid command. Please enter 'exec 1', 'exec 2', ..., or 'exit'.")
