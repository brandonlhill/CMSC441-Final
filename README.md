# CMSC441 Final - Experimental Evaluation of Two Methods for Factoring Large Integers
## Prime Factorization Algorithms Used for Testing: 
Pollards Rho
- Reference: https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm

Trial Divison
- Reference: https://en.wikipedia.org/wiki/Trial_division

Note: We are using the log cost model because we care about the size of the semibits in terms of bits.

## Report Generation and Testing Script
The "algorithm_test.py" script generations two report files containing information such as runtime and python runtime memory usuage of pollards rho and trial division against a list of semiprime numbers. 

```shell
$ python3 algorithm_test.py
```

## Data Generation and Provided semiprime dataset
The RSA-Digits.dat file contains a list of all the randomly generated semiprimes used for testing. The data within the file was collected from https://bigprimes.org using a modified get request. To get around throttling use external python IDE (online IDEs) as another environment to run the data collection script.

Run the following script to get data... note that data is not formatted into the RSA-Digits.dat
```shell
$ python3 get_semiprimes.py
```

## Regressional Analysis

Modify x1,x2,y1,y2 with the memory_grapher.py script to insert your own data (generated as output from algorithm_test.py). Furthermore, x axis corresponds to semiprimes (bit size) that was tested, and y axis corresponds to time usage.  

## RSA Brute Force Attack
The brute force demo script implements base RSA encyption and is able to compute 8 to 92 bit semiprime computations relatively fast. 
Note that prime factorization (pollards rho) is used to find the private key.

### Information about the code:
Pulled RSA key generation code from: https://github.com/Amaterazu7/rsa-python/blob/master/rsa.py
We implemented the "bruteforce()" function and cleaned up the stdout messages.

Demo output: 
```shell
$ python3 RSA_bruteforce.py
[STDIN] Enter a prime number: 17
[STDIN] Enter another prime number (Not one you entered above): 19
[STDIN] Enter a message to encrypt with your public key: brandon

[INFO] Generating your public / private key-pairs now . . .
	- Public key is (97, 323).
	- Private key is (193, 323).
[INFO] Your encrypted message is:  268114318127168264127
__________________________________________________________________________________________
[INFO] Attempt 0: Breaking RSA.
	- n = 323, p = 19, q = 17
	- Phi = 288
	- d = 193
	- p is 5 bits, q is 5 bits, n is 9 bits.
	- Prime Factor Combinations: [(19, 17)]
	- Breaking Time: 0.000186460994883
	- Private Key Pair: (193, 323)
	- Decrypted Message: brandon
```

## Authors

- [@brandonlhill](https://www.github.com/brandonlhill)
- [@dylan-hilderbrand](https://www.github.com/dylan-hilderbrand)
- [@nathanieljwise](https://www.github.com/nathanieljwise)