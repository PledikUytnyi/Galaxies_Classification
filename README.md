# Classification of Galaxies
This project is about how the optical spectra of galaxies can be used to determine their morphological class. The most common classes are illustrated below:

![](https://astro.wku.edu/astr106/tuningfork.jpg)

Basically they can be divided into spiral (S) and elliptical (E) classes (that have own subclasses as shown above). Note, that there are more types that are not shown in this picture: there are irregular galaxies that don't have a nice and smooth shape and there are merger galaxies consisting of two or more galaxies that are in the process of colliding and form a huge irregular cluster.  

A common way to classify the galaxies into these subclasses is to use ML models trained on images, that were labeled by volunteers. This has been sucessfully done by the [Galaxy Zoo](https://data.galaxyzoo.org) project. The volunteers distinguished between multiple subclasses of galaxies, including irregular and merger. 

While this is a very common approach to classification, there are some problems. Sometimes images are ambigious and blurred. Here are some examples: 

So the ML models based on images would struggle to correctly classify such galaxies. We may try to rely on some other data that may contain information related to the type of galaxy. In this project we use optical spectral data of galaxies to classify them. 

> [!NOTE]
> Spectra contains information about the amount of light that a galaxy emits, as a function of its wavelength (or basically a color). 

Compare the the spectra of a **elliptical** and **spiral** galaxies: 

We see that their shapes and peaks look different. This is because there are different physical processes that are going on in these galaxies. So we may try to use this information to distinguish between different classes. As a starting point we will try to distinguish between larger classes, such as elliptical and spiral. In our labeled data there is also an "uncertain" class. 

> [!NOTE]
> The spectra of galaxies that we observe depend not only on the physical processes inside the galaxy, but also on it's relative velocity with respect to the Earth. Because of this motion the spectra are basically stretched. This needs to be taken into account by multiplying each wavelength by some constant factor $z$. Otherwise we cannot compare the spectra properly. 
 
## Data used
* Spectral data is from [SDSS - IV](https://www.sdss.org) (Sloan Digital Sky Survey). The data is hosted by the [Flatiron Institute](https://users.flatironinstitute.org/~polymathic/data/MultimodalUniverse/v1/sdss/sdss/).
* Morphological data (labeled) is from [Galaxy Zoo Project, Table 2](https://data.galaxyzoo.org) that focused on labeling images of galaxies. 

## Tools and methods used 

The classification is performed with the Random Forest algorithm. Libraries used: sklearn, pandas, numpy, matplotlib, h5py and the astrophysics library healpy. 

## Project files

* **sdss_healpix.txt** This file contains the indices of healpixels (segments of the sky) that were scanned by SDSS.
* **spectral_data_merge.py** Preparing list of healpixels to download, merging data from the two datasets, to create labels for the spectral data. Saving the data for each healpix to a separate file. 
* **download_raw_data.py** A simple script that allows to download only the data we need, as the SDSS database contains information about more galaxies than we have the labels for.
* **set_slices.py** Taking the data that we created for each healpix, and put some part of this data to a single file (as we might not need all the data we have). In addition, we add a new column, that accounts for the redshift factor $z$.  This column is obtained by multiplying the array of wavelengths by the $z$ factor, unique for each galaxy.  
* **flatten_data.py**  Here we further prepare the data for analysis: we perform smoothing (as our data is noisy), we also apply a cutoff mask to our data, so that each data sample contains the same number of features, that correspond to approximately the same set of wavelengths. 
* **training.py** Here we perform the training and extract the performance data of our model and estimate importance of the features. 
