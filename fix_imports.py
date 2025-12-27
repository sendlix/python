import os
import re
import sys


def fix_imports(directory):
    print(f"Fixing imports in {directory}...")
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix: import x_pb2 as y -> from . import x_pb2 as y
            # This handles the imports in *_grpc.py files
            content_new = re.sub(
                r'^import (\w+_pb2) as', r'from . import \1 as', content, flags=re.MULTILINE)

            # Fix: import x_pb2 -> from . import x_pb2
            # This handles dependencies between *_pb2.py files
            # We look for "import x_pb2" at start of line, ensuring it's not part of a "from" import
            content_new = re.sub(r'^import (\w+_pb2)(?!\s+as)',
                                 r'from . import \1', content_new, flags=re.MULTILINE)

            if content != content_new:
                print(f"  Patched {filename}")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content_new)


if __name__ == "__main__":
    target_dir = "src/sendlix/proto"
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]

    if os.path.exists(target_dir):
        fix_imports(target_dir)
    else:
        print(f"Directory {target_dir} does not exist.")
