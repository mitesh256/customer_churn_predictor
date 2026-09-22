#!/bin/bash
# 1. Background mein FastAPI ko chalao port 8000 par
uvicorn api:app --host 127.0.0.1 --port 8000 &

# 2. Frontend mein Streamlit ko chalao jo Render ke main port par open hoga
streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
