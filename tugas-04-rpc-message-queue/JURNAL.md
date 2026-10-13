# Jurnal Proses — Tugas 4

## Jalur yang Dipilih

- **Jalur B — Message Queue (MQ):** Aryo memilih jalur B terlebih dahulu untuk dianalisis menggunakan RabbitMQ.
- Kelompok juga mengerjakan **Jalur A — RPC** sebagai pembanding komunikasi sinkron dan asinkron.

## Kendala Teknis

- Saat mengaktifkan virtual environment menggunakan `.\venv\Scripts\Activate.ps1`, PowerShell menolak menjalankan script karena kebijakan Execution Policy Windows.
- Kendala diatasi dengan menjalankan `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` pada sesi PowerShell yang digunakan.
- Setelah virtual environment berhasil diaktifkan, program dijalankan sesuai urutan untuk memastikan server RPC dan RabbitMQ siap digunakan.

## Uji "Pesan Tidak Hilang" (Khusus Jalur B)

- **Langkah uji:** Mematikan consumer, menjalankan publisher untuk mengirim beberapa pesan, kemudian mengaktifkan kembali consumer.
- **Hasil yang diamati:** Berdasarkan pengujian kelompok, pesan yang sudah masuk ke antrean tetap tersedia ketika consumer belum berjalan. Setelah consumer aktif kembali, pesan dapat diproses. Bukti pengujian ditampilkan pada screenshot di folder `bukti/`.
- Pengujian ini menunjukkan bahwa publisher dan consumer tidak harus aktif secara bersamaan. RabbitMQ menyimpan pesan di antrean selama pesan telah diterima dan belum dihapus dari antrean.

## Analisis RPC dan Message Queue

### Jalur A — RPC (Sinkron)

Client memanggil fungsi pada server dan menunggu hasilnya secara langsung. Metode ini cocok untuk proses yang membutuhkan respons segera, seperti permintaan hasil pembayaran. Namun, jika server tidak aktif atau koneksi gagal, permintaan dapat mengalami kegagalan atau tidak memperoleh respons.

### Jalur B — Message Queue (Asinkron)

Publisher mengirim event ke RabbitMQ tanpa harus menunggu consumer menyelesaikan pemrosesan. Consumer mengambil pesan dari antrean dan memprosesnya secara terpisah. Metode ini cocok untuk proses latar belakang, seperti pengiriman notifikasi setelah pembayaran berhasil.

### Penerapan pada FoodGo

RPC dapat digunakan untuk komunikasi yang membutuhkan respons langsung, sedangkan Message Queue dapat digunakan untuk mengirim event pembayaran kepada modul lain. Dengan MQ, proses notifikasi dapat berjalan tanpa membuat modul pembayaran harus menunggu consumer menyelesaikan seluruh pekerjaannya.

## Log Penggunaan AI (Level 2)

Penggunaan AI mengikuti kebijakan Level 2, yaitu untuk brainstorming dan penyusunan ide, bukan untuk menghasilkan seluruh kode atau analisis akhir.

| Tanggal | Tool AI | Prompt yang Diberikan | Ringkasan Saran/Ide AI | Bagaimana Diolah Menjadi Tulisan/Kode Sendiri |
|---|---|---|---|---|
| 11 Oktober 2026 | Gemini | Berikan panduan memahami studi kasus RPC dan Message Queue pada FoodGo serta struktur jurnal Tugas 4. | Membantu memahami perbedaan komunikasi sinkron dan asinkron serta menyusun struktur jurnal. | Saran digunakan untuk memahami konsep dan menyusun jurnal. Kode, pengujian, dan analisis disesuaikan dengan pekerjaan serta hasil pengujian kelompok. |
| 14 Oktober 2026 | ChatGPT | Bantu melengkapi jurnal proses Tugas 4 berdasarkan instruksi dan dokumentasi kelompok. | Memberikan saran untuk mencatat kendala teknis, pengujian pesan, dan analisis RPC dibandingkan MQ. | Saran dijadikan panduan penulisan, kemudian disesuaikan dengan dokumentasi dan bukti praktik kelompok. |

## Kesimpulan

RPC dan Message Queue memiliki fungsi yang berbeda. RPC cocok untuk komunikasi yang membutuhkan hasil secara langsung, sedangkan Message Queue cocok untuk komunikasi asinkron yang memungkinkan pesan diproses ketika consumer siap. Pengujian MQ menunjukkan pentingnya antrean pesan dalam membantu proses tetap berjalan ketika publisher dan consumer tidak aktif secara bersamaan.
