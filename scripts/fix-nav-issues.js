/**
 * Fix nav issues across all pages (root + lang dirs):
 * 1. Remove duplicate zhangjiajie entries in nav (all 8 langs × 48 pages = 376 pages)
 * 2. Add missing language-switcher div to silk.html
 * 3. Verify all root pages have language-switcher div
 */
const fs = require('fs-extra');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const langs = ['en', 'zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es'];

(async () => {
  let fixed = 0;
  let errors = [];

  // --- STEP 1: Fix duplicate zhangjiajie in all lang dir pages ---
  const pages = (await fs.readdir(rootDir)).filter(f => f.endsWith('.html') && f !== 'googlef501e2ee1025d72e.html');
  
  console.log(`=== Step 1: Fix duplicate zhangjiajie in ${langs.length} langs × ${pages.length} pages ===`);
  
  for (const lang of langs) {
    const langDir = path.join(rootDir, lang);
    if (!await fs.pathExists(langDir)) continue;
    
    for (const pageName of pages) {
      const filePath = path.join(langDir, pageName);
      if (!await fs.pathExists(filePath)) continue;
      
      let content = await fs.readFile(filePath, 'utf-8');
      
      // Find the nav section
      const navStart = content.indexOf('<nav');
      const navEnd = content.indexOf('</nav>');
      if (navStart === -1 || navEnd === -1) continue;
      
      const beforeNav = content.slice(0, navStart);
      const navContent = content.slice(navStart, navEnd + 6); // include </nav>
      const afterNav = content.slice(navEnd + 6);
      
      // In the nav, find and remove the SECOND zhangjiajie entry (keep first)
      let firstZj = true;
      const fixedNav = navContent.replace(
        /<a[^>]*href="[^"]*zhangjiajie[^"]*"[^>]*>[\s\S]*?<\/a>/g,
        (match) => {
          if (firstZj) {
            firstZj = false;
            return match; // keep first
          }
          // Remove the duplicate + its surrounding list item / div
          return '';
        }
      );
      
      // Clean up empty <div> or <li> left by removal
      const cleanedNav = fixedNav.replace(/<div[^>]*>\s*<\/div>/g, '').replace(/\n\s*\n/g, '\n');
      
      if (navContent !== cleanedNav) {
        const newContent = beforeNav + cleanedNav + afterNav;
        await fs.writeFile(filePath, newContent, 'utf-8');
        fixed++;
      }
    }
  }
  console.log(`  Fixed ${fixed} lang-dir pages`);

  // --- STEP 2: Fix silk.html root page ---
  console.log('\n=== Step 2: Fix silk.html root page ===');
  const silkPath = path.join(rootDir, 'silk.html');
  if (await fs.pathExists(silkPath)) {
    let silk = await fs.readFile(silkPath, 'utf-8');
    
    if (!silk.includes('id="language-switcher"')) {
      // Find the nav closing, add language-switcher div before nav closes
      const navEnd = silk.indexOf('</nav>');
      if (navEnd !== -1) {
        // Find the last div before </nav> (usually the flex container)
        const lastDivEnd = silk.lastIndexOf('</div>', navEnd);
        if (lastDivEnd !== -1 && lastDivEnd < navEnd) {
          silk = silk.slice(0, lastDivEnd) + 
            '\n <div class="flex items-center md:ml-2 mt-2 md:mt-0">\n' +
            ' <div id="language-switcher" class="flex flex-wrap justify-end bg-blue-50 p-1 rounded-full" aria-label="Language selector"></div>\n' +
            ' </div>\n' +
            silk.slice(lastDivEnd);
          await fs.writeFile(silkPath, silk, 'utf-8');
          console.log('  Added language-switcher div to silk.html');
          errors.push('Added language-switcher to silk.html - regenerate lang dirs needed');
        } else {
          const msg = 'silk.html: could not locate insertion point for language-switcher';
          console.error(`  ERROR: ${msg}`);
          errors.push(msg);
        }
      }
    } else {
      console.log('  silk.html already has language-switcher');
    }
  }

  // --- STEP 3: Verify all root pages have language-switcher ---
  console.log('\n=== Step 3: Verify root pages ===');
  let missingSwitcher = [];
  for (const pageName of pages) {
    const filePath = path.join(rootDir, pageName);
    let content = await fs.readFile(filePath, 'utf-8');
    if (!content.includes('id="language-switcher"')) {
      missingSwitcher.push(pageName);
    }
  }
  if (missingSwitcher.length > 0) {
    console.log(`  Pages WITHOUT language-switcher: ${missingSwitcher.join(', ')}`);
    errors.push(`Missing language-switcher: ${missingSwitcher.join(', ')}`);
  } else {
    console.log('  All root pages have language-switcher ✅');
  }

  console.log(`\n=== Summary ===`);
  console.log(`  Lang-dir pages fixed: ${fixed}`);
  console.log(`  Errors: ${errors.length ? errors.join('; ') : 'none'}`);
  
  // Write status file for cron to track
  await fs.writeFile(path.join(rootDir, '.nav-fix-status.json'), JSON.stringify({
    fixed,
    errors,
    timestamp: new Date().toISOString()
  }, null, 2));
  
  if (errors.length > 0) {
    console.log(`\n  ⚠️  ${errors.length} issue(s) need attention`);
    process.exit(1);
  }
})();