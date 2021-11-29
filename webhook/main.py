import requests
import json
import boto3
from typing import Optional
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from starlette.config import Config

SNS_HEADERS = ['x-amz-sns-message-type', 'x-amz-sns-message-id', 'x-amz-sns-topic-arn', 'user-agent']

_config = Config("config.ini")

CALLOUT_CONFIG = {
    "DestinationPhoneNumber" : _config('DestinationPhoneNumber'),
    "ContactFlowId" : _config('ContactFlowId'),
    "InstanceId" : _config('InstanceId'),
    "SourcePhoneNumber" : _config('SourcePhoneNumber')
}

def TranslateToChinese(msg):
    """
    Help function to translate message from english to chinese 
    """
    print("Tanslate message")
    translate = boto3.client(service_name='translate')
    result = translate.translate_text(Text=msg, SourceLanguageCode="en", TargetLanguageCode="zh")
    return result.get('TranslatedText')

def CalloutAlarm(subject: str, alarmsg: str):
    """
    Help function to callout use connect services,you should setup and config connect firstly
    """
    print("CalloutAlarm message")
    client = boto3.client('connect')
    resp = client.start_outbound_voice_contact(
               Attributes={
                   'AlarmMessage': '<speak><break time=\"3s\"/>'+TranslateToChinese(subject)+'<break time=\"2s\"/>'+TranslateToChinese(alarmsg)+'</speak>'
               },
               **CALLOUT_CONFIG
           )
    return resp

app = FastAPI(openapi_url=None)

def SubscriptionConfirmation(req: dict, bgtasks: BackgroundTasks):
    """
    handle the subscription confirmation
    """
    print("SubscriptionConfirmation")
    bgtasks.add_task(requests.get, req['SubscribeURL'])
    return JSONResponse({"status_code": 200, "message": "Subscription Confirmed"}, status_code=200)

def Notification(req: dict, bgtasks: BackgroundTasks):
    """
    handle the notification
    """
    print("Notification")
    if 'Message' in req and req['Message']:
        try:
            info = json.loads(req['Message'])
            if 'detail' in info and 'eventDescription' in info['detail'] and info['detail']['eventDescription']:
                bgtasks.add_task(CalloutAlarm, req['Subject'], info['detail']['eventDescription'][0]['latestDescription'])
        except ValueError as e:
            print("Message body is not json string") 
    return JSONResponse({"status_code": 200, "message": "Notification Confirmed"}, status_code=200)

def UnsubscribeConfirmation(req: dict, bgtasks: BackgroundTasks):
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
async def read_root(request: Request, bgtasks: BackgroundTasks):
    """
    the webhook for receive notification
    """
    req = await request.json()
    if req['Type'] in globals():
        print(req)
        return globals()[req['Type']](req, bgtasks)
    return JSONResponse({"status_code": 403, "message": "You are not allow to access this site"}, status_code=403)

