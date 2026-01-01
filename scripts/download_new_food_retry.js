const fs = require('fs');
const path = require('path');
const https = require('https');

const imagesToDownload = [
    {
        filename: 'hero-dim-sum.jpg',
        url: 'https://images.unsplash.com/photo-1595854341472-1c90df94918d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80', // Dim Sum try 2
    },
    {
        filename: 'hero-hotpot.jpg',
        url: 'https://plus.unsplash.com/premium_photo-1661610996884-6997b77ab4ce?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80', // Hotpot try 2
    },
    {
        filename: 'hero-dumplings.jpg',
        url: 'https://images.unsplash.com/photo-1563245372-f21724e3856d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80', // Dumplings try 2 (reusing duck img as placeholder if needed, but let's try a real dumpling one: 
    }
];

// Better dumpling url
imagesToDownload[2].url = 'https://images.unsplash.com/photo-1628203794829-d58671607593?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80';


const downloadImage = (url, filepath) => {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(filepath);
        https.get(url, (response) => {
            if (response.statusCode === 301 || response.statusCode === 302) {
                // Follow redirect
                downloadImage(response.headers.location, filepath).then(resolve).catch(reject);
                return;
            }
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

    console.log('Retrying food images...');

    for (const img of imagesToDownload) {
        const filepath = path.join(imagesDir, img.filename);
        if (fs.existsSync(filepath)) {
            // Check file size, if 0 delete it
            const stats = fs.statSync(filepath);
            if (stats.size > 0) {
                console.log(`${img.filename} already exists and seems valid. Skipping.`);
                continue;
            } else {
                console.log(`${img.filename} is empty. Retrying.`);
                fs.unlinkSync(filepath);
            }
        }

        try {
            console.log(`Downloading ${img.filename} from ${img.url}...`);
            await downloadImage(img.url, filepath);
            console.log(`Saved ${img.filename}`);
        } catch (error) {
            console.error(`Error downloading ${img.filename}:`, error.message);
        }
    }
    console.log('Retry Done.');
})();
