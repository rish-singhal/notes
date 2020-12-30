from random import randint
from sympy import Matrix
import numpy as np

## copied from Evaluation 1
h = 2
k = 6 #number of blocks
e = 3 #number of error blocks permissible
poly = []
numbits = 0


def pend():
  print(" ")

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

def hashfun(g, p, m):
    fb = m['x']
    lb = m['y']
    return  po(g, lb, p)*po(h, fb, p)%p

def sign(priv, m):
    x = priv['secret']
    p = priv['prime']
    g = priv['gen']
    y = priv['y'] #public key
    rn = randint(2, p-1)
    t = po(g, rn, p)
    c = hashfun(g, p, m)
    z = c*x + rn
    return {'t':t,'z':z}

def verify(pub, data):
    signm = data['sign']
    m = data['m']
    y = pub['y']
    t = signm['t']
    z = signm['z']
    g = pub['gen']
    p = pub['prime']
    c = hashfun(g,p,m)
 #   print("Hash of message: ",c)
  #  print("")
    if po(g,z,p) == ((t*po(y,c,p))%p):
       # print("Signature Verified.")
        return True
    #print("Signature Not Verified.")
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

def evaluate_poly(x, p):
	value = 0
	poi = 1
	for block in poly:
		value = (value + (block*poi)%p )%p
		poi = (poi*x)%p
	return value

def gen_points(n, p):
##to evaluate n random points for given polynomial range(n) wlog
	point = []
	for x in range(n):
		point.append({'x':x+1,'y':evaluate_poly(x+1,p)})
	return point

def verifypoints(endata, publicKey):
  ppr = []
  safepoints = []
  for message in endata:
    chk = verify(publicKey, message)
    ppr.append(chk)
    if verify(publicKey, message):
      safepoints.append(message['m'])
  print("Verification of Points: ",ppr)
  return safepoints[:k]

def reconstruct(f , p):
    X = []
    Y = []
    for point in f:
      v = 1
      val = []
      for _ in range(k):
        val.append(v)
        v = (v*point['x'])%p
      X.append(val)
      Y.append(point['y'])
    
    Y = np.array(Y).T
    Z = np.array(Matrix(np.array(X)).inv_mod(p))
    an = []
    for i in range(k):
      v = 0
      for j in range(k):
        v = (v + (Z[i][j]*Y[j])%p)%p
      an.append(v)
    
    return np.array(an)
    

# as (k+e)<=n ==> n = 6+3 = 9
n = k  + e  

data = int(input("Enter Data: "))
# b = number of bits in one of the k blocks
pend()

bitsData = len(bin(data)[2:])
print("Number of bits in data: ", bitsData)

#numebr of bits in a block
bbits = (bitsData//k)

if bitsData%k:
	bbits += 1

numbits = bbits


print("Number of block (k): ", k)
print("Number of bits in one block (b): ", bbits)
pend()

poly = []
copydata = data

while(copydata):
	msk = (1<<bbits) - 1
	poly.append(copydata&msk)
	copydata >>= bbits

print("Polynomial Coefficients: ", poly)
pend()

prime, fac = generate_prime(bbits+5)
#print("Prime: ", prime)

h = randint(2,prime-1)

gen = generator(prime, fac)
#print("Generator: ",gen)

n = k + e
points = gen_points(n, prime)
print("Random n points evaluated: ", points)
pend()

secret = randint(2,prime-1) 
y = po(gen, secret, prime) 
rn = randint(2, prime-1)
t = po(gen, rn, prime)

privateKey = {'secret':secret, 'prime':prime, 'gen':gen, 'y':y}
print("Private Key: ", privateKey)

publicKey = {'prime':prime, 'gen':gen, 'y':y }
print("Public Key: ",publicKey)
pend()

signed = []

print("Signing hashes of n points now...")
for m in points:
	signed.append({'m':m, 'sign':sign(privateKey,m)})

## to verify points
pend()
print("Verifying n signed hash points now...")
verifypoints(signed, publicKey)

## let's corrupt 3 blocks, by updating it to random values
signed[0]['m']['x'] = 31313
signed[1]['m']['x'] = 313
signed[2]['m']['x'] = 314

pend()
print("First 3 data points are corrupted now!!")
safepoints = verifypoints(signed, publicKey)
pend()

print("Uncorrupted k points: ",safepoints )


print("Reconstructing polynomial with these k points")
rPoly = reconstruct(safepoints, prime)
pend()
print("Reconstructed Polynomial: ",rPoly)
pend()
rData = 0
vv = 0
for xx in range(k):
  rData += (int(rPoly[xx])<<int(vv))
  vv+=bbits

print("Original Data: ", data)
print("Reconstructed Data: ", rData)
pend()
print("Are they equal?",end=" ")
print(data==rData)
