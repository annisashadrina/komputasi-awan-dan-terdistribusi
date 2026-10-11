# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- [RPC / MQ / keduanya], alasan: 
1. Aryo memilih jalur B dulu buat dianalisis, yaitu Message Queue menggunakan RabbitMQ.

## Kendala teknis
- Saat mengaktifkan virtual environment menggunakan `.\venv\Scripts\Activate.ps1` ,PowerShell menolak menjalankan script karena Execution Policy Windows.
- Masalah diatasi dengan mengubah Execution Policy hanya pada proses PowerShell yang sedang digunakan menggunakan `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
- Setelah itu virtual environment berhasil diaktifkan.

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: sesuai bukti yang udah aku cantumin , berdasarkan analisis yang aku lakuin di jalur B ketika consumer nyala dan publisher nyala hasilnya di RabbitMQ Dashboard tidak ada keterangan "Ready" atau 0  yang dimana ini artinya tidak ada proses nunggu (bukti ss di file bukti). Nah ketika consumer mati terus publisher nyala, publisher tetep nyelesaiin event antrian tetep munculin user id sama jumlah tappi hasilnya selesai bukan looping atau terus nunggu, tapi pas di cek di RabbitMQ Dashboard keterangan ready nya muncul sebanyak 3 antrian yang artinya publisher perlu validasi dari consumer (bukti ss di file bukti) Hal ini menunjukkan adanya asynchronous decoupling antara publisher dan consumer.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |11 Oktober 2026|ChatGPT|Berikan saya panduan memahami studi kasus RPC dan Message Queue pada FoodGo|Buat studi kasus ini disaranin bertahap menguji jalur B , ngasih gambaran juga perbedaan komunikasi sinkron dan asinkron serta alur pengerjaan Massage Queue|Menyesuaikan struktur pengerjaan, memahami konsep, melakukan pengujian dan debugging sendiri|
| ... | ... | ... | ... | ... |
