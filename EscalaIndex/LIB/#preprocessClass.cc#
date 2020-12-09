/* linePreprocess.cc -
 * 	
 *          
 *
 * Copyright (C) 2019 by Moisés Pastor i Gadea (mpastorg@dsic.upv.es) 
 *                        PRHLT group
 *****************************************************************************/

// compilar:  g++ -o linePreprocess linePreprocess.cc -I. `pkg-config --cflags --libs opencv4`  -O3 


#include <iostream>
#include <fstream>
#include <unistd.h>
#include <stdlib.h>
#include <functional>
#include <opencv2/opencv.hpp>

#define ANG_RANGE 20
#define BLACK 0
#define UMBRAL_VERTICAL 1

using namespace std;
using namespace cv;

class preprocess {
private:
  Mat image_orig,image_bin;
  int threshold;
  bool verbosity;
  int finalNumberRows;

  int * getV_Projection();
  float stdev(int *VPr, int dim_proj); 
  int **get_projections_rotate(const Mat & image, int & dim_prj);
  int **get_projections_shear(const Mat & image, int & dim_prj);
  float MVPV(const Mat & image, string action);
  Mat crop(Mat & image_res);
  
public:
  preprocess(Mat image, float threshold=1,\
	     int finalNumberRows= 64, bool verbosity = false);
  Mat run();
};

preprocess::preprocess(Mat image, float threshold,		\
		       int finalNumberRows, bool verbosity){
    this->image_orig = image;
    this->threshold = threshold;
    this->image_bin = Mat(image.size(),image.type());     
    cv::threshold(image_orig, this->image_bin, 0, 255, cv::THRESH_BINARY | THRESH_OTSU);
    this->finalNumberRows = finalNumberRows;
    this->verbosity = verbosity;
  }


inline float preprocess::stdev(int *HPr,int dim_proj) {
  float sum=0, sum2=0, var=0, mean=0;

  
  for (int j=0; j<dim_proj; HPr++,j++){
    sum += (float)(*HPr);
    sum2 += (float)(*HPr)*(*HPr);
  }

  mean=sum/dim_proj;
  //var = sum2/dim_proj - mean*mean;
  var=(sum2 - 2 * mean * sum + sum2)/dim_proj;
  return sqrt(var);
} 

int * preprocess::getV_Projection(){ 
    /* Calculamos la proyeccion vertical */
    int * histver;
    int i,j;
    histver= new int [image_bin.cols];
    for (j=0; j < image_bin.cols; j++)
        histver[j]=0;
    
    for (j=0; j < image_bin.cols; j++) {
      for (i=0; i < image_bin.rows ; i++) 
	if (image_bin.at<uchar>(i,j) == BLACK){ 
	  histver[j]++;
	}      
    }   

    return histver;
}


int ** preprocess::get_projections_shear(const Mat & image, int & dim_prj){
  int desp[2*ANG_RANGE+1];
  int ** proj;
  //  const uchar * pcol;
  
  dim_prj=image.cols+2*image.rows ;
  int despl_inicial=0;
  
  /* Pedimos memoria para las proyecciones */
  proj = new int*[2*ANG_RANGE+1];
  for (int i=0; i<=2*ANG_RANGE; i++) {
    proj[i] = new int[dim_prj];
    for (int col=0; col<dim_prj; col++)
      proj[i][col]=0; // Inicialización
  }

  /* Calculamos las proyecciones */
  for (int row=0;row<image.rows;row++){
    for (int a=0;a<=2*ANG_RANGE;a++)
      desp[a]=(int)((image.rows-row)*tan((float)(a-ANG_RANGE)*M_PI/180.0)); /* todos los  despl para  cada fila */
    
    const uchar *pcol=&image.at<uchar>(row,0);
    for (int col=0; col < image.cols; pcol++, col++)
      if (*pcol == BLACK)         /* lo tenemos en cuenta */
	for (int a=0;a<=2*ANG_RANGE;a++)          
	  if ((despl_inicial+col+desp[a]) >= 0 && (despl_inicial+col+desp[a]) < dim_prj)
	    proj[a][despl_inicial+col+desp[a]]++;
          
  }
  return proj;

}
int ** preprocess::get_projections_rotate(const Mat & image, int & dim_prj){
  int ** proj;
  

  dim_prj = (int)(2*sqrt(image.cols*image.cols+image.rows*image.rows/4));


  /* Pedimos memoria para las proyecciones y las inicializamos */
  proj = new int*[2*ANG_RANGE+1];
  for (int i=0; i<=2*ANG_RANGE; i++) {
    //proj[i] = (int *)malloc(sizeof(int)*dim_prj);
    proj[i] = new int[dim_prj];
    for (int row=0; row<dim_prj; row++) proj[i][row]=0; // Inicialización
  }

  /* Calculamos las proyecciones */
  for (int col=0; col<image.cols; col++)
    for (int row=0; row<image.rows; row++) 
      if (image.at<uchar>(row,col) == BLACK)  /* lo tenemos en cuenta */
	for (int a=0; a<=2*ANG_RANGE; a++) {      /* si es suficientemente negro */

	  int desp =  (int)((image.rows/2.0-row)*cos((float)(a-ANG_RANGE)*M_PI/180.0)\
			+ col*sin((float)(a-ANG_RANGE)*M_PI/180.0));
	  
	  if ((dim_prj/2+desp>=0) && (dim_prj/2+desp<dim_prj))
	    proj[a][dim_prj/2+desp]++;
	}
  
  return proj;
}

float preprocess::MVPV(const Mat & image, string action) {

 float var_max, var[2*ANG_RANGE+1];
  int ** proj;
  int  dim_prj;



 if (action == "slant")
   proj = get_projections_shear(image, dim_prj); //get_projections2(image, &preprocess::get_despl_slant2);     
 else if (action == "slope")
   proj = get_projections_rotate(image, dim_prj);//get_projections2(image, &preprocess::get_despl_slope2);
 else return 0.0;

  
 //  dim_prj = 2*sqrt(image.cols*image.cols+image.rows*image.rows/4);

  var_max = -1;
  
  for (int a=-ANG_RANGE; a<=ANG_RANGE; a++) {
    var[a+ANG_RANGE] = stdev(proj[a+ANG_RANGE],dim_prj);
    if (var_max < var[a+ANG_RANGE]) {
      var_max=var[a+ANG_RANGE];
    }
  }

  if (var_max == -1) return 0;
  // if (verbosity){
  //   cerr <<"#angle variance for "<< action<< endl;
  //   cerr <<"#----------------"<<endl;
  //   for (int a=-ANG_RANGE; a<=ANG_RANGE; a++)
  //     cerr << a << "  " << var[a+ANG_RANGE] << endl;  
  // }

  /* calculamos la media ponderada de todas las varianzas (centro de masas)
     que esten por debajo de un procentaje (threshold) del maximo */
  float sum=0;
  float cont=0;
  for (int a=-ANG_RANGE; a<=ANG_RANGE; a++){
    if (var[a+ANG_RANGE] >= var_max*threshold) {
      sum += var[a+ANG_RANGE] * a;
      cont += var[a+ANG_RANGE];      
    }
  }
  
  /* Liberamos la memoria de las proyectiones */
  for (int a=0; a<=2*ANG_RANGE; a++) free(proj[a]);
  free(proj);
  
  // Devuelve el valor de SLOPE del segmento en grados
  return(-sum/(1.0*cont));
}

Mat preprocess::crop(Mat & image){

   vector<vector<Point> > contours;
   vector<Vec4i> hierarchy;

   Mat img(image.size(), image.type());

   int pad=3;
   copyMakeBorder( image, img, pad, pad, pad,  pad , BORDER_CONSTANT, Scalar(255) );

   cv::threshold( img,img, 0, 255, THRESH_BINARY  | THRESH_OTSU);
   
   
   Mat img2(image.size(), image.type());
   img.copyTo(img2);

   cv::Mat element = cv::getStructuringElement(cv::MORPH_RECT , cv::Size(7, 3));
   cv::erode(img, img, element);
 
   findContours(img, contours, hierarchy, RETR_CCOMP, CHAIN_APPROX_SIMPLE, Point(0, 0) );

  
   /// Find the convex hull object for each contour
   vector<vector<Point> >hull( contours.size() );

   vector<Point> contour;
   float superficieMax=0;
   int contourMaxSuperficie=1;
   for( uint i = 0; i < contours.size(); i++ )  {
     
     if ( hierarchy[i][3] != -1 && contours[i].size() > 4){
       convexHull( Mat(contours[i]), hull[i] );
       approxPolyDP(Mat(hull[i]), contour, 0.001, true);
       float sup =  contourArea(hull[i]);
       if (sup > superficieMax){
	 superficieMax=sup;
	 contourMaxSuperficie = i;
       }
       // cout << i<< " " << contourArea(hull[i])<< " " << hull[i].size() << endl;
     }
   }
   
   // for( int i = 0; i< hull.size(); i++ )    {
   //   //drawContours( img, contours, i, Scalar(255), 1, 8, vector<Vec4i>(), 0, Point() );
   //   //if (i==contourMaxSuperficie)
   //   drawContours( img, hull, i, Scalar(255), 1, 8, vector<Vec4i>(), 0, Point() );
   // }
   // imwrite("kkk.jpg", img);
   // exit(-1);


   // float sum_max_y=0, sum_min_y=0;
   // int cont=0;
   // for (int i = 0; i < hull.size(); i++) {
   //   if (hull[i].size() > 14){
   //     cont++;
   //     int max_y=-1, min_y=100000;
   //     for (int h = 0; h < hull[i].size(); h++) {
   // 	 int y = hull[i][h].y;
   // 	 if (y > max_y) max_y = y;
   // 	 if (y < min_y) min_y = y;
   //     }
   //     sum_max_y+=max_y;
   //     sum_min_y+=min_y;
   //   }
   // }
   // //sum_max_y = sum_max_y/hull.size();
   // //sum_min_y = sum_min_y/hull.size();
   // sum_max_y = sum_max_y/cont;
   // sum_min_y = sum_min_y/cont;

  
  
   // int incr   = (sum_max_y - sum_min_y )*0.8;
   // //int y_orig =  sum_min_y - incr > 0 ?  sum_min_y-incr: 0;
   // int y_orig =  sum_min_y > 0 ?  sum_min_y: 0;
   // //int altura = (sum_max_y - sum_min_y) + incr*2 + y_orig < image.rows ? (sum_max_y - sum_min_y)+incr*2.0: image.rows - y_orig;
   // int altura = (sum_max_y - sum_min_y) + y_orig < image.rows ? (sum_max_y - sum_min_y): image.rows - y_orig;

     int altura = -1;
     int y_orig = 0;
     // for (int i = 0; i < hull.size(); i++) {
     //   if (contourMaxSuperficie==i)
     //       if (hull[i].size() > 4){
     int max_y=-1, min_y=100000;
     for (uint h = 0; h < hull[contourMaxSuperficie].size(); h++) {
       int y = hull[contourMaxSuperficie][h].y;
       if (y > max_y) max_y = y;
       if (y < min_y) min_y = y;
     }
     if (max_y-min_y > altura){
       altura = max_y-min_y;
       y_orig = min_y;
     }
     //   }
     // }

     altura = altura > -1 ? altura: img.rows;
     

     
//crop derecha  --------------------------
  
   int c_fin;
    for (c_fin=img2.cols-1; c_fin>=0;c_fin--){
      int N_pixels=0;
      for(int r=0;r<img2.rows;r++)
        if(img2.at<uchar>(r,c_fin) == BLACK)
          N_pixels++;
      if (N_pixels >= 5)  break;
    }
    c_fin = c_fin + 5 < img2.cols ? c_fin+5 : img2.cols-1;
  
    // crop izquierda ¿?
    int c_ini;
    for (c_ini=0; c_ini < img2.cols; c_ini++){
      int N_pixels=0;
      for(int r=4;r< img2.rows;r++)
        if(img2.at<uchar>(r,c_ini) == BLACK)
          N_pixels++;

      if (N_pixels >= 5)  break;
	      
    }
    c_ini = c_ini -5 > 0? c_ini - 5: 0;


    if (c_ini > c_fin){
      c_ini=0;
      c_fin=image.cols -1;
    }

    c_ini = c_ini - pad >= 0 ? c_ini - pad: 0;
    c_fin = c_fin < image.cols ? c_fin: image.cols-1;
    y_orig = y_orig - pad >= 0 ? y_orig-pad: 0;
    altura = altura + y_orig < image.rows ? altura: image.rows - y_orig;
    Rect rectCrop(c_ini, y_orig, c_fin-c_ini, altura);       
    image = Mat(image, rectCrop);


   float factor=float(this->finalNumberRows)/image.rows;
   cv::resize(image, image, cv::Size(int(image.cols*factor), this->finalNumberRows), 0, 0, INTER_LANCZOS4);// CV_INTER_LINEAR);



   return image;
}

Mat preprocess::run(){
  
  Mat fixedImage;
  cv::Mat shear_transf(2,3,CV_64F, Scalar(0.0));     
 
  //int desp_inicial=0;

  Mat croppedImage_bin(image_bin);
  Mat croppedImage_orig(image_orig);
  
    
  double rotate_angle = MVPV(croppedImage_bin, "slope");

  /// Rotate the warped image
  if (rotate_angle < -1 || rotate_angle > 1){      
      
    float scale = 1.0;
    Point center(croppedImage_bin.cols/2 , croppedImage_bin.rows/2);
    Mat rot_mat = getRotationMatrix2D( center, -rotate_angle, scale );
    //# compute the new bounding dimensions of the image
    //new_W = int((h * sin) + (w * cos))
    //new_H = int((h * cos) + (w * sin))
    double abs_cos = abs(rot_mat.at<double>(0,0));
    double abs_sin = abs(rot_mat.at<double>(0,1));
    
    int bound_w = int(croppedImage_bin.rows * abs_sin + croppedImage_bin.cols * abs_cos);
    int bound_h = int(croppedImage_bin.rows * abs_cos + croppedImage_bin.cols * abs_sin);
    
    rot_mat.at<double>(0, 2) += bound_w/2 - center.x;
    rot_mat.at<double>(1, 2) += bound_h/2 - center.y;

    cout << "-------------------------------------------------" << endl;
    warpAffine( croppedImage_bin, croppedImage_bin,  rot_mat, Size(bound_w, bound_h), INTER_LINEAR, BORDER_CONSTANT, Scalar(255));
    warpAffine( croppedImage_orig, croppedImage_orig, rot_mat, Size(bound_w, bound_h), INTER_LINEAR, BORDER_CONSTANT, Scalar(255));       
  }

 
  double shear_angle  = MVPV(croppedImage_bin, "slant");
  
  /// Shear the image
  if (shear_angle < -1 || shear_angle > 1){
    shear_transf.at<double>(0,0) = 1;    
    shear_transf.at<double>(1,1) = 1;
    shear_transf.at<double>(0,1) = tan(shear_angle*M_PI/180.0);

        
    // Point center( bound_w/2 -250 , bound_h/2);
    //Point center(int(cos(shear_angle*M_PI/180.0) *  croppedImage_orig.rows)/2.0),
    
    //pt = cv::Point2f(pt.x + pt.y*Bx, pt.y );
    
    // shear_transf.at<double>(0, 2) += (  center.x);
    // shear_transf.at<double>(1, 2) += (  center.y);
    
    
    int bound_w = int(sin(shear_angle*M_PI/180.0) *  croppedImage_orig.rows);
    //    int bound_h = int(cos(shear_angle*M_PI/180.0) *  croppedImage_orig.rows);
    
    if(  shear_transf.at<double>(0,1) > 0)
      copyMakeBorder( croppedImage_bin, croppedImage_bin, 0, 0, 0,  bound_w , BORDER_CONSTANT, Scalar(255) );
    else
      copyMakeBorder( croppedImage_bin, croppedImage_bin, 0, 0, -bound_w, 0 , BORDER_CONSTANT, Scalar(255) );
    

    
    warpAffine(croppedImage_orig, croppedImage_orig, shear_transf, croppedImage_bin.size(), INTER_LINEAR, BORDER_CONSTANT, Scalar(255));
    warpAffine(croppedImage_bin,  croppedImage_bin,  shear_transf, croppedImage_bin.size(), INTER_LINEAR, BORDER_CONSTANT, Scalar(255));

  }
  
  
  if (verbosity){
    cerr << ", shear angle: "  <<  shear_angle;
    cerr << " rotate angle: " <<  rotate_angle << endl;
    
  }     

  //return crop(croppedImage_orig);
  return (croppedImage_orig);
}


