#include<bits/stdc++.h>
using namespace std;

#include "matplotlibcpp.h"
namespace plt = matplotlibcpp;


int main() {
  // to take the first line as input
  //  and saving it into temp ... which won't be used

  ifstream fin;
  cout << "INPUT 1: Enter x, y, z and dx, dy, dz\n";
  double x, y, z, dx, dy, dz;

  cin >> x >> y >> z >> dx >> dy >> dz;

  cout << "Enter File Name (xyz.pdb):\n";
  string filename; 
  cin >> filename;
  
  fin.open(filename, ios::in);
  
  if(fin.fail())
  {
    cout << filename << " : This file does not exist !!\n";
    return 0;
  }

  string temp;
  for(int i = 0; i < 10; i++) {
    fin >> temp;
    if(!i && temp == "END")
      cout << "Empty File\n";
    cout << temp << endl;
  }

  int framecount = 0, count = 0;
  vector <double> outp; 
  while(!fin.eof())
  { 
    string st = "";
    while(!(st == "ATOM" || st == "END"))
      fin >> st;

    if(st == "END") {
      cout << "FRAME " << framecount <<" DONE!\n" <<endl;
      outp.push_back(count); 
      if(framecount == 250)
        break;
      framecount++;
      count = 0;
      continue;
    }
    if(st == "ATOM"){
         double count2, temp1, xx, yy, zz;
         string temp2;
         fin >> count2 >> temp2 >> temp2 >> temp1 >> xx >> yy >> zz >>temp1 >> temp1 >> temp2;
         cout << "READING ATOM: "<< count2 << " " << xx <<" "<< yy <<" "<< zz << endl;        
         if((xx >= x - (dx/2.0)) && (xx <= x + (dx/2.0)))
          if((yy >= y - (dy/2.0)) && (yy <= y + (dy/2.0)))
           if((zz >= z - (dz/2.0)) && (zz <= z + (dz/2.0)))
            count++;  
    }
   }

   for(auto &n: outp)
    n /= (dx*dy*dz);
  
   double average = accumulate(outp.begin(), outp.end(), 0.0/ outp.size());
   cout << "Average density: " << average << endl;
  
   vector <int> xax(outp.size());
   iota(xax.begin(), xax.end(), 0);  

   fin.close( );       //close file
   assert(!fin.fail( ));  

   return 0;
}
     

