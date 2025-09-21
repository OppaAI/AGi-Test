import torch
from torchvision.models import resnet18, ResNet18_Weights
from torch2trt import torch2trt
import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

weights = ResNet18_Weights.DEFAULT
model = resnet18(weights=weights).eval().to(device)

# Function to benchmark standard PyTorch and TensorRT
def benchmark_batch(batch_size, max_memory_mb=800):
    example_input = torch.randn(batch_size, 3, 224, 224).to(device)
    
    # --- Standard PyTorch GPU ---
    torch.cuda.reset_peak_memory_stats()
    start = time.time()
    with torch.no_grad():
        for _ in range(10):  # run multiple times for more stable measurement
            model(example_input)
            torch.cuda.synchronize()
    pytorch_time = (time.time() - start) / 10
    pytorch_mem = torch.cuda.max_memory_allocated() / 1024**2

    # --- TensorRT ---
    try:
        torch.cuda.reset_peak_memory_stats()
        model_trt = torch2trt(model, [example_input], fp16_mode=False)
        torch.cuda.synchronize()
        start = time.time()
        with torch.no_grad():
            for _ in range(10):
                model_trt(example_input)
                torch.cuda.synchronize()
        trt_time = (time.time() - start) / 10
        trt_mem = torch.cuda.max_memory_allocated() / 1024**2
    except RuntimeError as e:
        print(f"Batch {batch_size}: OOM or error -> {e}")
        return None

    print(f"Batch {batch_size}: PyTorch {pytorch_time*1000:.2f} ms, "
          f"TensorRT {trt_time*1000:.2f} ms | "
          f"Mem PyTorch {pytorch_mem:.2f} MB, TRT {trt_mem:.2f} MB")

    if pytorch_mem > max_memory_mb or trt_mem > max_memory_mb:
        return False
    return True

# Try increasing batch sizes
batch_size = 1
while True:
    ok = benchmark_batch(batch_size)
    if not ok:
        print(f"Optimal batch size ≈ {batch_size-1}")
        break
    batch_size += 1
