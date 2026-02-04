# Rudra AI Personal Assistant

A modern, responsive AI assistant built with React frontend and FastAPI backend, featuring chat, image analysis, and PDF interaction capabilities.

## Features

- **Chat Mode**: Natural conversation with AI assistant
- **Image Analysis**: Upload images and ask questions about them
- **PDF Chat**: Upload PDF documents and query their contents
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **Modular Architecture**: Clean separation of frontend and backend

## Project Structure

```
PersonalAssistantRUDRA/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application
│   │   ├── gemini_service.py # Gemini AI integration
│   │   └── pdf_service.py    # PDF processing
│   ├── requirements.txt
│   └── .env                 # API keys (not in version control)
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API service layer
│   │   └── App.jsx          # Main app component
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env` file and add your Google API key:

   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

5. Run the backend server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

4. Open your browser to `http://localhost:5173`

## API Endpoints

- `POST /chat` - Send text message for chat
- `POST /chat-with-image` - Send message with image file
- `POST /chat-with-pdf` - Send message with PDF file
- `POST /reset-chat` - Reset chat session

## Environment Variables

Create a `.env` file in the backend directory with:

```
GOOGLE_API_KEY=your_google_gemini_api_key
```

## Technologies Used

- **Frontend**: React, Vite, Tailwind CSS, Axios
- **Backend**: FastAPI, Python, Google Gemini AI
- **File Processing**: PyPDF2, Pillow

## Development

The project uses a modular architecture with clear separation of concerns:

- Frontend handles UI/UX and API communication
- Backend manages AI interactions and file processing
- Services are organized for maintainability

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
