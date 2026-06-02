import { definePreset } from "@primeuix/themes";
import Aura from "@primeuix/themes/aura";

const ErpTheme = definePreset(Aura, {
  semantic: {
    primary: {
      50: "#f8f5fc",
      100: "#eee8f8",
      200: "#dfd4f0",
      300: "#c9b8e4",
      400: "#ad91d4",
      500: "#9270c0",
      600: "#7557a8",
      700: "#664895",
      800: "#5c3f8c",
      900: "#4d3574",
      950: "#302047",
    },
    colorScheme: {
      light: {
        surface: {
          0: "#ffffff",
          50: "#fcfbfe",
          100: "#f8f5fc",
          200: "#f1ecf8",
          300: "#e4deed",
          400: "#cfc5dc",
          500: "#aaa0b7",
          600: "#82778f",
          700: "#62596d",
          800: "#443d4c",
          900: "#2c2733",
          950: "#19161e",
        },
        primary: {
          color: "#7557a8",
          contrastColor: "#ffffff",
          hoverColor: "#664895",
          activeColor: "#5c3f8c",
        },
        highlight: {
          background: "#eee8f8",
          focusBackground: "#dfd4f0",
          color: "#5c3f8c",
          focusColor: "#4d3574",
        },
      },
    },
  },
});

export default ErpTheme;
