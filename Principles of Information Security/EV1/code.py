from random import randint
import sympy as sp

numbits = 10

def po(a,n,p):
    an = 1
    a = a%p
    if a==0:
        return 0
    while(n):
        if(n&1):
            an = an*a%p
        n = n>>1
        an = an*an%p
    return an

def sign(g, p, x):
    rn = randint(2, p-1)
    t = po(g, rn, p)
    y = po(g, x, p)
    c = hashfun(g, p, y)
    z = c*x + rn
    return t, y, c, z

def verify(g, p, z, t, y):
    c = hashfun(g,p,y)
    if po(g,z,p) == ((t*po(y,c,p))%p):
        return True
    return False

def generator(p , f):
    phi = p - 1
    for x in range(2, p+1):
        tr = True
        for fac in [f, 2]:
            if po(x, phi/fac, p)==1:
                tr = False
                break
        if tr:
            return x
    return -1

def generate_p(n):
    while True:
        pr = randint(2**(n-1), 2**n)
        if sp.isprime(pr) and sp.isprime(2*pr+1):
            return 2*pr+1, pr

# input nbits
nbits = int(input("Enter number of bits: "))
print("Number of bits: ",numbits) 
prime, fac = generate_p(numbits)
print("Prime : ", prime)
gen = generator(prime, fac)



