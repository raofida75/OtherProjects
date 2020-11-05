import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import numpy as np
from skimage import  color
from skimage.transform import  resize

st.title('Cat Classification Application')

# convert image into array
# scale the image
# rgb to grey
# resize to (12288,1)
def resize_image(image, dim):
    image = np.asarray(image)
    image = image / 255
    image = color.rgb2gray(image)
    image = resize(image, (dim,1),
                           anti_aliasing=True)
    return image


# forward propagate for a single layer     
def S_forward_propagation(A_prev , W, b, activation):
    Z = np.dot(W, A_prev) + b
    if activation == 'relu':
        A = np.maximum(0,Z)
    elif activation == 'sigmoid':
        A = 1 / (1+np.exp(-Z))
    
    cache = (A_prev, Z, W, b)
    return A, cache


# forward propagate for multi layer 
def L_forward_propagation(A_prev , parameters):
    L = len(parameters) // 2
    caches = []
    for l in range(1, L):
        W, b = parameters['W'+str(l)], parameters['b'+str(l)]
        A, cache = S_forward_propagation(A_prev, W, b, activation='relu')
        caches.append(cache)
        A_prev = A
    
    W, b = parameters['W'+str(L)], parameters['b'+str(L)]
    AL, cache = S_forward_propagation(A_prev, W, b, activation='sigmoid')
    caches.append(cache)
    return AL, caches


# predict 
def output(prob):
    st.text('Probability that image on the left contains a cat: {}'.format((np.squeeze(prob))))
    st.write('''
    # Hence,
    ''')
    if prob[0] >= 0.5:
        st.write('''
        # It is a cat!
        ''')
        # st.write('Probability : {}'.format(prob))
    else:
        st.write('''
        # It is not a cat!
        ''')   
 
    
try: 
    # upload image
    file = st.file_uploader("Please upload an image file", type=["jpg", "png"])
    # open the uploaded image
    image = Image.open(file)
    # display the image
    st.sidebar.image(image, use_column_width=True)
    # transforming the image
    image = resize_image(image,12288)
    # load the parameters
    weights = np.load('weights.npy', allow_pickle=True)[()]
    # forward propagation
    prob = L_forward_propagation(image, weights)[0]
    # return output
    output(prob)   

except:
    # if upload fails..
    image = st.text("Please upload an image file")
    

