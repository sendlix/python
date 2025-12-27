if not exist ./src/sendlix/proto (
    mkdir ./src/sendlix/proto
)

python -m grpc_tools.protoc -I./proto --python_out=./src/sendlix/proto --grpc_python_out=./src/sendlix/proto ./proto/*.proto

python fix_imports.py
