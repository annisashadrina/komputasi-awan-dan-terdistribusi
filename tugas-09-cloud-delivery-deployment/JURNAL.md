# Jurnal Proses — Tugas 9

## Diskusi deployment model
Kelompok kami awalnya mempertimbangkan empat deployment model, yaitu Public Cloud, Private Cloud, Hybrid Cloud, dan Community Cloud. Pertama Public Cloud memiliki keunggulan dalam skalabilitas, tetapi kendali langsung terhadap infrastrukturnya lebih terbatas. Hybrid Cloud menggabungkan fleksibilitas Public Cloud dan kontrol Private Cloud, tetapi membutuhkan pengelolaan serta integrasi yang lebih kompleks. Sementara itu, Community Cloud memungkinkan penggunaan infrastruktur bersama oleh organisasi dengan kepentingan serupa.

Setelah mempertimbangkan kebutuhan sistem, kelompok kami memilih Private Cloud karena Sistem Data Kependudukan menyimpan data sensitif seperti NIK, alamat, dan biometrik penduduk. Private Cloud memungkinkan pemerintah memiliki kendali lebih besar terhadap infrastruktur, penyimpanan, dan kebijakan keamanan data. Meskipun membutuhkan perencanaan kapasitas yang baik untuk menghadapi lonjakan akses, model ini dinilai sesuai dengan kebutuhan kerahasiaan dan pengendalian data kependudukan.

## Diskusi service model per komponen
Kelompok kami mempertimbangkan tiga service model, yaitu IaaS, PaaS, dan SaaS. IaaS memberikan kendali lebih besar terhadap infrastruktur, PaaS memudahkan pengembangan dan pengelolaan aplikasi, sedangkan SaaS menyediakan aplikasi yang siap digunakan.

Pada akhirnya kelompok kami memilih kombinasi IaaS dan SaaS. IaaS digunakan untuk database inti karena membutuhkan kendali infrastruktur dan keamanan yang lebih besar, sedangkan SaaS digunakan untuk portal akses instansi agar lebih mudah digunakan oleh berbagai pengguna.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 20 November 2026 | ChatGPT | Jelaskan apa itu service model IaaS, PaaS, dan SaaS. Untuk penjelasan berikan yang mudah dipahami oleh pemula, lalu jelaskan kelemahan tiap service modelnya. | AI memberikan penjelasan dasar mengenai perbedaan IaaS, PaaS, dan SaaS beserta contoh penerapannya. | Penjelasan AI digunakan sebagai referensi untuk memahami ketiga service model. Kelompok kemudian mempertimbangkan penerapannya pada database inti dan portal akses instansi, lalu menyusun penjelasan berdasarkan hasil diskusi kelompok. |
