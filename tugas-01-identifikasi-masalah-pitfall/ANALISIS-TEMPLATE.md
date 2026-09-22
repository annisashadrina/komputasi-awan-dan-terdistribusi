# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Annisa Nur Shadrina] | [103072400134] | [Semua modul berebut resource yang sama] |
| [Fadia Nabila Shifa] | [103072400066] | [Latency is zero /Pembayaran lambat yang membuat modul pesanan menunggu] |
| [Aryo Abdillah Ainnurrofiq] | [103072400006] | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: Semua modul berebut resource yang sama (Monolithic Resource Contention / SPOF) — ditulis oleh Annisa N Shadrina

**Bukti di skenario:** Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.

**Kenapa ini keliru:** Dari kalimat tersebut, yang menarik menurut saya bukan cuma servernya "kewalahan", tetapi kenapa satu peningkatan traffic bisa membuat beberapa bagian sistem ikut terdampak, walaupun sebenarnya belum tentu semua modul sedang sibuk dengan tingkat yang sama.

Sebelum traffic meningkat, arsitektur sistem yang kami lihat seperti ini:
User -> Server FoodGo -> membawahi modul Order, Payment, dan Notification sekaligus.

Hal ini menyebabkan ketiga fungsi/modul berada dalam satu server dan satu proses monolitik yang sama, jadi FoodGo belum memisahkan resource (CPU, Memory, Thread Pool, DB Connection Pool) untuk masing-masing fungsi. Menganggap satu server monolitik bisa terus dipaksa menampung semua modul saat trafik melonjak adalah asumsi yang keliru. Di sistem terdistribusi, begitu satu modul kewalahan makan resource, seluruh server bakal terancam mati dan modul lain yang sebenarnya tidak terlalu sibuk ikut terseret tumbang.


**Dampak ke FoodGo:** 
Mekanisme kegagalannya terjadi secara berantai (cascading failure) seperti ini:
1. **Lonjakan Jam Makan Siang / Promo:** Ribuan pengguna melakukan checkout secara bersamaan. Modul pesanan mendadak memakan resource CPU tinggi dan membuka banyak koneksi ke database.
2. **Resource Monolitik Ludes:** Karena thread pool dan database connection pool sifatnya global (dipakai bersama oleh modul pesanan, pembayaran, dan notifikasi kurir), modul pesanan mengambil hampir seluruh slot koneksi dan thread yang ada.
3. **Modul Lain Tersandera (Bottleneck):** Ketika modul pembayaran dipanggil dan mengalami sedikit kelambatan (misalnya menunggu respon pihak ketiga), modul ini menahan sisa thread yang tersisa. Akhirnya, tidak ada lagi thread bebas di server untuk memproses request baru yang masuk.
4. **RAM Membengkak & OOM Killer:** Antrean request yang terus menumpuk di memori membuat penggunaan RAM membengkak drastis hingga batas maksimum server.
5. **Crash Total:** Server kehabisan resource dan memicu sistem operasi melakukan *Out of Memory (OOM) Killer* atau membuat proses aplikasi *freeze* total. Dampaknya, seluruh aplikasi FoodGo tumbang dan harus di-restart manual oleh tim devops. Fitur ringan seperti sekadar mengecek notifikasi kurir pun ikut mati total padahal tidak ada masalah pada modul tersebut.

**Solusi desain awal:** 
Untuk skala tim startup, solusinya tidak perlu langsung bikin microservices yang sangat kompleks, tapi bisa diterapkan langkah desain terpisah secara bertahap:
1. **Pemecahan Proses (Process Decoupling):** Pisahkan eksekusi modul ke dalam proses yang berbeda. Minimal, bedakan proses antara API Utama (Pesanan), Worker Pembayaran, dan Worker Notifikasi.
2. **Antrean Asinkron (Message Queue):** Ubah proses notifikasi kurir agar bersifat asinkron (*non-blocking*). Modul pesanan tidak perlu menunggu notifikasi terkirim; cukup kirim event/pesan ke message queue (seperti RabbitMQ atau Redis Queue) agar dikerjakan di background oleh worker notifikasi secara independen.
3. **Isolasi Resource dengan Container (Docker):** Bungkus tiap service/worker ke dalam container Docker masing-masing dengan alokasi batas CPU dan RAM yang jelas. Jika worker notifikasi mengalami *memory leak* atau kebanjiran job, hanya container notifikasi yang restart, sedangkan server pesanan tetap bisa melayani transaksi pengguna.

**Trade-off:** 
1. **Kompleksitas Operasional & Monitoring:** Tim engineering FoodGo yang awalnya hanya mengelola 1 proses aplikasi kini harus mengelola dan memantau beberapa service, proses worker, serta infrastruktur message broker tambahan.
2. **Overhead Jaringan & Latensi Tambahan:** Pemanggilan antar-modul yang sebelumnya berupa *in-memory function call* (sangat cepat) kini berubah menjadi pemanggilan jaringan (HTTP REST / gRPC / Message Broker). Ini menambah sedikit latensi antar-proses dan mewajibkan tim menangani potensi error jaringan baru.

---

## Pitfall 2: [Latency is zero] — ditulis oleh [Aryo Abdillah Ainnurrofiq]

**Bukti di skenario:** "Aplikasi jadi sangat lambat, beberapa permintaan timeout" Pada skenario FoodGo bahwa tidak ada timeout pada pemanggilan antar-service. Modul pembayaran dipanggil oleh modul pesanan lalu modul pembayaran menunggu respons tanpa batas waktu. Kondisi ini menurut saya menunjukkan bahwa sistem seolah menganggap komunikasi antar modul pembayaran akan selalu selesai dalam waktu yang cepat dan tidak mengalami keterlambatan   

**Kenapa ini keliru:** Asumsi tersebut menurut saya keliru karena komunikasi antar modul dalam sistem terdistribusi tidak selalu berlangsung secara instan. Jadi, ketika modul pesanan mengirim permintaan ke modul pembayaran, ada proses komunikasi dan proses yang membutuhkan waktu. Di modul pembayaran juga mengalami peningkatan beban sehingga respons jadi sangat lambat.
Menurut saya yang menarik untuk saya bahas adalah masalah utama FoodGo yang terjadi di modul pesanan tidak punya batas waktu ketika menunggu respons dari pembayaran. Akibatnya, ketika pembayaran mengalami keterlambatan, request dari modul pesanan tertahan. Jadi saat request bersamaan , semakin banyak proses yang harus menunggu respons pembayaran.

**Dampak ke FoodGo:**  Dampaknya menurut saya tejadi ketika modul pembayaran merespons dengan lambat, modul pesanan akan terus menunggu karena tidak punya timeout. Jadi, jika ada waktu yang sama banyak pengguna melakukan pemesanan, jumlah request yang menunggu juga semakin banyak. Jika kondisi ini terus berlangsung, resource pada modul pesanan dapat semakin terbebani sehingga kemampuan server untuk menangani request baru ikut menurun. Akibatnya, pengguna lain dapat mengalami waktu respons yang semakin lama dan beberapa request dapat mengalami timeout. Kondisi tersebut sesuai dengan gejala yang dialami FoodGo ketika aplikasi menjadi sangat lambat saat trafik meningkat.
Jadi alur sederhananya Payment lambat menyebabkan order menunggu karena tidak ada timeout hasilnya request banyak yang tertahan dan menyebabkan resource order terbebani lalu muncul request baru ikut melambat juga  




---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
