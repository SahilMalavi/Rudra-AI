import React, { useState } from 'react';
import { MessageCircle, Image, FileText, Menu, X, Sparkles } from 'lucide-react';

const Sidebar = ({ currentMode, setCurrentMode }) => {
    const [isOpen, setIsOpen] = useState(false);

    const modes = [
        {
            id: 'chat',
            label: 'Rudra AI',
            icon: MessageCircle,
            gradient: 'from-cyan-500 to-blue-500',
            description: 'AI assistant chat'
        },
        {
            id: 'image',
            label: 'Ask-to-Image',
            icon: Image,
            gradient: 'from-violet-500 to-purple-500',
            description: 'Image interaction'
        },
        {
            id: 'pdf',
            label: 'Chat-with-PDF',
            icon: FileText,
            gradient: 'from-fuchsia-500 to-pink-500',
            description: 'Document chatting'
        },
    ];

    const handleModeChange = (modeId) => {
        setCurrentMode(modeId);
        setIsOpen(false);
    };

    return (
        <>
            {/* Mobile menu button - MOVED TO TOP RIGHT CORNER */}
            {/* Positioned at top-6 right-6 to take the standard "Action" spot. 
                (You should move your existing Reset Chat button to the Left to swap them) */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="md:hidden fixed top-6 right-6 z-[60] p-3 bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/20 text-white hover:bg-white/20 transition-all duration-300 group"
                aria-label="Toggle menu"
            >
                {isOpen ? (
                    <X className="w-6 h-6 transition-transform group-hover:rotate-90" />
                ) : (
                    <Menu className="w-6 h-6 transition-transform group-hover:scale-110" />
                )}
            </button>

            {/* Overlay for mobile */}
            {isOpen && (
                <div
                    className="md:hidden fixed inset-0 bg-black/60 backdrop-blur-sm z-40 animate-fadeIn"
                    onClick={() => setIsOpen(false)}
                />
            )}

            {/* Sidebar */}
            <aside
                className={`fixed md:relative inset-y-0 left-0 z-50 w-72 bg-gradient-to-b from-slate-900/95 via-indigo-950/95 to-slate-900/95 backdrop-blur-xl border-r border-white/10 transform ${isOpen ? 'translate-x-0' : '-translate-x-full'
                    } md:translate-x-0 transition-transform duration-500 ease-out shadow-2xl`}
            >
                {/* Header - Standard padding */}
                <div className="p-6 border-b border-white/10">
                    <div className="flex items-center space-x-2 mb-1">
                        <div className="relative">
                            <Sparkles className="w-7 h-7 text-cyan-400 animate-pulse" />
                            <div className="absolute inset-0 blur-xl bg-cyan-400/50 animate-pulse"></div>
                        </div>
                        <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent tracking-tight">
                            Rudra AI
                        </h1>
                    </div>
                    <p className="text-xs text-slate-400 font-light ml-9">Personal Assistant</p>
                </div>

                {/* Navigation */}
                <nav className="px-4 py-6">
                    <div className="space-y-2">
                        {modes.map((mode, index) => {
                            const Icon = mode.icon;
                            const isActive = currentMode === mode.id;

                            return (
                                <button
                                    key={mode.id}
                                    onClick={() => handleModeChange(mode.id)}
                                    className={`w-full group relative overflow-hidden rounded-xl transition-all duration-300 ${isActive
                                        ? 'scale-105 shadow-2xl'
                                        : 'hover:scale-102 hover:shadow-xl'
                                        }`}
                                    style={{
                                        animationDelay: `${index * 100}ms`
                                    }}
                                >
                                    {/* Background gradient */}
                                    <div className={`absolute inset-0 bg-gradient-to-r ${mode.gradient} opacity-0 group-hover:opacity-100 transition-opacity duration-300 ${isActive ? 'opacity-100' : ''
                                        }`}></div>

                                    {/* Border glow */}
                                    <div className={`absolute inset-0 bg-gradient-to-r ${mode.gradient} blur-xl opacity-0 group-hover:opacity-50 transition-opacity duration-300 ${isActive ? 'opacity-50' : ''
                                        }`}></div>

                                    {/* Content */}
                                    <div className={`relative flex items-center px-4 py-3 border transition-all duration-300 rounded-xl ${isActive
                                        ? 'bg-white/5 border-white/20'
                                        : 'bg-white/5 border-white/10 hover:border-white/20'
                                        }`}>
                                        <div className={`p-2 rounded-lg mr-3 transition-all duration-300 ${isActive
                                            ? 'bg-white/20'
                                            : 'bg-white/10 group-hover:bg-white/20'
                                            }`}>
                                            <Icon className={`w-4 h-4 transition-all duration-300 ${isActive
                                                ? 'text-white'
                                                : 'text-slate-300 group-hover:text-white'
                                                }`} />
                                        </div>
                                        <div className="flex-1 text-left">
                                            <div className={`text-sm font-semibold transition-colors duration-300 ${isActive
                                                ? 'text-white'
                                                : 'text-slate-300 group-hover:text-white'
                                                }`}>
                                                {mode.label}
                                            </div>
                                            <div className="text-xs text-slate-500 mt-0.5">
                                                {mode.description}
                                            </div>
                                        </div>

                                        {/* Active indicator */}
                                        {isActive && (
                                            <div className="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></div>
                                        )}
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                </nav>

                {/* Footer info */}
                <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-white/10">
                    <div className="bg-white/5 backdrop-blur-sm rounded-lg p-3 border border-white/10">
                        <p className="text-xs text-slate-400 leading-relaxed">
                            Created by <span className="text-cyan-400 font-semibold">Sahil Malavi</span>
                        </p>
                        <p className="text-xs text-slate-500 mt-1">
                            Powered by AI technology
                        </p>
                    </div>
                </div>
            </aside>

            <style jsx>{`
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                .animate-fadeIn {
                    animation: fadeIn 0.3s ease-out;
                }
                .hover\\:scale-102:hover {
                    transform: scale(1.02);
                }
            `}</style>
        </>
    );
};

export default Sidebar;