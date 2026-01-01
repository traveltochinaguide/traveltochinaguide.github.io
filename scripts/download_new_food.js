const fs = require('fs');
const path = require('path');
const https = require('https');

// Simple focused script to download specific new food images
const imagesToDownload = [
    {
        filename: 'hero-peking-duck.jpg',
        url: 'https://images.unsplash.com/photo-1563245372-f21724e3856d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80', // Peking Duck looking roast duck
        alt: 'Peking Duck'
    },
    {
        filename: 'hero-dim-sum.jpg',
        url: 'https://images.unsplash.com/photo-1496116218417-1a781b1c423c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80', // Dim Sum baskets
        alt: 'Dim Sum'
    },
    {
        filename: 'hero-hotpot.jpg',
        url: 'https://images.unsplash.com/photo-1549488344-c7079f856420?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80', // Hotpot
        alt: 'Hotpot'
    },
    {
        filename: 'hero-dumplings.jpg',
        url: 'https://images.unsplash.com/photo-1541696490865-e6f720e99198?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80', // Dumplings
        alt: 'Dumplings'
    }
];

const downloadImage = (url, filepath) => {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(filepath);
        https.get(url, (response) => {
            if (response.statusCode !== 200) {
                reject(new Error(`Failed to download ${url}: Status Code ${response.statusCode}`));
                return;
            }
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                resolve();
            });
        }).on('error', (err) => {
            fs.unlink(filepath, () => { });
            reject(err);
        });
    });
};

(async () => {
    const imagesDir = path.join(__dirname, '..', 'images');
    if (!fs.existsSync(imagesDir)) {
        fs.mkdirSync(imagesDir);
    }

    console.log('Downloading food images...');

    for (const img of imagesToDownload) {
        const filepath = path.join(imagesDir, img.filename);
        if (fs.existsSync(filepath)) {
            console.log(`${img.filename} already exists. Skipping.`);
            continue;
        }

        try {
            console.log(`Downloading ${img.filename}...`);
            await downloadImage(img.url, filepath);
            console.log(`Saved ${img.filename}`);
        } catch (error) {
            console.error(`Error downloading ${img.filename}:`, error.message);
        }
    }
    console.log('Done.');
})();
