# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock

- Hasil `processed_count` yang didapat tidak konsisten. Pada beberapa percobaan, hasil yang diperoleh kurang dari 100, padahal nilai `num_orders` adalah 100.
- Perbedaan hasil terjadi karena beberapa thread dapat membaca nilai `processed_count` yang sama sebelum thread lain selesai memperbaruinya. Akibatnya, beberapa proses penambahan dapat saling menimpa.
- Pada percobaan ini digunakan kode:

      current = processed_count
      time.sleep(0.01)
      processed_count = current + 1

- Kondisi tersebut menyebabkan terjadinya **race condition**, sehingga hasil akhir berbeda-beda pada setiap percobaan.

### Hasil Percobaan

| Percobaan | Hasil |
|-----------|-------|
| 1 | 33 dari 100 |
| 2 | 37 dari 100 |
| 3 | 38 dari 100 |
| 4 | 34 dari 100 |
| 5 | 37 dari 100 |

Bukti percobaan disimpan pada:

`bukti/race-condition-tanpa-lock.png`

---

## Percobaan dengan Lock

- Setelah mengetahui adanya race condition, program diperbaiki dengan menggunakan `threading.Lock()`.
- Lock digunakan untuk melindungi proses membaca dan memperbarui `processed_count`, sehingga hanya satu thread yang dapat menjalankan proses tersebut pada satu waktu.
- Implementasi yang digunakan:

      lock = threading.Lock()

      with lock:
          current = processed_count
          time.sleep(0.01)
          processed_count = current + 1

### Hasil Percobaan

Program dijalankan sebanyak lima kali setelah menggunakan Lock dan menghasilkan:

- Percobaan 1: 100 dari 100
- Percobaan 2: 100 dari 100
- Percobaan 3: 100 dari 100
- Percobaan 4: 100 dari 100
- Percobaan 5: 100 dari 100

Hasil tersebut sesuai dengan jumlah pesanan yang seharusnya, yaitu 100.

Bukti percobaan disimpan pada:

`bukti/race-condition-with-lock.png`

---

## Perbandingan Hasil

| Percobaan | Tanpa Lock | Dengan Lock |
|-----------|------------|-------------|
| 1 | 33 | 100 |
| 2 | 37 | 100 |
| 3 | 38 | 100 |
| 4 | 34 | 100 |
| 5 | 37 | 100 |

Dari hasil percobaan dapat dilihat bahwa tanpa Lock terjadi race condition sehingga hasil tidak konsisten. Setelah menggunakan Lock, hasil menjadi konsisten dan sesuai dengan jumlah pesanan yang diproses.

---

## Kendala Docker

- Error yang ditemui saat menggunakan Docker adalah Docker Desktop pada awalnya tidak dapat berjalan dengan baik karena konfigurasi WSL belum aktif atau belum terdeteksi dengan benar.
- Setelah konfigurasi WSL diperbaiki dan Docker Desktop dapat berjalan, proses build dan menjalankan program dapat dilakukan.
- Selain itu, terdapat error `credential-desktop: executable file not found` ketika proses build membaca credential helper Docker. Error tersebut diperbaiki dengan menyesuaikan konfigurasi Docker sehingga proses build dapat berjalan.
- Setelah perbaikan dilakukan, program berhasil dijalankan menggunakan Docker dan menghasilkan nilai `processed_count` yang sesuai, yaitu 100.

---

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.
| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 6 Oktober 2026 | Gemini | Jelaskan untuk tugas 03 ini berikan aku pemahaman mengenai multithread atau lain sebagainya yang berhubungan dengan tugas kali ini | Menjelaskan multithread dan menjelaskan bagian logic code dengan detail tanpa memberikan copy code | Menulis code sesuai dengan pemahaman yang udah diberikan (Aryo) |
| 6 Oktober 2026 | Antigravity AI | Brainstorming materi tugas 3: analisis perbedaan efisiensi proses OS berat vs multithreading pada kasus FoodGo, mekanisme race condition tingkat bytecode, serta struktur Dockerfile | Menjelaskan perbandingan shared memory vs isolated address space, overhead PCB & TLB flush, instruksi non-atomik Python bytecode (LOAD_GLOBAL, BINARY_OP, STORE_GLOBAL), serta best practice base image slim | Mengembangkan dan menyusun penjelasan tersebut ke dalam bahasa dan pemahaman sendiri pada README.md poin 1–4 serta melengkapi Dockerfile (Annisa) |


