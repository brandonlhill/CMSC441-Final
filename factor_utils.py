import random
import math

def trialDivision(intToFactor):
    factorList = []
    factoredInt = intToFactor
    
    while not factoredInt % 2: # Check for 2 as a factor
        factorList.append(2)
        factoredInt //= 2
        
    factor = 3
    while factor ** 2 <= factoredInt: # Only check up to square root of the integer
        if not factoredInt % factor:
            factorList.append(factor)
            factoredInt //= factor
        else:
            factor += 2 # Already checked for 2 so now increment by 2 to stay on odd factors
            
    if factoredInt != 1: # Append final result to list of factors
        factorList.append(factoredInt)
        
    #factorList.append(intToFactor) # Every number has itself as a factor

    return factorList

def fermatLittle(a, n, p): # calculates (a^n) % p in O(log y)
    res = 1
    a = a % p 

    while n > 0:
        if n % 2:
            res = (res * a) % p
            n = n - 1
        
        else:
            a = (a ** 2) % p
            n = n // 2
             
    return res % p

def isPrime(n, k): # If n is prime, will always return true, if n is composite, will return false or true, as k increases, likelihood increases
    if n == 1 or n == 4: # trivial
        return False
    elif n == 2 or n == 3: # trivial
        return True

    else:
        for i in range(k):
            a = random.randint(2, n-2) # Choose random a from {2, 3, ..., n-2}
             
            if fermatLittle(a, n - 1, n) != 1:
                return False
                 
    return True

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
        return 1
    else:
        return d

def defaultPoly(c):
    return [[1, 2], [c, 0]] # change the constant in x^2 + c

def findAllPollard(intToFactor, it=-1): 
    factors = []
    isP= isPrime(intToFactor, 3) # check if prime

    while not isP: # if n is prime, dont pollard rho
        factor = pollardRho(intToFactor, polynomial= defaultPoly(it)) # find a factor 
        
        if isPrime(factor, 3):
            factors.append(factor) # append factor to list
            intToFactor //= factor # divide n by factor
        
        else: #found non-prime factor, change polynomial c 
            it += 1 

        isP= isPrime(intToFactor, 3)

    factors.append(intToFactor) # append final n

    return factors