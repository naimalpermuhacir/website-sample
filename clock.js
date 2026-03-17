document.addEventListener('DOMContentLoaded', () => {
    const locSpan = document.getElementById('user-location');
    const timeSpan = document.getElementById('user-time');

    if (!locSpan || !timeSpan) return;

    // First try to get location from timezone, which is fast and reliable
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
    let city = tz ? tz.split('/').pop().replace('_', ' ') : '';
    let country = '';

    function updateTime() {
        const now = new Date();
        timeSpan.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    // Set immediate default based on Timezone processing
    if (city) {
        locSpan.textContent = city;
    }
    
    // Fetch exact location via free IP API
    fetch('https://ipapi.co/json/')
        .then(res => res.json())
        .then(data => {
            if (data.city && data.country_name) {
                // Determine translation mapping if the user wants it to match current site language
                let ctry = data.country_name;
                const lang = localStorage.getItem('site_lang') || 'tr';
                if (lang === 'tr' && ctry.toLowerCase() === 'turkey') {
                    ctry = 'Türkiye';
                }
                locSpan.textContent = `${data.city}, ${ctry}`;
            }
        })
        .catch(err => console.log('Location fetch failed, falling back to TimeZone.', err));

    setInterval(updateTime, 1000);
    updateTime();
});
