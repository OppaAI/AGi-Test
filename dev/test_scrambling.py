import time
import numpy as np
from sympy import primerange
from secrets import token_bytes

# Cache for prime masks
_prime_mask_cache = {}

def get_prime_mask_cached(n: int) -> np.ndarray:
    """Return cached prime mask for length n."""
    if n not in _prime_mask_cache:
        primes = np.fromiter(primerange(0, n), int)
        mask = np.zeros(n, dtype=bool)
        mask[primes] = True
        _prime_mask_cache[n] = mask
    return _prime_mask_cache[n]

def prime_index_shuffle(secret: bytes, flag: bool = True) -> bytes:
    """
    Method 2: Prime Index Shuffle (cached)
    """
    n = len(secret)
    arr = np.frombuffer(secret, np.uint8)
    idx = np.arange(n)
    mask = get_prime_mask_cached(n)

    if flag:  # Scramble
        order = np.concatenate([idx[mask], idx[~mask]])
        return arr[order].tobytes()
    else:  # Descramble
        result = np.empty_like(arr)
        primes = mask.sum()
        result[idx[mask]] = arr[:primes]
        result[idx[~mask]] = arr[primes:]
        return result.tobytes()

def circular_shift(secret: bytes, flag: bool = True) -> bytes:
    """
    Method 4: Circular Shift (Rotation)
    Scramble / Descramble the secret text by rotating the characters by a fixed number of positions
    Steps:
        1) Get the shift number (2 if scrambling, 5 if descrambling).
        2) Rotate the characters by the shift number.
    """
    return bytes(np.concatenate([
        np.concatenate((chunk[-(2 if flag else 5):], chunk[:7 - (2 if flag else 5)])) if len(chunk) == 7 else chunk
        for chunk in [np.frombuffer(secret, np.uint8)[i:i+7] for i in range(0, len(secret), 7)]
    ]))
if __name__ == "__main__":
    
    for _ in range(10):
        secret=token_bytes(10*1024)
        scrambled = circular_shift(secret, True)
        descrambled = circular_shift(scrambled, False)
    t=0
    for _ in range(10):
        secret=token_bytes(10*1024)
        scrambled = circular_shift(secret, True)
        t0 = time.perf_counter()
        descrambled = circular_shift(scrambled, False)
        t1 = time.perf_counter()
        t = t + t1 - t0
        assert secret == descrambled, "Decrambled secret does not match original secret"

    print(f"Time: {t/10:.6f} seconds")
    

# Method #1 - 0.000048 seconds
# Method #2 - 0.006726 seconds (No cache)
# Method #2 - 0.000124 seconds (Cached prime mask)