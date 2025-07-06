from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# ➕ Encode integer PK (user id) into base64 for secure email link
def encode_uid(pk):
    return urlsafe_base64_encode(force_bytes(pk))

# 🔁 Decode back from base64 string to normal user id
def decode_uid(encoded_pk):
    return force_str(urlsafe_base64_decode(encoded_pk))
