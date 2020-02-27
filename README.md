# cosmic-rays-removal
This python application is intended to remove cosmic rays from astronomical data such as spectra or image. It used Laplacian algorith 
that was introduced by Pieter van Dokkum. 

It based on gui PyQt5 and astroscrappy package. Application may be compile in exe-file by pyinstall. You need to use for it a cosmic.py.
The interface is very simple. You can select few or one initial fits files, choose the directory for clean files and enter parameteres.

Parameters:
1. Readnoise - readnoise of CCD camera used in observations.
2. Gain - gain of CCD camera used in observations.
3. Sigma - manual parameter that affects on number detected cosmic rays. Recomended defualt value is sigma=5.0. 
More value gives less number of detected cosmics. If sigma value is low then algorith detect more cosmics.
