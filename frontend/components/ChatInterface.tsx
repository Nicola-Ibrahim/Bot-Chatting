import React, { useEffect, useRef, useState } from 'react';
import { Send, Bot, User, Sparkles, Loader2, AlertCircle } from 'lucide-react';
import { Message, Role } from '../types';
// Import chat service functions from the new backend-powered implementation
import { generateChatResponse, generateConversationTitle } from '../services/chatService';

interface ChatPageProps {
  messages: Message[];
  onSendMessage: (text: string, role: Role) => void;
  onUpdateTitle: (title: string) => void;
  isNewConversation: boolean;
}

export const ChatInterface: React.FC<ChatPageProps> = ({
  messages,
  onSendMessage,
  onUpdateTitle,
  isNewConversation
}) => {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [input]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessageText = input.trim();
    setInput('');
    setError(null);

    // Reset textarea height
    if (textareaRef.current) textareaRef.current.style.height = 'auto';

    // 1. Add User Message
    onSendMessage(userMessageText, Role.USER);
    setIsLoading(true);

    try {
      // Format history for AI
      // Exclude the very last message which we just added (as we need to pass it as 'newMessage')
      // However, state updates are async, so relying on 'messages' prop here might be stale or racey.
      // Better to use the prop messages + the current new message logic.

      const history = messages.map(m => ({
        role: m.role === Role.USER ? 'user' : 'model',
        parts: [{ text: m.content }]
      }));

      // 2. Call API
      const responseText = await generateChatResponse(history, userMessageText);

      // 3. Add AI Message
      onSendMessage(responseText, Role.MODEL);

      // 4. Generate Title if it's the first exchange
      if (isNewConversation && messages.length === 0) {
        const title = await generateConversationTitle(userMessageText);
        onUpdateTitle(title);
      }

    } catch (err: any) {
      console.error(err);
      setError(err.message || "Failed to get response from server.");
      // Optionally add an error message to the chat
      onSendMessage("Sorry, I encountered an error processing your request.", Role.MODEL);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 lg:p-8 scroll-smooth">
        <div className="max-w-3xl mx-auto space-y-8">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-6 animate-fade-in">
              <div className="w-20 h-20 bg-gray-800 rounded-2xl flex items-center justify-center shadow-2xl shadow-indigo-500/10">
                <Sparkles className="w-10 h-10 text-indigo-400" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">How can I help you today?</h2>
                <p className="text-gray-400 max-w-md mx-auto">
                  I can help you write code, analyze data, draft emails, or just have a conversation.
                </p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg">
                {['Explain quantum computing', 'Write a React component', 'Debug a Python script', 'Creative writing ideas'].map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => {
                      setInput(suggestion);
                      if (textareaRef.current) textareaRef.current.focus();
                    }}
                    className="p-3 bg-gray-900/50 border border-gray-800 rounded-xl hover:bg-gray-800 hover:border-gray-700 transition-all text-sm text-gray-300 text-left"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex gap-4 ${msg.role === Role.USER ? 'flex-row-reverse' : 'flex-row'} animate-slide-up`}
              >
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${msg.role === Role.USER
                    ? 'bg-indigo-600 text-white'
                    : 'bg-emerald-600 text-white'
                  }`}>
                  {msg.role === Role.USER ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
                </div>

                <div className={`flex flex-col max-w-[85%] lg:max-w-[75%] ${msg.role === Role.USER ? 'items-end' : 'items-start'}`}>
                  <div className={`px-5 py-3.5 rounded-2xl text-sm leading-relaxed shadow-sm ${msg.role === Role.USER
                      ? 'bg-gray-800 text-gray-100 rounded-tr-sm'
                      : 'bg-gray-900/50 border border-gray-800 text-gray-200 rounded-tl-sm'
                    }`}>
                    {/* Simple text rendering - In a real app, use ReactMarkdown here */}
                    <div className="whitespace-pre-wrap font-sans">
                      {msg.content}
                    </div>
                  </div>
                  <span className="text-xs text-gray-600 mt-1 px-1">
                    {msg.role === Role.USER ? 'You' : 'Horizon'} • {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex gap-4 animate-pulse">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center text-white">
                <Bot className="w-5 h-5" />
              </div>
              <div className="bg-gray-900/50 border border-gray-800 px-5 py-4 rounded-2xl rounded-tl-sm flex items-center gap-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          )}
          {error && (
            <div className="flex items-center justify-center p-4">
              <div className="bg-red-900/20 border border-red-800 text-red-300 px-4 py-3 rounded-lg flex items-center gap-2 text-sm">
                <AlertCircle className="w-4 h-4" />
                {error}
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="p-4 bg-gray-950 border-t border-gray-800/50 relative z-20">
        <div className="max-w-3xl mx-auto relative">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Send a message..."
            rows={1}
            className="w-full bg-gray-900 text-gray-100 rounded-2xl border border-gray-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 pl-4 pr-12 py-4 resize-none overflow-hidden shadow-lg transition-all outline-none scrollbar-hide text-sm md:text-base"
            style={{ minHeight: '56px' }}
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="absolute right-2 bottom-2 p-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-800 disabled:text-gray-600 text-white rounded-xl transition-all disabled:cursor-not-allowed shadow-md"
          >
            {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
          </button>
        </div>
        <div className="text-center mt-2">
          <p className="text-[10px] text-gray-600">
            AI can make mistakes. Check important info.
          </p>
        </div>
      </div>
    </div>
  );
};