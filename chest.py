import warnings
warnings.simplefilter("ignore")

import base64
import requests
import re
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

# Given JWK private key
jwk_private_key = {
            "alg":"RSA-OAEP-256",
            "d":"V_UOj0cxCuOMsGksunP3oJUdSsfWVozn1AL2CRUkeMu9jGGA56PE4C_eB5o7l-kijU70TzjU4_I4VdttBZ8ppp-V-1_4vgI1ge6zGezu0lzeyP6W7TLhiojBVeLQ0duQrETPdOMolvU4EZ3k0LjpkVEGMERkg3LDj1_PhjL-RNKuVLhJ7DfViQL7UY0tHdTX5VD7xIYqyg9SSrMhG_7iBBL67MGC4E1BPvorSmwfYp_5hkrByE2NtJfDHgmxCxI-ZSskeBsKie4UhBDD46vvafC63WuAn6DUnAcMBZf2oOoKbmH3FUuUrA-DNe0XoE1x5c8hzLRPvgMPwpfbmI9pIQ",
            "dp":"QCm3XhmEH1_qQBDgyx1pV6hHULYxoSGsfdlFwvR6052QeM8N50reb1KVfLq2duNUl5HTuVUPj5QrcqrLhuTKHzarx-z7Sx5p8Rcru5bMNE4gw7-ru56PpsRNdw_KMEjKU1WvmkSUm1Jkl9jT_48EA9F6Izfd3zd9SdJmcFwTxHk",
            "dq":"tIPQ5XCTa7UlAf8Erq09XnICWLUc7xoIbJ3mefF8O9xEOqzeYR_Uuc2NMLlnBPBexlp_SyNRT-z-rmJh3sVPgpq17cVakDjaHEPBx88AucVvEguTza93ievUOvBQ8-E59AypAKiH-l0rM43HarF1WQ9ArHVDFGr6gYMyV6jOHeE",
            "e":"AQAB",
            "ext":True,
            "key_ops":["decrypt"],
            "kty":"RSA",
            "n":"vsmbwGZ9p1g7rscWuJ0A3m_KUJqOF_0jrbwh7QOFXOG0L4IJMb3ZF5PwRRLAjmJ507dq_0fvkbWTlN3g7ihb09DcqMNAFrt77P0Tv0RzSwzfH8BIfgYxBOqysuGJlqsSfIe7wbq89qTxKZ5YV_aY-LfkOEgpagYO5YImuKD0fgYShXOxjg3Y08jmijXBlzUB0TK0s32r-re3FZ1mbR0r3RFjB-veh8QIyexmuHs57H9ffawmRXATv6Gg3gVq6PoiAA9H5f0JpxnbN3Fh_ydQ6VrcbS9pyUzHDGL-gD201p69pNvwn_vxXO7aYg1XcNVQ3OxbfvKxTLkXyERezFcEDw",
            "p":"--uAw5ZFtB1ZQl0jNoJ91q1ZpI4db6Pxg8zE_OfbUOwf_4CAb0t7pbaUkkD0L0O4BfzcSIYeIY1zYBp5XqmzYMGImQKv8avJhDglGIQjQrg9nvTD_fMLbkz-ZS4XMLGT2PvP50eydMnzw9czuKN7iNN-BFMz8lcudaiGBgzyNJc",
            "q":"weCkOlaYdcYsooceP0Yc4SLs5bwgThiiEaWg4ekrb5TeNvJlDI_OtAG1HT553ASlsat6pSxfMpa5e2Xhfwxk7EHz_I6K31_hv3MplRsaqzrBUcDTasstZkNaS6LQAY2TT_UdAPaFbJSSeI_DBLggIVBFyuUhjZON3zMU-NBhw0k",
            "qi":"CP-O07SwkCTv4ZnjuDikJQ-Y_CO6yoLWT7A5mp5Zn1cUuuFMMZYK1XNja5ey0FGmco9MaDRNIM_JjZNYE7O1MNclk0eJ69cFNW2BEQIETTsjVbUGb65fBKgXuGX3KS-dZ4rLdW23z5tJQ1mVaBncLyRb2ryTYo-Y5lSAQzqd37E"
        }
# Convert JWK to PEM
# Convert JWK to RSA Private Key
private_numbers = rsa.RSAPrivateNumbers(
    p=int.from_bytes(base64.urlsafe_b64decode(jwk_private_key['p'] + "=="), byteorder='big'),
    q=int.from_bytes(base64.urlsafe_b64decode(jwk_private_key['q'] + "=="), byteorder='big'),
    d=int.from_bytes(base64.urlsafe_b64decode(jwk_private_key['d'] + "=="), byteorder='big'),
    dmp1=int.from_bytes(base64.urlsafe_b64decode(jwk_private_key['dp'] + "=="), byteorder='big'),
    dmq1=int.from_bytes(base64.urlsafe_b64decode(jwk_private_key['dq'] + "=="), byteorder='big'),
    iqmp=int.from_bytes(base64.urlsafe_b64decode(jwk_private_key['qi'] + "=="), byteorder='big'),
    public_numbers=rsa.RSAPublicNumbers(
        e=int.from_bytes(base64.urlsafe_b64decode(jwk_private_key['e'] + "=="), byteorder='big'),
        n=int.from_bytes(base64.urlsafe_b64decode(jwk_private_key['n'] + "=="), byteorder='big')
    )
)
private_key = private_numbers.private_key(backend=default_backend())

# Decryption function
def decrypt_with_private_key(ciphertext, private_key):
    return private_key.decrypt(
        base64.b64decode(ciphertext),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}

url = "https://pastebin.com/u/bloodyboy"

response = requests.get(url, headers=headers).text
matches = re.findall(r'href="(.*?)">userdata', response)
urls = ['https://pastebin.com/raw' + s for s in matches]

for x in urls:
    raw = requests.get(x, headers=headers).text
    # Decrypting the text
    decrypted_text = decrypt_with_private_key(raw, private_key)
    print(decrypted_text.decode())
