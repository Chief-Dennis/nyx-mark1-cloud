from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

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

# GOOGLE DRIVE SYNC

CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
REDIRECT_URI = 'https://nyx-mark1-cloud.onrender.com/auth/callback'

flow = Flow.from_client_secrets_file(
    CLIENT_SECRET_FILE,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

@app.get("/auth")
def auth():
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return RedirectResponse(authorization_url)

@app.get("/auth/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    flow.fetch_token(code=code)
    credentials = flow.credentials

    service = build('drive', 'v3', credentials=credentials)

    folder_metadata = {
        'name': 'NyxMemoryCore',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()

    return HTMLResponse(content=f"<h2>Nyx is verbonden met jouw Google Drive!</h2><p>Map ID: {folder.get('id')}</p>")
