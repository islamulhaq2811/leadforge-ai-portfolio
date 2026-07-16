/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./Frontend/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#00A3FF',
        accent: '#1E90FF',
        dark: '#05060A',
        light: '#E6F1FF',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
