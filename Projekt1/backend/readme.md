```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
fastapi dev
uvicorn app.main:app --reload
http://127.0.0.1:8000/docs
```
