# Python program to illustrate ElGamal encryption 
  
import random  
from math import pow
  
a = random.randint(2, 10) 
  
def gcd(a, b): 
    if a < b: 
        return gcd(b, a) 
    elif a % b == 0: 
        return b; 
    else: 
        return gcd(b, a % b) 
  
# Generating large random numbers 
def gen_key(q): 
  
    key = random.randint(22, q) 
    while gcd(q, key) != 1: 
        key = random.randint(22, q) 
  
    return key 
  
# Modular exponentiation 
def power(a, b, c): 
    x = 1
    y = a 
  
    while b > 0: 
        if b % 2 == 0: 
            x = (x * y) % c; 
        y = (y * y) % c 
        b = int(b / 2) 
  
    return x % c 
  
# Asymmetric encryption 
def encrypt(msg, q, h, g): 
  
    en_msg = [] 
  
   # k = gen_key(q)# Private key for sender 
    k =  8069210170051978785
    print("k: ", k)
    s = power(h, k, q) 
    print("s: ", s)
    p = power(g, k, q) 
  
    print("g^k used : ", p) 
    print("g^ak used : ", s) 
  
    return s*msg, p 
  
def decrypt(en_msg, p, key, q): 
  
    dr_msg = [] 
    h = power(p, key, q) 
         
    return en_msg//h
  
# Driver code 
def main(): 
  
    msg = 100474728
    print("Original Message :", msg) 
  
    q = 14654990447141419379 
    g = 2 
  
   # key = gen_key(q)# Private key for receiver
    key =  4437044531233054673 
    h = power(g, key, q) 
    print("g used : ", g) 
    print("q used : ",q)
    print("key used : ",key)
    print("h used : ", h)
  
    en_msg, p = encrypt(msg, q, h, g) 
    dr_msg = decrypt(en_msg, p, key, q) 
    print("Decrypted Message :", dr_msg); 
  
  
if __name__ == '__main__': 
    main() 
