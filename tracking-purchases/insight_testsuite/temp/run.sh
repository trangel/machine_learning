#!/bin/bash


INPUT=src/anomaly_detection.py

#python $INPUT
python $INPUT ./src/process_log.py -i1 "batch_log.json" -i2 "stream_log.json" -o "flagged_purchases.json"
