#!/usr/bin/env python3

import cv2
import depthai as dai
import numpy as np

# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = False
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = True

def getFrame(queue):
    print("hello1")
    frame = queue.get()
    print("hello2")
    return frame.getCvFrame()

# Create pipeline
pipeline = dai.Pipeline()
pipeline.setOpenVINOVersion(dai.OpenVINO.VERSION_2021_4)

# Define sources and outputs
monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
manipLeft = pipeline.create(dai.node.ImageManip)
manipRight = pipeline.create(dai.node.ImageManip)
depth = pipeline.create(dai.node.StereoDepth)
# image_manip_script = pipeline.create(dai.node.Script)


monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)


monoLeft.out.link(manipLeft.inputImage)
monoRight.out.link(manipRight.inputImage)


manipLeft.initialConfig.setResize(288, 300)
manipRight.initialConfig.setResize(288, 300)


# NN that detects faces in the image
nnL = pipeline.create(dai.node.NeuralNetwork)
nnL.setBlobPath("/home/smit/Desktop/Spatial_AI_Image/Blob/blur_simplified1_openvino_2021.4_6shave.blob")
manipLeft.out.link(nnL.input)

nnR = pipeline.create(dai.node.NeuralNetwork)
nnR.setBlobPath("/home/smit/Desktop/Spatial_AI_Image/Blob/blur_simplified1_openvino_2021.4_6shave.blob")
manipRight.out.link(nnR.input)


# nn.out.link(image_manip_script.inputs['LEFT_IMAGE'])
# nn.out.link(image_manip_script.inputs['RIGHT_IMAGE'])


# nnR.passthrough.link(depth.right)
# nnL.passthrough.link(depth.left)

# xoutnnl = pipeline.create(dai.node.XLinkOut)
# xoutnnl.setStreamName("nnl")
# nnL.passthrough.link(xoutnnl.input)

# xoutnnr = pipeline.create(dai.node.XLinkOut)
# xoutnnr.setStreamName("nnr")
# nnR.passthrough.link(xoutnnr.input)

nnL.passthrough.link(depth.left)
nnR.passthrough.link(depth.right)
# print("sj")


xout = pipeline.create(dai.node.XLinkOut) 
xout.setStreamName("disparity")

# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
# depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
# depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
# depth.setLeftRightCheck(lr_check)
# depth.setExtendedDisparity(extended_disparity)
# depth.setSubpixel(subpixel)
depth.disparity.link(xout.input)
# image_manip_script.setScript("""
    
#     while True:

#         output_L = node.io['LEFT_IMAGE'].get()
#         output_R = node.io['RIGHT_IMAGE'].get()

#         node.io['LEFT_FINAL'].send(output_L)
#         node.io['RIGHT_FINAL'].send(output_R)

    

# """)
# nn_xoutR = pipeline.create(dai.node.XLinkOut)
# nn_xoutR.setStreamName("RIGHT_FRAME")

# nn_xoutL = pipeline.create(dai.node.XLinkOut)
# nn_xoutL.setStreamName("LEFT_FRAME")

with dai.Device(pipeline) as device:
    
    # nlq = device.getOutputQueue(name="nnl", maxSize=10, blocking=False)
    # nlr = device.getOutputQueue(name="nnr", maxSize=10, blocking=False)

    q = device.getOutputQueue(name="disparity", maxSize=10, blocking=False)

    # shape = (1, 288, 288)
    # def get_frame(imfFrame, shape):
    #     return np.array(imfFrame.get()).view(np.float16).reshape(shape).transpose(1, 2, 0).astype(np.uint8)

    while True:
        # print(q)
        # nlqf = getFrame(nlq)
        # cv2.imshow("ei", nlqf)
        # cv2.waitKey(1)
        frame = getFrame(q)
        print("hello3")
        # frame = cv2.resize(frame,shape)
        # frame = inDisparity.getFrame()
        # Normalization for better visualization
        frame = (frame * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)
        print("Hello4")
        cv2.imshow("disparity", frame)
        print("Hello")
        # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
        frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
        cv2.imshow("disparity_color", frame)

        if cv2.waitKey(1) == ord('q'):
            break