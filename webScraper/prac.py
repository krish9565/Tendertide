import rsa

# 1. Generate Public and Private Keys
public_key, private_key = rsa.newkeys(512)  # 512-bit key

# 2. Encryption
message = input("Enter keyword: ")
encrypted_message = rsa.encrypt(message.encode('utf-8'), public_key)
decrypted_message = rsa.decrypt(encrypted_message, private_key).decode('utf-8')
print("Decrypted Message:", decrypted_message)