import { useEffect, useRef } from 'react';
import { ThumbsUp, ThumbsDown, Copy } from 'lucide-react';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatWindowProps {
  messages: ChatMessage[];
}

/**
 * ChatWindow renders a vertical list of messages with distinct
 * styling for user and assistant messages.  It automatically
 * scrolls to the bottom whenever new messages arrive.
 */
export default function ChatWindow({ messages }: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-3">
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-slideUp`}
        >
          <div
            className={`max-w-sm md:max-w-md px-4 py-3 rounded-xl shadow-sm break-words space-y-1 ${
              msg.role === 'user'
                ? 'bg-primary text-white'
                : 'bg-panelLight text-gray-100 border border-border'
            }`}
          >
            <div>
              {msg.content || (msg.role === 'assistant' ? <span className="italic text-gray-400">…</span> : '')}
            </div>
            {msg.role === 'assistant' && msg.content && (
              <div className="flex gap-3 text-gray-500 text-sm pt-1">
                <button
                  title="Like"
                  className="hover:text-primary transition-colors"
                  onClick={() => { /* placeholder for like */ }}
                >
                  <ThumbsUp size={16} />
                </button>
                <button
                  title="Dislike"
                  className="hover:text-primary transition-colors"
                  onClick={() => { /* placeholder for dislike */ }}
                >
                  <ThumbsDown size={16} />
                </button>
                <button
                  title="Copy"
                  className="hover:text-primary transition-colors"
                  onClick={() => {
                    if (typeof navigator !== 'undefined') {
                      navigator.clipboard.writeText(msg.content).catch(() => {});
                    }
                  }}
                >
                  <Copy size={16} />
                </button>
              </div>
            )}
          </div>
        </div>
      ))}
      {/* dummy div to anchor scroll to bottom */}
      <div ref={bottomRef} />
    </div>
  );
}