def check_module_phase_stretch_transform():
	print("phase_stretch_transform.py  |  OK!");


############# Phase stretch transform (PST) from UCLA Jalali Lab by Madhuri Suthar #############
"""
Implementation of Phase Stretch Transform (PST) in Python
@author: Madhuri Suthar, Ph.D. candidate, Jalali Lab, Department of Electrical and Computer Engineering,  UCLA
PST or Phase Stretch Transform is a physics-inspired edge detection algorithm that detects intensity variations in an image [1,2]. 
PST operates on an input greyscale image and outputs an edge map. The output egde map, same as the size of the input image, is binary with 
pixel value equal to 1 where the PST operator finds sharp transitions in intensity and 0 elsewhere. The PST operator can also return 
a continous level edge map (i.e. without thresholding and morphological operations)
The PST operator cascades Gaussian smoothing, application of a nonlinear frequency-dependent phase kernel in frequency domain and a phase detection in spatial domain.
To implement the first step, an isotropic gaussian filter with a user defined scale (LPF) is designed and operated on the image. 
Next, a 2D PST phase kernel is designed in frequency domain and applied to the spectrum of the input image. The output of the transform is the
phase in the spatial domain. The amount of phase applied to the image is frequency dependent with higher amount of phase applied to higher frequency features of the
image. Since sharp transitions, such as edges and corners, contain higher frequencies, PST emphasizes the edge information. Features can
be further enhanced by applying thresholding and morphological operations.
For more information please visit: https://en.wikipedia.org/wiki/Phase_stretch_transform
[out PST_Kernel]= PST(Image,LPF,Phase_strength,Warp_strength, Threshold_min, Threshold_max, Morph_flag) takes the image I and applies
PST phase kernel parameters are described as follows:
Parameters
----------
LPF            : Isotropic Gaussian localization filter Full Width at Half Maximum (FWHM) (min : 0, max : 1)
Phase_strength : PST Kernel Phase Strength (min : 0, max : 1)
Warp_strength  : PST Kernel Warp Strength (min : 0, max : 1)
Threshold_min  : minimum threshold  (min : -1, max : 0)
Threshold_max  : maximum threshold  (min : 0, max : 1)
Morph_flag allows user to compute the analog edge (if Morph_flag=0) or the digital edge (analog edge followed
by thresholding and morphological operations, if Morph_flag=1).                                                    
Copyright
---------
PST function  is developed in Jalali Lab at University of California,
Los Angeles (UCLA).  PST is a spin-off from research on the photonic time stretch technique in Jalali lab at UCLA.
More information about the technique can be found in our group
website: http://www.photonics.ucla.edu
This function is provided for research purposes only. A license must be
obtained from the University of California, Los Angeles for any commercial
applications. The software is protected under a US patent.
 
Citations
---------
1. M. H. Asghari, and B. Jalali, "Edge detection in digital images using dispersive phase stretch," International Journal of Biomedical Imaging, Vol. 2015, Article ID 687819, pp. 1-6 (2015).
2. M. H. Asghari, and B. Jalali, "Physics-inspired image edge detection," IEEE Global Signal and Information Processing Symposium (GlobalSIP 2014), paper: WdBD-L.1, Atlanta, December 2014.
3. M. Suthar, H. Asghari, and B. Jalali, "Feature Enhancement in Visually Impaired Images", IEEE Access 6 (2018): 1407-1415.
4. Y. Han, and B. Jalali, "Photonic time-stretched analog-to-digital converter: Fundamental concepts and practical considerations", Journal of Lightwave Technology 21, no. 12 (2003): 3085.
"""
# Imports
# [] Need to install mahotas library for morphological operations
import os
import math
import numpy as np
import mahotas as mh 
import matplotlib.pylab as plt
from itertools import zip_longest

# Define functions
def cart2pol(x, y):
     theta = np.arctan2(y, x)
     rho = np.hypot(x, y)
     return (theta, rho)    
    
def PST(I,LPF,Phase_strength,Warp_strength, Threshold_min, Threshold_max, Morph_flag):
     L=0.5
     x = np.linspace(-L, L, I.shape[0])
     y = np.linspace(-L, L, I.shape[1])
     [X1, Y1] =(np.meshgrid(x, y))
     X=X1.T
     Y=Y1.T
     [THETA,RHO] = cart2pol(X,Y)
 
     # Apply localization kernel to the original image to reduce noise
     Image_orig_f=((np.fft.fft2(I)))  
     expo = np.fft.fftshift(np.exp(-np.power((np.divide(RHO, math.sqrt((LPF**2)/np.log(2)))),2)))
     Image_orig_filtered=np.real(np.fft.ifft2((np.multiply(Image_orig_f,expo))))
        
     # Constructing the PST Kernel
     PST_Kernel_1=np.multiply(np.dot(RHO,Warp_strength), np.arctan(np.dot(RHO,Warp_strength)))-0.5*np.log(1+np.power(np.dot(RHO,Warp_strength),2))
     PST_Kernel=PST_Kernel_1/np.max(PST_Kernel_1)*Phase_strength
    
     # Apply the PST Kernel
     temp=np.multiply(np.fft.fftshift(np.exp(-1j*PST_Kernel)),np.fft.fft2(Image_orig_filtered))
     Image_orig_filtered_PST=np.fft.ifft2(temp)

     # Calculate phase of the transformed image
     PHI_features=np.angle(Image_orig_filtered_PST)
     
     if Morph_flag ==0:
         out=PHI_features
     else:
         #   find image sharp transitions by thresholding the phase
         features = np.zeros((PHI_features.shape[0],PHI_features.shape[1]))
         features[PHI_features> Threshold_max] = 1 # Bi-threshold decision
         features[PHI_features< Threshold_min] = 1 # as the output phase has both positive and negative values
         features[I<(np.amax(I)/20)]=0 # Removing edges in the very dark areas of the image (noise)
   
         # apply binary morphological operations to clean the transformed image 
         out = features
         out = mh.thin(out, 1)
         out = mh.bwperim(out, 4)
         out = mh.thin(out, 1)
         out = mh.erode(out, np.ones((1, 1))); 
   
     return (out, PST_Kernel)

# Three images that are outputted are the Original, PST Detection, PST Overlay
def PST_Output(file_path, filename):
	imaging_results = [];

	os.chdir(file_path);
	Image_orig = mh.imread("./" + filename) # Read the image. (Note this is a numpy obj array)

	# Truncate the transperency of the 4th value in each channel (R,G,B,T) --> (R,G,B) using splicing
	# Image_orig = Image_orig[:, :, :3];

	if (Image_orig.ndim == 3) :
	    Image_orig_grey = mh.colors.rgb2grey(Image_orig)  # Image_orig is color image.
	else: 
	    Image_orig_grey = Image_orig;
	# Define various 
	# low-pass filtering (also called localization kernel) parameter
	# LPF = 0.15 # Gaussian Low Pass Filter
	LPF = 0.15 # Gaussian Low Pass Filter

	# PST parameters
	# NOTE THIS NEEDS AUTOMATIC FINE TUNING!
	Phase_strength = 0.48
	# Phase_strength = 100
	Warp_strength= 12.14
	# Warp_strength= 20
	# Thresholding parameters (for post processing after the edge is computed)
	Threshold_min = -1
	Threshold_max = 0.0019
	# [] Choose to compute the analog or digital edge,
	Morph_flag = 1 # [] To compute analog edge, set Morph_flag=0 and to compute digital edge, set Morph_flag=1w

	[Edge, PST_Kernel]= PST(Image_orig_grey, LPF, Phase_strength, Warp_strength, Threshold_min, Threshold_max, Morph_flag);

	if (Morph_flag == 0):
		Edge = (Edge/np.max(Edge))*3;

	Overlay = mh.overlay(Image_orig_grey,Edge);

    # Append results
	imaging_results.append(Image_orig);
	imaging_results.append(Edge);
	imaging_results.append(Overlay);

	return imaging_results; 
