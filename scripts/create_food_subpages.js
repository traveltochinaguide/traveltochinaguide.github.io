const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const templatePath = path.join(__dirname, '..', 'food.html');
const templateHtml = fs.readFileSync(templatePath, 'utf8');

const dishes = [
    {
        filename: 'peking-duck.html',
        titleKey: 'titlePekingDuck',
        subtitleKey: 'subtitlePekingDuck',
        contentKey: 'contentPekingDuck',
        heroImage: 'images/hero-peking-duck.jpg'
    },
    {
        filename: 'dim-sum.html',
        titleKey: 'titleDimSum',
        subtitleKey: 'subtitleDimSum',
        contentKey: 'contentDimSum',
        heroImage: 'images/hero-dim-sum.jpg'
    },
    {
        filename: 'hotpot.html',
        titleKey: 'titleHotpot',
        subtitleKey: 'subtitleHotpot',
        contentKey: 'contentHotpot',
        heroImage: 'images/hero-hotpot.jpg'
    },
    {
        filename: 'dumplings.html',
        titleKey: 'titleDumplings',
        subtitleKey: 'subtitleDumplings',
        contentKey: 'contentDumplings',
        heroImage: 'images/hero-dumplings.jpg'
    }
];

dishes.forEach(dish => {
    const $ = cheerio.load(templateHtml);

    // update Title
    $('title').attr('data-lang-key', dish.titleKey);
    // update Meta
    $('meta[property="og:title"]').attr('data-lang-key', dish.titleKey);
    $('meta[property="twitter:title"]').attr('data-lang-key', dish.titleKey);
    $('meta[property="og:image"]').attr('content', dish.heroImage); // Not localized usually, but image path
    $('meta[property="twitter:image"]').attr('content', dish.heroImage);

    // Update Hero
    $('.relative.h-\\[60vh\\] img').attr('src', dish.heroImage);
    $('.relative.h-\\[60vh\\] h1').attr('data-lang-key', dish.titleKey);
    $('.relative.h-\\[60vh\\] p').attr('data-lang-key', dish.subtitleKey);

    // Update Main Content
    // We will clear the existing "Intro", "Regional", "Popular Dishes" sections
    // And replace with a single content section

    const contentSection = `
        <section class="py-16 bg-white">
            <div class="container mx-auto px-6 max-w-4xl">
                <div class="prose prose-lg mx-auto text-gray-700" data-lang-key="${dish.contentKey}">
                    <!-- Content will be injected by language script -->
                    Loading content...
                </div>
                <div class="mt-12 text-center">
                    <a href="food.html" class="inline-block px-8 py-3 bg-blue-600 text-white font-bold rounded-full hover:bg-blue-700 transition-colors">
                        Back to Cuisine
                    </a>
                </div>
            </div>
        </section>
    `;

    // Remove existing sections inside <main>
    $('#main-content').empty();
    // Add Hero (re-created or preserved? We cleared main so we need to add back Hero + Content)

    // Wait, I cleared #main-content which contained the Hero too in food.html structure?
    // Let's check food.html structure.
    // Yes: <main id="main-content"> <section class="hero"> ... 

    // So I need to reconstruct or better yet, select specific sections to remove.
    // Reload to be safe
    const $2 = cheerio.load(templateHtml);

    // Update Hero in $2
    $2('.relative.h-\\[60vh\\] img').attr('src', '/' + dish.heroImage); // Ensure leading slash
    $2('.relative.h-\\[60vh\\] h1').attr('data-lang-key', dish.titleKey).text('Loading...');
    $2('.relative.h-\\[60vh\\] p').attr('data-lang-key', dish.subtitleKey).text('Loading...');

    // Remove sections AFTER hero
    // The Hero is the first section in main.
    // subsequent sections: Intro, Regional, Popular
    $2('#main-content > section:not(:first-child)').remove();

    // Append new content
    $2('#main-content').append(contentSection);

    // Update canonical
    $2('link[rel="canonical"]').attr('href', `https://www.travelchinaguide.dpdns.org/${dish.filename}`);

    // Update alternates
    $2('link[rel="alternate"]').each((i, el) => {
        const hreflang = $2(el).attr('hreflang');
        if (hreflang === 'x-default' || hreflang === 'en') {
            $2(el).attr('href', `https://www.travelchinaguide.dpdns.org/${dish.filename}`);
        } else {
            $2(el).attr('href', `https://www.travelchinaguide.dpdns.org/${hreflang}/${dish.filename}`);
        }
    });

    const outputPath = path.join(__dirname, '..', dish.filename);
    fs.writeFileSync(outputPath, $2.html(), 'utf8');
    console.log(`Created ${dish.filename}`);
});
