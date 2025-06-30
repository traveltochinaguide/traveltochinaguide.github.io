const LANGS = ['en', 'zh', 'ja', 'ko', 'ru', 'th', 'fr', 'de'];
let currentLang = 'en';

function detectLang() {
    const navLang = (navigator.language || navigator.userLanguage || 'en').toLowerCase();
    for (let lang of LANGS) {
        if (navLang.startsWith(lang)) {
            return lang;
        }
    }
    return 'en';
}
currentLang = detectLang();
