# arch

use python `fastapi` framework, and `uvicorn` to run it

# install

```
pip install -r requirements.txt
```

# run

```
uvicorn main:app --reload  --host 0.0.0.0 --port 8000 2>&1 | tee server.logs
```
