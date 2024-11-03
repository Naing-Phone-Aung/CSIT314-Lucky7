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
			...colors,
		},
		extend: {},
		fontFamily: {
			sora: "Sora",
		},
	},

	plugins: [require("flowbite/plugin"), require("preline/plugin")],
};
