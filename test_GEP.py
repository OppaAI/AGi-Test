from CNS import CryptoNode, Synapse  # 假設你呢兩個 class 喺你 project 入面
def test_GEP_encrypt_decrypt(cryptonode, original_data):
    # 建立 Synapse 物件，放入原始資料
    synapse = Synapse("test_sender", "test_receiver", original_data)
    
    # 加密
    encrypted_synapse = cryptonode.GEP_encrypt(synapse)
    encrypted_data = encrypted_synapse.signal["response"]
    print("Encrypted genome string:", encrypted_data)
    
    # 用加密後嘅字串建立新 Synapse，準備解密
    synapse_to_decrypt = Synapse("test_sender", "test_receiver", encrypted_data)
    
    # 解密
    decrypted_synapse = cryptonode.GEP_decrypt(synapse_to_decrypt)
    decrypted_data = decrypted_synapse.signal["response"]
    
    print("Decrypted data:", decrypted_data)
    
    # 檢查是否解密回原始資料（假設原始資料係 JSON 可轉 dict 或 list）
    assert decrypted_data == original_data, "解密後嘅資料唔同原始資料喇！"
    print("✅ 測試成功：加密及解密資料一致！")

# Example usage:
if __name__ == "__main__":
    # 假設你有 CryptoNode instance
    cryptonode = CryptoNode(dynamic_key="test_key")

    original = {
        "message": "Hello, this is a test.",
        "value": 123,
        "list": [1, 2, 3]
    }

    test_GEP_encrypt_decrypt(cryptonode, original)
