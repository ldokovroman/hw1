import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    
	ciphertext = ""
	
	for i in range(len(plaintext)):
		x = ord(plaintext[i])
		if 65 <= x <= 90:
			x = (x - 65 + shift) % 26 + 65 
		elif 97 <= x <= 122:
			x = (x - 97 + shift) % 26 + 97
		ciphertext += chr(x)
   
	return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
   
	plaintext = ""
	
	for i in range(len(ciphertext)):
		x = ord(ciphertext[i])
		if 65 <= x <= 90:
			x = (x - 65 - shift) % 26 + 65 
		elif 97 <= x <= 122:
			x = (x - 97 - shift) % 26 + 97
		plaintext += chr(x)
  
	return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
	
	return best_shift
