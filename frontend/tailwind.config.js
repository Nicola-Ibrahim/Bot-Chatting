/**
 * Tailwind CSS configuration for the chat frontend.
 *
 * Dark mode is enabled via class names, and content paths cover
 * Next.js app directories along with components and pages.  An
 * extended colour palette defines a primary purple accent used
 * throughout the UI.  Feel free to customise these values as you
 * iterate on the design.
 */
module.exports = {
  darkMode: 'class',
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#8b5cf6', // purple accent for buttons and highlights
          dark: '#6b21a8',    // darker shade used on hover
        },
        // Dark mode panel colours inspired by modern chat interfaces.  The
        // `panel` colour is used for the chat background; `panelLight`
        // colours the sidebar and cards; `border` defines subtle
        // borders between sections.
        panel: '#1f2437',
        panelLight: '#2b3153',
        border: '#3f4a7f',
      },
      // Custom keyframes and animations used throughout the UI.  The
      // fadeIn animation gradually increases opacity, while the
      // slideUp animation combines a fade with a subtle upward
      // movement.  These are applied to page transitions and
      // incoming chat messages.
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(0.5rem)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        fadeIn: 'fadeIn 0.5s ease-out forwards',
        slideUp: 'slideUp 0.5s ease-out forwards',
      },
    },
  },
  plugins: [],
};