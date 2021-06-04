import base64
import requests
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from Crypto.Cipher import AES
from binascii import b2a_hex

# 此处传入后台的秘钥
str_key = ""

encodestr = base64.b64decode(str_key.encode('utf-8'))

class AccessToken:
    def __init__(self, key=encodestr):
           # 对传入的秘钥等进行初始化
        self.key = key.encode('utf-8')

        # 加密模式
        self.mode = AES.MODE_CBC
        self.iv = encodestr

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
          data = data.encode()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    # python的AES加密算法

    def encrypt_AES(self, password):
        cryptor = AES.new(self.key, self.mode, self.iv)
        text = password.encode('utf-8')
        text = self.pkcs7_padding(text)
        ciphertext = cryptor.encrypt(text)
        return (b2a_hex(ciphertext).decode().lower())

        # 用户登录

