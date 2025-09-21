import torch
import time

# Choose device: GPU if available, otherwise CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Matrix size
N = 4096  # smaller than 10k to avoid memory issues on Jetson

# Create random tensors
a = torch.rand((N, N), device=device)
b = torch.rand((N, N), device=device)

# Warm-up GPU (important for CUDA timing)
if device == "cuda":
    for _ in range(5):
        torch.matmul(a, b)

# Time matrix multiplication
start_time = time.time()
c = torch.matmul(a, b)
if device == "cuda":
    torch.cuda.synchronize()  # make sure GPU finishes
end_time = time.time()

print(f"Matrix multiplication {N}x{N} done in {end_time - start_time:.4f} seconds")

