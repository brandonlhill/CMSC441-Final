import random
import math
import sys
import time
import datetime
import psutil

import factor_utils
from memory_profiler import profile

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
    integerList = []
    digits = 0
    report = None
    
    def __init__(self, resultsFile, integerFile=None):
        if resultsFile == None or resultsFile == '':
            raise Exception("[ERROR] No File Given.")
        self.resultsFile = open(resultsFile, "w")
    
    def generateTestData(self, digits, iterations):
        self.integerList = self.getInts(digits, iterations)
        self.digits = digits
    
    def report(self, msg):
        self.resultsFile.write(msg)
        print(msg, end="")
    
    def createNewFile(self, filename=""):
        fn = self.resultsFile.name
        self.resultsFile.close()
        if filename == "":
            self.resultsFile = open(fn + "_" +str(datetime.datetime.now()), "w")
        else:
            self.resultsFile = open(filename, "w")
        
    
    def test(self, algorithm):
        # clear spaceUsage
        self.spaceUsage = []

        # create new report title
        # self.report(f"[INFO] Prime List: {self.integerList}\n")
        self.report(f"[TEST] Preformance Test: {algorithm.__name__} \n")
        x = 20 if self.digits < 20 else self.digits
        self.report("\t%-*s%-*s%-*s%-*s%-*s\n" % (x,"[Integer to Factor]", 20, "[Elapsed Time]", 20, "[Memory Usage]", 20, "[Int Memory Usage]", 20, "[Factors]"))

        for line in self.integerList:
            # report
            self.report(f"\t")
            self.report(f"{line:<20}")
            
            # start timer
            startTime = time.time()
            
            # get prime factors
            numberFactors = algorithm(line)
           
            # end time - in micro-seconds
            endTime = time.time()
            elapsedTime = endTime - startTime
            elapsedTime = round(elapsedTime, 15)

            # get space usage and size of processed number
            space_usage_algo = sys.getsizeof(algorithm(line)) * 8
            space_usage_num = sys.getsizeof(line) * 8
            self.spaceUsage.append((space_usage_algo, space_usage_num))
            self.report(f"{str(elapsedTime):<20}")
            self.report(f"{space_usage_algo:<20}")
            self.report(f"{space_usage_num:<20}")
            
            # generate report for iteration
            self.report("[" + ", ".join(str(i) for i in numberFactors) + "]\n")

        # report final stats
        total = sum(self.spaceUsage[0])
        self.report(f"\n[INFO] Total space usage: {total}")
        average = total / len(self.spaceUsage)
        self.report(f"\n[INFO] Average space usage: {average}")
        self.report("\n[INFO] Testing Complete.\n")

# main
if __name__ == "__main__":
    # setup class
    _driver = Driver("results.txt")
    
    # test pollard's rho
    _driver.report(f"\n%s\n" % ('-'*120))
    _driver.generateTestData(10,3)
    _driver.test(factor_utils.findAllPollard)
    
    # test trail division (same data)
    _driver.report(f"\n%s\n" % ('-'*120))
    _driver.createNewFile()
    _driver.test(factor_utils.trialDivision)
    _driver.report(f"\n%s\n" % ('-'*120))
