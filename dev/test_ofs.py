import hashlib
import numpy as np
import os
import random
import secrets
from sympy import primerange
from functools import lru_cache
import time

@lru_cache(maxsize=None)

def pairs_reversal_classic(secret: bytes, flag: bool = True) -> bytes:
    pos = len(secret) % 3
    fill = (3 - pos) % 3 if not flag else 0
    padded = secret[:pos] + (b" " * fill if fill else b"") + secret[pos:] if not flag else secret
    chunks = [padded[i:i+3] for i in range(0, len(padded), 3)]
    if not flag:
        chunks[0] = chunks[0][:3 - fill]
    return b"".join(chunks[::-1])    
def pairs_reversal_numpy(secret: bytes, flag: bool = True) -> bytes:
    arr = np.frombuffer(secret, dtype=np.uint8)
    pos = len(arr) % 3
    fill = (3 - pos) % 3 if not flag else 0

    if not flag and fill:
        arr = np.concatenate((arr[:pos], np.full(fill, 32, dtype=np.uint8), arr[pos:]))

    # Now arr length is divisible by 3, safe to reshape
    chunks = arr.reshape(-1, 3)

    if not flag and fill:
        chunks[0] = np.pad(chunks[0][:3 - fill], (0, fill), constant_values=32)

    return bytes(np.flip(chunks, axis=0).ravel())

def main():
    
    secret = secrets.token_bytes(512)

    t0 = time.perf_counter()
    obfuscated = pairs_reversal_numpy(secret, True)
    deobfuscated = pairs_reversal_numpy(obfuscated, False)
    t1n = time.perf_counter() - t0
    print("Match:", secret == deobfuscated)
    print(f"Numpy Method Time: {t1n:.6f} seconds")

    t0 = time.perf_counter()
    obfuscated = pairs_reversal_classic(secret, True)
    deobfuscated = pairs_reversal_classic(obfuscated, False)
    t1c = time.perf_counter() - t0
    print("Match:", secret == deobfuscated)
    print(f"Classic Method Time: {t1c:.6f} seconds")

    fast_slow = "faster" if t1n < t1c else "slower"
    # print in red colour if slower, green if faster
    color_code ="\033[92m" if fast_slow == "faster" else "\033[91m"
    print(f"{color_code}Numpy Method is {abs(t1n - t1c):.6f} seconds {fast_slow} than Classic Method\033[0m")
    print()

if __name__ == "__main__":
    main()