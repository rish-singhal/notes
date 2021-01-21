#include<bits/stdc++.h>
using namespace std;

int main() {
  // to take the first line as input
  //  and saving it into temp ... which won't be used

  ifstream fin;
  cout << "INPUT 2: Enter x, y, z and dx, dy, dz FOR FIRST POINT:\n";
  double x, y, z, dx, dy, dz;

  cin >> x >> y >> z >> dx >> dy >> dz;
  
  cout << "INPUT 2: Enter x, y, z and dx, dy, dz FOR SECOND POINT:\n";
  double x2, y2, z2, dx2, dy2, dz2;

  cin >> x2 >> y2 >> z2 >> dx2 >> dy2 >> dz2;


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

  int framecount = 0, count = 0, countx = 0;
  
  int outp = 0;

  while(!fin.eof())
  { 
    string st = "";
    while(!(st == "ATOM" || st == "END"))
      fin >> st;

    if(st == "END") {
      cout << "FRAME " << framecount <<" DONE!\n" <<endl;
      if(count && countx)
        outp++;
      if(framecount == 250)
        break;
      framecount++;
      count = countx = 0;
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

         if((xx >= x2 - (dx2/2.0)) && (xx <= x2 + (dx2/2.0)))
           if((yy >= y2 - (dy2/2.0)) && (yy <= y2 + (dy2/2.0)))
             if((zz >= z2 - (dz2/2.0)) && (zz <= z2 + (dz2/2.0)))
               countx++;  
    }
   }
  
   cout << "Number of timestamps where both are non empty: " << outp << endl;

   fin.close();       //close file
   assert(!fin.fail());
   return 0;
}
     

