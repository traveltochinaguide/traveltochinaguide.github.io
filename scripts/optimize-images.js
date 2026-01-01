const fs = require('fs-extra');
const path = require('path');
const sharp = require('sharp');

const imagesDir = path.resolve(__dirname, '../images');

async function optimizeImages() {
    console.log('Starting image optimization (WebP conversion)...');

    if (!await fs.pathExists(imagesDir)) {
        console.error('Images directory not found!');
        return;
    }

    const files = await fs.readdir(imagesDir);
    let count = 0;

    for (const file of files) {
        if (file.match(/\.(jpg|jpeg|png)$/i)) {
            const inputPath = path.join(imagesDir, file);
            const outputPath = path.join(imagesDir, file.replace(/\.(jpg|jpeg|png)$/i, '.webp'));

            // specific quality settings
            if (!await fs.pathExists(outputPath)) {
                try {
                    await sharp(inputPath)
                        .webp({ quality: 80 })
                        .toFile(outputPath);
                    console.log(`Converted: ${file} -> ${path.basename(outputPath)}`);
                    count++;
                } catch (err) {
                    console.error(`Error converting ${file}:`, err);
                }
            } else {
                // console.log(`Skipping ${file}, WebP already exists.`);
            }
        }
    }

    console.log(`Optimization complete. Converted ${count} images.`);
}

optimizeImages();
