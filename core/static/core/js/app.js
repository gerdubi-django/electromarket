const removeFlashMessages = () => {
  document.querySelectorAll('.alert').forEach((element) => {
    setTimeout(() => element.remove(), 4000);
  });
};

const initializeLanguageSelector = () => {
  const selector = document.querySelector('[data-language-selector]');

  if (!selector) {
    return;
  }

  selector.addEventListener('change', ({ target }) => {
    const nextUrl = target.value;

    if (nextUrl) {
      window.location.assign(nextUrl);
    }
  });
};

const initializeApp = () => {
  removeFlashMessages();
  initializeLanguageSelector();
};

initializeApp();
