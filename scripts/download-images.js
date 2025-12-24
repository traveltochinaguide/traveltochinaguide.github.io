const fs = require('fs');
const https = require('https');
const path = require('path');

const images = [
    // Heroes / Cities
    { name: 'hero-great-wall.jpg', url: 'https://images.unsplash.com/photo-1608037521277-154cd1b89191?w=1600' },
    { name: 'hero-shanghai.jpg', url: 'https://images.unsplash.com/photo-1727478431214-67846b1d62be?w=1600' },
    { name: 'hero-xian.jpg', url: 'https://images.unsplash.com/photo-1527922891260-918d42a4efc8?w=1600' },
    { name: 'hero-guilin.jpg', url: 'https://images.unsplash.com/photo-1625820006696-dd7f545b36a5?w=1600' },
    { name: 'hero-zhangjiajie.jpg', url: 'https://images.unsplash.com/photo-1567266565446-d9c40ccf59a4?w=1600' },
    { name: 'hero-jiuzhaigou.jpg', url: 'https://images.unsplash.com/photo-1694565176775-ec282698b5e9?w=1600' },
    { name: 'hero-yangtze.jpg', url: 'https://images.unsplash.com/photo-1491552222800-c124480c9b02?w=1600' },
    { name: 'hero-iching.jpg', url: 'https://images.unsplash.com/photo-1524499982521-1ffd58dd89ea?w=1200' },

    // Attractions (Beijing)
    { name: 'attr-798-art.jpg', url: 'https://images.unsplash.com/photo-1547891654-e66ed7ebb968?w=1600' },
    { name: 'attr-great-wall-detail.jpg', url: 'https://images.unsplash.com/photo-1583405584623-58f4b7d1380f?w=1600' },

    // Food (Using source.unsplash.com which redirects)
    { name: 'food-peking-duck.jpg', url: 'https://source.unsplash.com/600x600/?peking+duck' },
    { name: 'food-dim-sum.jpg', url: 'https://source.unsplash.com/600x600/?dim+sum' },
    { name: 'food-hotpot.jpg', url: 'https://source.unsplash.com/600x600/?sichuan+hotpot' },
    { name: 'food-dumplings.jpg', url: 'https://source.unsplash.com/600x600/?chinese+dumplings' }
];

const downloadImage = (url, filepath) => {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(filepath);
        https.get(url, (response) => {
            if (response.statusCode === 302 || response.statusCode === 301) {
                downloadImage(response.headers.location, filepath).then(resolve).catch(reject);
                return;
            }
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                console.log(`Downloaded ${filepath}`);
                resolve();
            });
        }).on('error', (err) => {
            fs.unlink(filepath, () => { });
            console.error(`Error downloading ${url}: ${err.message}`);
            reject(err);
        });
    });
};

const downloadAll = async () => {
    for (const img of images) {
        try {
            await downloadImage(img.url, path.join(__dirname, '..', 'images', img.name));
        } catch (e) {
            console.error(`Failed to download ${img.name}`);
        }
    }
};

downloadAll();
