# Jurnal Proses — Tugas 2

## [Tanggal 28 September 2026]
- Opsi arsitektur yang dipertimbangkan: 
1. SOA (Service-Oriented Architecture) , menurut ku SOA ini untuk memisahkan sistem FoodGo jadi beberapa layanan sesuai fungsinya seperti; Pesanan, Pembayaran, Katalog resto, dan Kurir.
2. Publish-Subscribe, jadi ini menggunakan mekanisme event supaya layanan bisa bertukar informasi tanpa harus saling berkomunikasi secara langsung.
3. Kombinasi SOA dan Pub-Sub yang aku sarankan untuk tugas ini ( kita akan memakai kombinasi ini). Menggunakan SOA untuk memisahkan layanan utama dan Publish-Subscribe untuk komunikasi berbasis event
- Kenapa akhirnya pilih [SOA/Pub-Sub]: Pada rencana pertama aku memilih kombinasi dua SOA & Pub-Sub ini karena FoodGo membutuhkan pemisahan layanan sekaligus yang dimana komunikasi yang tidak selalu bergantung sama layanan lain. Aku akan bagi yang aku pikirkan disini jadi SOA ini berfungsi untuk memisahkan fungsi utama seperti pesanan, pembayaran, katalog resto. Nah untuk yang Pub-Sub digunakan untuk mengirimkan informasi berupa event ke layanan yang ngebutuhin. Jadi rancangan ini tujuanya agar ketergantungan antar layanan bisa dikurangi , walupun sistem jadi lebih kompleks karena merluin massage broker
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): Diagram baru ingin dibuat dan masih dalam tahap perancangan awal.

## [Tanggal 28 September 2026 - jam 19.15] ini annisa
- Aktivitas: Melanjutkan pengerjaan analisis pada `README.md` untuk poin nomor 1 dan nomor 4 (analisis cara arsitektur mengatasi masalah coupling dari Tugas 1 serta trade-off-nya).
- Hasil analisis & keputusan:
  - Untuk nomor 1, memutuskan kombinasi SOA dan Pub-Sub: SOA digunakan untuk transaksi inti (validasi katalog dan eksekusi pembayaran) karena butuh respons langsung dan konsistensi seketika, sedangkan Pub-Sub digunakan untuk komunikasi ke resto, kurir, dan notifikasi agar proses berjalan asinkron dan tidak saling memblokir
  - Untuk nomor 4, mengaitkan solusi dengan hasil evaluasi Tugas 1: SOA memutus *Resource & Deployment Coupling* (tiap modul punya resource sendiri dan deploy terpisah), sedangkan Pub-Sub memutus *Temporal Coupling* (modul pesanan tidak perlu menggantung menunggu resto/kurir)
  - Trade-off yang diidentifikasi: alur komunikasi menjadi non-linear sehingga debugging/tracing lebih kompleks (butuh Correlation ID) serta adanya tantangan *eventual consistency* jika terjadi pembatalan pesanan

## [ Tanggal.. ]

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|28 sep |ChatGpt| Jelaskan apa itu SOA,Pub-Sub dan berikan fungsinya untuk brainstorm ku di tugas kedua  | ngasih penjelasan tentang SOA-Pub-Sub terus dia menjelaskan 2 komponen itu untuk tugas 02 | dengan brainstorm itu aku ( aryo ) berfikir untuk memakai 2 opsi arsitektur itu dan untuk bagian ku akan mengerjakan bagian service pesanan + service pembayaran|
| 28 sep | Gemini | Jelaskan untuk alur end-to-end FoodGo dan berikan saya contoh agar bisa dipahami | dengan saran yang diberikan aku (aryo) membuat alur end-to-end sesuai contoh namun tidak langsung asal copas Ai | membuat diagram sequence dari hasil kesimpulan brainstorm ai tanpa lansung mencopas |
| 28 sep (19.15) | Gemini | Analisis hubungan pitfall coupling Tugas 1 dengan rancangan SOA/Pub-Sub Tugas 2 untuk nomor 1 dan 4 | Memberikan penjelasan keterkaitan pitfall coupling Tugas 1 dengan solusi SOA + Pub-Sub serta rincian trade-off (debugging non-linear & eventual consistency) | Membaca dan memahami poin penjelasan AI, lalu merangkum serta menuliskan kembali jawaban nomor 1 dan 4 ke README.md dengan pemahaman dan kalimat sendiri |
