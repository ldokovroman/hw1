import random
import typing as tp
import math as m


def is_prime(n: int) -> bool:
	
	x = 2
	while x <= m.sqrt(n) and n % x != 0:
		x = x + 1
	if x <= m.sqrt(n) or n <2:
		return False
	else:
		return True
   


def gcd(a: int, b: int) -> int:

	while not (a == 0 or b == 0):
		if a > b:
			a = a % b
		else:
			b = b % a
	return a + b


def multiplicative_inverse(e: int, phi: int) -> int:

	a = []
	a.append([e, phi, e % phi, e // phi])
	i = 1
	while a[-1][2] != 0:
		a.append([a[-1][1], a[-1][2], 0, 0])
		a[-1][2] = a[-1][0] % a[-1][1]
		a[-1][3] = a[-1][0] // a[-1][1]
		i = i + 1
	x = 0
	y = 1
	i = i - 2
	while i >= 0:
		t = x
		x = y
		y = t - y * a[i][3]
		i = i - 1
	while x < 0:
		x = x + phi
	return x

  

def generate_keypair(p: int, q: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:

	if not (is_prime(p) and is_prime(q)):
		raise ValueError('Both numbers must be prime.')	
	elif p == q:
		raise ValueError('p and q cannot be equal')

	n = p * q
	phi = (p - 1) * (q - 1)
	e = random.randrange(1, phi)
	g = gcd(e, phi)
	while g != 1:
		e = random.randrange(1, phi)
		g = gcd(e, phi)

	d = multiplicative_inverse(e, phi)
	return ((e, n), (d, n))


def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return "".join(plain)


if __name__ == "__main__":
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print("".join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
