from flask import Flask,render_template,request,redirect
from flask import *
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow import keras
import os
import cv2

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("demented.html")

@app.route("/front")
def frontfunc():
    return render_template("frontpage.html")

@app.route("/detector",methods=["POST"])
#takes the file upload variable from html form and saves the image in local directory
def thirdpage():
    #return request.form.get("myimage")
    try:
        f = request.files.get('fileToUpload', '')
    except IOError:
        return "Failure"
    f.save("alzipic.PNG")
    return redirect("/result")

@app.route("/result")
def result():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    adder= 'alzipic.PNG'
    news=os.path.join(dir_path,adder)
    temp=tf.keras.preprocessing.image.img_to_array(load_img(news))
    print(temp.shape)
    temp = cv2.resize(temp, (224, 224))
    print(temp.shape)
    x = np.expand_dims(temp, axis=0)
    model = keras.models.load_model('C://Users//arjun//Desktop//inhouse//flask_app//alzi_model.h5')
    t= x.shape
    res= model.predict(x)
    res=res[0]
    max_indx=-1
    max_val=-1
    for i in range(len(res)):
        if res[i]>max_val:
            max_val=res[i]
            max_indx=i
    if max_indx==2:
        return render_template("positive.html")
    else:
        return render_template("negative.html")
    
    return "hehe"

    

