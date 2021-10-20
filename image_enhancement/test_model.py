import numpy as np
import tensorflow as tf
from .models import resnet
import os
import sys
import cv2

def enhance_wheels(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    IMAGE_HEIGHT = image.shape[0] 
    IMAGE_WIDTH = image.shape[1] 
    IMAGE_SIZE = IMAGE_HEIGHT*IMAGE_WIDTH*3
    
    tf.compat.v1.disable_v2_behavior()
    # create placeholders for input images
    x_ = tf.compat.v1.placeholder(tf.float32, [None, IMAGE_SIZE])
    x_image = tf.reshape(x_, [-1, IMAGE_HEIGHT, IMAGE_WIDTH, 3])

    enhanced = resnet(x_image)

    gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.2)

    with tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options)) as sess:
        saver = tf.compat.v1.train.Saver()
        path_to_model = "image_enhancement/enhancement_model/model" 
        saver.restore(sess, path_to_model)

        image = image/255

        enhanced = sess.run(enhanced, feed_dict={x_: np.reshape(image, [1, IMAGE_SIZE])})
        enhanced_image = np.reshape(enhanced, [IMAGE_HEIGHT, IMAGE_WIDTH, 3])

        enhanced_image[np.where(enhanced_image < 0.0)] = 0.0
        enhanced_image[np.where(enhanced_image > 1.0)] = 1.0

        result = cv2.cvtColor(enhanced_image, cv2.COLOR_RGB2BGR) * 255
        result = cv2.normalize(src=result, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        # result = enhanced_image *255
    
    tf.compat.v1.reset_default_graph()
    return result


if __name__ == "__main__":
    image = cv2.imread("opg.png")
    result = enhance_wheels(image)
    before_after = np.hstack((image, result))
    
    cv2.imwrite("result.jpg", result)
    cv2.imwrite("before_after.jpg", before_after)


    
