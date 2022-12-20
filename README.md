# Depth-Estimation  


## Table of contents
- [Aim](#Aim)
- [About the Project](#About-The-Project)
- [Getting Started](#Getting-Started)
- [Prerequisites and Installations](#Prerequisites-And-Installations)
- [Methodologies Proposed](#Methodologies-Proposed)
  - [Part 1 : Using Processing Techniques](#Part-1--Implementing-Pre--Post-Processing)
  - [Part 2 : Using MDE](#Part-2--Applying-Midas-Model-On-RGB-Video-MDE)
  - [Part 3 : Fusion Of Stereo And MDE](#Part-3--Fusing-Stereo-Disparity-Map-and-MDE-Disparity-Map)
-  [Results](#Results)
-  [License](#License)

## Aim


To improve depth estimation and disparity map generation using OAK-D Pro camera. To justify a method to get highly accurate depth map by utilizing traditional knowledge and modern deep learning techniques.

## About The Project

Depth estimation is traditionally done using a pair of cameras called a stereo pair. 
Depth Estimation algorithms using Neural Networks have made enormous strides recently. Some algorithms estimate depth using a single image (monocular depth), others use neural networks to improve the depth estimated using a stereo pair, and some improve the depth estimation for RGBD cameras.
| Original Image | Disparity Map
|-----|-----|
|![RGB](Assets/Results/Result_Image_2/FrameRGB_3.jpg)|![Depth](Assets/Results/Result_Image_2/FusedRGB_3.jpg)|

## Getting Started


## Prerequisites And Installations

1. Install Depthai and many other important librariesutilized in this project by running following command :
```
    pip install -r requirements.txt
```
2. You must have an OAK-D camera
3. Required weights and models for code can be installed from [scripts](scripts) 

## Methodologies Proposed


### Part 1 : Implementing Pre + Post Processing

While going through various research paper we found that performing pre processing on stereo left and stereo right image and then implementing stereo rectification as well as triangulation method increases depth perception of camera manifolds. As well as reduce its noise.Preprocessing on images with certain touch on it with inbuilt OAK D post processing  filters has improved its depth a lot.
For Example , 
|Stereo Map Generated By OAK-D|Stereo Map After Pre+Post Processing|
|--------|---------|
|![Oak-D-Stereo](Assets/Images/Raw_stereo.jpeg)|![Pre+Post+Stereo](Assets/Images/Stereo_pre_post.jpeg)

#### Demo
1. Download prerequisite files from [scripts](scripts) and then perform following steps.
2. Run following command on terminal
```
    python3 Processing.py
```
### Part 2 : Applying Midas Model On RGB Video [MDE]


MiDAS is a pretrained model which improves Monocular Depth Estimation (MDE) of monocular RGB video. It generates a state of the art image.
The success of monocular depth estimation relies on large and diverse training sets. Due to the challenges associated with acquiring dense ground-truth depth across different environments at scale, a number of datasets with distinct characteristics and biases have emerged.
MiDaS was trained on 10 datasets (ReDWeb, DIML, Movies, MegaDepth, WSVD, TartanAir, HRWSI, ApolloScape, BlendedMVS, IRS) with multi-objective optimization.

| Normal RGB Image | MiDAS MDE |
|-------|---------|
| ![RGB_Trial.jpg](Assets/Images/OrgRGB.png) | ![MiDAS_MDE.jpg](Assets/Images/Midasimage.png) |

#### Demo
1. Download prerequisite files from the [scripts](scripts) and perform following step.
2. Run following command on terminal
```
    python3 Midas.py
```

### Part 3 : Fusing Stereo Disparity Map and MDE Disparity Map


In this approach we fuse disparity map generated by OAK-D using stereo cameras and disparity map generated using MiDAS model (MDE) on rgb video. This method aims to combine excellent features of Stereo as well as Monocular Depth Estimations and reduce noise generated by one disparity map by superimposing quality of other disparity map.
For further information kindly check folder [Fusion](Fusion)

| Original Scene | Steeo Disparity By OAK-D | MiDAS Disparity | Fused Disparity Map |
|--------|--------|--------|--------|
|![Original-Scene](Assets/Images/OrgRGB.png)|![Stereo-Disparity](Assets/Images/StereoImg.png)|![MiDAS-Disparity](Assets/Images/Midasimage.png)|![Fused-Disparity](Assets/Images/FusedImg.png)|

#### Demo
1. Download prerequisite files from [scripts](scripts) and then perform following steps.
2. Run following command on terminal
```
    python3 main.py
```

## Results


| Original Scene | OAK-D Stereo | MiDAS MDE | Fusion |
|-----|-----|-----|-----|
|![Original-Scene](Assets/Results/Result_Image_1/FrameRGB_2.jpg)|![Stereo-Disparity](Assets/Results/Result_Image_1/FrameStereo_2.jpg)|![MiDAS-Disparity](Assets/Results/Result_Image_1/FrameMidas_2.jpg)|![Fused-Disparity](Assets/Results/Result_Image_1/FusedRGB_2.jpg)|
|![Original-Scene](Assets/Results/Result_Image_2/FrameRGB_3.jpg)|![Stereo-Disparity](Assets/Results/Result_Image_2/FrameStereo_3.jpg)|![MiDAS-Disparity](Assets/Results/Result_Image_2/FrameMidas_3.jpg)|![Fused-Disparity](Assets/Results/Result_Image_2/FusedRGB_3.jpg)|
|![Original-Scene](Assets/Images/ResultVideo1_RGB_1.gif)|![Stereo-Disparity](Assets/Images/ResultVideo1_Stereo_1.gif)|![MiDAS-Disparity](Assets/Images/ResultVideo1_Midas_1.gif)|![Fused-Disparity](Assets/Images/ResultVideo1_Fusion_1.gif)|
|![Original-Scene](Assets/Images/ResultVideo2_RGB.gif)|![Stereo-Disparity](Assets/Images/ResultVideo2_Stereo.gif)|![MiDAS-Disparity](Assets/Images/ResultVideo2_Midas.gif)|![Fused-Disparity](Assets/Images/ResultVideo2_Fusion.gif)|

Following is the final result of our methodology with its real time analysis in Frames Per Second (FPS)

| Methods | FPS |
|-----------|----------|
| Pre+ post processing on Stereo | 25 |
| Only MiDAS | 18 |
| Fusion Using CMAP From OAK - D | 15 |
| Fusion Using canny edge on RGB | 13|

## License


[MIT License]() is added to project. 
