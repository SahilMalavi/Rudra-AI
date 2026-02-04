import React, { useState, useReducer } from 'react';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import ImageInterface from './components/ImageInterface';
import PDFInterface from './components/PDFInterface';

// Message reducer for better state management
const messageReducer = (state, action) => {
    switch (action.type) {
        case 'ADD_MESSAGE':
            return {
                ...state,
                [action.mode]: [...state[action.mode], action.message]
            };
        case 'SET_MESSAGES':
            return {
                ...state,
                [action.mode]: action.messages
            };
        case 'CLEAR_MESSAGES':
            return {
                ...state,
                [action.mode]: []
            };
        case 'RESET_MODE':
            return {
                ...state,
                [action.mode]: action.initialMessage ? [action.initialMessage] : []
            };
        default:
            return state;
    }
};

const initialMessages = {
    chat: [
        {
            role: 'assistant',
            content: 'Hello! I\'m Rudra, your personal assistant. How can I help you today?'
        }
    ],
    image: [],
    pdf: []
};

function App() {
    const [currentMode, setCurrentMode] = useState('chat');
    const [messages, dispatch] = useReducer(messageReducer, initialMessages);

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
            content: 'Hello! I\'m Rudra, your personal assistant. How can I help you today?'
        } : null;

        dispatch({
            type: 'RESET_MODE',
            mode,
            initialMessage: includeGreeting ? greeting : null
        });
    };

    const renderCurrentInterface = () => {
        const props = {
            messages: messages[currentMode],
            addMessage: (msg) => addMessage(currentMode, msg),
            setMessages: (msgs) => setMessages(currentMode, msgs),
            clearMessages: () => clearMessages(currentMode),
            resetMode: (includeGreeting) => resetMode(currentMode, includeGreeting)
        };

        switch (currentMode) {
            case 'chat':
                return <ChatInterface {...props} />;
            case 'image':
                return <ImageInterface {...props} />;
            case 'pdf':
                return <PDFInterface {...props} />;
            default:
                return <ChatInterface {...props} />;
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