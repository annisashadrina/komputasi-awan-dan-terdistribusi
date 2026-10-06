# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: engga konsisten soalnya pas awal coba nilai nya kurang dari 100 padahal nilai num_orders nya 100 yang ku dapetin tadi di awal tadi malahan nilai nya 0 karena terjadi crash yang numpuk karena variabel nya belum kedefinisi
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): nilai jadi meleset karena operasi "processed_count +=1" bukan operasi komputasi yang tunggal, tapi ada 3 tahap baca : membaca nilai saat ini, tambahin nilai nya sama 1, terus nyimpen nilai baru tapi karena gada proteksi beberapa thread pekerja bisa membaca nilai, proses, dan menyimpan nilai nya hampir barengan, jadi perhitungan satu thread ketimpa sama thread lain yang mengeksekusi data memori yang sama yang bisa jumlah perhitungan hasil akhirnya ga sesuai dengan jumlah pesanan ( bukti di file bukti)

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100 ( sesuai sama jumlah pesanan "num_orders"). Jadi ketika aku nambahin "with lock" terus menghapus tag "lock" di todo 1 code berjalan lancar dan sesuai dengan hasil yang di inginkan jadi operasi penambahan nilai nya berjalan aman (thread safe) tanpa ada data yang menimpa

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya:
  1. **Perintah `docker` tidak dikenali di terminal:** Saat Docker Desktop baru selesai diinstall, terminal PowerShell lama belum mendeteksi perintah `docker` (`The term 'docker' is not recognized`). Hal ini terjadi karena variabel `$env:Path` pada sesi terminal lama belum diperbarui. Solusinya: membuka sesi tab terminal baru atau mereload environment path secara manual.
  2. **Error `docker-credential-desktop: executable file not found in %PATH%`:** Terjadi saat proses build membaca kredensial helper Docker Desktop. Hal ini teratasi setelah path `DockerDesktop\resources\bin` termuat secara lengkap ke dalam environment path sistem.
  3. **Hasil `docker run`:** Setelah image `foodgo-order-sim` berhasil di-build, kontainer dijalankan dengan `docker run --rm foodgo-order-sim` dan sukses menghasilkan `Total pesanan diproses: 100 (seharusnya 100)` tanpa error.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.
| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 6 Oktober 2026 | Gemini | Jelaskan untuk tugas 03 ini berikan aku pemahaman mengenai multithread atau lain sebagainya yang berhubungan dengan tugas kali ini | Menjelaskan multithread dan menjelaskan bagian logic code dengan detail tanpa memberikan copy code | Menulis code sesuai dengan pemahaman yang udah diberikan (Aryo) |
| 6 Oktober 2026 | Antigravity AI | Brainstorming materi tugas 3: analisis perbedaan efisiensi proses OS berat vs multithreading pada kasus FoodGo, mekanisme race condition tingkat bytecode, serta struktur Dockerfile | Menjelaskan perbandingan shared memory vs isolated address space, overhead PCB & TLB flush, instruksi non-atomik Python bytecode (LOAD_GLOBAL, BINARY_OP, STORE_GLOBAL), serta best practice base image slim | Mengembangkan dan menyusun penjelasan tersebut ke dalam bahasa dan pemahaman sendiri pada README.md poin 1–4 serta melengkapi Dockerfile (Annisa) |


