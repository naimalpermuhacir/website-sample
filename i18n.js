(function() {
    const translations = window.SITE_TRANSLATIONS || {};
    let currentLang = localStorage.getItem('site_lang') || 'tr'; // Default to TR

    function walkDOM(node) {
        if (node.nodeType === 3) { 
            let originalText = node.originalValue;
            if (originalText === undefined) {
                originalText = node.nodeValue;
                node.originalValue = originalText;
            }
            let trimmedText = originalText.trim();
            if (trimmedText && translations[trimmedText] && translations[trimmedText][currentLang]) {
                node.nodeValue = originalText.replace(trimmedText, translations[trimmedText][currentLang]);
            } else if (trimmedText && translations[trimmedText]) {
                 // Fallback if we switch back
                 node.nodeValue = originalText.replace(translations[trimmedText][currentLang === 'tr' ? 'en' : 'tr'], translations[trimmedText][currentLang]);
            }
        } else if (node.nodeType === 1 && node.nodeName !== 'SCRIPT' && node.nodeName !== 'STYLE') {
            if (node.placeholder) {
                 if (node.originalPlaceholder === undefined) node.originalPlaceholder = node.placeholder.trim();
                 if (translations[node.originalPlaceholder] && translations[node.originalPlaceholder][currentLang]) {
                     node.placeholder = translations[node.originalPlaceholder][currentLang];
                 }
            }
            // Skip elements that GSAP has already split if we run late (just in case)
            if (!node.classList.contains('split-text') || true) {
                 node.childNodes.forEach(walkDOM);
            }
        }
    }

    // Special handler for the 'Contact us' button animated chars
    function translateAnimatedButton(lang) {
        const btnTextContainer = document.querySelector('.special-btn .button__text');
        if (btnTextContainer) {
            const word = lang === 'en' ? "Contact-us!" : "Bize-ulaşın!";
            btnTextContainer.innerHTML = '';
            for (let i = 0; i < word.length; i++) {
                const char = word[i];
                btnTextContainer.innerHTML += `<span style="--index: ${i};">${char}</span>`;
            }
        }
    }

    function applyLanguage(lang) {
        lang = lang || currentLang;
        currentLang = lang;
        localStorage.setItem('site_lang', lang);
        
        walkDOM(document.body);
        translateAnimatedButton(lang);
        
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.lang === lang);
            btn.style.opacity = btn.dataset.lang === lang ? '1' : '0.5';
        });
    }

    // Export to window for dynamic AJAX modals
    window.applyLanguage = applyLanguage;
    window.walkDOM = walkDOM;

    // Run string replacement completely synchronously right now 
    // before GSAP or custom.min.js initialize
    walkDOM(document.body);

    document.addEventListener('DOMContentLoaded', () => {
        // Inject language switcher UI to top right (navbar)
        const rightNav = document.querySelector('.navbar-utilities ul');
        if (rightNav && !document.querySelector('.lang-switcher')) {
            const langHtml = `
                <li class="desktop-only header-lang-wrapper me-3 me-lg-4" style="display: flex; align-items: center;">
                    <div class="lang-switcher" style="display: flex; gap: 8px; background: rgba(255,255,255,0.1); padding: 5px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); backdrop-filter: blur(10px); pointer-events: auto;">
                        <button class="lang-btn ${currentLang === 'tr' ? 'active' : ''}" data-lang="tr" style="background:none; border:none; color:white; font-size: 14px; font-weight: bold; cursor: pointer; opacity: ${currentLang === 'tr' ? '1' : '0.5'}; transition: 0.3s;">TR</button>
                        <span style="color: rgba(255,255,255,0.3);">|</span>
                        <button class="lang-btn ${currentLang === 'en' ? 'active' : ''}" data-lang="en" style="background:none; border:none; color:white; font-size: 14px; font-weight: bold; cursor: pointer; opacity: ${currentLang === 'en' ? '1' : '0.5'}; transition: 0.3s;">EN</button>
                    </div>
                </li>
            `;
            rightNav.insertAdjacentHTML('afterbegin', langHtml);
            
            document.querySelectorAll('.lang-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    // Because DOM is already split by GSAP after load, a full generic walkDOM might break things.
                    // The safest way is to force a page reload with the new language to get clean HTML!
                    localStorage.setItem('site_lang', e.target.dataset.lang);
                    window.location.reload();
                });
            });
        }
        
        if (currentLang !== 'ro') {
            translateAnimatedButton(currentLang);
        }
    });

})();
