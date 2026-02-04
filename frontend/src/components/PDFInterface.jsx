import React, { useState, useRef, useEffect } from 'react';
import { Upload, Send, X, FileText, Loader2 } from 'lucide-react';
import { chatAPI } from '../services/api';
import MarkdownContent from './MarkdownContent';

const PDFInterface = ({ messages, addMessage, clearMessages }) => {
    const [inputMessage, setInputMessage] = useState('');
    const [uploadedPDF, setUploadedPDF] = useState(null);
    const [pdfName, setPdfName] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const fileInputRef = useRef(null);
    const inputRef = useRef(null);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        if (uploadedPDF) {
            inputRef.current?.focus();
        }
    }, [uploadedPDF]);

    const handlePDFUpload = (file) => {
        if (file && file.type === 'application/pdf') {
            if (file.size > 20 * 1024 * 1024) { // 20MB limit
                alert('PDF size should be less than 20MB');
                return;
            }

            setUploadedPDF(file);
            setPdfName(file.name);
            clearMessages();
        } else {
            alert('Please upload a valid PDF file');
        }
    };

    const handleFileChange = (e) => {
        const file = e.target.files?.[0];
        if (file) handlePDFUpload(file);
    };

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        const file = e.dataTransfer.files?.[0];
        if (file) handlePDFUpload(file);
    };

    const handleRemovePDF = () => {
        setUploadedPDF(null);
        setPdfName('');
        clearMessages();
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    const handleSendMessage = async (e) => {
        e?.preventDefault();
        if (!inputMessage.trim() || !uploadedPDF || isLoading) return;

        const userMessage = { role: 'user', content: inputMessage.trim() };
        addMessage(userMessage);
        setInputMessage('');
        setIsLoading(true);

        try {
            const response = await chatAPI.sendPDFMessage(inputMessage.trim(), uploadedPDF);
            const assistantMessage = {
                role: 'assistant',
                content: response.response || 'I analyzed the PDF but couldn\'t generate a response.'
            };
            addMessage(assistantMessage);
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage = {
                role: 'assistant',
                content: '⚠️ Sorry, I encountered an error processing the PDF. Please try again.'
            };
            addMessage(errorMessage);
        } finally {
            setIsLoading(false);
            inputRef.current?.focus();
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <div className="flex flex-col h-full">
            {/* Header */}
            <header className="backdrop-blur-xl bg-white/5 border-b border-white/10 px-4 md:px-8 py-4">
                <h2 className="text-lg md:text-xl font-bold text-white tracking-tight">Chat-with-PDF</h2>
                <p className="text-xs md:text-sm text-slate-400 mt-0.5">Upload a PDF for document chatting</p>
            </header>

            {/* Content */}
            <div className="flex-1 overflow-y-auto px-4 md:px-8 py-4 md:py-6 scrollbar-thin scrollbar-thumb-white/20 scrollbar-track-transparent">
                <div className="max-w-5xl mx-auto">
                    {!uploadedPDF ? (
                        <div className="flex flex-col items-center justify-center min-h-[400px] md:min-h-[500px]">
                            <div
                                className={`w-full transition-all duration-300 ${dragActive ? 'scale-105' : 'scale-100'
                                    }`}
                                onDragEnter={handleDrag}
                                onDragLeave={handleDrag}
                                onDragOver={handleDrag}
                                onDrop={handleDrop}
                            >
                                <div className={`relative border-2 border-dashed rounded-2xl md:rounded-3xl p-8 md:p-12 text-center transition-all duration-300 ${dragActive
                                        ? 'border-fuchsia-500 bg-fuchsia-500/10'
                                        : 'border-white/20 bg-white/5 hover:border-fuchsia-500/50 hover:bg-white/10'
                                    }`}>
                                    {/* Glow effect */}
                                    <div className={`absolute inset-0 rounded-2xl md:rounded-3xl blur-2xl transition-opacity duration-300 ${dragActive ? 'opacity-50' : 'opacity-0'
                                        } bg-gradient-to-br from-fuchsia-500/30 to-pink-600/30`}></div>

                                    <div className="relative z-10">
                                        <div className="w-16 h-16 md:w-20 md:h-20 mx-auto mb-4 md:mb-6 bg-gradient-to-br from-fuchsia-500 to-pink-600 rounded-2xl md:rounded-3xl flex items-center justify-center shadow-2xl">
                                            <FileText className="w-8 h-8 md:w-10 md:h-10 text-white" />
                                        </div>
                                        <h3 className="text-xl md:text-2xl font-bold text-white mb-2 md:mb-3">
                                            {dragActive ? 'Drop your PDF here' : 'Upload a PDF'}
                                        </h3>
                                        <p className="text-sm md:text-base text-slate-400 mb-6 md:mb-8 max-w-md mx-auto px-4">
                                            Drag and drop a PDF document or click to browse
                                        </p>

                                        <input
                                            ref={fileInputRef}
                                            type="file"
                                            accept="application/pdf"
                                            onChange={handleFileChange}
                                            className="hidden"
                                            id="pdf-upload"
                                        />
                                        <label
                                            htmlFor="pdf-upload"
                                            className="inline-flex items-center gap-2 px-6 md:px-8 py-3 md:py-4 bg-gradient-to-r from-fuchsia-500 to-pink-600 text-white rounded-lg md:rounded-xl hover:from-fuchsia-600 hover:to-pink-700 cursor-pointer transition-all duration-300 font-medium shadow-xl hover:shadow-2xl hover:scale-105 active:scale-95 text-sm md:text-base"
                                        >
                                            <Upload className="w-4 h-4 md:w-5 md:h-5" />
                                            Choose PDF
                                        </label>
                                        <p className="text-xs text-slate-500 mt-4 md:mt-6">
                                            Supports PDF files • Max 20MB
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="space-y-4 md:space-y-6">
                            {/* PDF info card */}
                            <div className="relative group">
                                <div className="absolute inset-0 bg-gradient-to-br from-fuchsia-500/20 to-pink-600/20 rounded-2xl md:rounded-3xl blur-2xl group-hover:blur-3xl transition-all duration-300"></div>
                                <div className="relative bg-white/5 backdrop-blur-xl border border-white/20 rounded-2xl md:rounded-3xl p-4 md:p-6 shadow-2xl flex items-center gap-3 md:gap-4">
                                    <div className="flex-shrink-0 w-12 h-12 md:w-16 md:h-16 bg-gradient-to-br from-fuchsia-500 to-pink-600 rounded-xl md:rounded-2xl flex items-center justify-center shadow-lg">
                                        <FileText className="w-6 h-6 md:w-8 md:h-8 text-white" />
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <p className="font-semibold text-white truncate text-sm md:text-lg">{pdfName}</p>
                                        <p className="text-xs md:text-sm text-slate-400 mt-0.5 md:mt-1">PDF loaded and ready for questions</p>
                                    </div>
                                    <button
                                        onClick={handleRemovePDF}
                                        className="flex-shrink-0 p-2 md:p-2.5 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg md:rounded-xl transition-all duration-300 group/btn"
                                        aria-label="Remove PDF"
                                    >
                                        <X className="w-4 h-4 md:w-5 md:h-5 group-hover/btn:rotate-90 transition-transform duration-300" />
                                    </button>
                                </div>
                            </div>

                            {/* Success message */}
                            {messages.length === 0 && (
                                <div className="bg-gradient-to-r from-fuchsia-500/10 to-pink-600/10 backdrop-blur-sm border border-fuchsia-500/30 rounded-xl md:rounded-2xl p-3 md:p-4 flex items-center gap-3">
                                    <div className="w-2 h-2 bg-fuchsia-400 rounded-full animate-pulse"></div>
                                    <p className="text-xs md:text-sm text-fuchsia-200 font-medium">
                                        ✨ PDF uploaded! Ask questions below
                                    </p>
                                </div>
                            )}

                            {/* Messages */}
                            <div className="space-y-3 md:space-y-4">
                                {messages.map((message, index) => (
                                    <div
                                        key={index}
                                        className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-slideIn`}
                                        style={{ animationDelay: `${index * 50}ms` }}
                                    >
                                        <div className={`max-w-[90%] md:max-w-3xl ${message.role === 'user'
                                                ? 'bg-gradient-to-br from-fuchsia-500/20 to-pink-600/20 backdrop-blur-xl border border-fuchsia-500/30'
                                                : 'bg-white/10 backdrop-blur-xl border border-white/20'
                                            } px-3 py-2 md:px-5 md:py-4 rounded-xl md:rounded-2xl shadow-xl`}>
                                            {message.role === 'assistant' ? (
                                                <MarkdownContent content={message.content} accentColor="fuchsia" />
                                            ) : (
                                                <p className="text-sm text-white leading-relaxed">{message.content}</p>
                                            )}
                                        </div>
                                    </div>
                                ))}

                                {/* Loading indicator */}
                                {isLoading && (
                                    <div className="flex justify-start animate-slideIn">
                                        <div className="bg-white/10 backdrop-blur-xl border border-white/20 px-3 py-2 md:px-5 md:py-4 rounded-xl md:rounded-2xl shadow-xl">
                                            <div className="flex items-center gap-3">
                                                <Loader2 className="w-4 h-4 md:w-5 md:h-5 text-fuchsia-400 animate-spin" />
                                                <span className="text-xs md:text-sm text-slate-300">Analyzing PDF...</span>
                                            </div>
                                        </div>
                                    </div>
                                )}
                                <div ref={messagesEndRef} />
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Input form */}
            {uploadedPDF && (
                <form onSubmit={handleSendMessage} className="px-4 md:px-8 py-4 backdrop-blur-xl bg-white/5 border-t border-white/10">
                    <div className="max-w-5xl mx-auto">
                        <div className="flex items-end gap-2 md:gap-3 bg-white/10 backdrop-blur-sm p-2 md:p-3 rounded-xl md:rounded-2xl border border-white/20 focus-within:border-fuchsia-500/50 transition-all duration-300">
                            <input
                                ref={inputRef}
                                type="text"
                                value={inputMessage}
                                onChange={(e) => setInputMessage(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Ask about the PDF..."
                                className="flex-1 bg-transparent px-3 md:px-4 py-2 md:py-3 text-white placeholder-slate-500 focus:outline-none text-sm"
                                disabled={isLoading}
                                maxLength={2000}
                            />
                            <button
                                type="submit"
                                disabled={!inputMessage.trim() || isLoading}
                                className="px-3 md:px-5 py-2 md:py-3 bg-gradient-to-r from-fuchsia-500 to-pink-600 text-white rounded-lg md:rounded-xl hover:from-fuchsia-600 hover:to-pink-700 disabled:from-slate-700 disabled:to-slate-800 disabled:cursor-not-allowed transition-all duration-300 flex items-center gap-2 font-medium shadow-lg hover:shadow-2xl hover:scale-105 active:scale-95 group"
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
            )}

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

export default PDFInterface;