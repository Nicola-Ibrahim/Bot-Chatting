'use client';

import { SettingsPage } from '@/components/SettingsPage';
import { useAppContext } from '@/context/AppContext';

export default function Page() {
  const { user } = useAppContext();
  return <SettingsPage user={user} />;
}