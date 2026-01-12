#!/bin/bash
echo "Starting Streamlit with specific settings..."
streamlit run app_enhanced.py \
  --server.port=8501 \
  --server.address=127.0.0.1 \
  --server.headless=true \
  --browser.serverAddress=localhost \
  --browser.gatherUsageStats=false
