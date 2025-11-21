'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserProfile, Conversation, Message, Role, AppContextType } from '../types';
import { useRouter } from 'next/navigation';

const AppContext = createContext<AppContextType | undefined>(undefined);

const generateId = () => Math.random().toString(36).substr(2, 9);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const router = useRouter();

  const login = (loggedInUser: UserProfile) => {
    setUser(loggedInUser);
    // Mock initial data
    setConversations([
        {
            id: '1',
            title: 'Introduction to Horizon',
            messages: [
                { id: 'm1', role: Role.USER, content: 'Hello!', timestamp: new Date(Date.now() - 100000) },
                { id: 'm2', role: Role.MODEL, content: 'Welcome to Horizon Chat! How can I assist you today?', timestamp: new Date(Date.now() - 90000) }
            ],
            updatedAt: new Date()
        }
    ]);
    router.push('/chat');
  };

  const guestLogin = () => {
    const guestUser: UserProfile = {
        id: 'guest-' + generateId(),
        name: 'Guest User',
        email: 'guest@horizon.ai',
        isGuest: true
    };
    setUser(guestUser);
    setConversations([]);
    router.push('/chat');
  };

  const logout = () => {
    setUser(null);
    setConversations([]);
    setCurrentConversationId(null);
    router.push('/');
  };

  const createNewConversation = () => {
    const newConv: Conversation = {
      id: generateId(),
      title: 'New Chat',
      messages: [],
      updatedAt: new Date()
    };
    setConversations(prev => [newConv, ...prev]);
    setCurrentConversationId(newConv.id);
    router.push('/chat');
  };

  const sendMessage = (text: string, role: Role) => {
    if (!currentConversationId) {
        createNewConversation();
        // Note: In a strictly async real-world scenario, we'd handle the message queuing here.
        // For this mock, if ID is null, next render will fix it, but let's not break logic.
        return; 
    }

    setConversations(prev => prev.map(conv => {
        if (conv.id === currentConversationId) {
            const newMessage: Message = {
                id: generateId(),
                role,
                content: text,
                timestamp: new Date()
            };
            return {
                ...conv,
                messages: [...conv.messages, newMessage],
                updatedAt: new Date()
            };
        }
        return conv;
    }));
  };

  const updateTitle = (title: string) => {
      if (!currentConversationId) return;
      setConversations(prev => prev.map(conv => 
        conv.id === currentConversationId ? { ...conv, title } : conv
      ));
  };

  const deleteConversation = (id: string) => {
      setConversations(prev => prev.filter(c => c.id !== id));
      if (currentConversationId === id) {
          setCurrentConversationId(null);
      }
  };

  return (
    <AppContext.Provider value={{
      user,
      conversations,
      currentConversationId,
      login,
      logout,
      guestLogin,
      setCurrentConversationId,
      createNewConversation,
      sendMessage,
      updateTitle,
      deleteConversation
    }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};
