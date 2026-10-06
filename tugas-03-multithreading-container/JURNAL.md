# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: engga konsisten soalnya pas awal coba nilai nya kurang dari 100 padahal nilai num_orders nya 100 yang ku dapetin tadi di awal tadi malahan nilai nya 0 karena terjadi crash yang numpuk karena variabel nya belum kedefinisi
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): nilai jadi meleset karena operasi "processed_count +=1" bukan operasi komputasi yang tunggal, tapi ada 3 tahap baca : membaca nilai saat ini, tambahin nilai nya sama 1, terus nyimpen nilai baru tapi karena gada proteksi beberapa thread pekerja bisa membaca nilai, proses, dan menyimpan nilai nya hampir barengan, jadi perhitungan satu thread ketimpa sama thread lain yang mengeksekusi data memori yang sama yang bisa jumlah perhitungan hasil akhirnya ga sesuai dengan jumlah pesanan ( bukti di file bukti)

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100 ( sesuai sama jumlah pesanan "num_orders"). Jadi ketika aku nambahin "with lock" terus menghapus tag "lock" di todo 1 code berjalan lancar dan sesuai dengan hasil yang di inginkan jadi operasi penambahan nilai nya berjalan aman (thread safe) tanpa ada data yang menimpa

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri | | 6 Oktober 2026 | Gemini | Jelaskan untuk tugas 03 ini berikan aku pemahaman mengenai multithread atau lain sebagainya yang berhubungan dengan tugas kali ini | Menjelaskan multithread dan menjelaskan bagian logic code dengan detail tanpa memberikan copy code | Menulis code sesuai dengan pemahaman yang udah diberikan |

