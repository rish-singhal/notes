### -------------- from evaluation 1

from random import randint
import sympy as sp
import numpy as np

numbits = 128

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


def hashfun(g, p, m):
    fb = m & ((1<<(numbits//2))-1)
    lb = m >> (numbits//2)
    return  po(g, lb, p)*po(h, fb, p)%p

def sign(priv, m):
    x = priv['secret']
    p = priv['prime']
    g = priv['gen']
    y = priv['y'] #public key
    rn = randint(2, p-1)
    t = po(g, rn, p)
    c = hash(m)%p
    z = c*x + rn
    return {'t':t,'z':z}

def verify(pub, m, signm):
    y = pub['y']
    t = signm['t']
    z = signm['z']
    g = pub['gen']
    p = pub['prime']
   # c = hashfun(g,p,m)
    c = hash(m)%p
    if po(g,z,p) == ((t*po(y,c,p))%p):
        return True
    return False

print("Generating Prime")
pend()
prime, fac = generate_prime(numbits)
#prime =  288067729799970807451858326285132490847
print("Prime: ", prime)

gen = generator(prime, fac)
#gen = 5
print("Generator: ",gen)
pend()

## h for hash-function
h = randint(2,prime-1)

def generateKeys():
    secret = randint(2,prime-1) 
    y = po(gen, secret, prime) 
    rn = randint(2, prime-1)
    t = po(gen, rn, prime)
    privateKey = {'secret':secret, 'prime':prime, 'gen':gen, 'y':y}
    publicKey = {'prime':prime, 'gen':gen, 'y':y }
    return {'private':privateKey, 'public':publicKey}

### -------------- end ----------------



###---- start of Linked List

class LinkedList:
  def __init__(self):
    self.hpointer_next = None
    self.address = {}
  
  def appendFront(self, data):
    NewBlock = Block(self, data, self.hpointer_next)
    self.hpointer_next = NewBlock.addkey
  
  def appendEnd(self, data):
    nxt_pointer = self.hpointer_next
    block = None
    while nxt_pointer:
      block = self.address[nxt_pointer]
      nxt_pointer = block.pointer_next

    NewBlock = Block(self, data, None)
    if block:
      block.pointer_next = NewBlock.addkey
    else :
      self.hpointer_next = NewBlock.addkey

  def traverseList(self):
    print("---------------------")
    print("Printing List------")
    pend()
    cnt = 1
    nxt_pointer = self.hpointer_next
    while nxt_pointer:
      block = self.address[nxt_pointer]
      if cnt == 1:
        print("Head: ",end=' ')
      else:
        print("Block ",cnt,": ",end=' ')
      print(block)
      pend()
      nxt_pointer = block.pointer_next
      cnt += 1

    print("End of the List-----")
    print("---------------------")
    pend()

class Block:
  def __init__(self, list, data, pointer_next):
    self.data = data
    self.pointer_next = pointer_next
    self.addkey = randint(1,1010101010)
    list.address[self.addkey] = self

  def __repr__(self):  
     return "data: % s, addkey: %s, pointer_next: % s" % (self.data, self.addkey, self.pointer_next) 


###---- end of Linked List


###---- start of Hash Linked List

class HashLinkedList:
  def __init__(self):
    self.hhash_next = None
    self.hpointer_next = None
    self.address = {}
  
  def appendBlock(self, data):
    NewBlock = HashBlock(self, data, self.hhash_next, self.hpointer_next)
    self.hhash_next = NewBlock.calc_hash()
    self.hpointer_next = NewBlock.addkey

  def traverseList(self):
    print("---------------------")
    print("Printing HashList------")
    pend()
    cnt = 1
    nxt_pointer = self.hpointer_next
    nxt_hash = self.hhash_next
    while nxt_pointer:
      block = self.address[nxt_pointer]
      if cnt == 1:
        print("Head: ",end=' ')
      else:
        print("Block ",cnt,": ",end=' ')
      print(block)

      if nxt_hash == block.calc_hash():
          print("### Block Hash Matches ###")
      else :
        print("### Block Hash Doesn't Match ###")
        break
      pend()
      cnt += 1
      nxt_pointer = block.pointer_next
      nxt_hash = block.hash_next
    print("End of the HashList-----")
    print("---------------------")
    pend()

class HashBlock:
  def __init__(self, list, data, hash_next, pointer_next):
    self.data = data
    self.hash_next = hash_next
    self.pointer_next = pointer_next
    self.addkey = randint(1,1010101010)
    list.address[self.addkey] = self

  def __repr__(self):  
     return "data: % s, hash: % s, addkey: %s, hash_next: % s, pointer_next: % s" % (self.data, self.calc_hash(), self.addkey,
                                                                                         self.hash_next, self.pointer_next) 

  def calc_hash(self):
    blck = [self.data, self.hash_next, self.pointer_next]
    dt =""
    for i in blck:
      if i:
        dt+=str(i)
      else:
        dt+="0"
    dt = int(dt)%prime
    return hashfun(gen, prime, dt)%prime


###---- end of Hashed Linked List


###---- start of Signed Hash Linked List

class SignHashLinkedList:
  def __init__(self):
    self.hhash_next = None
    self.hpointer_next = None
    self.hsign_next = {'t':None,'z':None}
    self.pid_next = None
    self.address = {}
  
  def appendBlock(self, data, pid):
    NewBlock = SignHashBlock(self, data, self.hhash_next, self.hpointer_next, self.hsign_next,self.pid_next)
    self.hhash_next = NewBlock.calc_hash()
    self.hpointer_next = NewBlock.addkey
    self.hsign_next = ids[pid].psign(self.hhash_next)
    self.pid_next = pid 
   

  def traverseList(self):
    print("---------------------")
    print("Printing SignedHashList------")
    pend()
    cnt = 1
    
    nxt_pointer = self.hpointer_next
    nxt_hash = self.hhash_next
    nxt_sign = self.hsign_next
    nxt_pid = self.pid_next

    while nxt_pointer:
      block = self.address[nxt_pointer]  
      if cnt == 1:
        print("Head: ",end=' ')
      else:
        print("Block ",cnt,": ",end=' ')
      print(block)

      if verify(ids[nxt_pid].publicKey,block.calc_hash(),nxt_sign):
        print("### Block Signature Verified ###")
      else :
        print("### Block Signature Corrupted ###")
        break
      pend()
      cnt += 1

      nxt_pointer = block.pointer_next
      nxt_hash =  block.hash_next
      nxt_sign = block.sign_next
      nxt_pid = block.pid_next

    print("End of the SignedHashList-----")
    print("---------------------")
    pend()

class SignHashBlock:
  def __init__(self, list, data, hash_next, pointer_next, sign_next, pid_next):
    self.data = data
    self.hash_next = hash_next
    self.sign_next = sign_next
    self.pointer_next = pointer_next
    self.pid_next = pid_next
    self.addkey = randint(1,1010101010)
    list.address[self.addkey] = self

  def __repr__(self):  
     return "data: % s, hash: % s, addkey: %s, hash_next: % s, sign_next: % s, pointer_next: % s" % (self.data, self.calc_hash(), self.addkey,
                                                                                         self.hash_next, self.sign_next, self.pointer_next) 

  def calc_hash(self):
    blck = [self.data, self.hash_next, self.pointer_next, self.sign_next['t'], self.sign_next['z']]
    dt =""
    for i in blck:
      if i:
        dt+=str(i)
      else:
        dt+="0"
    dt = int(dt)%prime
    return hashfun(gen, prime, dt)%prime

###---- end of Signed Hashed Linked List


class Person:
  def __init__(self):
     keys = generateKeys()
     self.__privateKey = keys['private']
     self.publicKey = keys['public']

  def psign(self, m):
    return sign( self.__privateKey,m)

ids = {}

for i in range(10):
  ids[i] = Person()

List = LinkedList()
HList = HashLinkedList()
SHList = SignHashLinkedList()

print("Adding a node to Linked List at End --- ")
List.appendEnd("324234325")
print("Traversing Linked List ---")
List.traverseList()
pend()
print("Adding a node to Linked List at End --- ")
List.appendEnd("42353")
print("Traversing Linked List ---")
List.traverseList()
print("Adding a node to Linked List in Front --- ")
List.appendFront("3251")
print("Traversing Linked List ---")
List.traverseList()
pend()

print("Adding a node to Hashed Linked List --- ")
HList.appendBlock("6545")
print("Traversing Linked List ---")
HList.traverseList()
pend()

print("Adding a node to Hashed Linked List --- ")
HList.appendBlock("7657")
print("Traversing Hashed Linked List ---")
HList.traverseList()
pend()

print("Adding a node to Hashed Linked List --- ")
HList.appendBlock("09070709")
print("Traversing Hashed Linked List ---")
HList.traverseList()
pend()

print("Person 1 adds a node to Signed Hashed Linked List-- ")
SHList.appendBlock("312424",1)
print("Traversing Signed Hashed Linked List ---")
SHList.traverseList()
pend()

print("Person 2 adds a node to Signed Hashed Linked List-- ")
SHList.appendBlock("42351",2)
print("Traversing Signed Hashed Linked List ---")
SHList.traverseList()
pend()