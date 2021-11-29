# arch

use python `fastapi` framework, and `uvicorn` to run it.

1. automatically subscript notification
2. if it is health event, it will callout with voice of event detail
    - depend on AWS translate for translate event detail to chinese
    - depend on the [aws callout solutions](https://github.com/forhead/amazon-connect-callout)
    - for china phone number, you need open a support case and whitelist +86 numbers.

# install

```
pip install -r requirements.txt
```

# run

```
uvicorn main:app --reload  --host 0.0.0.0 --port 8000 2>&1 | tee server.logs
```

