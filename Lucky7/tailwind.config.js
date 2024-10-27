/** @type {import('tailwindcss').Config} */

const colors = require('tailwindcss/colors')

module.exports = {
  content: [
    "./templates/*",
    "./node_modules/preline/dist/*.js",
    "./node_modules/flowbite/dist/*.js"
  ],

  darkMode: "class",

  theme: {
    colors: {
      ...colors,
    },
    extend: {},
    fontFamily: {
      sora: "Sora",
    },
  },

  plugins: [
    require("flowbite/plugin"),
    require("preline/plugin")
  ],
}

