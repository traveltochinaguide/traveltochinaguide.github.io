// 轮播图
const images = document.querySelectorAll('.carousel img');
let current = 0;
setInterval(() => {
    images[current].classList.remove('active');
    current = (current + 1) % images.length;
    images[current].classList.add('active');
}, 3000);

// 支持的语言列表
const langList = ['en','fr','de','es','it','zh','ja','ko','th'];

// 语言别名映射
const langAlias = {
    'en': 'en', 'en-US': 'en', 'en-GB': 'en',
    'fr': 'fr', 'fr-FR': 'fr', 'fr-CA': 'fr',
    'de': 'de', 'de-DE': 'de',
    'es': 'es', 'es-ES': 'es', 'es-MX': 'es',
    'it': 'it', 'it-IT': 'it',
    'zh': 'zh', 'zh-CN': 'zh', 'zh-TW': 'zh',
    'ja': 'ja', 'ja-JP': 'ja',
    'ko': 'ko', 'ko-KR': 'ko',
    'th': 'th', 'th-TH': 'th'
};

// 检测浏览器语言
function detectLang() {
    let langs = [];
    if (navigator.languages) {
        langs = navigator.languages;
    } else if (navigator.language) {
        langs = [navigator.language];
    }
    for (let l of langs) {
        l = l.split('-')[0] + (l.indexOf('-') > -1 ? '-' + l.split('-')[1].toUpperCase() : '');
        if (langAlias[l]) return langAlias[l];
        if (langList.includes(l)) return l;
    }
    return 'en'; // 默认英文
}

function setLang(lang) {
    document.getElementById('title').innerText = langData[lang].title;
    document.getElementById('subtitle').innerText = langData[lang].subtitle;
    document.getElementById('nav-scenic').innerText = langData[lang].nav[0];
    document.getElementById('nav-food').innerText = langData[lang].nav[1];
    document.getElementById('nav-info').innerText = langData[lang].nav[2];
    document.getElementById('scenic').innerText = langData[lang].scenic;
    document.getElementById('scenic1-title').innerText = langData[lang].scenic1[0];
    document.getElementById('scenic1-desc').innerText = langData[lang].scenic1[1];
    document.getElementById('scenic2-title').innerText = langData[lang].scenic2[0];
    document.getElementById('scenic2-desc').innerText = langData[lang].scenic2[1];
    document.getElementById('scenic3-title').innerText = langData[lang].scenic3[0];
    document.getElementById('scenic3-desc').innerText = langData[lang].scenic3[1];
    document.getElementById('scenic4-title').innerText = langData[lang].scenic4[0];
    document.getElementById('scenic4-desc').innerText = langData[lang].scenic4[1];
    document.getElementById('food').innerText = langData[lang].food;
    document.getElementById('food1-title').innerText = langData[lang].food1[0];
    document.getElementById('food1-desc').innerText = langData[lang].food1[1];
    document.getElementById('food2-title').innerText = langData[lang].food2[0];
    document.getElementById('food2-desc').innerText = langData[lang].food2[1];
    document.getElementById('food3-title').innerText = langData[lang].food3[0];
    document.getElementById('food3-desc').innerText = langData[lang].food3[1];
    document.getElementById('food4-title').innerText = langData[lang].food4[0];
    document.getElementById('food4-desc').innerText = langData[lang].food4[1];
    document.getElementById('info').innerText = langData[lang].info;
    document.getElementById('info1').innerHTML = langData[lang].info1;
    document.getElementById('info2').innerHTML = langData[lang].info2;
    document.getElementById('info3').innerHTML = langData[lang].info3;
    document.getElementById('info4').innerHTML = langData[lang].info4;
    document.getElementById('info5').innerHTML = langData[lang].info5;
    document.getElementById('footer').innerHTML = langData[lang].footer;
    // Highlight active button
    langList.forEach(l => {
        const btn = document.getElementById('btn-' + l);
        if (btn) btn.classList.toggle('active', lang === l);
    });
    // Set html lang attribute
    document.documentElement.lang = lang;
}

// 绑定所有按钮
langList.forEach(l => {
    const btn = document.getElementById('btn-' + l);
    if (btn) btn.onclick = () => setLang(l);
});

// 自动检测并设置语言
setLang(detectLang());
