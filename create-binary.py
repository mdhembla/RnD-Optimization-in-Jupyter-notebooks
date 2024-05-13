import os
import nbformat
import argparse

def extract_cells(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)

    code_cells = [cell.source.strip() for cell in notebook_content.cells if cell.cell_type == 'code']

    return code_cells

def compile_and_save(cell_content, output_path):
    temp_script_path = 'temp_script.py'
    with open(temp_script_path, 'w', encoding='utf-8') as temp_script:
        temp_script.write(cell_content)

    # os.system(f'pypy3 -c "from py_compile import compile; compile(\'{temp_script_path}\', \'{output_path}\')"')
    os.system(f'python3 -c "from py_compile import compile; compile(\'{temp_script_path}\', \'{output_path}\')"')
    os.remove(temp_script_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the existing compiled binary for a specific cell in a Jupyter notebook.")
    parser.add_argument("--notebook_path", help="Path to the Jupyter notebook")
    parser.add_argument("--output_dir", help="Enter the directory to store the compiled binaries")
    args = parser.parse_args()
    code_cells = extract_cells(args.notebook_path)

    for i, cell_content in enumerate(code_cells):
        output_path = os.path.join(args.output_dir, f'compiled_cell_{i}.pyc')
        compile_and_save(cell_content, output_path)
        print(f"Compiled binary for cell {i} saved at: {output_path}")

    print("Compilation complete.")

# discuss-
#     even pandas not compatible with pypy
#     inter cell dependencies will cause major issue
#     a background script ?? 
#       - bg thread using Ipython, maybe
#       - NBlyzer: entire extension built/else cli for nb events
    