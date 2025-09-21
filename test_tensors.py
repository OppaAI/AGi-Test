import torch
import numpy as np
import time
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import lru_cache, partial
import hashlib
from sympy import primerange
import secrets

def prime_index_shuffle_torch_batch(secretlist, flag=True, batch_size=1000):
    results = []
    for i in range(0, len(secretlist), batch_size):
        batch = secretlist[i:i+batch_size]
        scrambled = prime_index_shuffle_torch(batch, flag)
        results.extend(scrambled)
    return results

def prime_index_shuffle_torch(secretlist: list[bytes], flag: bool = True) -> list[bytes]:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    length = len(secretlist[0])
    batch_size = len(secretlist)
    
    assert all(len(s) == length for s in secretlist), "All secrets must have same length"
    
    secret_tensor = torch.empty((batch_size, length), dtype=torch.uint8, device=device)
    for i, secret in enumerate(secretlist):
        secret_tensor[i] = torch.tensor(list(secret), dtype=torch.uint8, device=device)

    primes = list(primerange(0, length))
    prime_indices = torch.tensor(primes, dtype=torch.long, device=device)
    all_indices = torch.arange(length, device=device)
    non_prime_mask = ~torch.isin(all_indices, prime_indices)
    non_prime_indices = all_indices[non_prime_mask]

    if flag:
        primes_part = secret_tensor[:, prime_indices]
        non_primes_part = secret_tensor[:, non_prime_indices]
        shuffled = torch.cat((primes_part, non_primes_part), dim=1)
        return [bytes(s.cpu().tolist()) for s in shuffled]
    else:
        original = torch.empty_like(secret_tensor)
        prime_len = len(prime_indices)
        original[:, prime_indices] = secret_tensor[:, :prime_len]
        original[:, non_prime_indices] = secret_tensor[:, prime_len:]
        return [bytes(s.cpu().tolist()) for s in original]
    
def prime_index_shuffle_numpy(secret: bytes, flag: bool = True) -> bytes:
    """
    Method 2: Index Shuffle Based on Prime Positions (NumPy Version)
    Scramble / Descramble the secret bytes by shuffling based on prime positions.
    """
    secret_array = np.frombuffer(secret, dtype=np.uint8)
    length = len(secret_array)

    # Get prime and non-prime indices using NumPy
    prime_mask = np.zeros(length, dtype=bool)
    prime_indices = np.fromiter(primerange(0, length), dtype=int)
    prime_mask[prime_indices] = True

    primes = np.where(prime_mask)[0]
    non_primes = np.where(~prime_mask)[0]

    if flag:
        # Scramble: concatenate prime and non-prime indexed bytes
        scrambled = np.concatenate((secret_array[primes], secret_array[non_primes]))
        return scrambled.tobytes()
    else:
        # Descramble: separate the prime and non-prime bytes
        prime_part = secret_array[:len(primes)]
        non_prime_part = secret_array[len(primes):]

        original = np.empty_like(secret_array)
        original[primes] = prime_part
        original[non_primes] = non_prime_part

        return original.tobytes()

def prime_index_shuffle(secret: bytes, flag: bool = True) -> bytes:
    """
        Method 2: Index Shuffle Based on Prime Positions
        Scramble / Descramble the secret bytes by shuffling the characters based on prime positions
        Steps:
            1) Get the prime and non-prime positions.
            2) If scrambling, shuffle the characters based on prime positions.
            3) If descrambling, put the characters back in their original positions.
            4) Join the characters to form the scrambled / descrambled secret.
        """
    prime_set: set = set(primerange(0, len(secret)))
    primes = [i for i in range(len(secret)) if i in prime_set]
    non_primes = [i for i in range(len(secret)) if i not in prime_set]

    if flag:
        return bytes(secret[i] for i in primes + non_primes)
    else:
        prime_part = secret[:len(primes)]
        non_prime_part = secret[len(primes):]
        original = bytearray(len(secret))
        for idx, i in enumerate(primes):
            original[i] = prime_part[idx]
        for idx, i in enumerate(non_primes):
            original[i] = non_prime_part[idx]
        return bytes(original)


# Test example
if __name__ == "__main__":
    secretlist = [secrets.token_bytes(1024) for _ in range(10000)]
    t0 = time.perf_counter()
    scrambled = prime_index_shuffle_torch(secretlist, True)
    descrambled = prime_index_shuffle_torch(scrambled, False)
    t1 = time.perf_counter()
    print(f"Match: {descrambled == secretlist}")
    print(f"🔥Torch Time: {t1 - t0:.6f} seconds")

    t0 = time.perf_counter()
    scrambled = prime_index_shuffle_torch_batch(secretlist, True)
    descrambled = prime_index_shuffle_torch_batch(scrambled, False)
    t1 = time.perf_counter()
    print(f"Match: {descrambled == secretlist}")
    print(f"🔥Torch Batch Time: {t1 - t0:.6f} seconds")

    secret = secrets.token_bytes(1024)*10000
    t0 = time.perf_counter()
    scrambled = prime_index_shuffle_numpy(secret, True)
    descrambled = prime_index_shuffle_numpy(scrambled, False)
    t1 = time.perf_counter()
    print(f"Match: {secret == descrambled}")
    print(f"🐍NumPy Time: {t1 - t0:.6f} seconds")

    t0 = time.perf_counter()
    scrambled = prime_index_shuffle(secret, True)
    descrambled = prime_index_shuffle(scrambled, False)
    t1 = time.perf_counter()
    print(f"Match: {secret == descrambled}")
    print(f"🧠Original method time: {t1 - t0:.6f} seconds")
