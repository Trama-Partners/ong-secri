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
        // Amarelo — chamadas para ação (doar, ajudar) e selos de validação.
        // Reservado: nunca usar como cor de acento de projeto, ou o botão de
        // doação deixa de se destacar.
        gold: { 50: '#FEFBF1', 100: '#FDF6E1', 300: '#F8DF92', 500: '#F2C438', 700: '#856B1E' },
        // Verde — eixo Esporte (Canoa Viva, Judô). Cor secundária do manual de marca.
        // O 700 é #58792A e não o #60842E derivado pela mesma proporção das
        // outras cores: aquele dava 4.34:1 sobre branco e reprovava em AA.
        verde: { 50: '#F6F9F1', 100: '#EBF3E1', 300: '#B9D494', 500: '#81B13E', 700: '#58792A' },
        // Laranja — eixo Convivência e bem-estar (Engajando Futuros, Movimento 50+).
        // Cor secundária do manual de marca.
        laranja: { 50: '#FCF4F0', 100: '#F8E7E0', 300: '#E5AB90', 500: '#D06736', 700: '#9B4D28' },
        // Neutros
        ink:  { 50: '#F8F8F8', 100: '#F2F2F2', 200: '#E4E4E4', 300: '#CDCDCD',
                400: '#9B9B9B', 500: '#7A7A7A', 600: '#595959', 800: '#2F2F2F', 900: '#0D0D0D' },
      },
      fontFamily: {
        display: ['Montserrat', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
    },
  },
};
