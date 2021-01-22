#include<bits/stdc++.h>
using namespace std;

float round2(double var) 
{ 
    // 37.66666 * 100 =3766.66 
    // 3766.66 + .5 =3767.16    for rounding off value 
    // then type cast to int so value is 3767 
    // then divided by 100 so the value converted into 37.67 
    float value = (int)(var * 100 + .5); 
    return (float)value / 100; 
} 

int main() {
  // to take the first line as input
  //  and saving it into temp ... which won't be used

  ifstream fin;

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

  int framecount = 0;
  vector <double> xc, yc, zc;

  while(!fin.eof())
  { 
    string st = "";
    while(!(st == "ATOM" || st == "END"))
      fin >> st;

    if(st == "END") {
     // cout << "FRAME " << framecount <<" DONE!\n" <<endl;
      if(framecount == 250)
        break;
      framecount++;
      continue;
    }
    if(st == "ATOM"){
         double count2, temp1, xx, yy, zz;
         string temp2;
         fin >> count2 >> temp2 >> temp2 >> temp1 >> xx >> yy >> zz >>temp1 >> temp1 >> temp2;
        // cout << "READING ATOM: "<< count2 << " " << xx <<" "<< yy <<" "<< zz << endl; 
        if(framecount == 250) {
         xc.push_back(xx);
         yc.push_back(yy);
         zc.push_back(zz);
     }
    }
   }
  
   int num = (int) xc.size();

   map <float, int> distcount;

   for(int i = 0; i < num; i++)
   	 for(int j = i + 1; j < num; j++) {
   	 	// calculate distance between pairs
   	 	double dist = sqrt((xc[i] - xc[j])*(xc[i] - xc[j]) + (yc[i] - yc[j])*(yc[i] - yc[j]) + (zc[i] - zc[j])*(zc[i] - zc[j]));
   	 	distcount[round2(dist)]++;

   	 }
   
   for(auto v: distcount)
   	cout << v.first << " ," << v.second << endl;

   fin.close();       //close file
   assert(!fin.fail());
   return 0;
}
     

