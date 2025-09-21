# PyTorch test
import torch, torchvision, torchaudio
print("CUDA available:", torch.cuda.is_available())
print("CUDA device count:", torch.cuda.device_count())
print()

#print software versions
print("PyTorch version:", torch.__version__)
print("PyTorch vision version:", torchvision.__version__)
print("PyTorch audio version:", torchaudio.__version__)
print("PyTorch CUDA version:", torch.version.cuda)
print("PyTorch cuDNN version:", torch.backends.cudnn.version())

print()

#print hardware versions
print("GPU name:", torch.cuda.get_device_name(0))
print("GPU count:", torch.cuda.device_count())
print("GPU capability:", torch.cuda.get_device_capability(0))
print("GPU total memory:", torch.cuda.get_device_properties(0).total_memory)
print("GPU multi processor count:", torch.cuda.get_device_properties(0).multi_processor_count)
