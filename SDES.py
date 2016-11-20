P10 = (2,4,1,6,3,9,0,8,7,5)
P8 = (5,2,6,3,7,4,9,8)
IP = (1,5,2,0,3,7,4,6)
IP_INVERSE = (3,0,2,4,6,1,7,5)
E_P = (3,0,1,2,1,2,3,0)
P4 = (1,3,2,0)

S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
S1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]

def getInput():
    while(True):
        plaintext = input("Give 8-bit plaintext: ")
        if(len(plaintext) == 8):
            counter = 0
            for c in plaintext:
                if(c == "0" or c == "1"):
                    counter += 1

            if(counter == len(plaintext)):
                break
            else:
                print("bitstring does not contain only 0's and 1's")
        else:
            print("Wrong number of bits. Try again!")

    return plaintext

def getKey():
    while(True):
        key = input("Give 10-bit key: ")
        if(len(key) == 10):
            counter = 0
            for c in key:
                if(c == "0" or c == "1"):
                    counter += 1

            if(counter == len(key)):
                break
            else:
                print("bitstring does not contain only 0's and 1's")
        else:
            print("Wrong number of bits. Try again!")

    return key

def permutation(key, P):
    return ''.join(key[i] for i in P)

def left(key):
    return key[:int(len(key)/2)]

def right(key):
    return key[int(len(key)/2):]

def shift(key):
    l = left(key)[1:] + left(key)[0]
    r = right(key)[1:] + right(key)[0]
    return l + r

def key1(key):
    return permutation(shift(permutation(key, P10)), P8)

def key2(key):
    return permutation(shift(shift(permutation(key, P10))), P8)

def xor(text, key):
    return ''.join(str(((bit + keyBit) % 2)) for bit, keyBit in zip(map(int, text), map(int, key)))

def sbox(text, sbox):
    row = int(text[0] + text[3], 2)#convert in base 2
    column = int(text[1] + text[2], 2)
    return '{0:02b}'.format(sbox[row][column])#return the number in base 10

def f(r, key):
    perm = permutation(r, E_P)
    xored = xor(perm, key)
    sboxResult = sbox(left(xored), S0) + sbox(right(xored), S1)
    result = permutation(sboxResult, P4)
    return result

def f_k(text, key):
    l = left(text)
    r = right(text)
    xored = xor(f(r, key), l)
    return xored + r

def sw(text):
    l = left(text)
    r = right(text)
    return r + l

def encrypt(plaintext, key1, key2):
    perm = permutation(plaintext, IP)
    fResult = f_k(perm, key1)
    interchanged = sw(fResult)
    fResult2 = f_k(interchanged, key2)
    encrypted = permutation(fResult2, IP_INVERSE)
    return encrypted

def decrypt(ciphertext, key1, key2):
    perm = permutation(ciphertext, IP)
    fResult = f_k(perm, key2)
    interchanged = sw(fResult)
    fResult2 = f_k(interchanged, key1)
    decrypted = permutation(fResult2, IP_INVERSE)
    return decrypted

plaintext = getInput()
key = getKey()
''' key generation '''
key1 = key1(key)
key2 = key2(key)
'''encryption'''
encrypted = encrypt(plaintext, key1, key2)
'''decryption'''
decrypted = decrypt(encrypted, key1, key2)

print("Plaintext: " + str(plaintext))
print("Key: " + str(key))
print("Encrypted: " + str(encrypted))
print("Decrypted: " + str(decrypted))
