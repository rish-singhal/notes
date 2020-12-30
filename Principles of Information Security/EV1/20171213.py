from random import randint

numbits = 10
h = 2

def po(a,n,p):
    if n==0:
      return 1
    an = po(a,n//2,p)
    an = an*an%p
    if (n%2):
      return an*a%p
    return an

def isprime(p):
    if p == 1:
        return False
    for x in range(min(1000,p-1)):
        ran = randint(1, p - 1)
        if po(ran, p-1, p) != 1:
            return False
    return True

def hashfun(g, p, y):
    fb = y & ((1<<(numbits//2))-1)
    lb = y >> (numbits//2)
    return  po(g, lb, p)*po(h, fb, p)%p

def sign(g, p, m):
    x = randint(2,p-1) #private key
    rn = randint(2, p-1)
    t = po(g, rn, p)
    y = po(g, x, p) #public key
    c = hashfun(g, p, m)
    z = c*x + rn
    #print("z is:",z)
    return t, y, c, z

def verify(g, p, z, t, y, m):
    c = hashfun(g,p,m)
    print("Hash of message: ",c)
    print("")
    if po(g,z,p) == ((t*po(y,c,p))%p):
        print("Signature Verified.")
        return True
    print("Signature Not Verified.")
    return False

def generator(p , f):
    phi = p - 1
    for x in range(2, p+1):
        tr = True
        for ff in [f, 2]:
            if po(x, phi//ff, p)==1:
                tr = False
                break
        if tr:
            return x
    return -1

def generate_prime(n):
    while True:
        pr = randint(2**(n-2), 2**(n-1))
        if isprime(pr) and isprime(2*pr+1):
            return 2*pr+1, pr

numbits = int(input("Enter number of bits: "))

prime, fac = generate_prime(numbits)
print("Prime: ", prime)

h = randint(2,prime-1)

gen = generator(prime, fac)
print("Generator: ",gen)

message = int(input("Enter message: "))

t, y, c, z = sign(gen, prime, message)
print("Signature (hash(m)*private + random, g**random): ", z, t)

chk = verify(gen, prime, z, t, y, message)
