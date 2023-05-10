import random
import math
import time
from itertools import combinations

def gcd(a, b):
    '''
    Euclid's algorithm for determining the greatest common divisor
    Use iteration to make it faster for larger integers
    '''
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    '''
    Euclid's extended algorithm for finding the multiplicative inverse of two numbers
    '''

    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

def is_prime(num):
    '''
    Tests to see if a number is prime.
    '''

    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def generate_key_pair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    # n = pq
    n = p * q

    # Phi is the totient of n
    phi = (p-1) * (q-1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private key_pair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [pow(ord(char), key, n) for char in plaintext]
    # Return the array of bytes
    return cipher

def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    aux = [str(pow(char, key, n)) for char in ciphertext]
    # Return the array of bytes as a string
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)


def g(val, intToFactor, polynomial): # Polynomial in format of [ (coefficient_1, degree_1), (c2,d2), ...  ]
    result = 0 
    for term in polynomial: #evaluate polynomial(x)
        result += term[0] * (val ** term[1])

    return result % intToFactor # Return g(x) = polynomial(x) mod n

def pollardRho(intToFactor, x= 2, y= 2, polynomial= [[1, 2], [1, 0]]): # Set default polynomial to x^2 + 1, and x and y to 2
    if intToFactor == 1: # trivial 
        return 1
    if intToFactor % 2 == 0: # trivial
        return 2

    d = 1

    while d == 1:
        x = g(x, intToFactor, polynomial) # tortoise node
        y = g(g(y, intToFactor, polynomial), intToFactor, polynomial) # hare node
        d = math.gcd(abs(x - y), intToFactor) 

    if d == intToFactor: # no factor was found
        return pollardRho(intToFactor, polynomial + [1,0])
    else:
        return d

def defaultPoly(c):
    return [[1, 2], [c, 0]] # change the constant in x^2 + c

def findAllPollard(intToFactor): 
    factors = [pollardRho(intToFactor)]
    intToFactor //= factors[0]
    factors.append(intToFactor)
    
    return factors

def breakRSA(publicKey, encrypted_msg, message):
    counter = 0

    startTime = time.perf_counter()
    primefactors = findAllPollard(publicKey[1])

    # try every combination of prime factors in pairs of 2 (this is only useful for dictionary coprimes)
    # note that if pollardRho happens to find the coprimes there will only ever be two coprimes because of the property of semiprimes
    primefactorCombinations = list(combinations(primefactors, 2))
    
    # attempt bruteforce on each combination
    for x in primefactorCombinations:
        n = x[0] * x[1]                                 # guess n = p * q
        phi = (x[0] - 1) * (x[1] - 1)                   # φ(n) = (p-1)*(q-1)
        public_exponent = publicKey[0]                  # given e
        d = multiplicative_inverse(public_exponent, phi)# e − 1 (mod φ(n))
        privateKey = (d,n)                              # 
        decrypt_msg = decrypt(privateKey, encrypted_msg)
        
        # information
        print(f"[INFO] Attempt {counter}: Breaking RSA.")
        print(f"\t- n = {n}, p = {x[0]}, q = {x[1]}\n\t- Phi = {phi}\n\t- d = {d}")
        print(f"\t- p is {p.bit_length()} bits, q is {q.bit_length()} bits, n is {n.bit_length()} bits.")
        if (message == decrypt_msg):
            totalTime = round((time.perf_counter() - startTime),15)
            print(f"\t- Prime Factor Combinations: {primefactorCombinations}")
            print(f"\t- Breaking Time: {totalTime}") 
            print(f"\t- Private Key Pair: {privateKey}")
            print(f"\t- Decrypted Message: {decrypt_msg}")
            break
        counter+=1

if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''

    p = int(input("[STDIN] Enter a prime number: "))
    q = int(input("[STDIN] Enter another prime number (Not one you entered above): "))
    message = input("[STDIN] Enter a message to encrypt with your public key: ")
    
    print("[INFO] Generating your public / private key-pairs now . . .")
    public, private = generate_key_pair(p, q)

    print(f"\t- Public key is {public}.\n\t- Private key is {private}.")
    encrypted_msg = encrypt(public, message)

    print("[INFO] Your encrypted message is: ", ''.join(map(lambda x: str(x), encrypted_msg)))
    print("[INFO] Decrypting message with private key ", private, " . . .")
    print("[INFO] Your message is: ", decrypt(private, encrypted_msg))

    print("_"*90)
    breakRSA(public, encrypted_msg, message)