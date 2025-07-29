// postcss.config.js
module.exports = {
  plugins: {
    // This is the correct plugin name for newer Tailwind CSS versions
    '@tailwindcss/postcss': {}, // <-- Make sure this line is correct
    autoprefixer: {},
  },
};