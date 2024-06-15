import os
from flask import Flask, redirect, render_template, request
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
import cv2


disease_info = pd.read_csv('disease_info.csv' , encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv',encoding='cp1252')

model = CNN.CNN(39)    
model.load_state_dict(torch.load("plant_disease_model_1_latest.pt"))
model.eval()

def prediction(image_path):
    


    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index


app = Flask(__name__, static_url_path='/static')
# @app.route('/')
# def home_page():
#     return render_template('home.html')

    
@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/home')
def home():
    return render_template('home.html')
    

@app.route('/contact')  
def contact():
    return render_template('contact-us.html')

@app.route('/index')
def ai_engine_page():
    return render_template('leaf.html')


# Routes for each crop
@app.route('/barley')
def barley():
    return render_template('barley.html')

@app.route('/maize')
def maize():
    return render_template('maize.html')

@app.route('/rice')
def rice():
    return render_template('rice.html')

@app.route('/soybean')
def soybean():
    return render_template('soybean.html')

@app.route('/cotton')
def cotton():
    return render_template('cotton.html')

@app.route('/sugarcane')
def sugarcane():
    return render_template('sugarcane.html')

# Define routes for each fruits
@app.route('/grapes')
def grapes():
    return render_template('grapes.html')

@app.route('/pomegranate')
def pomegranate():
    return render_template('pomegranate.html')

@app.route('/banana')
def banana():
    return render_template('banana.html')

@app.route('/mango')
def mango():
    return render_template('mango.html')

@app.route('/guava')
def guava():
    return render_template('guava.html')

@app.route('/watermelon')
def watermelon():
    return render_template('watermelon.html')

@app.route('/rose')
def rose():
    return render_template('rose.html')

@app.route('/marigold')
def marigold():
    return render_template('marigold.html')

@app.route('/jasmine')
def jasmine():
    return render_template('jasmine.html')

@app.route('/brinjal')
def brinjal():
    return render_template('brinjal.html')

@app.route('/potato')
def potato():
    return render_template('potato.html')

@app.route('/chilli')
def chilli():
    return render_template('chilli.html')

@app.route('/tomato')
def tomato():
    return render_template('tomato.html')

@app.route('/spinach')
def spinach():
    return render_template('spinach.html')

@app.route('/carrot')
def carrot():
    return render_template('carrot.html')


# Define routes for each crop
@app.route('/aloevera')
def aloevera():
    return render_template('aloevera.html')

@app.route('/amla')
def amla():
    return render_template('amla.html')

@app.route('/ashwagandha')
def ashwagandha():
    return render_template('ashwagandha.html')

@app.route('/pages-faq')
def faq():
    return render_template('faq.html')

@app.route('/pages-register')
def register():
    return render_template('register.html')  
 
@app.route('/mobile-device')     
def mobile_device_detected_page():
    return render_template('mobile-device.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        image = request.files['image']
        filename = image.filename
        file_path = os.path.join('static/uploads', filename)
        image.save(file_path)
        print(file_path)
        pred = prediction(file_path)
        title = disease_info['disease_name'][pred]
        description =disease_info['description'][pred]
        prevent = disease_info['Possible Steps'][pred]
        image_url = disease_info['image_url'][pred]
        supplement_name = supplement_info['supplement name'][pred]
        supplement_image_url = supplement_info['supplement image'][pred]
        supplement_buy_link = supplement_info['buy link'][pred]
        return render_template('submit.html' , title = title , desc = description , prevent = prevent , 
                               image_url = image_url , pred = pred ,sname = supplement_name , simage = supplement_image_url , buy_link = supplement_buy_link)

@app.route('/market', methods=['GET', 'POST'])
def market():
    return render_template('market.html', supplement_image = list(supplement_info['supplement image']),
                        supplement_name = list(supplement_info['supplement name']), disease = list(disease_info['disease_name']), buy = list(supplement_info['buy link']))

if __name__ == '__main__':
    app.run(debug=True)
