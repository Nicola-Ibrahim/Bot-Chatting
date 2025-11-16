import Link from 'next/link';

/**
 * Landing page for the chat application.  Presents a short
 * description and a call‑to‑action button linking to the chat UI.
 */
export default function HomePage() {
  return (
    <main className="flex items-center justify-center min-h-[calc(100vh-3.5rem)] bg-gray-950 text-gray-100 animate-fadeIn">
      <div className="text-center space-y-6 p-8 max-w-xl">
        <h1 className="text-5xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500">
          Welcome to HorizonChat
        </h1>
        <p className="text-gray-400">
          A minimal, streaming chat experience powered by FastAPI and Next.js. Messages
          stream token by token for a responsive, real‑time feel. Create an account
          to save your conversation history or continue as a guest.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="/auth/register"
            className="px-8 py-3 rounded-md bg-primary hover:bg-primary-dark transition-colors shadow-md"
          >
            Sign Up
          </Link>
          <Link
            href="/auth/login"
            className="px-8 py-3 rounded-md bg-gray-800 hover:bg-gray-700 transition-colors shadow-md text-gray-100"
          >
            Sign In
          </Link>
          <Link
            href="/chat"
            className="px-8 py-3 rounded-md border border-gray-700 hover:bg-gray-800 transition-colors shadow-md text-gray-100"
          >
            Continue as Guest
          </Link>
        </div>
      </div>
    </main>
  );
}
