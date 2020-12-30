
from random import randint
from sympy import Matrix
import numpy as np
import socket      
import json

k = 6
h = 2
e = 3

port = 1001

def pend():
  print(" ")

def power(a, b, c): 
    x = 1
    y = a 
  
    while b > 0: 
        if b % 2 == 0: 
            x = (x * y) % c; 
        y = (y * y) % c 
        b = int(b / 2) 
  
    return x % c 

def po(a,n,p):
    if n==0:
      return 1
    an = po(a,n//2,p)
    an = (an*an)%p
    if (n%2):
      return (an*a)%p
    return an

def isprime(p):
    if p == 1:
        return False
    for x in range(min(1000,p-1)):
        ran = randint(1, p - 1)
        if po(ran, p-1, p) != 1:
            return False
    return True

def gcd(a, b):
	
	if a < b:
		return gcd(b,a)
	elif a%b == 0:
		return b
	else:
		return gcd(b, a%b)


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

def gen_key(q): 
  
    key = randint(22, q) 
    while gcd(q, key) != 1: 
        key = randint(22, q) 
  
    return key 

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
  
def encrypt(mssg, publicKey):
	q = publicKey['q']
	g = publicKey['g']
	h = publicKey['h']
	
	k = gen_key(q)
	s = power(h, k, q)
	p = power(g, k, q)
	
	enc_mssg = {}
	enc_mssg['en_msg'] = s*mssg
	enc_mssg['p'] = p

	return enc_mssg

def takeXor(r, point):
  val = {'m':{'x':0,'y':0}, 'sign':0} 
  val['m']['x'] = r^point['m']['x'] 
  val['m']['y'] = r^point['m']['y']
  val['sign'] = point['sign']

  return val

publicKeyEl = {'g': 2, 'q': 14654990447141419379,'h':2046460228384107056}

publicKey = {'prime':14654990447141419379, 'gen':2, 'y':4496635397630804717 }


print("Public Key Elgamel: ",publicKeyEl)
print("Public Key for Digital Signature: ", publicKey)
pend()

s = socket.socket()         


s.connect(('127.0.0.1', port))   
print("Connecting with Server.....")
pend()

r = randint(1,221413242)
#r = 100474728
random2 = {}
random2['en_msg'] = randint(1,221413242)
random2['p'] =  randint(1,221413242)

sent = {'type':1, 'mssg1':encrypt(r,publicKeyEl), 'mssg2': random2}


print("Generating Random Array with 1st index Encrypted... \n : ", sent)
pend()
print("Generating N points from the Polynomial Whose coefficients are these random values")
pend()
print("Sending the n points of polynomial... \n : ", sent)
pend()
snmmsg =json.dumps(sent)
s.send(snmmsg.encode())

rec  = s.recv(4096) 
rec = json.loads(rec.decode())
rec = rec['mssg1']
print("Recieves Message from Server...")
pend()

signed = []

print("Takes 1st index and Xor it with random Value Sent...")
pend()
for m in rec:
     signed.append(takeXor(r,m))


snmmsg =json.dumps({'type':2})
s.send(snmmsg.encode())
s.close()        


prime = 14654990447141419379
gen = 2

pend()
safepoints = verifypoints(signed, publicKey)
pend()

print("Uncorrupted k points: ",safepoints )
pend()

print("Reconstructing polynomial with these k points")
rPoly = reconstruct(safepoints, prime)
pend()
print("Reconstructed Polynomial: ",rPoly)
pend()
