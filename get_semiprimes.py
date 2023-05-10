import requests
import json


def get_semi_primes(bits, iterations):
  url = "https://big-primes.ue.r.appspot.com/RSA?numBits=" + str(bits)
  numbers = []
  isDuplicate = False

  for i in range(iterations):
    response = requests.get(url)
    data = json.loads(response.content)

    try:
      rsanumber = data["RSANumber"]
    except:
      print("you are throttled")
      return numbers, isDuplicate

    if rsanumber not in numbers:
      numbers.append(rsanumber)
    else:
      isDuplicate = True

  return numbers, isDuplicate


if __name__ == "__main__":
  bit = 100
  amount = 50
  lst, duplicate = get_semi_primes(bit, amount)
  print(f"bits: {bit}\n{lst}\n{len(lst)} RSA numbers")
