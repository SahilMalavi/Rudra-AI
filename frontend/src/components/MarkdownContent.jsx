import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const MarkdownContent = ({ content, accentColor = 'cyan' }) => {
    const colorClasses = {
        cyan: 'prose-a:text-cyan-400 prose-code:text-cyan-300',
        violet: 'prose-a:text-violet-400 prose-code:text-violet-300',
        fuchsia: 'prose-a:text-fuchsia-400 prose-code:text-fuchsia-300',
    };

    return (
        <div className={`text-sm text-white leading-relaxed prose prose-invert prose-sm max-w-none prose-headings:text-white prose-p:text-slate-200 prose-strong:text-white prose-pre:bg-black/30 ${colorClasses[accentColor] || colorClasses.cyan}`}>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {content}
            </ReactMarkdown>
        </div>
    );
};

export default MarkdownContent;