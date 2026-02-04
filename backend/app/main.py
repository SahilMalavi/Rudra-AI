from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.gemini_service import gemini_response, process_image_from_bytes, create_chat
from app.pdf_service import extract_text_from_pdf_bytes


app = FastAPI(title="Rudra AI Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://rudra-ai-bot.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat = create_chat()

@app.get("/")
async def root():
    return {"message": "Rudra AI Assistant API running 🚀"}

@app.post("/chat")
async def chat_endpoint(message: str = Form(...)):
    try:
        response = gemini_response(message, chat)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat-with-image")
async def chat_with_image(
    prompt: str = Form(...),
    file: UploadFile = File(...)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        image_bytes = await file.read()
        response = process_image_from_bytes(image_bytes, prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat-with-pdf")
async def chat_with_pdf(
    prompt: str = Form(...),
    file: UploadFile = File(...)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        pdf_bytes = await file.read()
        pdf_text = extract_text_from_pdf_bytes(pdf_bytes)
        combined_prompt = f"Based on the PDF content:\n{pdf_text}\n\n{prompt}"
        response = gemini_response(combined_prompt, chat)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset-chat")
async def reset_chat():
    global chat
    chat = create_chat()
    return {"message": "Chat reset successfully"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)