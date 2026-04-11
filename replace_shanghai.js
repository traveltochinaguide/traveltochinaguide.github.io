const fs = require('fs');

function processFile(filename, isZh) {
    let content = fs.readFileSync(filename, 'utf8');

    // Make sure we get the correct contentHtml inside the <script> tags too,
    // so let's just do a RegExp replacement on the HTML body.

    // 1. Replace Attractions
    const attractionsRegexEn = /<h3 class="text-xl font-semibold mt-6 mb-2">Top attractions<\/h3>\s*<ul>[\s\S]*?<\/ul>/;
    const newAttractionsEn = `<h3 class="text-xl font-semibold mt-6 mb-2">Top attractions</h3>
            <ul>
              <li><strong>The Bund</strong> - Historic riverside promenade admiring colonial-era buildings, offering the best views of the iconic Pudong skyline across the Huangpu River.</li>
              <li><strong>Lujiazui Skyline</strong> - Experience the futuristic side of Shanghai by visiting the observation decks of the Shanghai Tower, Jin Mao Tower, or the Oriental Pearl TV Tower for spectacular panoramic views.</li>
              <li><strong>Yu Garden & City God Temple</strong> - A beautifully preserved classic Ming dynasty garden located in the bustling Old City area, perfect for experiencing traditional Chinese architecture and culture.</li>
              <li><strong>Shanghai Disney Resort</strong> - A world-class theme park featuring unique attractions and the enchanting Enchanted Storybook Castle, blending Disney magic with distinct Chinese elements.</li>
              <li><strong>Nanjing Road Pedestrian Street</strong> - One of the world's busiest shopping streets, filled with historic department stores, modern malls, and vibrant neon signs.</li>
              <li><strong>French Concession</strong> - A charming area with tree-lined streets, historic European-style villas, cozy cafés, and chic boutique shops.</li>
              <li><strong>Zhujiajiao Water Town</strong> - An ancient water town with centuries-old stone bridges, traditional courtyards, and scenic boat rides, located in the suburbs of Shanghai.</li>
            </ul>

            <h3 class="text-xl font-semibold mt-6 mb-2">Local Food & Specialties</h3>
            <ul>
              <li><strong>Xiaolongbao (Soup Dumplings)</strong> - Famous Shanghai steamed buns filled with hot, savory broth.</li>
              <li><strong>Shengjianbao</strong> - Pan-fried pork buns with a crispy bottom and a soft, airy top.</li>
              <li><strong>Hong Shao Rou</strong> - Classic red braised pork belly, sweet and savory.</li>
            </ul>`;

    const attractionsRegexZh = /<h3 class="text-xl font-semibold mt-6 mb-2">主要景点<\/h3>\s*<ul>[\s\S]*?<\/ul>/;
    const newAttractionsZh = `<h3 class="text-xl font-semibold mt-6 mb-2">主要景点</h3>
            <ul>
              <li><strong>外滩</strong> - 著名的黄浦江畔步道，汇聚万国建筑博览群，也是欣赏对岸浦东陆家嘴天际线的最佳位置。</li>
              <li><strong>陆家嘴天际线</strong> - 体验上海现代化的一面，可登上海中心大厦、金茂大厦或东方明珠广播电视塔，俯瞰绝美城市全景。</li>
              <li><strong>豫园与城隍庙</strong> - 位于老城厢的经典明代江南古典园林，体验传统建筑与民俗文化的绝佳去处。</li>
              <li><strong>上海迪士尼度假区</strong> - 世界级的主题乐园，拥有独特的游乐设施与奇幻童话城堡，融合了迪士尼魔法与中国元素。</li>
              <li><strong>南京路步行街</strong> - 世界上最繁忙的商业街之一，云集了历史悠久的百货公司、现代购物中心以及璀璨的霓虹灯牌。</li>
              <li><strong>法租界</strong> - 充满梧桐树的迷人街区，保留了大量欧式老洋房，遍布精致的咖啡馆与独立小店。</li>
              <li><strong>朱家角水乡</strong> - 位于上海郊区的一座历史悠久的江南水乡，拥有古老的石桥、传统院落及惬意的游船体验。</li>
            </ul>

            <h3 class="text-xl font-semibold mt-6 mb-2">特色美食</h3>
            <ul>
              <li><strong>小笼包</strong> - 上海经典面点，皮薄汁多，味道鲜美。</li>
              <li><strong>生煎包</strong> - 底部金黄酥脆、上半部松软的面点，内含鲜肉与汤汁。</li>
              <li><strong>红烧肉</strong> - 浓油赤酱的本帮菜代表，肥而不腻。</li>
            </ul>`;

    if (isZh) {
        content = content.replace(attractionsRegexZh, newAttractionsZh);
        // Also fix the contentHtml in the injected script so it doesn't get overridden
        const scriptMatch = content.match(/("contentHtml":")([\s\S]*?)("})/);
        if (scriptMatch) {
            let replacedHtml = scriptMatch[2]
                .replace(/<h3 class=\\"text-xl font-semibold mt-6 mb-2\\">主要景点<\/h3>\\n\s*<ul>[\\n\s\S]*?<\/ul>/g, newAttractionsZh.replace(/\n/g, '\\n').replace(/"/g, '\\"'));
            content = content.replace(scriptMatch[0], scriptMatch[1] + replacedHtml + scriptMatch[3]);
        }
    } else {
        content = content.replace(attractionsRegexEn, newAttractionsEn);
        const scriptMatch = content.match(/("contentHtml":")([\s\S]*?)("})/);
        if (scriptMatch) {
            let replacedHtml = scriptMatch[2]
                .replace(/<h3 class=\\"text-xl font-semibold mt-6 mb-2\\">Top attractions<\/h3>\\n\s*<ul>[\\n\s\S]*?<\/ul>/g, newAttractionsEn.replace(/\n/g, '\\n').replace(/"/g, '\\"'));
            content = content.replace(scriptMatch[0], scriptMatch[1] + replacedHtml + scriptMatch[3]);
        }
    }

    fs.writeFileSync(filename, content, 'utf8');
    console.log(`Updated ${filename}`);
}

processFile('shanghai.html', false);
processFile('zh-CN/shanghai.html', true);
