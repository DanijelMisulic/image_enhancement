#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 19:46:07 2021

@author: danijelmisulic
"""
import os
import subprocess
import numpy as np
import cv2
from tensorflow_enhancement.test_model import enhance_wheels

    
#Auto exposure leveling through image magick
def apply_magick_exposure(image_path):
    cmd = "convert " + image_path + " -auto-level -auto-gamma output/image_magick_applied.png"
    subprocess.call(cmd, shell=True)
    
#Image preprocessing through predefined raw therapee profile   
def raw_therapee_preprocessing(image_path, output_folder):
    cmd = "rawtherapee-cli -o " + output_folder + "/raw_therapee_applied.jpg" + " -p raw_therapee_profiles/profile.pp3 -n -Y -c " + image_path
    subprocess.run(cmd.split(" "))

#Opencv CLAHE thresholding of image
def apply_clahe(image):        
    lab= cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8,8))
    cl = clahe.apply(l)

    limg = cv2.merge((cl,a,b))
    out = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return out

#Getting information on image brightness (bonus)
def calculate_brightness(image):
    YCrCbImage = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    Y,Cr,Cb = cv2.split(YCrCbImage)
    mean_Y = np.mean(Y)
    return mean_Y


if __name__ == "__main__":
    path_to_input_image = "input_image/opg.jpg"
    path_to_output_folder = "output"
    os.makedirs(path_to_output_folder, exist_ok=True)
    
    image = cv2.imread(path_to_input_image)
    brightness = calculate_brightness(image)
    
    result = apply_clahe(image)
    cv2.imwrite(path_to_output_folder + "/open_cv_applied.png", result)
    
    apply_magick_exposure(path_to_input_image)
    
    raw_therapee_preprocessing(path_to_input_image, path_to_output_folder)
    
    result = enhance_wheels(image)
    before_after = np.hstack((image, result))
    
    cv2.imwrite(path_to_output_folder + "/tensorflow_applied.jpg", result)
    cv2.imwrite(path_to_output_folder + "/before_after_tensorflow.jpg", before_after)
    

