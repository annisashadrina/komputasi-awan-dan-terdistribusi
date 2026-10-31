# Jurnal Proses — Tugas 6

## Implementasi find_successor
- **Kesalahan pertama yang ditemui:** Pada proses pencarian successor, perlu diperhatikan kondisi ketika hash key lebih besar daripada seluruh ID node yang tersedia. Jika kondisi tersebut tidak ditangani, pencarian successor tidak dapat mengikuti aturan ring Chord.
- **Cara memperbaikinya:** Mengurutkan seluruh ID node menggunakan `sorted()` dan mencari node pertama yang memiliki ID lebih besar atau sama dengan hash key. Jika tidak ditemukan, fungsi mengembalikan node dengan ID terkecil sebagai successor melalui mekanisme *wrap-around*.

## Skenario join/leave
- **Hasil sebelum dan sesudah node baru bergabung:**
  
  Sebelum node baru bergabung, ring memiliki empat node, yaitu `node-bandung-1` (ID 40), `node-jakarta-2` (ID 102), `node-surabaya-1` (ID 136), dan `node-jakarta-1` (ID 177).

  Setelah `node-medan-1` dengan ID 123 bergabung, node tersebut menjadi successor untuk data dengan hash 123. Berdasarkan output program, data `kurir-uji-join-9` yang sebelumnya menjadi tanggung jawab node 136 berpindah ke node 123.

  ```text
  [TRANSFER] Data hash 123 berpindah dari node 136 ke node 123
  ```

- **Hasil sebelum dan sesudah node keluar:**

  Sebelum node keluar, `node-jakarta-1` dengan ID 177 bertanggung jawab atas data dengan hash 169.

  Setelah `node-jakarta-1` keluar dari ring, tanggung jawab data tersebut berpindah ke `node-bandung-1` dengan ID 40 melalui mekanisme *wrap-around*.

  ```text
  [TRANSFER] Data hash 169 berpindah dari node 177 ke node 40
  ```

  Hasil lookup setelah perubahan topologi menunjukkan bahwa `kurir-001` tetap menghasilkan alamat IP `192.168.1.10` dan `kurir-002` menghasilkan `192.168.1.11`.


## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.


| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 31 Oktober 2026 | ChatGPT | Meminta bantuan memahami implementasi simulasi Chord DHT pada file `src/chord_simulation.py`, khususnya fungsi `find_successor()`, `join()`, `leave()`, dan `lookup()`. | Mendapatkan penjelasan mengenai konsep successor, consistent hashing, mekanisme wrap-around, serta alur perubahan tanggung jawab data ketika node bergabung dan keluar. | Saran digunakan sebagai bahan pemahaman. Implementasi kode diperiksa dan disesuaikan kembali dengan skeleton tugas, kemudian hasilnya diuji melalui program Python. |
| 31 Oktober 2026 | ChatGPT | Meminta bantuan menyusun struktur dan memahami poin analisis yang harus dimasukkan ke dalam `README.md` dan `JURNAL.md`. | Mendapatkan ide mengenai perbandingan DHT dengan flat naming dan DNS, ring topology, mapping ID kurir, serta dokumentasi hasil pengujian. | Kelompok mencocokkan penjelasan dengan kode program, hasil hashing, dan screenshot output sebelum menyusun dokumentasi akhir. |
