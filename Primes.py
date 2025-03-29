import math
# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Generate prime numbers up to a certain limit
def generate_primes(limit):
    primes = []
    for num in range(2, limit + 1):
        if is_prime(num):
            primes.append(num)
    return primes

# Define the limit
limit = 250
# Generate prime numbers
primes = generate_primes(limit)

with open('results.txt', 'w') as f:
    for prime in generate_primes(limit):
        f.write(str(prime) + ', ')