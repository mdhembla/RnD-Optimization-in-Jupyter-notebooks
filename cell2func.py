import os
import nbformat
import argparse
import ast
import textwrap
import builtins
import json

##IMP:
# keywords
# import module stmts are executed before!?
# class defs!!
# indentation

def extract_variables_from_cell(cell_content, cell_num, cell_vars):
    parsed_code = ast.parse(cell_content)
    cell_vars[cell_num] = set()
    for node in parsed_code.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    cell_vars[cell_num].add(target.id)

        if isinstance(node, ast.FunctionDef):
            cell_vars[cell_num].add(node.name)
    cell_vars[cell_num] = list(cell_vars[cell_num])

def extract_cells(notebook_path, cell_vars):
    with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)

    code_cells = [cell.source.strip() for cell in notebook_content.cells if cell.cell_type == 'code']
    
    for i, cell in enumerate(notebook_content.cells):
        if cell.cell_type == 'code':
            extract_variables_from_cell(cell.source, i+1, cell_vars)

    return code_cells

class FreeVariableVisitor(ast.NodeVisitor):
    def __init__(self):
        self.defined_variables = set()
        self.free_variables = set()
        self.current_function_params = set()


    def visit_Assign(self, node):
        # Only add variables on the LHS to the defined set
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined_variables.add(target.id)

        # Process the RHS separately to identify free variables
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.defined_variables.add(alias.asname if alias.asname else alias.name.split('.')[-1])
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        # Add function name to defined variables
        self.defined_variables.add(node.name)
        self.current_function_params.update(param.arg for param in node.args.args)

        self.generic_visit(node)
        self.current_function_params.clear()

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            self.defined_variables.add(f"{module}.{alias.asname if alias.asname else alias.name}")
        self.generic_visit(node)

    def visit_For(self, node):
        # Exclude variables defined within for loops
        if isinstance(node.target, ast.Name):
            self.defined_variables.add(node.target.id)
        elif isinstance(node.target, ast.Tuple):
            for target in node.target.elts:
                if isinstance(target, ast.Name):
                    self.defined_variables.add(target.id)

        self.generic_visit(node)

    def visit_While(self, node):
        # Exclude variables defined within while loops
        self.generic_visit(node)

    def visit_Name(self, node):
        # Check if the variable is used before being defined
        if node.id not in self.defined_variables and node.id not in self.current_function_params:
            self.free_variables.add(node.id)
        self.generic_visit(node)

    def visit_Subscript(self, node):
        # Check if the subscript target is a Name
        if isinstance(node.value, ast.Name):
            if node.value.id not in self.defined_variables and node.value.id not in self.current_function_params:
                self.free_variables.add(node.value.id)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Check if the attribute value is a Name
        if isinstance(node.value, ast.Name):
            if node.value.id not in self.defined_variables and node.value.id not in self.current_function_params:
                self.free_variables.add(node.value.id)
        self.generic_visit(node)

def find_free_vars_inner(tree):
    visitor = FreeVariableVisitor()
    visitor.visit(tree)
    # print(visitor.free_variables)
    builtin_function_names = set(dir(builtins))
    return visitor.free_variables - builtin_function_names


def save_func(cell_content, output_path, cell_num):
    # Parse the input code into an AST
    parsed_code = ast.parse(cell_content)
    if cell_num==0:
        pass
    else:
    # Extract free variables from the entire parsed code
        free_variables = find_free_vars_inner(parsed_code)
        print(free_variables)
        # Save the code to the specified output path
        with open(output_path, "w") as file:
            func_header = f"def func_{cell_num}(" + ', '.join(free_variables) + '):\n'
            func_body = textwrap.dedent(cell_content)
            func_return = '    return ' +  ','.join(cell_vars[cell_num+1])
            func = func_header + textwrap.indent(func_body, '    ') + '\n'+func_return
            # indented_code = textwrap.indent(func, '\t')
            file.write(func)

        file.close()
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the existing compiled binary for a specific cell in a Jupyter notebook.")
    parser.add_argument("--notebook_path", help="Path to the Jupyter notebook")
    parser.add_argument("--output_dir", help="Enter the directory to store the compiled binaries")
    args = parser.parse_args()
    cell_vars = {}
    code_cells = extract_cells(args.notebook_path, cell_vars)
    print(cell_vars)
    for i, cell_content in enumerate(code_cells):
        output_path = os.path.join(args.output_dir, f'func_{i}.py')
        save_func(cell_content, output_path, i)

    with open(f'{args.output_dir}/cell_vars.json', 'w') as f:
        json.dump(cell_vars, f)
    print("Conversion complete.")

    