/*
 *   Copyright 2020, Moisés Pastor i Gadea
 *
 *   Licensed under the Apache License, Version 2.0 (the "License");
 *   you may not use this file except in compliance with the License.
 *   You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 *
 * 
 * translate.cpp
 *
 *  Created on: 25/11/2020
 *      Author: Moisés Pastor i Gadea
 */
// compile: g++ -o escalaIndex escalaIndex.cc ./libXmlPAGE.cc ./libPoints.o  `pkg-config --cflags --libs opencv4` -lpugixml  -O3

#include <unistd.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>

#include <opencv2/opencv.hpp>
#include "pugixml.hpp"
#include <libXmlPAGE.h>

using namespace cv;
using namespace std;
//---------------------------------------------------------------------
struct  k{
  bool operator() (cv::Point pt1, cv::Point pt2) { if(pt1.x < pt2.x) return true; else if (pt1.x > pt2.x) return false; else return pt1.x < pt2.y ;}
} sort_points_func;

//---------------------------------------------------------------------
//---------------------------------------------------------------------
struct k1{
  bool operator() (vector< Point > v1, vector < Point > v2){
    double sum_y_v1=0;
    for (unsigned int i = 0; i < v1.size(); ++i){
      sum_y_v1+=v1[i].y;
    }

    double sum_y_v2=0;
    for (unsigned int i = 0; i < v2.size(); ++i){
      sum_y_v2+=v2[i].y;
    }

    double mean_y_v1=sum_y_v1/v1.size();
    double mean_y_v2=sum_y_v2/v2.size();
    if (mean_y_v1 <= mean_y_v2) return true;
    else return false;
  }
} sort_lines_func;


//----------------------------------------------------------
void usage (char * programName){

  cerr << "Usage: "<<programName << " options " << endl;
  cerr << "      options:" << endl;
  cerr << "             -i idexPageName" << endl;
  cerr << "             -x baselinesFileName (XML PAGE format)" << endl;
  cerr << "             -o outputfile " << endl;
}
//----------------------------------------------------------
int main(int argc,  char ** argv) {
  string idxFileName="", outFileName="", xmlFileName="";
  int num_lin=-1; //vol dir totes les linies
  int option;
  
  if(argc == 1){
    usage(argv[0]);
    return -1;
  }

  while ((option=getopt(argc,argv,"i:o:x:v"))!=-1)
    switch (option)  {
    case 'i':
      idxFileName = optarg;
      break;
    case 'o':
      outFileName = optarg;
      break;
    case 'x':
      xmlFileName = optarg;
      break;
    default:
      usage(argv[0]);
      return(-1);
    }

  if (idxFileName.size()==0 || outFileName.size()==0 || xmlFileName.size()==0){
    cerr << argv[0] << " Error: input and output and xml file names must be provided" << endl;
    usage(argv[0]);
    return (-1);
  }
  

  pugi::xml_document page;
  pugi::xml_parse_result result = page.load_file(xmlFileName.c_str());
  if (!result){
    cerr << "ERROR: file: " << xmlFileName << " cannot not been opened" << endl;
    exit(-1);
  }
  int anchoPag = getWidth(page);

  map<string,vector<cv::Point> > line_id2Points;
  vector <LineStruct>  lines= getBaselines_id(page);

  /*for (int l = 0; l < lines.size(); l++) {
    std::sort(lines[l].lineStruct.begin(), lines[l].lineStruct.end(), sort_points_func);  
  }
  */

  for (int l = 0; l < lines.size(); l++) {
    line_id2Points[lines[l].name] = lines[l].linePoints;
  }
 //ordenem les linies
  //std::sort(lines.begin(), lines.end(), sort_lines_func);
  
  ifstream idxFile;
  idxFile.open(idxFileName.c_str());
  if(!idxFile){
    cerr << "Error: File \""<<idxFileName <<  "\" could not be open "<< endl;
    exit(-1);
  }
  
  ofstream outFile;
  outFile.open(outFileName.c_str());
  if(!outFile){
    cerr << "Error: File \""<<outFileName <<  "\" could not be open "<< endl;
    exit(-1);
  }
  
  string word, lin_id;
  float prob;
  int posX1, posX2, longX;
  while( idxFile >>  word >> prob >> posX1 >> posX2 >> longX >> lin_id){

    if (posX1 == posX2)
      continue; 

    
    float long_baseLine = anchoPag;

    vector <cv::Point> line = line_id2Points[lin_id];
    if (line.size()<=0) continue;
    
    float angle_baseline = atan((line[line.size()-1].y - line[0].y) / float(line[line.size()-1].x - line[0].x));

    int x1 = int(posX1 * (long_baseLine/longX));
    if (x1 < line[0].x){
      x1 = line[0].x;
    }

    int x2 = int(x1 + (posX2 - posX1)*(long_baseLine/longX));

    if (x1 == x2)
      continue;

    int i = 0;
    while (i < line.size()-1 && x1 < line[i+1].x ) i++;
    int j = 0;
    while (j < line.size()-1 && x2 < line[j+1].x) j++;

    if (i < j){
      x1 = line[i].x;
      x2 = line[j].x;
    }
    int y1 = int (x1 * tan(angle_baseline) + 0.5) + line[0].y;
    int y2 = int (x2 * tan(angle_baseline) + 0.5) + line[0].y;

    outFile << word << " "<<prob << " " << x1  << " " << y1 << " " << x2 << " " << y2 << endl;
    
  }


  idxFile.close();
  outFile.close();
  return 0;
}
