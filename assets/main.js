// 轮播图
const images = document.querySelectorAll('.carousel img');
let current = 0;
setInterval(() => {
    images[current].classList.remove('active');
    current = (current + 1) % images.length;
    images[current].classList.add('active');
}, 3000);

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
    ['en','fr','de','es','it','zh'].forEach(l => {
        document.getElementById('btn-' + l).classList.toggle('active', lang === l);
    });
    // Set html lang attribute
    document.documentElement.lang = lang;
}

document.getElementById('btn-en').onclick = () => setLang('en');
document.getElementById('btn-fr').onclick = () => setLang('fr');
document.getElementById('btn-de').onclick = () => setLang('de');
document.getElementById('btn-es').onclick = () => setLang('es');
document.getElementById('btn-it').onclick = () => setLang('it');
document.getElementById('btn-zh').onclick = () => setLang('zh');

// 默认英文
setLang('en');
