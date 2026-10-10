import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ১. মানগুলো নির্ধারণ করুন
key = bytes.fromhex("f655ba9d09a112d4968c63579db590b4")
iv = bytes.fromhex("98344c2eee86c3994890592585b49f80")
cipher_data = bytes.fromhex("c4c77a73718eb5bb248fe400eef76eb5")

# ২. AES-CBC ডিক্রিপ্ট করে কুকির মান বের করুন
cipher = AES.new(key, AES.MODE_CBC, iv)
cookie_val = unpad(cipher.decrypt(cipher_data), AES.block_size).hex()

print(f"Generated __test cookie: {cookie_val}")

# ৩. সেশন তৈরি করে কুকিসহ আসল পেজে রিকোয়েস্ট পাঠান
session = requests.Session()
session.cookies.set("__test", cookie_val, domain="appxpremium.site.je")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = session.get("https://appxpremium.site.je/?i=1", headers=headers)
print(response.text)
