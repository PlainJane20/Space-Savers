import tensorflow as tf
import tensorflow_hub as hub

import numpy as np

import glob
import os

os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

# Function get jpg path, rescale image and convert jpg in uint8 tensor
def load_img(path):
    # read file
    
    img = tf.io.read_file(path)
    img = tf.io.decode_jpeg(img, channels=3)
    # resize img
    img = tf.image.resize_with_pad(img, 224, 224)
    img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]

    return img

def get_image_feature_vectors():
    module_handle = "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/4"
    module = hub.load(module_handle)

    for filename in glob.glob('static/img/Uploads/*'):
        print(filename)
        img = load_img(filename)
        features = module(img)
        feature_set = np.squeeze(features)
        outfile_name = os.path.basename(filename) + ".npz"
        out_path = os.path.join('static/img/img_vectors/', outfile_name)
        np.savetxt(out_path, feature_set, delimiter=',')

get_image_feature_vectors()


