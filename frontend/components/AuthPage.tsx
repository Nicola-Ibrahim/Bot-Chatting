'use client';

import React, { useState } from 'react';
import { Sparkles, ArrowRight, Mail, Lock, User, UserCircle } from 'lucide-react';
import { useAppContext } from '@/context/AppContext';

export const AuthPage: React.FC = () => {
  const { login, guestLogin } = useAppContext();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    setTimeout(() => {
      login({
        id: '1',
        name: name || email.split('@')[0],
        email: email,
      });
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen w-full bg-gray-950 flex">
      <div className="hidden lg:flex w-1/2 bg-gray-900 relative overflow-hidden items-center justify-center">
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop')] bg-cover bg-center opacity-20"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/40 to-black/60"></div>
        <div className="relative z-10 p-12 text-white max-w-lg">
            <div className="w-16 h-16 bg-indigo-600 rounded-2xl flex items-center justify-center mb-8 shadow-2xl shadow-indigo-500/30">
                <Sparkles className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-5xl font-bold mb-6 tracking-tight">Welcome to Horizon Chat</h1>
            <p className="text-lg text-gray-300 leading-relaxed">
                Experience the next generation of conversational intelligence. 
                Seamlessly integrated with our advanced AI engine for faster, smarter, and more intuitive interactions.
            </p>
        </div>
      </div>

      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-gray-950">
        <div className="w-full max-w-md space-y-8 animate-fade-in">
          <div className="text-center lg:text-left">
            <h2 className="text-3xl font-bold text-white tracking-tight">
                {isLogin ? 'Sign in to your account' : 'Create your account'}
            </h2>
            <p className="mt-2 text-gray-400">
                {isLogin ? "Don't have an account?" : "Already have an account?"}
                <button 
                    onClick={() => setIsLogin(!isLogin)}
                    className="ml-2 text-indigo-400 hover:text-indigo-300 font-medium transition-colors"
                >
                    {isLogin ? 'Sign up' : 'Log in'}
                </button>
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6 mt-8">
            {!isLogin && (
                <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300 ml-1">Full Name</label>
                    <div className="relative">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <User className="h-5 w-5 text-gray-500" />
                        </div>
                        <input
                            type="text"
                            required
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className="block w-full pl-10 pr-3 py-3 border border-gray-800 rounded-xl leading-5 bg-gray-900 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 sm:text-sm transition-all"
                            placeholder="John Doe"
                        />
                    </div>
                </div>
            )}

            <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300 ml-1">Email Address</label>
                <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Mail className="h-5 w-5 text-gray-500" />
                    </div>
                    <input
                        type="email"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="block w-full pl-10 pr-3 py-3 border border-gray-800 rounded-xl leading-5 bg-gray-900 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 sm:text-sm transition-all"
                        placeholder="you@example.com"
                    />
                </div>
            </div>

            <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300 ml-1">Password</label>
                <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Lock className="h-5 w-5 text-gray-500" />
                    </div>
                    <input
                        type="password"
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="block w-full pl-10 pr-3 py-3 border border-gray-800 rounded-xl leading-5 bg-gray-900 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 sm:text-sm transition-all"
                        placeholder="••••••••"
                    />
                </div>
            </div>

            <div className="space-y-4">
                <button
                    type="submit"
                    disabled={loading}
                    className="w-full flex justify-center py-3.5 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:scale-[1.01] active:scale-[0.99]"
                >
                    {loading ? (
                        <span className="flex items-center gap-2">
                            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                            Processing...
                        </span>
                    ) : (
                        <span className="flex items-center gap-2">
                            {isLogin ? 'Sign In' : 'Create Account'} 
                            <ArrowRight className="w-4 h-4" />
                        </span>
                    )}
                </button>

                <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                        <div className="w-full border-t border-gray-800"></div>
                    </div>
                    <div className="relative flex justify-center text-sm">
                        <span className="px-2 bg-gray-950 text-gray-500">Or</span>
                    </div>
                </div>

                <button
                    type="button"
                    onClick={guestLogin}
                    className="w-full flex justify-center items-center gap-2 py-3.5 px-4 border border-gray-800 hover:border-gray-700 rounded-xl shadow-sm text-sm font-medium text-gray-300 bg-transparent hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-800 transition-all hover:text-white"
                >
                    <UserCircle className="w-5 h-5" />
                    Continue as Guest
                </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};