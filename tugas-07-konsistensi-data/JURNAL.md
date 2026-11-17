# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan: Kami mempertimbangkan dua model konsistensi, yaitu Sequential Consistency dan Eventual Consistency. Pada Eventual Consistency, data pada setiap server tidak harus langsung sama karena proses replikasi membutuhkan waktu. Hal ini dapat menyebabkan saldo di server Jakarta dan Bandung berbeda untuk sementara waktu. Jika kondisi tersebut terjadi pada aplikasi FoodGo, pengguna bisa melihat saldo yang belum diperbarui setelah melakukan top-up. Akibatnya, pengguna dapat mengalami kebingungan saat melakukan transaksi karena saldo yang terbaca belum sesuai dengan perubahan terakhir.

- Kesimpulan akhir dan alasan: Kami memilih Sequential Consistency sebagai model konsistensi yang dipertimbangkan untuk menjaga urutan operasi pada replika. Selain itu, mekanisme Read-Your-Writes digunakan agar pengguna dapat langsung melihat hasil perubahan data yang telah dilakukan sendiri. Namun, Sequential Consistency saja tidak menjamin bahwa pembacaan selalu mendapatkan data terbaru berdasarkan waktu nyata. Untuk transaksi pembayaran, sistem juga tetap membutuhkan mekanisme tambahan seperti operasi saldo yang atomik dan konsistensi yang lebih kuat agar tidak terjadi kesalahan dalam pemrosesan transaksi.

## Simulasi
- Hasil skenario naif vs Read-Your-Writes: Pada skenario pertama, pengguna melakukan top-up sebesar Rp50.000 pada server Jakarta. Setelah itu, pengguna mencoba membaca saldo melalui server Bandung sebelum proses replikasi selesai. Hasil pembacaan masih menunjukkan Rp0 karena data terbaru belum diterima oleh server Bandung. Hal ini menunjukkan adanya perbedaan data sementara antara kedua server akibat keterlambatan replikasi.

- Pada skenario berikutnya, pengguna melakukan top-up kembali sebesar Rp20.000 sehingga saldo pada server Jakarta menjadi Rp70.000. Ketika pengguna membaca saldo melalui server Bandung, sistem memeriksa versi data yang dimiliki server tersebut. Karena versi data Bandung masih tertinggal dari versi terbaru di Jakarta, sistem mengalihkan proses pembacaan ke server Jakarta. Dengan demikian, pengguna tetap mendapatkan saldo terbaru sebesar Rp70.000 meskipun proses replikasi ke Bandung belum selesai.

- Setelah waktu replikasi terpenuhi, data pada server Bandung akan diperbarui sehingga kedua server memiliki saldo yang sama. Dari simulasi ini terlihat bahwa mekanisme Read-Your-Writes dapat membantu mengatasi masalah pembacaan data lama setelah pengguna melakukan perubahan data sendiri.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
|16 November 2026|Claude|Analisis & berikan aku panduan untuk ngerjain tugas-07 dan berikan aku analogi tanpa menulis code nya langsung sesuai aturan biar aku paham|Ai melakukan saran untuk detail checking lagi agar tidak ada kesalahan|Memahami logika yang di berikan oleh ai lalu aku kerjain dan bertanya detail code kalo aku lupa dan salah|
| 17 November 2026 | Codex | Meminta melengkapi README dan jurnal berdasarkan pekerjaan yang sudah ada. | AI menulis analisis, diagram, hasil simulasi, dan memperbaiki jurnal. | Hasil tersebut dibuat langsung oleh AI dan belum diolah sendiri; penggunaan ini melampaui batas Level 2 pada tugas dan perlu ditangani kelompok sesuai aturan dosen. |
