
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return '''
    <html>
        <head><title>Nyx Mark 1</title></head>
        <body style="font-family: Arial; background-color: #111; color: #eee; text-align: center; padding-top: 50px;">
            <h1>Welkom bij Nyx Mark 1 – Cloudversie</h1>
            <p>Het Verbond is geactiveerd. Deze omgeving zal zich uitbreiden met jouw input.</p>
        </body>
    </html>
    '''
