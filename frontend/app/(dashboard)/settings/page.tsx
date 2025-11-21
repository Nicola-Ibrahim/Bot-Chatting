'use client';

import { SettingsForm } from '@/components/SettingsForm';
import { useAppContext } from '@/context/AppContext';

export default function Page() {
  const { user } = useAppContext();
  return <SettingsForm user={user} />;
}