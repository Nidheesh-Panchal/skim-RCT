import os
import logging
from model import predict
from utils.const import get_dirs
from flask import Flask, app, render_template, request, url_for, send_from_directory

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
logger = logging.getLogger('main')
logger.info('Starting app')

dirs = get_dirs()

logger.info("Starting flask app")

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def home():
	logger.info("Home page")
	return render_template("home.html")

@app.route("/api/predict", methods = ["POST"])
def predict_api():
	pred = predict.predict(request.json["text"])
	logger.info(f"Received prediction : {pred}")
	return {"result": pred}
  
@app.route('/', methods = ['POST'])  
def req_predict():
	logger.info("Request received for prediciton")
	print(request.form)
	logger.info("Sending data for prediction")
	pred = predict.predict(request.form["abstract"])
	logger.info(f"Received prediction : {pred}")

	return render_template("home.html", pred = pred, old_text = request.form["abstract"])
  
if __name__ == '__main__':  
	app.run(debug=True)