module.exports = {
  // 1. Configure content sources
  content: [
    './src/**/*.{html,js,jsx,ts,tsx}',
    './public/index.html',
    './components/**/*.{js,ts,jsx,tsx}',
  ],

  // 2. Theme customization
  theme: {
    screens: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
    },
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#10B981',
        dark: '#1E293B',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      spacing: {
        128: '32rem',
      },
    },
  },

  // 3. Core plugins configuration
  corePlugins: {
    aspectRatio: false, // Disable if using @tailwindcss/aspect-ratio
  },

  // 4. Additional plugins
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
    require('tailwindcss-animate'),
  ],

  // 5. Dark mode configuration
  darkMode: 'class', // or 'media'

  // 6. Important selector
  important: '#app', // Useful for scoping Tailwind
}