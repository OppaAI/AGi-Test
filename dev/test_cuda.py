import torch

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("CUDA version:", torch.version.cuda)
    print("GPU device count:", torch.cuda.device_count())
    print("GPU name:", torch.cuda.get_device_name(0))

    # Simple GPU test: matrix multiplication
    a = torch.rand(10000, 10000, device='cuda')
    b = torch.rand(10000, 10000, device='cuda')
    c = torch.matmul(a, b)
    print("Matrix multiplication done on GPU!")

