#!/bin/bash
cd /opt/server_monitoring
source venv/bin/activate
python3 temperature/temperature_check.py 
