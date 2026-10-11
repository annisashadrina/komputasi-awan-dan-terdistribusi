# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- [RPC / MQ / keduanya], alasan: Kelompok memilih Jalur B, yaitu Message Queue menggunakan RabbitMQ.

## Kendala teknis
- Saat mengaktifkan virtual environment menggunakan `.\venv\Scripts\Activate.ps1` ,PowerShell menolak menjalankan script karena Execution Policy Windows.
- Masalah diatasi dengan mengubah Execution Policy hanya pada proses PowerShell yang sedang digunakan menggunakan `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
- Setelah itu virtual environment berhasil diaktifkan.

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
