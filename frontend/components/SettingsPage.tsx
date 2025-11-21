import React from 'react';
import { UserProfile } from '../types';
import { Bell, Shield, Moon, Smartphone, Monitor, Save } from 'lucide-react';

interface SettingsPageProps {
  user: UserProfile | null;
}

export const SettingsPage: React.FC<SettingsPageProps> = ({ user }) => {
  return (
    <div className="flex-1 h-full overflow-y-auto p-4 lg:p-12 animate-fade-in">
      <div className="max-w-3xl mx-auto space-y-8">
        
        <div>
            <h2 className="text-2xl font-bold text-white">Settings</h2>
            <p className="text-gray-400 mt-1">Manage your account preferences and application settings.</p>
        </div>

        <div className="space-y-6">
            {/* Account Section */}
            <section className="bg-gray-900/50 border border-gray-800 rounded-2xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <Shield className="w-5 h-5 text-indigo-400" />
                    Account Information
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                        <label className="text-sm text-gray-400">Display Name</label>
                        <input 
                            type="text" 
                            defaultValue={user?.name} 
                            className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-2.5 text-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                        />
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm text-gray-400">Email Address</label>
                        <input 
                            type="email" 
                            defaultValue={user?.email} 
                            disabled
                            className="w-full bg-gray-950/50 border border-gray-800 rounded-lg px-4 py-2.5 text-gray-500 cursor-not-allowed"
                        />
                    </div>
                </div>
            </section>

            {/* Appearance Section */}
            <section className="bg-gray-900/50 border border-gray-800 rounded-2xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <Monitor className="w-5 h-5 text-indigo-400" />
                    Appearance
                </h3>
                <div className="grid grid-cols-3 gap-4">
                    <button className="flex flex-col items-center gap-2 p-4 rounded-xl border border-gray-700 bg-gray-800 text-white">
                        <Moon className="w-6 h-6" />
                        <span className="text-sm font-medium">Dark</span>
                    </button>
                    <button className="flex flex-col items-center gap-2 p-4 rounded-xl border border-gray-800 hover:bg-gray-800/50 text-gray-400 hover:text-white transition-colors">
                        <Smartphone className="w-6 h-6" />
                        <span className="text-sm font-medium">Light</span>
                    </button>
                    <button className="flex flex-col items-center gap-2 p-4 rounded-xl border border-gray-800 hover:bg-gray-800/50 text-gray-400 hover:text-white transition-colors">
                        <Monitor className="w-6 h-6" />
                        <span className="text-sm font-medium">System</span>
                    </button>
                </div>
            </section>

            {/* Notifications Section */}
            <section className="bg-gray-900/50 border border-gray-800 rounded-2xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <Bell className="w-5 h-5 text-indigo-400" />
                    Notifications
                </h3>
                <div className="space-y-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-white font-medium">Email Notifications</p>
                            <p className="text-sm text-gray-500">Receive updates about your account activity.</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" defaultChecked className="sr-only peer" />
                            <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                        </label>
                    </div>
                    <div className="flex items-center justify-between pt-4 border-t border-gray-800">
                        <div>
                            <p className="text-white font-medium">New Feature Announcements</p>
                            <p className="text-sm text-gray-500">Be the first to know about new capabilities.</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" className="sr-only peer" />
                            <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                        </label>
                    </div>
                </div>
            </section>

            <div className="flex justify-end pt-4">
                <button className="flex items-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-medium transition-all shadow-lg shadow-indigo-900/20">
                    <Save className="w-4 h-4" />
                    Save Changes
                </button>
            </div>
        </div>
      </div>
    </div>
  );
};