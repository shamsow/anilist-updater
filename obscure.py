def encode(string, key):
	cypher = ''
	for i in string:
		if i.isalpha():
			if i.islower():
				x = ((ord(i) + key) - 97 ) % 26 + 97
			if i.isupper():
				x = ((ord(i) + key) - 65 ) % 26 + 65
			cypher += chr(x)
		else:
			cypher += i
	return cypher

def decode(string, key):
	original = ''
	for i in string:
		if i.isalpha():
			if i.islower():
				x = ((ord(i) - key) - 97 ) % 26 + 97
			if i.isupper():
				x = ((ord(i) - key) - 65 ) % 26 + 65
			original += chr(x)
		else:
			original += i
	return original


if __name__ == '__main__':
	password = input("string: ")
	key      = int(input())
	cypher   = encode(password, key)
	print(cypher)