import os
import re
import base64
import requests
from flask import Flask, jsonify
from Crypto.Cipher import AES

app = Flask(__name__)

def get_final_html():
    # ধাপ ১: AES ডিক্রিপশন দিয়ে __test কুকি তৈরি
    key = bytes.fromhex("f655ba9d09a112d4968c63579db590b4")
    iv = bytes.fromhex("98344c2eee86c3994890592585b49f80")
    cipher_data = bytes.fromhex("c4c77a73718eb5bb248fe400eef76eb5")

    cipher = AES.new(key, AES.MODE_CBC, iv)
    cookie_val = cipher.decrypt(cipher_data).hex()

    session = requests.Session()
    session.cookies.set("__test", cookie_val, domain="appxpremium.site.je")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # ধাপ ২: config.js ফেচ করা
    config_url = "https://appxpremium.site.je/config.js"
    res_config = session.get(config_url, headers=headers)
    config_text = res_config.text

    # config.js থেকে _K এবং _D মান খুঁজে বের করা
    k_match = re.search(r'_K\s*=\s*["\']([^"\']+)["\']', config_text)
    d_match = re.search(r'_D\s*=\s*["\']([^"\']+)["\']', config_text)

    if not k_match or not d_match:
        return "Could not find _K or _D in config.js"

    _K = k_match.group(1)
    _D = d_match.group(1)

    # ধাপ ৩: জাভাস্ক্রিপ্টের XOR ডিক্রিপশন পাইথনে বাস্তবায়ন
    p = base64.b64decode(_K)
    b = base64.b64decode(_D)

    r_bytes = bytearray()
    for i in range(len(b)):
        r_bytes.append(b[i] ^ p[i % len(p)])

    # ধাপ ৪: চূড়ান্ত Base64 ডিকোড
    final_html = base64.b64decode(r_bytes).decode('utf-8', errors='ignore')
    return final_html

@app.route('/')
def home():
    try:
        content = get_final_html()
        return content
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Render-এর জন্য PORT নির্ধারণ
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
