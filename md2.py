#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput

pi_s = [ 41, 46, 67, 201, 162, 216, 124, 1, 61, 54, 84, 161, 236, 240, 6,
  19, 98, 167, 5, 243, 192, 199, 115, 140, 152, 147, 43, 217, 188,
  76, 130, 202, 30, 155, 87, 60, 253, 212, 224, 22, 103, 66, 111, 24,
  138, 23, 229, 18, 190, 78, 196, 214, 218, 158, 222, 73, 160, 251,
  245, 142, 187, 47, 238, 122, 169, 104, 121, 145, 21, 178, 7, 63,
  148, 194, 16, 137, 11, 34, 95, 33, 128, 127, 93, 154, 90, 144, 50,
  39, 53, 62, 204, 231, 191, 247, 151, 3, 255, 25, 48, 179, 72, 165,
  181, 209, 215, 94, 146, 42, 172, 86, 170, 198, 79, 184, 56, 210,
  150, 164, 125, 182, 118, 252, 107, 226, 156, 116, 4, 241, 69, 157,
  112, 89, 100, 113, 135, 32, 134, 91, 207, 101, 230, 45, 168, 2, 27,
  96, 37, 173, 174, 176, 185, 246, 28, 70, 97, 105, 52, 64, 126, 15,
  85, 71, 163, 35, 221, 81, 175, 58, 195, 92, 249, 206, 186, 197,
  234, 38, 44, 83, 13, 110, 133, 40, 132, 9, 211, 223, 205, 244, 65,
  129, 77, 82, 106, 220, 55, 200, 108, 193, 171, 250, 36, 225, 123,
  8, 12, 189, 177, 74, 120, 136, 149, 139, 227, 99, 232, 109, 233,
  203, 213, 254, 59, 0, 29, 57, 242, 239, 183, 14, 102, 88, 208, 228,
  166, 119, 114, 248, 235, 117, 75, 10, 49, 68, 80, 180, 143, 237,
  31, 26, 219, 153, 141, 51, 159, 17, 131, 20 ]

def bytelist(plaintext): #convierte de str a una lista de bytes
	return list(str.encode(plaintext))

def paddington(plainbytes): #agrega bytes para realizar el padding de acuerdo al algoritmo
	#if ternario, 16 bytes si es congruente a 0 mod 16, si no a 16 menos el modulo
	bytesmissing = 16 if len(plainbytes) % 16 == 0 else 16-(len(plainbytes) % 16)
	while True:
		plainbytes.append(bytesmissing)
		if len(plainbytes) % 16 == 0:
			break

def checksum(paddedbytes): #generacion del checksum
	chksm = [0] * 16 #inicializacion de lista con 16 ceros
	L = 0
	for i in range(int(len(paddedbytes)/16)):
		for j in range(16):
			c = paddedbytes[i*16+j]
			L = chksm[j] = chksm[j] ^ pi_s[ c ^ L]
	paddedbytes+= chksm

def hashing(inputbytes): #funcion de hashing
	digest_buffer = [0]*48
	for i in range(int(len(inputbytes)/16)):
		for j in range(16):
			digest_buffer[j+16] = inputbytes[i*16+j]
			digest_buffer[j+32] = digest_buffer[j+16] ^ digest_buffer[j]
		t = 0
		for j in range(18):
			for k in range(48):
				digest_buffer[k] = t = digest_buffer[k] ^ pi_s[t]
			t = (t+j)%256
	return digest_buffer

def hashingformat(raw_hash): #convierte la lista con bytes a un string en formato hexadecimal
	hexhash_list = [format(r, '02x') for r in raw_hash] #lista de hexa con padding a cero en caso de ser necesario
	hexhash_string = ''.join(hexhash_list) #string de hexa
	return hexhash_string


lines = []
for line in fileinput.input():
 	lines.append(line.replace('\n',''))
if lines[0] == "\"\"":
	lines[0] = ""


messagebytes = bytelist(lines[0]) #datos de entrada a lista de bytes
paddington(messagebytes) #se añade padding
checksum(messagebytes) #se calcula el padding
final_hash = hashing(messagebytes)[0:16] #calculamos el hash y tomamos los primeros 16 bytes del digest
print(hashingformat(final_hash)) #mostramos el hash en string hexadecimal
