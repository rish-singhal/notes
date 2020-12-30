from random import randint
from sympy import Matrix
import numpy as np
import socket              
import json

s = socket.socket()          
print("Socket successfully created")

port = 1001
s.bind(('', port))         
print("socket binded to ",port)

s.listen(5)
print("Socket is listening")

## copied from Evaluation 1
h = 2
k = 6 #number of blocks
e = 3 #number of error blocks permissible
poly = []
numbits = 0


def power(a, b, c): 
    x = 1
    y = a 
  
    while b > 0: 
        if b % 2 == 0: 
            x = (x * y) % c; 
        y = (y * y) % c 
        b = int(b / 2) 
  
    return x % c 

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
    

def decryptEl(enc_mssg, privateKey):
  en_msg = enc_mssg['en_msg']
  p = enc_mssg['p']
  key = privateKey['key']
  q = privateKey['q']
  h = power(p, key, q)
  return en_msg//h

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

prime = 14654990447141419379
print("Prime: ", prime)

gen = 2
print("Generator: ",gen)

n = k + e
points = gen_points(n, prime)
print("Random n points evaluated: ", points)
pend()

secret = 3753978530724879923
y =  4496635397630804717

rn = randint(2, prime-1)
t = po(gen, rn, prime)

privateKey = {'secret':secret, 'prime':prime, 'gen':gen, 'y':y}
print("Private Key: ", privateKey)

publicKey = {'prime':prime, 'gen':gen, 'y':y }

privateKeyEl = {'g':2, 'q':14654990447141419379,
  'h':2046460228384107056, 'key': 4437044531233054673}
print("Public Key: ",publicKey)
print("Private Key Elgamel: ",privateKeyEl)
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

dataObj = json.dumps(signed)

def takeXor(r, point):
  val = {'m':{'x':0,'y':0}, 'sign':0}
  val['m']['x'] = r^point['m']['x'] 
  val['m']['y'] = r^point['m']['y']
  val['sign'] = point['sign']

  return val


while True: 
   c, addr = s.accept()      
   print('Got connection from ', addr) 
   mssg = c.recv(4096) 
   mssg = json.loads(mssg.decode())
   print("Got message from Client...")
   pend()
   if mssg['type'] == 1:
      print("Recieved Message")
      pend()
      rr = mssg['mssg1']
      print("Reconstructing Random Array")
      pend()
      print("Reconstructed : ", mssg)
      pend()
      rr = decryptEl(rr,privateKeyEl)
      print("Decrypting Random Value Recieved... ")

      rr2 = decryptEl(mssg['mssg2'],privateKeyEl)
      new_sign = []
      new_sign2 = []

      print("Taking Xor with n points to send, with e points corrupted... ")
      pend()
      for m in signed:
        new_sign.append(takeXor(rr,m))
        new_sign2.append(takeXor(rr2,m))
      print(new_sign)
      sentmssg = {'mssg1':new_sign, 'mssg2':new_sign2}
      print("Sent Mssg: ",sentmssg)
      pend()
      new_sign = json.dumps(sentmssg)
      c.send(new_sign.encode())
   else:
      print("Closing Connection")
      c.close() 
   




