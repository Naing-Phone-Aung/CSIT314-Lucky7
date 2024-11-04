/** @type {import('tailwindcss').Config} */

const colors = require("tailwindcss/colors");

module.exports = {
	content: [
		"./templates/**/*.html",
		"./node_modules/flowbite/**/*.js",
		"node_modules/preline/dist/*.js",
		"./node_modules/tailwindcss/",
	],

	darkMode: "class",
	theme: {
	  colors: {
		azure: "#1463F3",
		milk: "#FAF9F6",
		lava: "#605E5D",
		moon: "#1C1917",
		...colors,
	  },
	  extend: {},
	  fontFamily: {
		sora: ["Sora", "sans-serif"],
	  },
	},

	plugins: [require("flowbite/plugin"), require("preline/plugin")],
};
