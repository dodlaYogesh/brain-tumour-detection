import cv2
import numpy as np
import streamlit as st
import tensorflow as tf
from run import tiff_call
from skimage import io as io_
from tensorflow.keras import backend as K

IMAGE_SHAPE = (256, 256)
st.set_option('deprecation.showfileUploaderEncoding', False)
st.title("Brain Tumor Detection")

def dice_coef(y_true,y_pred):
    y_truef = K.flatten(y_true)
    y_predf = K.flatten(y_pred)
    cal=K.sum(y_truef*y_predf)
    
    return ((2*cal+100)/(K.sum(y_truef)+K.sum(y_predf)+100))

def dice_coef_loss(y_true,y_pred):
    return -dice_coef(y_true,y_pred)

def iou(y_true,y_pred):
    intersection = K.sum(y_true*y_pred)
    sum_ = K.sum(y_true+y_pred)
    jac = (intersection+100)/(sum_-intersection+100)
    return jac

@st.cache(allow_output_mutation=True)
def load_model():
    model = tf.keras.models.load_model("unet_brain_mri_seg.hdf5", 
                                        custom_objects={'dice_coef_loss': dice_coef_loss, 
                                                        'iou': iou, 
                                                        'dice_coef': dice_coef})
    return model

with st.spinner('Loading model into memmory...'):
    model = load_model()

def load_and_prep_image(image):
    """
    Reads an image from filename, and preprocessess 
    it according to the model.
    """
    img = io_.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

def file_Uploader():
    file = st.file_uploader("Upload file", type=["png", "jpeg", "jpg"])
    show_file = st.empty()

    if not file:
        show_file.info("Upload image of Brain MRI.")
        return

    content = file.name
    
    path = tiff_call(content)

    st.write("Detection is shown in red")
    with st.spinner("Classifying....."):
            img = load_and_prep_image(path)
            pred_mask = model.predict(tf.expand_dims(img, axis=0)/255)
            pred_mask = pred_mask[np.newaxis, :, :, :]
            pred_mask = np.squeeze(pred_mask) > .5

            img[pred_mask == 1] = (255, 0, 0)

    st.write("")
    st.image(img, caption="Detected Tumor", use_column_width=True)

file_Uploader()
# Conver the files from here - https://tiff2jpg.com/


