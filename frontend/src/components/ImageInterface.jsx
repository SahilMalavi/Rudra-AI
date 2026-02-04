import React, { useState, useRef, useEffect } from 'react';
import { Upload, Send, X, Image as ImageIcon, Loader2 } from 'lucide-react';
import { chatAPI } from '../services/api';
import MarkdownContent from './MarkdownContent';

const ImageInterface = ({ messages, addMessage, clearMessages, uploadedImage, imagePreview, setImageFile, clearImageFile }) => {
    const [inputMessage, setInputMessage] = useState('');
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
        if (uploadedImage) {
            inputRef.current?.focus();
        }
    }, [uploadedImage]);

    const handleImageUpload = (file) => {
        if (file && file.type.startsWith('image/')) {
            if (file.size > 10 * 1024 * 1024) { // 10MB limit
                alert('Image size should be less than 10MB');
                return;
            }

            const reader = new FileReader();
            reader.onload = (e) => {
                setImageFile(file, e.target.result, file.name);
            };
            reader.onerror = () => alert('Error reading image file');
            reader.readAsDataURL(file);
            clearMessages();
        } else {
            alert('Please upload a valid image file (PNG, JPG, GIF, WebP)');
        }
    };

    const handleFileChange = (e) => {
        const file = e.target.files?.[0];
        if (file) handleImageUpload(file);
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
        if (file) handleImageUpload(file);
    };

    const handleRemoveImage = () => {
        clearImageFile();
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    const handleSendMessage = async (e) => {
        e?.preventDefault();
        if (!inputMessage.trim() || !uploadedImage || isLoading) return;

        const userMessage = { role: 'user', content: inputMessage.trim() };
        addMessage(userMessage);
        setInputMessage('');
        setIsLoading(true);

        try {
            const response = await chatAPI.sendImageMessage(inputMessage.trim(), uploadedImage);
            const assistantMessage = {
                role: 'assistant',
                content: response.response || 'I analyzed the image but couldn\'t generate a response.'
            };
            addMessage(assistantMessage);
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage = {
                role: 'assistant',
                content: '⚠️ Sorry, I encountered an error processing the image. Please try again.'
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
                <h2 className="text-lg md:text-xl font-bold text-white tracking-tight">Ask-to-Image</h2>
                <p className="text-xs md:text-sm text-slate-400 mt-0.5">Upload an image for interaction</p>
            </header>

            {/* Content */}
            <div className="flex-1 overflow-y-auto px-4 md:px-8 py-4 md:py-6 scrollbar-thin scrollbar-thumb-white/20 scrollbar-track-transparent">
                <div className="max-w-5xl mx-auto">
                    {!uploadedImage ? (
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
                                        ? 'border-violet-500 bg-violet-500/10'
                                        : 'border-white/20 bg-white/5 hover:border-violet-500/50 hover:bg-white/10'
                                    }`}>
                                    {/* Glow effect */}
                                    <div className={`absolute inset-0 rounded-2xl md:rounded-3xl blur-2xl transition-opacity duration-300 ${dragActive ? 'opacity-50' : 'opacity-0'
                                        } bg-gradient-to-br from-violet-500/30 to-purple-600/30`}></div>

                                    <div className="relative z-10">
                                        <div className="w-16 h-16 md:w-20 md:h-20 mx-auto mb-4 md:mb-6 bg-gradient-to-br from-violet-500 to-purple-600 rounded-2xl md:rounded-3xl flex items-center justify-center shadow-2xl">
                                            <ImageIcon className="w-8 h-8 md:w-10 md:h-10 text-white" />
                                        </div>
                                        <h3 className="text-xl md:text-2xl font-bold text-white mb-2 md:mb-3">
                                            {dragActive ? 'Drop your image here' : 'Upload an Image'}
                                        </h3>
                                        <p className="text-sm md:text-base text-slate-400 mb-6 md:mb-8 max-w-md mx-auto px-4">
                                            Drag and drop an image or click to browse
                                        </p>

                                        <input
                                            ref={fileInputRef}
                                            type="file"
                                            accept="image/*"
                                            onChange={handleFileChange}
                                            className="hidden"
                                            id="image-upload"
                                        />
                                        <label
                                            htmlFor="image-upload"
                                            className="inline-flex items-center gap-2 px-6 md:px-8 py-3 md:py-4 bg-gradient-to-r from-violet-500 to-purple-600 text-white rounded-lg md:rounded-xl hover:from-violet-600 hover:to-purple-700 cursor-pointer transition-all duration-300 font-medium shadow-xl hover:shadow-2xl hover:scale-105 active:scale-95 text-sm md:text-base"
                                        >
                                            <Upload className="w-4 h-4 md:w-5 md:h-5" />
                                            Choose Image
                                        </label>
                                        <p className="text-xs text-slate-500 mt-4 md:mt-6">
                                            Supports PNG, JPG, GIF, WebP • Max 10MB
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="space-y-4 md:space-y-6">
                            {/* Image preview */}
                            <div className="relative group">
                                <div className="absolute inset-0 bg-gradient-to-br from-violet-500/20 to-purple-600/20 rounded-2xl md:rounded-3xl blur-2xl group-hover:blur-3xl transition-all duration-300"></div>
                                <div className="relative bg-white/5 backdrop-blur-xl border border-white/20 rounded-2xl md:rounded-3xl overflow-hidden shadow-2xl">
                                    <img
                                        src={imagePreview}
                                        alt="Uploaded"
                                        className="w-full h-auto max-h-[300px] md:max-h-96 object-contain"
                                    />
                                    <button
                                        onClick={handleRemoveImage}
                                        className="absolute top-2 right-2 md:top-4 md:right-4 p-2 md:p-2.5 bg-red-500/90 backdrop-blur-sm text-white rounded-lg md:rounded-xl hover:bg-red-600 transition-all duration-300 shadow-lg hover:scale-110 active:scale-95 group"
                                        aria-label="Remove image"
                                    >
                                        <X className="w-4 h-4 md:w-5 md:h-5" />
                                    </button>
                                </div>
                            </div>

                            {/* Success message */}
                            {messages.length === 0 && (
                                <div className="bg-gradient-to-r from-violet-500/10 to-purple-600/10 backdrop-blur-sm border border-violet-500/30 rounded-xl md:rounded-2xl p-3 md:p-4 flex items-center gap-3">
                                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-pulse"></div>
                                    <p className="text-xs md:text-sm text-violet-200 font-medium">
                                        ✨ Image uploaded! Ask questions below
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
                                                ? 'bg-gradient-to-br from-violet-500/20 to-purple-600/20 backdrop-blur-xl border border-violet-500/30'
                                                : 'bg-white/10 backdrop-blur-xl border border-white/20'
                                            } px-3 py-2 md:px-5 md:py-4 rounded-xl md:rounded-2xl shadow-xl`}>
                                            {message.role === 'assistant' ? (
                                                <MarkdownContent content={message.content} accentColor="violet" />
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
                                                <Loader2 className="w-4 h-4 md:w-5 md:h-5 text-violet-400 animate-spin" />
                                                <span className="text-xs md:text-sm text-slate-300">Analyzing image...</span>
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
            {uploadedImage && (
                <form onSubmit={handleSendMessage} className="px-4 md:px-8 py-4 backdrop-blur-xl bg-white/5 border-t border-white/10">
                    <div className="max-w-5xl mx-auto">
                        <div className="flex items-end gap-2 md:gap-3 bg-white/10 backdrop-blur-sm p-2 md:p-3 rounded-xl md:rounded-2xl border border-white/20 focus-within:border-violet-500/50 transition-all duration-300">
                            <input
                                ref={inputRef}
                                type="text"
                                value={inputMessage}
                                onChange={(e) => setInputMessage(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Ask about the image..."
                                className="flex-1 bg-transparent px-3 md:px-4 py-2 md:py-3 text-white placeholder-slate-500 focus:outline-none text-sm"
                                disabled={isLoading}
                                maxLength={2000}
                            />
                            <button
                                type="submit"
                                disabled={!inputMessage.trim() || isLoading}
                                className="px-3 md:px-5 py-2 md:py-3 bg-gradient-to-r from-violet-500 to-purple-600 text-white rounded-lg md:rounded-xl hover:from-violet-600 hover:to-purple-700 disabled:from-slate-700 disabled:to-slate-800 disabled:cursor-not-allowed transition-all duration-300 flex items-center gap-2 font-medium shadow-lg hover:shadow-2xl hover:scale-105 active:scale-95 group"
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

export default ImageInterface;