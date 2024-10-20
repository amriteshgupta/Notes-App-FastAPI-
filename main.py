from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient, errors

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Establish MongoDB connection
conn = MongoClient("mongodb+srv://blpamritesh:oo8HCnX92eCTUbNY@mongotest.stuir.mongodb.net/?retryWrites=true&w=majority")

@app.post("/submit_note")
async def submit_note(request: Request, title: str = Form(...), noteText: str = Form(...)):
    db = conn.notes
    db.notes.insert_one({"title": title, "note": noteText})

    return RedirectResponse(url='/', status_code=303)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    db = conn.notes
    docs = db.notes.find({})
    newDocs = [{"id": str(doc["_id"]), "note": doc["note"]} for doc in docs]

    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})
