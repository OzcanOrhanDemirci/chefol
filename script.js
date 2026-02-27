/* ==========================================================================
   CHEFOL - PREMIUM JAVASCRIPT LOGIC
   Features: Theme Toggle, Language Toggle, Accordion, Scroll Reveal, Scroll to Top
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. Tema Yönetimi ---
    const themeToggleBtn = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;
    
    let savedTheme;
    try {
        savedTheme = localStorage.getItem('chefol_theme');
    } catch (e) { console.warn("Local storage disabled"); }
    
    const systemPrefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
    
    if (savedTheme) {
        htmlElement.setAttribute('data-theme', savedTheme);
    } else if (systemPrefersLight) {
        htmlElement.setAttribute('data-theme', 'light');
    } else {
        htmlElement.setAttribute('data-theme', 'dark');
    }

    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = htmlElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        htmlElement.setAttribute('data-theme', newTheme);
        try {
            localStorage.setItem('chefol_theme', newTheme);
        } catch (e) {}
    });

    // --- 2. Dil Yönetimi (Güvenli Yapı) ---
    const langToggleBtn = document.getElementById('langToggle');
    const langTrSpan = document.getElementById('lang-tr');
    const langEnSpan = document.getElementById('lang-en');
    
    let savedLang = 'tr';
    try {
        savedLang = localStorage.getItem('chefol_lang') || 'tr';
    } catch (e) {}
    
    setLanguage(savedLang, false);

    langToggleBtn.addEventListener('click', () => {
        const currentLang = htmlElement.getAttribute('lang');
        const newLang = currentLang === 'tr' ? 'en' : 'tr';
        setLanguage(newLang, true);
    });

    function setLanguage(lang, animate) {
        try {
            if (animate) {
                // Şeffaflığı CSS class ile güvenli şekilde tetikle
                document.body.classList.add('lang-animating');
                
                setTimeout(() => {
                    applyLanguage(lang);
                    
                    // Şeffaflığı yavaşça geri almak için ufak bir bekleme
                    setTimeout(() => {
                        document.body.classList.remove('lang-animating');
                    }, 50);
                }, 200); // 200ms bekle (şeffaflaşma süresi)
            } else {
                applyLanguage(lang);
            }
        } catch (e) {
            console.error("Dil geçiş animasyon hatası:", e);
            // Hata olursa animasyonsuz anında değiştir (bozulmayı önler)
            applyLanguage(lang);
            document.body.classList.remove('lang-animating');
        }
    }

    function applyLanguage(lang) {
        htmlElement.setAttribute('lang', lang);
        try {
            localStorage.setItem('chefol_lang', lang);
        } catch (e) {}

        if (lang === 'tr') {
            langTrSpan.classList.add('active');
            langEnSpan.classList.remove('active');
        } else {
            langEnSpan.classList.add('active');
            langTrSpan.classList.remove('active');
        }
    }

    // --- 3. Akordeon (Yasal Metinler) ---
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const isExpanded = header.getAttribute('aria-expanded') === 'true';
            header.setAttribute('aria-expanded', !isExpanded);
        });
    });

    // --- 4. Scroll Animasyonları ---
    const revealElements = document.querySelectorAll('.reveal');

    const revealOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const revealOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            
            entry.target.classList.add('active');
            observer.unobserve(entry.target);
        });
    }, revealOptions);

    revealElements.forEach(el => {
        revealOnScroll.observe(el);
    });
    
    setTimeout(() => {
        revealElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight) {
                el.classList.add('active');
            }
        });
    }, 100);

    // --- 5. Yukarı Kaydırma (Footer Logoya Tıklayınca) ---
    const footerLogo = document.querySelector('.footer-logo');
    if (footerLogo) {
        footerLogo.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

});