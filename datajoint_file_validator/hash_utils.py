import hashlib
from typing import Any

def generate_id(obj: Any, length: int = 7) -> str:
	return hashlib.sha1(hex(hash(obj)).encode("utf-8")).hexdigest()[:length]

