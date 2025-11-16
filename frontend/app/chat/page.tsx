"use client";

import { useState, useEffect, useRef } from 'react';
import {
  Plus,
  Search,
  MessageSquare,
  Settings,
  UserCircle,
  Menu,
} from 'lucide-react';
import ChatWindow, { ChatMessage } from '@/components/ChatWindow';
import Composer from '@/components/Composer';
import { streamTokens } from '@/lib/sse';

interface ConversationSummary {
  id: string;
  num_messages: number;
}

/**
 * Main chat page.  Presents a two‑column layout with a collapsible
 * sidebar listing conversation histories and a chat pane for the
 * current conversation.  Messages stream token‑by‑token via SSE.
 */
export default function ChatPage() {
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [currentId, setCurrentId] = useState<string | null>(null);
  const [messageMap, setMessageMap] = useState<Record<string, ChatMessage[]>>({});
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  // Keep a ref to the current messages so that closures always access the latest list
  const messagesRef = useRef<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Fetch conversation summaries on mount
  useEffect(() => {
    loadConversations().catch((err) => console.error(err));
  }, []);

  const loadConversations = async () => {
    try {
      const res = await fetch('/api/conversations', { cache: 'no-store' });
      if (!res.ok) throw new Error(await res.text());
      const data: ConversationSummary[] = await res.json();
      setConversations(data);
    } catch (err) {
      console.error('Failed to load conversations', err);
    }
  };

  // Select an existing conversation and load its messages from local state
  const selectConversation = (id: string) => {
    setCurrentId(id);
    setMessages(messageMap[id] ?? []);
  };

  // Start a new conversation by clearing current ID and messages
  const startNewConversation = () => {
    setCurrentId(null);
    setMessages([]);
  };

  // Handle sending a new user message
  const handleSend = async (content: string) => {
    if (loading) return;
    setLoading(true);
    const userMessage: ChatMessage = { role: 'user', content };
    // Append user message locally
    setMessages((prev) => [...prev, userMessage]);
    // Call backend send endpoint
    try {
      const res = await fetch('/api/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversation_id: currentId,
          messages: [userMessage],
        }),
      });
      if (!res.ok) {
        throw new Error(await res.text());
      }
      const data: { conversation_id: string } = await res.json();
      const convId = data.conversation_id;
      // If new conversation, update list
      if (!currentId) {
        // add placeholder to conversation list; load actual list afterwards
        await loadConversations();
      }
      setCurrentId(convId);
      // Add assistant placeholder message
      const assistantPlaceholder: ChatMessage = { role: 'assistant', content: '' };
      setMessages((prev) => [...prev, assistantPlaceholder]);
      // Start streaming tokens via SSE
      streamTokens(
        `/api/stream?conversation_id=${encodeURIComponent(convId)}`,
        (delta) => {
          // On each token, update the last assistant message
          setMessages((prev) => {
            if (prev.length === 0) return prev;
            const last = prev[prev.length - 1];
            if (last.role !== 'assistant') return prev;
            const updatedLast: ChatMessage = {
              ...last,
              content: last.content + delta,
            };
            return [...prev.slice(0, -1), updatedLast];
          });
        },
        () => {
          // When streaming finishes, persist the message list to the map
          setMessageMap((prev) => ({ ...prev, [convId]: messagesRef.current }));
          setLoading(false);
          // Refresh the conversation summaries
          loadConversations().catch(() => {});
        },
        (err) => {
          console.error('Streaming error', err);
          setLoading(false);
        },
      );
    } catch (err) {
      console.error('Failed to send message', err);
      setLoading(false);
    }
  };

  // Sidebar toggle
  const toggleSidebar = () => setSidebarOpen((open) => !open);

  // Clear all conversations (local state only).  This resets the
  // message map and conversation summaries.  In a real application
  // you might also call the backend to clear persisted history.
  const clearConversations = () => {
    setConversations([]);
    setMessageMap({});
    setCurrentId(null);
    setMessages([]);
  };

  // Update the messagesRef whenever messages change
  useEffect(() => {
    messagesRef.current = messages;
  }, [messages]);

  // Save current messages into messageMap when currentId changes (e.g. when starting a new conversation)
  useEffect(() => {
    if (currentId) {
      setMessageMap((prev) => ({ ...prev, [currentId]: messages }));
    }
  }, [currentId]);

  return (
    <div className="flex h-[calc(100vh-3.5rem)] overflow-hidden">
      {/* Sidebar */}
      <aside
        className={`flex-shrink-0 bg-panelLight border-r border-border flex flex-col transition-transform duration-300 ease-in-out ${
          sidebarOpen ? 'translate-x-0 w-72' : '-translate-x-full w-72 md:translate-x-0'
        }`}
      >
        {/* New chat and search */}
        <div className="p-4 flex items-center gap-2">
          <button
            onClick={startNewConversation}
            className="flex items-center gap-2 px-3 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors w-full"
          >
            <Plus size={18} /> <span className="whitespace-nowrap">New chat</span>
          </button>
          <button
            className="p-2 rounded-lg border border-border text-gray-400 hover:bg-panel transition-colors"
            aria-label="Search"
          >
            <Search size={18} />
          </button>
        </div>
        {/* Conversations header */}
        <div className="flex items-center justify-between px-4 text-xs text-gray-400">
          <span>Your conversations</span>
          <button onClick={clearConversations} className="text-primary hover:underline">Clear All</button>
        </div>
        {/* Conversation list */}
        <div className="flex-1 overflow-y-auto mt-2 space-y-1 px-2">
          {conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => selectConversation(conv.id)}
              className={`group flex items-center gap-2 w-full px-3 py-2 rounded-lg transition-colors ${
                conv.id === currentId ? 'bg-panel text-primary' : 'hover:bg-panel'
              }`}
            >
              <MessageSquare
                size={16}
                className={`${conv.id === currentId ? 'text-primary' : 'text-gray-400 group-hover:text-primary'}`}
              />
              <span className="text-sm truncate flex-1 font-medium">{conv.id}</span>
              <span className="text-xs text-gray-500">{conv.num_messages}</span>
            </button>
          ))}
        </div>
        {/* Last 7 days section (placeholder) */}
        {conversations.length > 0 && (
          <div className="mt-2 border-t border-border px-4 py-2 text-xs text-gray-400">Last 7 Days</div>
        )}
        {/* Footer with settings and profile */}
        <div className="p-4 border-t border-border mt-auto space-y-2">
          <button
            onClick={() => { window.location.assign('/settings'); }}
            className="flex items-center gap-2 w-full px-3 py-2 rounded-lg hover:bg-panel transition-colors"
          >
            <Settings size={16} className="text-gray-400 group-hover:text-primary" />
            <span className="text-sm">Settings</span>
          </button>
          <button
            onClick={() => { window.location.assign('/profile'); }}
            className="flex items-center gap-2 w-full px-3 py-2 rounded-lg hover:bg-panel transition-colors"
          >
            <UserCircle size={16} className="text-gray-400 group-hover:text-primary" />
            <span className="text-sm">Profile</span>
          </button>
        </div>
      </aside>
      {/* Main Chat Area */}
      <div className="flex flex-col flex-1">
        {/* Mobile top bar */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-panelLight md:hidden">
          <button onClick={toggleSidebar} className="text-gray-400 hover:text-primary" aria-label="Toggle sidebar">
            <Menu size={20} />
          </button>
          <h1 className="text-lg font-semibold">Chat</h1>
          <div className="text-xs text-gray-500 truncate max-w-[10rem]">
            {currentId ? currentId : ''}
          </div>
        </div>
        {/* Chat window */}
        <div className="flex-1 overflow-y-auto">
          <ChatWindow messages={messages} />
        </div>
        {/* Composer */}
        <Composer disabled={loading} onSend={handleSend} />
      </div>
    </div>
  );
}
