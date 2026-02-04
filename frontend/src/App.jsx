import React, { useState, useReducer } from 'react';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import ImageInterface from './components/ImageInterface';
import PDFInterface from './components/PDFInterface';

// Combined state reducer for messages and files
const appReducer = (state, action) => {
    switch (action.type) {
        case 'ADD_MESSAGE':
            return {
                ...state,
                messages: {
                    ...state.messages,
                    [action.mode]: [...state.messages[action.mode], action.message]
                }
            };
        case 'SET_MESSAGES':
            return {
                ...state,
                messages: {
                    ...state.messages,
                    [action.mode]: action.messages
                }
            };
        case 'CLEAR_MESSAGES':
            return {
                ...state,
                messages: {
                    ...state.messages,
                    [action.mode]: []
                }
            };
        case 'RESET_MODE':
            return {
                ...state,
                messages: {
                    ...state.messages,
                    [action.mode]: action.initialMessage ? [action.initialMessage] : []
                }
            };
        case 'SET_IMAGE':
            return {
                ...state,
                files: {
                    ...state.files,
                    image: {
                        file: action.file,
                        preview: action.preview,
                        name: action.name
                    }
                }
            };
        case 'CLEAR_IMAGE':
            return {
                ...state,
                files: {
                    ...state.files,
                    image: null
                },
                messages: {
                    ...state.messages,
                    image: []
                }
            };
        case 'SET_PDF':
            return {
                ...state,
                files: {
                    ...state.files,
                    pdf: {
                        file: action.file,
                        name: action.name
                    }
                }
            };
        case 'CLEAR_PDF':
            return {
                ...state,
                files: {
                    ...state.files,
                    pdf: null
                },
                messages: {
                    ...state.messages,
                    pdf: []
                }
            };
        default:
            return state;
    }
};

const initialState = {
    messages: {
        chat: [
            {
                role: 'assistant',
                content: 'Hello! I\'m Rudra, your personal assistant created by Sahil Malavi. How can I help you today?'
            }
        ],
        image: [],
        pdf: []
    },
    files: {
        image: null,
        pdf: null
    }
};

function App() {
    const [currentMode, setCurrentMode] = useState('chat');
    const [state, dispatch] = useReducer(appReducer, initialState);

    const addMessage = (mode, message) => {
        dispatch({ type: 'ADD_MESSAGE', mode, message });
    };

    const setMessages = (mode, messageList) => {
        dispatch({ type: 'SET_MESSAGES', mode, messages: messageList });
    };

    const clearMessages = (mode) => {
        dispatch({ type: 'CLEAR_MESSAGES', mode });
    };

    const resetMode = (mode, includeGreeting = false) => {
        const greeting = mode === 'chat' ? {
            role: 'assistant',
            content: 'Hello! I\'m Rudra, your personal assistant created by Sahil Malavi. How can I help you today?'
        } : null;

        dispatch({
            type: 'RESET_MODE',
            mode,
            initialMessage: includeGreeting ? greeting : null
        });
    };

    // File management functions
    const setImageFile = (file, preview, name) => {
        dispatch({ type: 'SET_IMAGE', file, preview, name });
    };

    const clearImageFile = () => {
        dispatch({ type: 'CLEAR_IMAGE' });
    };

    const setPDFFile = (file, name) => {
        dispatch({ type: 'SET_PDF', file, name });
    };

    const clearPDFFile = () => {
        dispatch({ type: 'CLEAR_PDF' });
    };

    const renderCurrentInterface = () => {
        const baseProps = {
            messages: state.messages[currentMode],
            addMessage: (msg) => addMessage(currentMode, msg),
            setMessages: (msgs) => setMessages(currentMode, msgs),
            clearMessages: () => clearMessages(currentMode),
            resetMode: (includeGreeting) => resetMode(currentMode, includeGreeting)
        };

        switch (currentMode) {
            case 'chat':
                return <ChatInterface {...baseProps} />;
            case 'image':
                return <ImageInterface
                    {...baseProps}
                    uploadedImage={state.files.image?.file}
                    imagePreview={state.files.image?.preview}
                    setImageFile={setImageFile}
                    clearImageFile={clearImageFile}
                />;
            case 'pdf':
                return <PDFInterface
                    {...baseProps}
                    uploadedPDF={state.files.pdf?.file}
                    pdfName={state.files.pdf?.name}
                    setPDFFile={setPDFFile}
                    clearPDFFile={clearPDFFile}
                />;
            default:
                return <ChatInterface {...baseProps} />;
        }
    };

    return (
        <div className="flex h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900 overflow-hidden">
            <Sidebar currentMode={currentMode} setCurrentMode={setCurrentMode} />
            <main className="flex-1 overflow-hidden md:ml-0 relative">
                {/* Decorative background elements */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                    <div className="absolute top-20 right-20 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl animate-pulse"></div>
                    <div className="absolute bottom-20 left-20 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
                </div>
                <div className="relative z-10 h-full">
                    {renderCurrentInterface()}
                </div>
            </main>
        </div>
    );
}

export default App;