/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*"],
  theme: {
    extend: {
      screens: {
        xs: { max: "500px" },
        sx: { max: "900px" },
      },
      fontFamily: {
        roboto: ["Roboto", "sans-serif"],
        "roboto-condensed": ["Roboto Condensed", "sans-serif"],
        "roboto-slab": ["Roboto Slab", "serif"],
        poppins: ["Poppins", "sans-serif"],
        "courier-prime": ["Courier Prime", "monospace"],
        exo: ["Exo", "sans-serif"],
        lora: ["Lora", "serif"],
        barlow: ["Barlow", "sans-serif"],
        "open-sans": ["Open Sans", "sans-serif"],
        lato: ["Lato", "sans-serif"],
        merriweather: ["Merriweather", "serif"],
      },
    },
  },
  plugins: [],
};
