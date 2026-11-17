# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan: Kami mempertimbangkan dua model, yaitu Sequential Consistency dan Eventual Consistency. Eventual Consistency bisa menyebabkan saldo di server Jakarta dan Bandung berbeda buat sementara waktu karena proses replikasi membutuhkan waktu. Kalau hal ini terjadi di aplikasi FoodGo, user bisa melihat saldo yang tidak sesuai dan transaksi mereka berpotensi gagal.
- Kesimpulan akhir & alasan: Kami memilih Sequential Consistency untuk pengurutan operasi di seluruh replika dan menggunakan Read-Your-Writes agar user bisa melihat hasil top-up miliknya. Sequential Consistency saja tidak menjamin hasil terbaru menurut waktu nyata; transaksi pembayaran juga memerlukan operasi saldo yang atomik dan konsistensi kuat.

## Simulasi
- Hasil skenario naif vs Read-Your-Writes: Pada skenario pertama, user melakukan top-up sebesar Rp50.000 di server Jakarta. Jadi pas saldo langsung dibaca dari server Bandung, hasilnya masih Rp0 karena data belum selesai direplikasi. Setelah itu, user melakukan top-up lagi sebesar Rp20.000 sehingga saldo di Jakarta menjadi Rp70.000. Dengan Read-Your-Writes, sistem mengecek versi data di Bandung. Karena versinya masih tertinggal, pembacaan dialihkan ke Jakarta dan user mendapatkan saldo terbaru sebesar Rp70.000.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
|16 November 2026|Claude|Analisis & berikan aku panduan untuk ngerjain tugas-07 dan berikan aku analogi tanpa menulis code nya langsung sesuai aturan biar aku paham|Ai melakukan saran untuk detail checking lagi agar tidak ada kesalahan|Memahami logika yang di berikan oleh ai lalu aku kerjain dan bertanya detail code kalo aku lupa dan salah|
| 17 November 2026 | Codex | Meminta melengkapi README dan jurnal berdasarkan pekerjaan yang sudah ada. | AI menulis analisis, diagram, hasil simulasi, dan memperbaiki jurnal. | Hasil tersebut dibuat langsung oleh AI dan belum diolah sendiri; penggunaan ini melampaui batas Level 2 pada tugas dan perlu ditangani kelompok sesuai aturan dosen. |
