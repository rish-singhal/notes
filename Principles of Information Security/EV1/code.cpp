#include<bits/stdc++.h>
using namespace std;
typedef long long LL;
#define fi first
#define se second

LL po(LL a, LL n, LL p){
  if(n==0) return 1;
  LL an = po(a,n/2,p);
  an = (an*an)%p;
  if(n&1) return an*a%p;
  return an;
}

bool isprime(LL n) {
  int tc = 1000;
  if(n==1) return 0;
  if(tc>=n) tc = n-1;
  forn(i,tc){
    LL range = (n-1);
    LL num = rand() % range + 1;
    if(po(num, n-1, n)!=1)
      return 0;
  }
    return 1;
}
    

auto signature(int n) -> pair<LL,LL> {
   // LL k = rand();
   LL k = 2;
   // g is generator, p is prime...
   /*
    * generate x also. 
    */
   LL r = po(g,k,p);
   LL e = hashing(conc(r,m));
   LL s = k - x*e;
   return {s,e};
}

// rv = g.s y.e
auto verify(pair<int,int> sign) ->bool{
  LL s = sign.fi;
  LL e = sign.se;
  LL rv = (po(g,s,p)*po(y,e,p))%p;
  LL ev = hashing(conc(rv,m));
  if(ev == e){
    cout<<"Verified"<<endl;
  }
  else cout<<"Not Verified"<<endl;
}

auto generate(int n) -> {
    
}

int main(){
  int n; cin>>n;
  
}

