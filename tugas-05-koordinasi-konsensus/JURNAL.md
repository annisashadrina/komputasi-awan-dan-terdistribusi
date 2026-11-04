# Jurnal Proses — Tugas 5

## Implementasi Bully

- **Kendala saat mengisi TODO 1–4:** Kendala yang perlu diperhatikan adalah memahami alur komunikasi antarnode, menangani pesan `ELECTION`, `OK`, dan `COORDINATOR`, serta mengatur waktu tunggu respons. Selain itu, proses pemantauan leader perlu dilakukan agar node lain dapat memulai election kembali ketika leader tidak merespons.
- **Penyelesaian:** Memahami fungsi setiap jenis pesan, penggunaan `threading.Event` untuk menunggu respons `OK`, serta penggunaan `lock` untuk membantu mengelola status election dan leader agar tidak mudah terjadi konflik antar-thread.

## Skenario 1: Start normal

- **Leader yang terpilih:** Node 5 (sesuai hasil yang diharapkan karena memiliki ID tertinggi di antara lima node aktif).
- **Log/observasi:** Node melakukan proses election dengan mengirim pesan `ELECTION` kepada node yang memiliki ID lebih tinggi. Node yang masih aktif memberikan respons `OK` jika memenuhi aturan algoritma. Node 5 diharapkan menjadi leader dan mengirim pesan `COORDINATOR` kepada node lain.
- **Hasil aktual:** Pada uji lima proses, Node 5 mendeklarasikan diri dan Node 1–4 mencatat Node 5 sebagai leader.
- **Bukti:** `bukti/log_node1.txt` sampai `bukti/log_node5.txt` dan screenshot skenario 1.

## Skenario 2: Leader dimatikan

- **Leader baru yang terpilih:** Node 4 (sesuai hasil yang diharapkan setelah Node 5 dihentikan).
- **Berapa lama waktu sampai leader baru terdeteksi:** Tidak diukur secara tepat; log tidak memuat timestamp. Pengamatan berlanjut selama 25 detik setelah Node 5 dihentikan.
- **Log/observasi:** Setelah proses Node 5 dihentikan menggunakan `Ctrl+C`, node lain seharusnya mendeteksi bahwa leader tidak merespons melalui pesan `PING`. Node yang mendeteksi kegagalan memulai election kembali. Karena Node 4 merupakan node dengan ID tertinggi yang masih aktif, Node 4 diharapkan menjadi leader baru dan mengirim pesan `COORDINATOR` kepada node lain.
- **Hasil aktual:** Node 4 mendeklarasikan diri sebagai leader; Node 1–3 mencatat Node 4 sebagai leader.
- **Bukti:** `bukti/log_node1.txt` sampai `bukti/log_node4.txt` dan screenshot skenario 2.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 20 Oktober 2026 | ChatGPT | Meminta bantuan memahami tugas Bully Algorithm, memeriksa alur pesan antarnode, serta menyusun README dan jurnal proses berdasarkan instruksi dosen. | AI membantu menjelaskan fungsi pesan `ELECTION`, `OK`, `COORDINATOR`, dan `PING`, menjelaskan skenario pemilihan leader, serta menyarankan struktur dokumentasi dan pengujian. | Penjelasan dibandingkan dengan instruksi tugas. Dokumentasi perlu dibaca, diperiksa, dan disesuaikan dengan hasil pengujian aktual. Implementasi kode harus ditinjau dan dikerjakan sesuai batas penggunaan AI yang ditetapkan dosen. |

| 4 November 2026 | Codex | Pelajari folder tugas 05, cari yang belum dilakukan, kemudian perbaiki. | Memperbaiki percabangan pesan dan kondisi balapan, menjalankan uji lima proses, serta memperbarui dokumentasi dan bukti. | Perubahan kode dan dokumentasi dihasilkan AI; hal ini melampaui batas Level 2 yang tercantum pada tugas dan harus ditinjau serta ditangani oleh kelompok sesuai aturan dosen. |

## Kesimpulan

Bully Algorithm digunakan untuk memilih leader berdasarkan ID node tertinggi yang masih aktif. Dalam pengujian normal, Node 5 diharapkan menjadi leader. Ketika Node 5 tidak aktif, node lain melakukan election ulang dan Node 4 diharapkan menjadi leader baru. Keberhasilan kedua skenario perlu dipastikan melalui hasil program dan bukti terminal.

