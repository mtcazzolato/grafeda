# Makefile to run graf-eda app demo

INPUT_DIR=data
SAMPLE_FILE=example_EHR.csv

run:
	streamlit run app.py --server.maxUploadSize 5000
	
demo:
	streamlit run app.py --server.maxUploadSize 5000

prep:
	pip3 install -r requirements.txt
