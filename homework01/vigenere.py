def encrypt_vigenere(plaintext: str, keyword: str) -> str:
   
	ciphertext = ""
	for i in range(len(plaintext)):
		x = ord(plaintext[i])
		if i < len(keyword):
			y = ord(keyword[i]) 
		elif (i + 1) % len(keyword) == 0:
			y = ord(keyword[len(keyword) - 1]) 
		else:
			k = (i + 1) % len(keyword) - 1
			y = ord(keyword[k]) 
		if 65 <= y <= 90:
			y = y - 65
		else:
			y = y - 97
		if 65 <= x <= 90:
			x = (x - 65 + y) % 26 + 65 
		elif 97 <= x <= 122:
			x = (x - 97 + y) % 26 + 97
		ciphertext += chr(x)
   
	return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
   
	plaintext = ""
	for i in range(len(ciphertext)):
		x = ord(ciphertext[i])
		if i < len(keyword):
			y = ord(keyword[i]) 
		elif (i + 1) % len(keyword) == 0:
			y = ord(keyword[len(keyword) - 1]) 
		else:
			k = (i + 1) % len(keyword) - 1
			y = ord(keyword[k]) 
		if 65 <= y <= 90:
			y = y - 65
		else:
			y = y - 97
		if 65 <= x <= 90:
			x = (x - 65 - y) % 26 + 65 
		elif 97 <= x <= 122:
			x = (x - 97 - y) % 26 + 97
		plaintext += chr(x)

	return plaintext

