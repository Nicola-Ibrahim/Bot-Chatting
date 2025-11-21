'use client';

import { ChatPage } from '@/components/ChatPage';
import { useAppContext } from '@/context/AppContext';
import { useEffect } from 'react';

export default function Page() {
  const { 
    conversations, 
    currentConversationId, 
    sendMessage, 
    updateTitle,
    user,
    createNewConversation
  } = useAppContext();

  useEffect(() => {
    if (user && !currentConversationId && conversations.length === 0) {
        createNewConversation();
    }
  }, [user, currentConversationId, conversations, createNewConversation]);

  const currentMessages = conversations.find(c => c.id === currentConversationId)?.messages || [];
  const isNew = currentMessages.length === 0;

  return (
    <ChatPage
      messages={currentMessages}
      onSendMessage={sendMessage}
      onUpdateTitle={updateTitle}
      isNewConversation={isNew}
    />
  );
}