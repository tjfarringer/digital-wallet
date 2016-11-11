#!/usr/bin/env bash

# example of the run script for running the fraud detection algorithm with a python file,
# but could be replaced with similar files from any m       ajor language

# I'll execute my programs, with the input directory paymo_input and output the files in the directory paymo_output
#python ./src/antifraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt

python ~/Desktop/digital-wallet-master/src/feature_code.py /Users/talmadgefarringer/Desktop/Insight_code_challenge/stream_payment.csv /Users/talmadgefarringer/Desktop/Insight_code_challenge/batch_payment.csv ~/Desktop/digital-wallet-master/paymo_output/output1.txt ~/Desktop/digital-wallet-master/paymo_output/output2.txt ~/Desktop/digital-wallet-master/paymo_output/output3.txt

