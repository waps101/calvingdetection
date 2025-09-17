# Detection of Glacier Calving Events From Time-Lapse Images

Lakhan Mankani<sup> 1</sup>, [William A. P. Smith](https://www-users.cs.york.ac.uk/waps101)<sup> 1</sup>, Oskar Głowacki<sup> 3</sup> and Paulina Lewińska<sup> 1,2</sup>
 <br/>
 <sup>1 </sup>Department of Computer Science, University of York, UK
 <br/>
 <sup>2 </sup>Department of Polar and Marine Research, The Institute of Geophysics, Polish Academy of Sciences,
 <br/>
 <sup>3 </sup>Faculty of Geo-Data Science, Geodesy, and Environmental Engineering, AGH University of Krakow
 <br/>

## Abstract
Ground-based time-lapse cameras are often used to monitor glacier recession which is primarily driven by the falling of ice from the glacier front, known as calvings or more commonly calving events. Glaciologists can utilise these images by manually identifying calving events, a laborious task that requires the analysis of thousands of images in order to identify image pairs that represent the glacier front before, during, and after calving. We present a computer vision based method to filter out images rendered unusable due to weather effects such as fog and precipitation by calculating the number of salient features detected in the image using the SIFT (Scale-Invariant Feature Transform) algorithm as an indicator of the visibility of the glacier front and discarding any image with fewer features than a defined threshold. We propose the use of SNN (Siamese neural network) and show that it is useful in detecting calving events since it allows to separately calculate features on two images and then merges them together in order to track differences between them thus detecting calving areas. The trained model achieved an overall accuracy of 92%, with 79% of calvings and 93% of non-calvings being correctly classified on an unseen test set formed from imagery in the same time period as the training data. The model was able to generalise to new time periods (and therefore small changes in viewpoint and alignment) to some extent with an overall accuracy of 82%, with 27% of calvings and 90% of non-calvings being correctly classified.

![Glacier calving animation](https://github.com/waps101/calvingdetection/blob/main/resources/Calving%20example.gif?raw=true)
