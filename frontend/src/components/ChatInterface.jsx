import React, { useState, useEffect, useRef } from 'react';
import { Send, RotateCcw, Loader2 } from 'lucide-react';
import { chatAPI } from '../services/api';
import MarkdownContent from './MarkdownContent';

const ChatInterface = ({ messages, addMessage, resetMode }) => {
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        // Focus input on mount
        inputRef.current?.focus();
    }, []);

    const handleSendMessage = async (e) => {
        e?.preventDefault();
        if (!inputMessage.trim() || isLoading) return;

        const userMessage = { role: 'user', content: inputMessage.trim() };
        addMessage(userMessage);
        setInputMessage('');
        setIsLoading(true);

        try {
            const response = await chatAPI.sendMessage(inputMessage.trim());
            const assistantMessage = {
                role: 'assistant',
                content: response.response || 'I received your message but couldn\'t generate a response.'
            };
            addMessage(assistantMessage);
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage = {
                role: 'assistant',
                content: '⚠️ Sorry, I encountered an error. Please check your connection and try again.'
            };
            addMessage(errorMessage);
        } finally {
            setIsLoading(false);
            inputRef.current?.focus();
        }
    };

    const handleResetChat = () => {
        resetMode(true);
        setInputMessage('');
        inputRef.current?.focus();
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <div className="flex flex-col h-full">
            {/* Header Configuration 
                - Mobile: pr-20 to clear the Top-Right Hamburger.
                - Desktop: px-8 standard padding.
            */}
            <header className="backdrop-blur-xl bg-white/5 border-b border-white/10 px-4 pr-20 md:px-8 py-4 flex justify-between items-center">

                {/* Left Side Container */}
                <div className="flex items-center gap-3">
                    {/* MOBILE RESET BUTTON (Top-Left Position) */}
                    <button
                        onClick={handleResetChat}
                        className="md:hidden p-2 -ml-2 text-slate-300 hover:text-white bg-white/5 rounded-lg border border-white/10 transition-colors"
                        aria-label="Reset chat"
                    >
                        <RotateCcw className="w-5 h-5" />
                    </button>

                    {/* Title Group */}
                    <div>
                        <h2 className="text-lg md:text-xl font-bold text-white tracking-tight">Rudra AI</h2>
                        <p className="text-xs md:text-sm text-slate-400 mt-0.5">Your AI Personal Assistant</p>
                    </div>
                </div>

                {/* DESKTOP RESET BUTTON (Right Side) 
                    - Hidden on mobile (md:flex) because mobile uses the icon on the left.
                */}
                <button
                    onClick={handleResetChat}
                    className="hidden md:flex items-center gap-2 px-3 md:px-4 py-2 text-xs md:text-sm bg-white/10 hover:bg-white/20 text-white rounded-lg transition-all duration-300 backdrop-blur-sm border border-white/10 hover:border-white/20 group"
                    aria-label="Reset chat"
                >
                    <RotateCcw className="w-3 h-3 md:w-4 md:h-4 group-hover:rotate-180 transition-transform duration-500" />
                    <span className="hidden sm:inline font-medium">New Chat</span>
                </button>
            </header>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto px-4 md:px-8 py-4 md:py-6 space-y-4 md:space-y-6 scrollbar-thin scrollbar-thumb-white/20 scrollbar-track-transparent">
                <div className="max-w-5xl mx-auto space-y-4 md:space-y-6">
                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-slideIn`}
                            style={{ animationDelay: `${index * 50}ms` }}
                        >
                            <div className={`flex items-start gap-2 md:gap-3 max-w-[90%] md:max-w-3xl ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
                                }`}>
                                {/* Avatar */}
                                <div className={`flex-shrink-0 w-8 h-8 md:w-10 md:h-10 rounded-xl md:rounded-2xl flex items-center justify-center font-bold text-xs md:text-sm shadow-lg ${message.role === 'user'
                                    ? 'bg-gradient-to-br from-cyan-500 to-blue-600 text-white'
                                    : 'bg-gradient-to-br from-violet-500 to-purple-600 text-white'
                                    }`}>
                                    {message.role === 'user' ? 'You' : 'R'}
                                </div>

                                {/* Message Bubble */}
                                <div className={`relative group ${message.role === 'user'
                                    ? 'bg-gradient-to-br from-cyan-500/20 to-blue-600/20 backdrop-blur-xl border border-cyan-500/30'
                                    : 'bg-white/10 backdrop-blur-xl border border-white/20'
                                    } rounded-xl md:rounded-2xl px-3 py-2 md:px-5 md:py-4 shadow-xl transition-all duration-300 hover:shadow-2xl`}>

                                    {/* Glow effect */}
                                    <div className={`absolute inset-0 rounded-xl md:rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 blur-xl ${message.role === 'user'
                                        ? 'bg-gradient-to-br from-cyan-500/30 to-blue-600/30'
                                        : 'bg-white/10'
                                        }`}></div>

                                    <div className="relative z-10">
                                        {message.role === 'assistant' ? (
                                            <MarkdownContent content={message.content} accentColor="cyan" />
                                        ) : (
                                            <p className="text-sm text-white leading-relaxed">{message.content}</p>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}

                    {/* Loading Indicator */}
                    {isLoading && (
                        <div className="flex justify-start animate-slideIn">
                            <div className="flex items-start gap-2 md:gap-3 max-w-[90%] md:max-w-3xl">
                                <div className="flex-shrink-0 w-8 h-8 md:w-10 md:h-10 rounded-xl md:rounded-2xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center text-white font-bold text-xs md:text-sm shadow-lg">
                                    R
                                </div>
                                <div className="bg-white/10 backdrop-blur-xl border border-white/20 px-3 py-2 md:px-5 md:py-4 rounded-xl md:rounded-2xl shadow-xl">
                                    <div className="flex items-center gap-3">
                                        <Loader2 className="w-4 h-4 md:w-5 md:h-5 text-cyan-400 animate-spin" />
                                        <span className="text-xs md:text-sm text-slate-300">Thinking...</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Form */}
            <form onSubmit={handleSendMessage} className="px-4 md:px-8 py-4 backdrop-blur-xl bg-white/5 border-t border-white/10">
                <div className="max-w-5xl mx-auto">
                    <div className="flex items-end gap-2 md:gap-3 bg-white/10 backdrop-blur-sm p-2 md:p-3 rounded-xl md:rounded-2xl border border-white/20 focus-within:border-cyan-500/50 transition-all duration-300">
                        <input
                            ref={inputRef}
                            type="text"
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Ask Rudra anything..."
                            className="flex-1 bg-transparent px-3 md:px-4 py-2 md:py-3 text-white placeholder-slate-500 focus:outline-none text-sm"
                            disabled={isLoading}
                            maxLength={2000}
                        />
                        <button
                            type="submit"
                            disabled={!inputMessage.trim() || isLoading}
                            className="px-3 md:px-5 py-2 md:py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-lg md:rounded-xl hover:from-cyan-600 hover:to-blue-700 disabled:from-slate-700 disabled:to-slate-800 disabled:cursor-not-allowed transition-all duration-300 flex items-center gap-2 font-medium shadow-lg hover:shadow-2xl hover:scale-105 active:scale-95 group"
                            aria-label="Send message"
                        >
                            <Send className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                            <span className="hidden sm:inline text-sm">Send</span>
                        </button>
                    </div>
                    <p className="text-xs text-slate-500 mt-2 text-center hidden md:block">
                        Press Enter to send • Shift+Enter for new line
                    </p>
                </div>
            </form>

            <style jsx>{`
                @keyframes slideIn {
                    from {
                        opacity: 0;
                        transform: translateY(10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                .animate-slideIn {
                    animation: slideIn 0.3s ease-out forwards;
                }
                .scrollbar-thin::-webkit-scrollbar {
                    width: 6px;
                }
                .scrollbar-thin::-webkit-scrollbar-track {
                    background: transparent;
                }
                .scrollbar-thin::-webkit-scrollbar-thumb {
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 3px;
                }
                .scrollbar-thin::-webkit-scrollbar-thumb:hover {
                    background: rgba(255, 255, 255, 0.3);
                }
            `}</style>
        </div>
    );
};

export default ChatInterface;