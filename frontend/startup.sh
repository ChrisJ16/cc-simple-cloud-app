#!/bin/#!/bin/bash

# install all necessary dependencies
pip install -r requirements.txt

# start the streamlit demo app
streamlit run app.py --server.port $PORT --server.address 0.0.0.0