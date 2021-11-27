import requests
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

SNS_HEADERS = ['x-amz-sns-message-type', 'x-amz-sns-message-id', 'x-amz-sns-topic-arn', 'user-agent']

app = FastAPI(openapi_url=None)

def SubscriptionConfirmation(req):
    """
    handle the subscription confirmation
    """
    print("SubscriptionConfirmation")
    requests.get(req['SubscribeURL'])
    return JSONResponse({"status_code": 200, "message": "Subscription Confirmed"}, status_code=200)

def Notification(req):
    """
    handle the notification
    """
    print("Notification")
    return JSONResponse({"status_code": 200, "message": "Notification Confirmed"}, status_code=200)

def UnsubscribeConfirmation(req):
    """
    handle the UnsubscribeConfirmation
    """
    print("UnsubscribeConfirmation")
    return JSONResponse({"status_code": 200, "message": "Unsubscribe Confirmed"}, status_code=200)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    check every requests to verify it is amazon request
    """
    print(request.headers)
    invalid = False
    for hd in SNS_HEADERS:
        if hd not in request.headers:
            invalid = True
    if  request.headers['user-agent'] != 'Amazon Simple Notification Service Agent':
        invalid = True
    if invalid:
        return JSONResponse({"status_code": 403, "message": "You are not allow to access this site"}, status_code=403)
    return await call_next(request)

@app.post("/webhook/sns")
async def read_root(request: Request):
    """
    the webhook for receive notification
    """
    req = await request.json()
    if req['Type'] in globals():
        print(req)
        return globals()[req['Type']](req)
    return JSONResponse({"status_code": 403, "message": "You are not allow to access this site"}, status_code=403)

