# Magic5 Clone (TR/EN)

Bu proje, orijinal [Magic5.ro](https://magic5.ro/) web sitesinin %100 birebir statik klonudur. Node.js ve Vite altyapısı kullanılarak yerel ortama taşınmış ve içerisindeki tüm Romence metinler yerel bir sözlük sistemi kurularak otomatik Türkçe ve İngilizce dillerine çevrilmiştir.

## Özellikler

*   **Birebir Klon:** `web-design`, `app-development`, `portofoliu`, `echipa`, `blog` gibi tüm alt sayfalar eksiksiz olarak kopyalanmıştır.
*   **Dinamik Çeviri (i18n):** Orijinal siteden kazınan 850'den fazla metin; Vite tabanlı, tamamen yerel ve asenkron çalışan bir dil sistemi (`i18n.js` ve `translations.js`) üzerinden Türkçe (varsayılan) ve İngilizce'ye anında çevrilir. Sayfa yenilemesine gerek kalmadan çalışır.
*   **Offline/Lokal Dinamik Proje Modalları:** Orijinal sitenin dış sunuculara attığı (AJAX) istekler (`/get-project-content`) yerel HTML snapshot'ları alınarak (`/project-modals` klasörüne) offline çalışabilir ve arayüz içi tercüme edilebilir hale getirilmiştir.
*   **Otomatik Varlık (Asset) Yönetimi:** Tüm görsel varlıklar (`uploads/`) projenin boyutunu ufak tutmak amacıyla canlı sunucudan (hotlink) çekilmektedir.

## Kullanılan Teknolojiler

*   **Frontend:** HTML, Vanilla CSS, Vanilla JavaScript
*   **Build Aracı:** [Vite](https://vitejs.dev/) (Hızlı geliştirme ve optimize edilmiş statik çıktılar için)
*   **Animasyonlar:** GSAP (ScrollTrigger, SplitText, ScrollSmoother)
*   **Kütüphaneler:** jQuery, Bootstrap 5, Slick Slider

## Bağımlılıklar (Dependencies)

Projeyi yerel ortamınızda geliştirebilmek için bilgisayarınızda kurulu olması gerekenler:
*   [Node.js](https://nodejs.org/en/) (v18.0.0 veya üzeri tavsiye edilir)
*   [npm](https://www.npmjs.com/) (veya yarn)

---

## Yerel Ortamda Çalıştırma (Development)

Projeyi bilgisayarınıza indirdikten sonra terminali klasör dizininde açın ve aşağıdaki adımları izleyin:

1.  **Bağımlılıkları Yükleyin:**
    ```bash
    npm install
    ```

2.  **Geliştirme Sunucusunu Başlatın (Vite):**
    ```bash
    npm run dev
    ```
    *(Bu komut lokalde bir sunucu başlatacak ve siteye `http://localhost:5173` adresinden ulaşabileceksiniz.)*

3.  **Siteyi Üretim İçin Derleyin (Production Build):**
    ```bash
    npm run build
    ```
    *(Bu komut kodları optimize eder ve `dist/` klasörü içerisine deploy edilebilir statik HTML, CSS ve JS dosyalarınızı çıkarır.)*

4.  **Derlenmiş Versiyonu Önizleyin:**
    ```bash
    npm run preview
    ```

---

## Docker ile Çalıştırma (Dockerize)

Proje, çok aşamalı (multi-stage) en hafif yapıda bir **Nginx Alpine** imajı kullanılarak Dockerize edilmiştir. Bilgisayarınıza Node.js bile kurmadan projeyi ayağa kaldırabilirsiniz.

### 1) İmajı Oluşturun (Build)
Proje kök dizinindeyken aşağıdaki komutu çalıştırarak Docker imajını derleyin (imaja `magic5-clone` ismini verdik):
```bash
docker build -t magic5-clone .
```

### 2) Konteyneri Çalıştırın (Run)
İmaj oluştuktan sonra, uygulamayı örneğin `8080` portunda yayınlamak için şu komutu kullanın:
```bash
docker run -d -p 8080:80 --name magic5-app magic5-clone
```

### 3) Siteyi Görüntüleyin
Tarayıcınızı açın ve [http://localhost:8080](http://localhost:8080) adresine gidin. Proje sorunsuz bir şekilde yüksek performanslı Nginx sunucusu üzerinden yayında olacaktır!

> Konteyneri durdurmak için: `docker stop magic5-app`
> Konteyneri kaldırmak için: `docker rm magic5-app`

## Proje Yapısı

*   `/*.html`: Tüm sayfa şablonları
*   `/project-modals/*.html`: Portföy AJAX modallarının indirildiği önbellek (cache) tasarımlar
*   `/js/custom.min.js`: Tüm animasyon (GSAP) ve bileşen tetikleyicilerini yöneten çekirdek
*   `/i18n.js`: Sayfayı eşzamanlı olarak tarayan (DOM-walking) ve çeviren sözlük motoru
*   `/translations.js`: 850'den fazla Türkçe/İngilizce çeviri kelimesini JSON formatında barındıran kütüphane dosyası