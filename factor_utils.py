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