import requests
from flask import Flask, render_template, request
import base64
import os
import requests

def classify_image(inp):
    temp = 'data:image/png;base64,'+ inp
    
    response = requests.post("https://jkompalli-plant-disease-detection.hf.space/run/predict",
                             json={ "data": [temp] }).json()

    data = response["data"]
    app.logger.info(data[0]['label'])
    label = data[0]['label']

    return label, label + '.html'

app = Flask(__name__)

# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')

# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        app.logger.info(file)
        filename = file.filename        
        
        file_path = os.path.join('D:/VSCode/plantdiseasedetection/static/upload/test/', filename)
        file.save(file_path)

        file_data = open(file_path, "rb").read()
        file_data = base64.b64encode(file_data).decode('utf-8')
        
        pred, output_page = classify_image(file_data)  
        return render_template(output_page, pred_output = pred, user_image = file_path)
    
# For local system & cloud
if __name__ == "__main__":
    app.run(threaded=False,port=8080) 