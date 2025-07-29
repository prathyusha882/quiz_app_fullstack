// tailwind.config.js

/** @type {import('tailwindcss').Config} */
module.exports = {
  // Configure Tailwind to scan these files for CSS classes
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Scans all .js, .jsx, .ts, .tsx files inside the 'src' directory
    "./public/index.html",       // Also scans your main HTML file for any classes
  ],
  theme: {
    extend: {
      // You can define custom colors, fonts, spacing, etc., here.
      // Example:
      // colors: {
      //   'primary-blue': '#007bff',
      //   'dark-gray': '#333',
      // },
      // fontFamily: {
      //   'sans': ['Inter', 'sans-serif'],
      // },
    },
  },
  plugins: [],
}