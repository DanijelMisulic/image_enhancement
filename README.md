# Python scripts for preprocessing dental images

Firstly create and activate new conda environment:

    conda create --name image_enhance python=3.6
    conda activate image_enhance

In the requirements.txt are needed dependencies for project to be running smoothly.
    
    pip install -r requirements.txt 

In the input folder there is one example image which was used for testing. Path to this image is hardcoded in the main function under analyse_images.py. Change this to test on some other input image. Position yourself in the root of the project and run:
    
    python analyse_images.py 

Keep in mind that running the script in the newly created environment will last much longer than any other runs. Output images will be saved into output folder with names reflecting which method has been done. 
