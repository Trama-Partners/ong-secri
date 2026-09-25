/* Comportamentos compartilhados do site SECRI.
   Cada bloco só age se os elementos correspondentes existirem na página. */
(function () {
  'use strict';

  // --- Menu mobile -----------------------------------------------------
  var btn = document.getElementById('menuBtn');
  var panel = document.getElementById('mobileNav');

  if (btn && panel) {
    var setOpen = function (open) {
      panel.classList.toggle('hidden', !open);
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
      document.getElementById('iconOpen').classList.toggle('hidden', open);
      document.getElementById('iconClose').classList.toggle('hidden', !open);
    };

    btn.addEventListener('click', function () {
      setOpen(panel.classList.contains('hidden'));
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !panel.classList.contains('hidden')) {
        setOpen(false);
        btn.focus();
      }
    });

    // Volta ao layout desktop com o painel fechado, evitando estado preso.
    window.matchMedia('(min-width: 1024px)').addEventListener('change', function (e) {
      if (e.matches) setOpen(false);
    });
  }

  // --- Carrossel de depoimentos (Home) ---------------------------------
  var quoteEl = document.getElementById('quoteText');

  if (quoteEl) {
    // ATENÇÃO: depoimentos ILUSTRATIVOS, escritos para a versão de validação.
    // As pessoas citadas NÃO existem. Substituir por falas reais coletadas com
    // participantes e famílias antes de o site ir ao ar. A seção na home exibe
    // um selo avisando que são exemplos — não remover esse selo antes da troca.
    var testimonials = [
      { quote: 'O SECRI foi o lugar onde aprendi que minha voz importa. Hoje ajudo outros jovens do bairro a acreditarem no mesmo.', name: 'Depoimento ilustrativo', role: 'Exemplo de fala de adolescente atendido' },
      { quote: 'Meu filho encontrou na música um motivo para acordar cedo todos os dias. A mudança em casa foi enorme.', name: 'Depoimento ilustrativo', role: 'Exemplo de fala de mãe de participante' },
      { quote: 'Como voluntária, recebo muito mais do que ofereço. É impossível sair do SECRI sem o coração mais leve.', name: 'Depoimento ilustrativo', role: 'Exemplo de fala de voluntária' },
    ];

    var nameEl = document.getElementById('nameText');
    var roleEl = document.getElementById('roleText');
    var dotsEl = document.getElementById('dots');
    var active = 0;

    var render = function () {
      var t = testimonials[active];
      quoteEl.textContent = '"' + t.quote + '"';
      nameEl.textContent = t.name;
      roleEl.textContent = t.role;
      dotsEl.innerHTML = '';

      testimonials.forEach(function (item, idx) {
        var d = document.createElement('button');
        d.type = 'button';
        d.className = 'h-2 rounded-full transition-all ' +
          (idx === active ? 'w-6 bg-rose-500' : 'w-2 bg-ink-300 hover:bg-ink-400');
        d.setAttribute('aria-label', 'Ver depoimento ' + (idx + 1));
        d.setAttribute('aria-current', idx === active ? 'true' : 'false');
        d.addEventListener('click', function () { active = idx; render(); });
        dotsEl.appendChild(d);
      });
    };

    document.getElementById('prevBtn').addEventListener('click', function () {
      active = (active - 1 + testimonials.length) % testimonials.length;
      render();
    });

    document.getElementById('nextBtn').addEventListener('click', function () {
      active = (active + 1) % testimonials.length;
      render();
    });

    setInterval(function () {
      active = (active + 1) % testimonials.length;
      render();
    }, 7000);

    render();
  }

  // --- Formulários (confirmação local, sem backend) --------------------
  [['volForm', 'volConfirm']].forEach(function (pair) {
    var form = document.getElementById(pair[0]);
    var confirm = document.getElementById(pair[1]);
    if (!form || !confirm) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      form.classList.add('hidden');
      confirm.classList.remove('hidden');
      confirm.focus();
    });
  });

  // --- WhatsApp: links e formulário de contato ------------------------
  // Celular abre o app pelo api.whatsapp.com; PC vai para o WhatsApp Web.
  // Basta um sinal de celular: userAgentData não existe em Safari/Firefox e
  // pode divergir do user agent quando este é alterado.
  var ehCelular = function () {
    if (navigator.userAgentData && navigator.userAgentData.mobile === true) {
      return true;
    }
    var ua = navigator.userAgent || '';
    if (/Android|iPhone|iPad|iPod|Mobile|Windows Phone|webOS|BlackBerry|Opera Mini|IEMobile/i.test(ua)) {
      return true;
    }
    // iPadOS se apresenta como Mac; a tela sensível ao toque denuncia.
    return navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1;
  };

  var urlWhatsApp = function (telefone, texto) {
    var base = ehCelular()
      ? 'https://api.whatsapp.com/send/'
      : 'https://web.whatsapp.com/send/';
    return base + '?phone=' + telefone + (texto ? '&text=' + encodeURIComponent(texto) : '');
  };

  // Links <a data-whatsapp="55..."> recebem a URL do dispositivo. Sem JS, o
  // href do HTML (api.whatsapp.com) continua funcionando nos dois.
  document.querySelectorAll('a[data-whatsapp]').forEach(function (link) {
    link.href = urlWhatsApp(link.getAttribute('data-whatsapp'));
  });

  // Formulário de contato: sem backend, a mensagem é montada aqui e aberta no
  // WhatsApp do SECRI, onde o visitante confirma o envio. O número vem do
  // data-whatsapp do <form>.
  var contactForm = document.getElementById('contactForm');

  if (contactForm) {
    var contactConfirm = document.getElementById('contactConfirm');
    var contactLink = document.getElementById('contactWhatsLink');
    var telefone = contactForm.getAttribute('data-whatsapp');

    var campo = function (nome) {
      return (contactForm.elements[nome].value || '').trim();
    };

    // Formatação do WhatsApp: *negrito*, _itálico_.
    var montaMensagem = function () {
      return [
        '*Contato pelo site do SECRI*',
        '',
        '*Nome:* ' + campo('nome'),
        '*E-mail:* ' + campo('email'),
        '*Assunto:* ' + campo('assunto'),
        '',
        '*Mensagem:*',
        campo('mensagem'),
        '',
        '_Enviado pelo formulário de secri.org.br/contato_',
      ].join('\n');
    };

    // O navegador valida os campos obrigatórios antes de disparar o submit.
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var url = urlWhatsApp(telefone, montaMensagem());
      window.open(url, '_blank', 'noopener');
      if (contactLink) contactLink.href = url;
      if (contactConfirm) {
        contactConfirm.classList.remove('hidden');
        contactConfirm.focus();
      }
    });
  }

  // --- Botões "Copiar" (chave Pix) -------------------------------------
  // navigator.clipboard pode faltar fora de contexto seguro; nesse caso o
  // texto fica selecionado para o visitante copiar com Ctrl+C.
  document.querySelectorAll('[data-copiar]').forEach(function (botao) {
    var alvo = document.getElementById(botao.getAttribute('data-copiar'));
    if (!alvo) return;
    var rotulo = botao.textContent;

    var avisa = function (texto) {
      botao.textContent = texto;
      setTimeout(function () { botao.textContent = rotulo; }, 2000);
    };

    botao.addEventListener('click', function () {
      var texto = alvo.textContent.trim();
      var seleciona = function () {
        var faixa = document.createRange();
        faixa.selectNodeContents(alvo);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(faixa);
        avisa('Selecionado');
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(texto).then(function () { avisa('Copiado!'); }, seleciona);
      } else {
        seleciona();
      }
    });
  });
})();
