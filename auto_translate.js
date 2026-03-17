const fs = require('fs');
const https = require('https');

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

function translate(text, targetLang) {
    return new Promise((resolve) => {
        const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=ro&tl=${targetLang}&dt=t&q=${encodeURIComponent(text)}`;
        const options = {
            timeout: 5000,
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        };

        const req = https.get(url, options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const parsed = JSON.parse(data);
                    let translatedText = '';
                    if (parsed[0] && Array.isArray(parsed[0])) {
                        parsed[0].forEach(p => { if (p[0]) translatedText += p[0]; });
                    }
                    resolve({ text, lang: targetLang, trans: translatedText || text });
                } catch (e) {
                    resolve({ text, lang: targetLang, trans: text });
                }
            });
        }).on('error', () => resolve({ text, lang: targetLang, trans: text }))
          .on('timeout', () => { req.destroy(); resolve({ text, lang: targetLang, trans: text }); });
    });
}

async function processChunk(chunkTexts) {
    const promises = [];
    chunkTexts.forEach(t => {
        promises.push(translate(t, 'en'));
        promises.push(translate(t, 'tr'));
    });
    const results = await Promise.all(promises);
    
    // Group back by text
    const map = {};
    chunkTexts.forEach(t => map[t] = { en: t, tr: t });
    results.forEach(r => { map[r.text][r.lang] = r.trans; });
    return map;
}

async function main() {
    const texts = JSON.parse(fs.readFileSync('inner_texts.json', 'utf8'));
    console.log(`Starting CONCURRENT translation of ${texts.length} phrases...`);
    
    let existingContent = fs.readFileSync('translations.js', 'utf8');
    // We already have some appended from the last run!
    // But since keys just overwrite if duplicates, we can just append or regenerate
    // Actually, we should filter existing keys
    let currentMap = {};
    const lines = existingContent.split('\\n');
    lines.forEach(l => {
        if(l.includes('": {')) {
            const k = l.split('": {')[0].trim().replace(/^"|"$/g, '');
            currentMap[k] = true;
        }
    });
    
    const unmappedTexts = texts.filter(t => !currentMap[t.replace(/"/g, '\\\\"')]);
    console.log(`Remaining un-translated phrases: ${unmappedTexts.length}`);
    
    existingContent = existingContent.replace(/};\s*$/g, ',');
    
    const CHUNK_SIZE = 15;
    let appendedObj = '';

    for (let i = 0; i < unmappedTexts.length; i += CHUNK_SIZE) {
        const chunk = unmappedTexts.slice(i, i + CHUNK_SIZE);
        const map = await processChunk(chunk);
        
        chunk.forEach((text, idx) => {
            const en = map[text].en;
            const tr = map[text].tr;
            
            const key = text.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n');
            const enVal = en.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n');
            const trVal = tr.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n');
            
            appendedObj += `\n  "${key}": { "en": "${enVal}", "tr": "${trVal}" },`;
        });
        
        console.log(`Progress: ${Math.min(i + CHUNK_SIZE, unmappedTexts.length)}/${unmappedTexts.length}`);
        
        // Save incrementally
        fs.writeFileSync('translations.js', existingContent + appendedObj.replace(/,$/, '') + '\n};\n');
        existingContent = fs.readFileSync('translations.js', 'utf8').replace(/};\s*$/g, ',');
        appendedObj = '';
        
        await delay(500); // 500ms between chunks of 30 requests
    }
    
    console.log("Translations completed!");
}

main();
