'use client';

import React from 'react';
import { MessageSquare, Settings, User, LogOut, Plus, Menu, X } from 'lucide-react';
import { useRouter, usePathname } from 'next/navigation';
import { useAppContext } from '@/context/AppContext';
import Link from 'next/link';

interface SidebarProps {
  children: React.ReactNode;
}

export const DashboardShell: React.FC<SidebarProps> = ({ children }) => {
  const {
    user,
    logout,
    conversations,
    currentConversationId,
    setCurrentConversationId,
    createNewConversation,
    deleteConversation
  } = useAppContext();

  const router = useRouter();
  const pathname = usePathname();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  const NavItem = ({ href, icon: Icon, label }: { href: string; icon: any; label: string }) => {
    const isActive = pathname === href;
    return (
      <Link
        href={href}
        onClick={() => setIsMobileMenuOpen(false)}
        className={`flex items-center w-full px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${isActive
            ? 'bg-indigo-600/10 text-indigo-400'
            : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
          }`}
      >
        <Icon className="w-5 h-5 mr-3" />
        {label}
      </Link>
    );
  };

  return (
    <div className="flex h-screen bg-gray-950 text-gray-100 overflow-hidden">
      {/* Mobile Header */}
      <div className="lg:hidden fixed top-0 left-0 right-0 h-16 bg-gray-950/80 backdrop-blur-md border-b border-gray-800 z-50 flex items-center justify-between px-4">
        <div className="flex items-center gap-2 font-bold text-xl tracking-tight text-white">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
            <MessageSquare className="w-5 h-5 text-white" />
          </div>
          Horizon
        </div>
        <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="p-2 text-gray-400">
          {isMobileMenuOpen ? <X /> : <Menu />}
        </button>
      </div>

      {/* Sidebar */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 w-72 bg-gray-900 border-r border-gray-800 transform transition-transform duration-300 ease-in-out z-40 lg:transform-none flex flex-col ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
          } lg:flex`}
      >
        <div className="h-16 flex items-center px-6 border-b border-gray-800/50 hidden lg:flex">
          <div className="flex items-center gap-2 font-bold text-xl tracking-tight text-white">
            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <MessageSquare className="w-5 h-5 text-white" />
            </div>
            Horizon
          </div>
        </div>

        <div className="p-4">
          <button
            onClick={() => {
              createNewConversation();
              if (window.innerWidth < 1024) setIsMobileMenuOpen(false);
            }}
            className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white py-2.5 px-4 rounded-xl font-medium transition-all shadow-lg shadow-indigo-900/20 active:scale-95"
          >
            <Plus className="w-5 h-5" />
            New Chat
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1 custom-scrollbar">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider px-3 mb-2 mt-2">
            History
          </div>
          {conversations.length === 0 ? (
            <div className="text-center py-10 px-4 text-gray-500 text-sm">
              No conversations yet. Start a new chat!
            </div>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.id}
                className={`group flex items-center justify-between w-full text-left px-3 py-2.5 rounded-lg text-sm transition-colors cursor-pointer ${currentConversationId === conv.id && pathname === '/chat'
                    ? 'bg-gray-800 text-white'
                    : 'text-gray-400 hover:bg-gray-800/50 hover:text-gray-200'
                  }`}
                onClick={() => {
                  router.push('/chat');
                  setCurrentConversationId(conv.id);
                  setIsMobileMenuOpen(false);
                }}
              >
                <span className="truncate max-w-[180px]">{conv.title}</span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteConversation(conv.id);
                  }}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-400 transition-opacity"
                  title="Delete conversation"
                >
                  <X className="w-3 h-3" />
                </button>
              </div>
            ))
          )}
        </div>

        <div className="p-3 border-t border-gray-800 bg-gray-900/50">
          <div className="space-y-1">
            <NavItem href="/settings" icon={Settings} label="Settings" />
            <button
              onClick={logout}
              className="flex items-center w-full px-3 py-2.5 rounded-lg text-sm font-medium text-red-400 hover:bg-red-900/10 hover:text-red-300 transition-colors"
            >
              <LogOut className="w-5 h-5 mr-3" />
              Log Out
            </button>
          </div>

          {user && (
            <div className="mt-4 flex items-center px-3 pb-2">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-xs">
                {user.name.charAt(0)}
              </div>
              <div className="ml-3 overflow-hidden">
                <p className="text-sm font-medium text-white truncate">{user.name}</p>
                <p className="text-xs text-gray-500 truncate">{user.email}</p>
              </div>
            </div>
          )}
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative w-full h-full pt-16 lg:pt-0 bg-gray-950">
        {children}
      </main>

      {/* Overlay for mobile */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-30 lg:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </div>
  );
};