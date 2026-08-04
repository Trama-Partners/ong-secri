/* Design tokens da SECRI — consumidos pelo Tailwind Play CDN.
   Precisa ser carregado logo APÓS o script do CDN e ANTES do conteúdo. */
tailwind.config = {
  theme: {
    extend: {
      colors: {
        // Rosa — cor de marca, acentos e destaques
        rose: { 50: '#FCF5F7', 100: '#F9EBEE', 300: '#EAB4C2', 500: '#D97791', 700: '#A2596C' },
        // Azul — programas e links
        sky:  { 50: '#F6F9FC', 100: '#EDF2F9', 300: '#BBD0EA', 500: '#84A9D9', 700: '#556D8D' },
        // Amarelo — chamadas para ação (doar, ajudar)
        gold: { 50: '#FEFBF1', 100: '#FDF6E1', 300: '#F8DF92', 500: '#F2C438', 700: '#856B1E' },
        // Neutros
        ink:  { 50: '#F8F8F8', 100: '#F2F2F2', 200: '#E4E4E4', 300: '#CDCDCD',
                400: '#9B9B9B', 600: '#595959', 800: '#2F2F2F', 900: '#0D0D0D' },
      },
      fontFamily: {
        display: ['Montserrat', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
    },
  },
};
