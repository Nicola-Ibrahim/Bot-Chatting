
export enum Role {
  USER = 'user',
  MODEL = 'model'
}

export interface Message {
  id: string;
  role: Role;
  content: string;
  timestamp: Date;
  isError?: boolean;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  updatedAt: Date;
}

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  avatarUrl?: string;
  isGuest?: boolean;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: UserProfile | null;
}

export type View = 'chat' | 'settings' | 'profile';

export interface AppContextType {
  user: UserProfile | null;
  conversations: Conversation[];
  currentConversationId: string | null;
  login: (user: UserProfile) => void;
  logout: () => void;
  guestLogin: () => void;
  setCurrentConversationId: (id: string) => void;
  createNewConversation: () => void;
  sendMessage: (text: string, role: Role) => void;
  updateTitle: (title: string) => void;
  deleteConversation: (id: string) => void;
}