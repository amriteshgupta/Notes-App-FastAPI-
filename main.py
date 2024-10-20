from bson import ObjectId
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

@app.post("/delete_note")
async def delete_note(noteId: str = Form(...)):
    print(f"Note ID to be deleted: {noteId}")  # Debugging line

    try:
        db = conn.notes
        # Convert the noteId to ObjectId and delete it
        result = db.notes.delete_one({"_id": ObjectId(noteId)})
        print(f"Deletion result: {result.deleted_count}")  # Debugging line
    except Exception as e:
        print(f"Error: {str(e)}")  # Debugging line to catch potential issues

    # Redirect to homepage after deletion
    return RedirectResponse(url='/', status_code=303)