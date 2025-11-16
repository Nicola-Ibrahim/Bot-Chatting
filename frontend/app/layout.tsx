import './globals.css';
import { ReactNode } from 'react';
import dynamic from 'next/dynamic';

// Dynamically import the navigation bar as a client component.  This
// prevents Next.js from attempting to render it on the server and
// allows us to use hooks (such as usePathname) within the NavBar.
const NavBar = dynamic(() => import('@/components/NavBar'), { ssr: false });

/**
 * Root layout for all pages.  This component wraps the application
 * with the necessary HTML and body tags and imports the global
 * styles.  It also sets a default title for the application via
 * metadata.
 */
export const metadata = {
  title: 'Chat App',
  description: 'Minimal streaming chat built with FastAPI and Next.js',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body>
        {/* Global navigation */}
        <NavBar />
        {/* Page content */}
        {children}
      </body>
    </html>
  );
}
