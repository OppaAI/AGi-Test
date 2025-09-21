import secrets, time
import numpy as np
import torch, math
from concurrent.futures import ThreadPoolExecutor

def scramble_bytes_simple(secret: bytes) -> bytes:
    # 將 secret 切成每 2 bytes 一組，然後反轉整個 list，再 join
    return b"".join([secret[i:i+2] for i in range(0, len(secret), 2)][::-1])

# descramble = scramble_bytes_simple (apply twice returns original)

def scramble_bytearray_inplace(buf: bytearray, chunk_size: int = 2) -> bytearray:
    """
    In-place swap chunks: chunk 0 <-> chunk n-1, chunk 1 <-> chunk n-2, ...
    If length is not a multiple of chunk_size, the final chunk stays as a single-length chunk (keeps position within chunk scheme).
    Returns the same bytearray object.
    """
    n = len(buf)
    chunks = (n + chunk_size - 1) // chunk_size
    for i in range(chunks // 2):
        a = i * chunk_size
        b = (chunks - 1 - i) * chunk_size
        # swap chunk at a (a:a+chunk_size) with chunk at b (b:b+chunk_size)
        # handle edges when remaining length < chunk_size
        a_slice = buf[a:a+chunk_size]    # view -> creates new bytearray but small
        b_slice = buf[b:b+chunk_size]
        buf[a:a+chunk_size] = b_slice
        buf[b:b+chunk_size] = a_slice
    return buf

# descramble_bytearray_inplace = scramble_bytearray_inplace (idempotent when applied twice)

def scramble_numpy(secret: bytes) -> bytes:
    arr = np.frombuffer(secret, dtype=np.uint8)
    pad_len = len(arr) % 2
    if pad_len:  # 如果長度係奇數，pad 一個 0 byte
        arr = np.concatenate([arr, np.zeros(1, dtype=np.uint8)])
    # reshape -> reverse chunk order -> flatten -> remove padding
    return bytes(arr.reshape(-1, 2)[::-1].reshape(-1)[:len(secret)])
def xor_numpy_parallel(data: bytes, key: bytes, num_workers=4, chunk_size=None) -> bytes:
    if not key: raise ValueError("Key must not be empty")
    data_len = len(data)
    if chunk_size is None: chunk_size = -(-data_len // num_workers)
    with ThreadPoolExecutor(max_workers=num_workers) as ex:
        return b"".join(ex.map(lambda s: (lambda a: (a ^ np.frombuffer(key * -(-len(a) // len(key)), np.uint8)[:len(a)]).tobytes())(np.frombuffer(data[s:min(s+chunk_size, data_len)], np.uint8)), range(0, data_len, chunk_size)))

def xor_gpu_fast(data: bytes, key: bytes, chunk_size: int = None) -> bytes:
    if not key:
        raise ValueError("Key must not be empty")
    data_len = len(data)
    key_len = len(key)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if chunk_size is None:
        chunk_size = data_len

    output = bytearray(data_len)
    key_tensor = torch.tensor(list(key), dtype=torch.uint8, device=device)

    data_writable = bytearray(data)  # <-- 這裏改動
    data_tensor_cpu = torch.frombuffer(data_writable, dtype=torch.uint8)

    for start in range(0, data_len, chunk_size):
        end = min(start + chunk_size, data_len)
        chunk_len = end - start

        chunk = data_tensor_cpu[start:end].to(device)

        reps = math.ceil(chunk_len / key_len)
        krep = key_tensor.repeat(reps)[:chunk_len]

        result = torch.bitwise_xor(chunk, krep)
        output[start:end] = result.cpu().numpy().tobytes()

    return bytes(output)

def reverse_triplets_simple(secret: bytes, flag=False) -> bytes:
    pos = len(secret) % 3
    fill = (3 - pos) % 3 if not flag else 0
    padded = secret[:pos] + (b" " * fill if fill else b"") + secret[pos:] if not flag else secret
    chunks = [padded[i:i+3] for i in range(0, len(padded), 3)]
    if not flag:
        chunks[0] = chunks[0][:3 - fill]
    return b"".join(chunks[::-1])

def reverse_triplets(secret: bytes, flag=False) -> bytes:
    arr = np.frombuffer(secret, dtype=np.uint8)
    fill = 0
    pos = 0

    if not flag:
        pos = len(arr) % 3
        fill = (3 - pos) % 3
        if fill:
            arr = np.concatenate((arr[:pos], np.full(fill, 32, np.uint8), arr[pos:]))

    # Pad tail to multiple of 3 if needed
    pad_len = (-len(arr)) % 3
    if pad_len:
        arr = np.pad(arr, (0, pad_len), constant_values=32)

    arr = arr.reshape(-1, 3)[::-1].ravel()

    if not flag and fill:
        arr = np.delete(arr, pos + np.arange(fill))

    return arr[:len(secret)].tobytes()

# 假設上面嘅函數都已定義

def example():
    # Create 1 GB test data (pattern repeat for speed)
    test_data = secrets.token_bytes(1024)*1024
    key = b"mysecretkey"

    # Warm-up GPU
    if torch.cuda.is_available():
        _ = torch.tensor([1], device="cuda")
    print(torch.cuda.is_available(), "CUDA is available")

    _ = xor_numpy_parallel(test_data, key)
    _ = xor_gpu_fast(test_data, key)

    # Simple XOR test
    start_time = time.perf_counter()
    sn = scramble_numpy(test_data)
    rn = scramble_numpy(sn)
    elapsed_simple = time.perf_counter() - start_time
    assert rn == test_data, "Mismatch between CPU and GPU results!"
    print(f"Simple XOR completed in {elapsed_simple:.6f} seconds")

    # NumPy CPU test
    start_time = time.perf_counter()
    sn = xor_numpy_parallel(test_data, key)
    rn = xor_numpy_parallel(sn, key)
    elapsed_cpu = time.perf_counter() - start_time
    assert rn == test_data, "Mismatch between CPU and GPU results!"
    print(f"NumPy CPU XOR completed in {elapsed_cpu:.6f} seconds")

    # PyTorch GPU test
    start_time = time.perf_counter()
    sn = xor_gpu_fast(test_data, key, chunk_size=len(test_data) // 64)
    rn = xor_gpu_fast(sn, key, chunk_size=len(sn) // 64)
    elapsed_gpu = time.perf_counter() - start_time
    assert rn == test_data, "Mismatch between CPU and GPU results!"
    print(f"PyTorch GPU XOR completed in {elapsed_gpu:.6f} seconds")

    # Simple Triplet shuffle test
    start_time = time.perf_counter()
    sn = reverse_triplets_simple(test_data, True)
    elapsed_triplet = time.perf_counter() - start_time
    print(f"Simple Triplet shuffle completed in {elapsed_triplet:.6f} seconds")

    # Triplet shuffle test
    start_time = time.perf_counter()
    sn = reverse_triplets(test_data, True)
    elapsed_triplet = time.perf_counter() - start_time
    print(f"Triplet shuffle completed in {elapsed_triplet:.6f} seconds")

    # Print
    print("Times -> Numpy: ", elapsed_cpu, "\nTimes -> PyTorch GPU: ", elapsed_gpu)
    methods = {"numpy": elapsed_cpu, "pytorch_gpu": elapsed_gpu}
    fastest = min(methods, key=methods.get)
    print(f"\033[92mFastest: {fastest} ({methods[fastest]:.6f} seconds by percentage: {100 * (1-methods[fastest] / max(methods.values())):.2f}%)\033[0m")


if __name__ == "__main__":
    example()