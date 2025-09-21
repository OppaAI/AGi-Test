import numpy as np
import json
from typing import Any
from timeit import repeat
import gc

gc.disable()

NEURON_SPIKES = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉"] # Neuron spikes bars (from thinnest to full block) with a space for empty bytes (0)

def _to_bytes(data: Any) -> bytes:
    """
    Convert the data to bytes if it's a string or dict/list, otherwise return as is. 

    Args:
        data (Any): The data to convert.

    Returns:
        bytes: The data in bytes.
    """
    if isinstance(data, bytes):
        # If the data is already in bytes, return as is
        return data
    elif isinstance(data, (dict, list)):
        # If the data is a dict or list, convert to JSON string and then to bytes
        return json.dumps(data).encode("utf-8")
    elif isinstance(data, str):
        # If the data is a string, encode to bytes
        return data.encode("utf-8")
    else:
        # Otherwise, convert to string and then to bytes
        return str(data).encode("utf-8")
    
def _rate_encode(data: Any) -> str:
    """
    Visualize the encrypted data with neural encoding spike train using base-8 width bars.

    Args:
        data (Any): The data to encrypt.
        If it's a dict or list, it will be converted to a JSON string.
        If it's a string, it will be encoded to bytes.

    Returns:
        str: The neural encoded spike train using varying width bars.
    """
    # Convert data to array of bytes
    data = _to_bytes(data)
    arr = np.frombuffer(data, dtype=np.uint8)
    bits = np.unpackbits(arr, bitorder='big')

    # Add padding to make length multiple of 3
    pad_len = (3 - len(bits) % 3) % 3
    bits = np.concatenate((bits, np.zeros(pad_len, dtype=np.uint8)))

    # Reshape to groups of 3 bits
    triplets = bits.reshape(-1, 3)

    # Convert 3-bit groups to base-8 indices
    indices = triplets[:,0]*4 + triplets[:,1]*2 + triplets[:,2]

    # Convert indices to corresponding spike train
    return "".join(NEURON_SPIKES[i] for i in indices)

if __name__ == "__main__":

    #test time
    test_str = "Hello, this is a test.Hello"*10

    # 執行時間測試，lambda 裡面呼叫 _rate_encode
    t = repeat(lambda: _rate_encode(test_str), repeat=10, number=1000)

    # 計算平均時間
    avg_time = sum(t) / len(t)

    # 這裡 p 沒定義，改用 _rate_encode(test_str) 呼叫結果
    p = _rate_encode(test_str)

    print("Neural Signal: ", p)
    print(f"Average time: {avg_time:.6f} seconds")