from typing import Optional
# import asyncio
from pyppeteer import launch
import time
import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"Status":"running"}

@app.get("/snip/")
async def snip(url):
    statusmsg = ''
    try:
        # print("get " + url + "...")
        # print(len(url))
        if len(url)== 0:
            statusmsg = 'Empty URL'
            # return Response(content={"Error":"Empty url"}, status_code=400)
        browser = await launch(headless=True, args=['--no-sandbox'])
        page = await browser.newPage()
        await page.setViewport({
            "width":1024,
            "height":768,
            "deviceScaleFactor": 1
            })
        await page.goto(url)
        imgBin = await page.screenshot({'fullPage': True, 'type':'png', 'encoding':'binary', 'quality':100})
        await browser.close()
        ifname = "SnipApp-"+str(int(time.time()))+".png"
        # print("finished")
        return Response(content=imgBin, media_type="image/png", headers = {
                'content-Disposition':'attachment; filename='+ifname}, status_code=200 )
    except Exception as e:
        if(len(statusmsg) == 0):
            statusmsg = str(e)
        return Response(content=("Exception : {}".format(statusmsg)), status_code=400)
        # return Response({"Exception":e}, status_code=400, media_type='application/json')