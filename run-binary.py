import os
import argparse

def run_existing_binary(notebook_directory, cell_number):
    compiled_binary_path = f'{notebook_directory}/binaries/compiled_cell_{cell_number}.pyc'

    if os.path.exists(compiled_binary_path):
        # os.system(f'pypy3 {compiled_binary_path}')
        os.system(f'python3 -W ignore {compiled_binary_path}')
        print(f"Successfully ran the compiled binary for cell {cell_number}.")
    else:
        print(f"Compiled binary for cell {cell_number} not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the existing compiled binary for a specific cell in a Jupyter notebook.")
    parser.add_argument("--notebook_dir", help="Path to the Jupyter notebook")
    parser.add_argument("--cell_number", type=int, help="Cell number to run")

    args = parser.parse_args()

    run_existing_binary(args.notebook_dir, args.cell_number)
