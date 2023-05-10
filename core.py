from memory_profiler import memory_usage
import random
import math
import sys
import time
import datetime
import configparser
import json

import factor_utils
from memory_profiler import profile

# globals
DATAFILE = "RSA-Digits.dat"
DATAFILESECTIONS = ["8-bits", "16-bits", "32-bits", "48-bits", "56-bits", "58-bits", "59-bits", "60-bits", "61-bits", "63-bits", "64-bits", "70-bits"]

class Num_Utils:
    def randomIntGen(self, numDigits):
        digits = [random.randint(0, 9) for _ in range (numDigits)] # Change range to create more digits
        lastDigit = random.choice([1, 3, 7, 9]) # Avoid even digits or 5 as final digit
        digits.append(lastDigit)
        largeInteger = int("".join(str(_) for _ in digits))
        return largeInteger
    
    def getInts(self, numDigits, numIterations):
        temp = []
        for _ in range(numIterations):
            temp.append(self.randomIntGen(numDigits))
        return temp

class Driver(Num_Utils):
    spaceUsage = []
    primeList = []
    digits = 0
    report = None
    datafile = None
    
    def __init__(self, resultsFile, integerFile=None):
        if resultsFile == None or resultsFile == '':
            raise Exception("[ERROR] No File Given.")
        
        self.datafile = configparser.ConfigParser()
        self.datafile.read(DATAFILE)
        self.resultsFile = open(resultsFile, "w")
    
    def generateTestData(self, digits, iterations):
        self.primeList = self.getInts(digits, iterations)
        self.digits = digits

    def report(self, msg):
        #self.resultsFile.write(msg)
        print(msg, end="")
    
    def createNewFile(self, filename=""):
        fn = self.resultsFile.name
        self.resultsFile.close()
        if filename == "":
            self.resultsFile = open(fn + "_" +str(datetime.datetime.now()), "w")
        else:
            self.resultsFile = open(filename, "w")
    
    def test(self, algorithm, bits):
        # clear spaceUsage
        self.spaceUsage = []

        # create new report title
        self.report(f"\n[TEST] Preformance Test: {algorithm.__name__} with {bits} primes.")
        x = 25 if self.digits < 20 else self.digits + 5
        self.report("\n\t%-*s%-*s%-*s\n" % (x,"[Integer to Factor]", 30, "[Elapsed Time]", 20, "[Factors]"))
        
        # write to raw file
        self.resultsFile.write(f"\n[TEST] Preformance Test: {algorithm.__name__} with {bits} primes.")
        self.resultsFile.write("\n[Integer to Factor]\t[Elapsed Time]\t[Factors]\n")
        
        for line in self.primeList:
            # start timer
            startTime = time.perf_counter()
            
            # get prime factors (mem_usage, retval)
            numberFactors = algorithm(line)

            # end time - in micro-seconds
            endTime = time.perf_counter()
            elapsedTime = endTime - startTime
            elapsedTime = round(elapsedTime, 15)
            
            # generate report for iteration
            factors = ", ".join(str(i) for i in numberFactors)
            
            # write to console & file: prime, time, factors
            self.report(f"\t")
            self.report(f"{line:<{x}}")
            self.report(f"{str(elapsedTime):<30}")
            self.report("[" + factors + "]\n")
            self.resultsFile.write(f"{line}\t{elapsedTime}\t{factors}\n")
        

        # report final stats
        self.report(f"\n[INFO] Prime number stack size (size of an object in bytes): {sys.getsizeof(self.primeList[0])} bytes.")
        self.report(f"\n[INFO] Function stack size (size of an object in bytes): {sys.getsizeof(algorithm(self.primeList[0]))} bytes.")
        self.report(f"\n[INFO] Function runtime stack size: (size of an object in bytes): {self.getMemorySize(algorithm, self.primeList[0])} Mib.\n")
        
        # write code to stat file
        self.resultsFile.write(f"\n[INFO] Prime number stack size (size of an object in bytes): {sys.getsizeof(self.primeList[0])} bytes.")
        self.resultsFile.write(f"\n[INFO] Function stack size (size of an object in bytes): {sys.getsizeof(algorithm(self.primeList[0]))} bytes.")
        self.resultsFile.write(f"\n[INFO] Function runtime stack size: (size of an object in bytes): {self.getMemorySize(algorithm, self.primeList[0])} Mib.\n")
    
    def getMemorySize(self, algorithm, line):
        #(memory, numberFactors) = memory_usage(proc=(algorithm, (line,), {}), retval=True)
        temp = memory_usage(proc=(algorithm, (line,), {}))
        # return average memory usage
        return temp
        #return sum(temp) / len(temp)

    def testFromFile(self, algorithm):
        for datasections in DATAFILESECTIONS:
            output = list(self.datafile.items(datasections))
            if (output == []):
                self.report("\n[INFO] Hit Empty List... Skipping.")
                continue
            
            self.primeList = json.loads(output[0][1])
            self.primeList = list(map(int, self.primeList))
            self.test(algorithm,datasections)
# main
if __name__ == "__main__":
    try:
        _driver = Driver("results_PR_MEM_2.txt")
        _driver.testFromFile(factor_utils.trialDivision)
        _driver.report("\n[INFO] Testing Complete.")
    except KeyboardInterrupt as inst:
        print("[INFO] Ctrl + C shutdown.")
