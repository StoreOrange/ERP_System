import { definePreset } from "@primeuix/themes";
import Aura from "@primeuix/themes/aura";

const ErpTheme = definePreset(Aura, {
  semantic: {
    primary: {
      50: "#f3f7fa",
      100: "#e4edf4",
      200: "#cedde9",
      300: "#adc5d8",
      400: "#84a7c0",
      500: "#5f88a5",
      600: "#456b88",
      700: "#35566f",
      800: "#2f4f6f",
      900: "#243d56",
      950: "#17283a",
    },
    colorScheme: {
      light: {
        surface: {
          0: "#ffffff",
          50: "#fdfbf9",
          100: "#f7f4ef",
          200: "#efe8de",
          300: "#e2d8ca",
          400: "#cfc0ad",
          500: "#ab9986",
          600: "#847565",
          700: "#665a4d",
          800: "#463f37",
          900: "#2d2924",
          950: "#1a1714",
        },
        primary: {
          color: "#2f4f6f",
          contrastColor: "#ffffff",
          hoverColor: "#243d56",
          activeColor: "#17283a",
        },
        highlight: {
          background: "#e9eef3",
          focusBackground: "#dbe5ed",
          color: "#243d56",
          focusColor: "#17283a",
        },
      },
    },
  },
});

export default ErpTheme;
