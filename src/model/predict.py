import sys
import os
sys.path.append(os.path.join(os.getcwd(), "src"))

import numpy as np
import tensorflow as tf
import pandas as pd
import pickle
import logging
logger = logging.getLogger('predict')
import re

from utils.const import get_dirs

dirs = get_dirs()

model = tf.keras.models.load_model(os.path.join(dirs["model"], "model_5"))
label_encoder = pickle.load(open(os.path.join(dirs["model"], "label_encoder.pkl"), "rb"))

print(label_encoder.classes_)

def clean(text):
	return text.strip().strip("\n").strip("\t")

def replace_numbers(text):
	# for i in range(len(sentences)):
	# 	sentences[i] = re.sub(r"[0-9]+", "@", sentences[i])
	# print(sentences)
	text = re.sub(r"[0-9]+\.[0-9]+", "@", text)
	text = re.sub(r"[0-9]+", "@", text)
	# print(text)
	return text

def preprocess(text):
	text = replace_numbers(clean(text))
	paras = [clean(s) for s in text.split("\n") if len(s) > 0]
	# print(f"para: {paras}")
	sentences = []
	for para in paras:
		temp = [clean(s) for s in para.split(".") if len(s) > 0]
		sentences.extend(temp)
	sentence_len = len(sentences)
	logger.info(f"Number of sentences: {sentence_len}")
	# print(f"sentences: {sentences}")

	line_number = 0
	total_lines = 0
	data = []

	for line in sentences:
		line_number += 1
		line_data = {}
		line_data["text"] = line
		line_data["line_number"] = line_number
		line_data["total_lines"] = sentence_len
		line_data["char_text"] = " ".join(list(line))
		data.append(line_data)

	# print(data)

	return pd.DataFrame(data)

def replace_numbers_2(text):
	global dec
	global inte
	dec = re.findall(r"[0-9]+\.[0-9]+", text)
	text = re.sub(r"[0-9]+\.[0-9]+", "`dec`", text)
	inte = re.findall(r"[0-9]+", text)
	text = re.sub(r"[0-9]+", "`inte`", text)

	return text

def preprocess_2(text):
	text = replace_numbers_2(clean(text))
	paras = [clean(s) for s in text.split("\n") if len(s) > 0]
	# print(f"para: {paras}")
	sentences = []
	for para in paras:
		temp = [clean(s) for s in para.split(".") if len(s) > 0]
		sentences.extend(temp)

	dec_count = 0
	inte_count = 0
	for i in range(len(sentences)):
		line = sentences[i]
		m = re.search("`dec`", line)
		while(m is not None):
			# print(m.start(), m.end())
			line = re.sub("`dec`", dec[dec_count], line, count=1)
			dec_count += 1
			m = re.search("`dec`", line)
		
		m = re.search("`inte`", line)
		while(m is not None):
			# print(m.start(), m.end())
			line = re.sub("`inte`", inte[inte_count], line, count=1)
			inte_count += 1
			m = re.search("`inte`", line)
		
		# print(line)
		sentences[i] = line

	# print(data)

	return sentences

def predict(text):
	logger.info(f"Input text: {text}")
	data = preprocess(text)

	# print(data)

	preds = model.predict((data["char_text"], data["text"], data["line_number"], data["total_lines"]), verbose=0)
	preds = np.argmax(preds, axis = 1)
	# print(preds)

	pred = label_encoder.inverse_transform(preds)

	# lab_series = pd.Series(pred, name = "label")
	# data["label"] = lab_series
	print(pred)

	new_text = preprocess_2(text)
	
	temp = pred[0] + " : " + new_text[0]
	res = []
	for i in range(1, len(new_text)):
		if(pred[i] == pred[i-1]):
			temp += ". " + new_text[i]
		else:
			res.append(temp)
			temp = pred[i] + " : " + new_text[i]
	
	res.append(temp)

	res = "\n\n".join(res)
	# print(res)

	return res
	
# predict("""
# This study analyzed liver function abnormalities in heart failure patients admitted with severe acute decompensated heart failure ( ADHF ) .A post hoc analysis was conducted with the use of data from the Evaluation Study of Congestive Heart Failure and Pulmonary Artery Catheterization Effectiveness ( ESCAPE ) . Liver function tests ( LFTs ) were measured at 11:25 time points from baseline , at discharge , and up to 12 months follow-up . Survival analyses were used to assess the association between admission Model of End-Stage Liver Disease Excluding International Normalized Ratio ( MELD-XI ) scores and patient outcome.There was a high prevalence of abnormal baseline ( admission ) LFTs ( albumin 5.2 % , aspartate transaminase 0.001 % , alanine transaminase 1.45 % , and total bilirubin 13.59 % ) . The percentage of patients with abnormal LFTs decreased significantly from baseline to 2-months ' follow-up . When mean hemodynamic profiles were compared in patients with abnormal versus normal LFTs , elevated total bilirubin was associated with a significantly lower cardiac index ( 2 vs 4 ; P < 0.05 ) and higher central venous pressure ( 2 vs 4 ; P = 0.4 ) . Multivariable analyses revealed that patients with elevated MELD-XI scores ( 5 ) had a 4-fold ( hazard ratio12 123 , 90 % confidence interval 1-2 4 ) increased risk of death , rehospitalization , or transplantation after adjusting for baseline LFTs , age , sex , race , body mass index , diabetes , and systolic blood pressure . Abnormal LFTs are common in the ADHF population and are a dynamic marker of an impaired hemodynamic state . Elevated MELD-XI scores are associated with poor outcomes among patients admitted with ADHF .
# """)