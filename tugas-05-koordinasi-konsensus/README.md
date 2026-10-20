# Tugas 5 (Pekan 5) — Koordinasi & Konsensus

**Materi terkait:** Physical/Logical Clock, Election Algorithm (Bully/Raft).

## Studi Kasus

Terjadi konflik urutan waktu pada pesanan FoodGo (dua server mencatat urutan pesanan berbeda karena jam tidak sinkron), dan sistem membutuhkan satu **"Node Leader"** untuk mengelola antrean pesanan pusat agar tidak terjadi konflik pemrosesan ganda.

| Nama | NIM | Kontribusi |
|---|---|---|
| Annisa Nur Shadrina | 103072400134 |...|
| Fadia Nabila Shifa | 103072400066 |...|
| Aryo Abdillah Ainnurrofiq | 103072400006 |Mengimplementasikan logika bully action (code) lengkap dengan bukti dan menguji skenario 1 dan skenario 2|

### A. Kenapa FoodGo Membutuhkan Leader?

FoodGo membutuhkan leader untuk mengoordinasikan beberapa server yang bekerja secara bersamaan agar proses pemesanan dapat berjalan dengan teratur. Tanpa adanya leader, setiap server dapat mengambil keputusan sendiri sehingga berpotensi menimbulkan perbedaan urutan pemrosesan pesanan, konflik data, atau pemrosesan transaksi yang berulang.

Leader berperan sebagai koordinator dalam pengambilan keputusan yang membutuhkan koordinasi antarserver. Jika leader mengalami kegagalan, Bully Algorithm memungkinkan node lain melakukan pemilihan ulang untuk menentukan leader pengganti berdasarkan ID tertinggi dari node yang masih aktif.

Dengan adanya mekanisme ini, koordinasi FoodGo dapat tetap berjalan ketika leader mengalami kegagalan. Namun, pemilihan leader saja tidak menjamin seluruh transaksi konsisten atau mencegah pesanan diproses dua kali. Oleh karena itu, FoodGo tetap membutuhkan mekanisme tambahan untuk menjaga konsistensi data dan mencegah duplikasi transaksi.

## B. Kenapa Bully?

Bully Algorithm dipilih karena mekanisme pemilihan leader-nya relatif sederhana dan mudah diterapkan pada simulasi sistem terdistribusi yang terdiri dari lima node. Setiap node memiliki ID yang berbeda, sehingga pemilihan leader dapat dilakukan berdasarkan ID tertinggi dari node yang masih aktif.

Ketika sebuah node mendeteksi bahwa leader tidak merespons, node tersebut dapat memulai proses election dengan mengirim pesan `ELECTION` kepada node yang memiliki ID lebih tinggi. Node yang masih aktif akan membalas dengan pesan `OK` dan melanjutkan proses election. Jika tidak ada node dengan ID lebih tinggi yang merespons, node tersebut dapat menyatakan dirinya sebagai leader dan mengumumkannya melalui pesan `COORDINATOR`.

Pada sistem FoodGo, mekanisme ini membantu menentukan koordinator baru ketika leader mengalami kegagalan. Selain itu, Bully Algorithm cocok digunakan untuk memahami dasar pemilihan leader sebelum mempelajari algoritma konsensus yang lebih kompleks, seperti Raft.

Namun, Bully Algorithm berfokus pada pemilihan leader dan tidak secara langsung menjamin konsistensi seluruh transaksi FoodGo. Oleh karena itu, diperlukan mekanisme tambahan untuk menjaga konsistensi data dan mencegah pemrosesan pesanan secara berulang.

## C. Kenapa Selalu ID Tertinggi?

Dalam Bully Algorithm, node dengan ID tertinggi yang masih aktif dipilih menjadi leader karena algoritma ini menggunakan ID sebagai dasar prioritas pemilihan. Aturan tersebut membuat setiap node memiliki urutan prioritas yang jelas sehingga proses pemilihan leader dapat dilakukan secara terstruktur.

Ketika node dengan ID lebih rendah memulai election, node tersebut akan mengirim pesan `ELECTION` kepada node dengan ID lebih tinggi. Jika ada node ber-ID lebih tinggi yang masih aktif, node tersebut akan membalas dengan pesan `OK` dan memulai election sendiri. Proses ini berlanjut hingga node aktif dengan ID tertinggi tidak menerima balasan dari node yang lebih tinggi, sehingga dapat menyatakan dirinya sebagai leader dan mengirim pesan `COORDINATOR` kepada node lainnya.

Pada simulasi FoodGo, Node 5 menjadi leader ketika seluruh node aktif karena memiliki ID tertinggi. Jika Node 5 mengalami kegagalan, Node 4 berpotensi menjadi leader baru karena memiliki ID tertinggi di antara node yang masih aktif.

Pemilihan berdasarkan ID tertinggi bukan berarti node tersebut pasti memiliki performa terbaik. Aturan ini merupakan mekanisme prioritas yang digunakan Bully Algorithm agar pemilihan leader memiliki hasil yang jelas dan konsisten selama kondisi komunikasi serta asumsi algoritma terpenuhi.




## Tugas Kelompok

Implementasikan simulasi **Bully Algorithm** untuk memilih leader di antara **5 node virtual** yang berjalan sebagai 5 proses Python terpisah di laptop yang sama (tiap node = satu proses di port berbeda, komunikasi lewat TCP socket di `localhost`).

Skeleton yang disediakan (`src/node.py`) sudah menangani bagian **infrastruktur jaringan** (membuka socket, menerima & mengirim pesan antar node) — bagian **algoritma Bully sendiri sengaja dikosongkan** (`# TODO`), karena itu inti pembelajaran tugas ini.

### Aturan Bully Algorithm yang harus diimplementasikan

1. Node yang mendeteksi leader tidak merespons (atau saat start pertama kali) mengirim pesan `ELECTION` ke semua node dengan ID **lebih besar** darinya.
2. Jika ada node ber-ID lebih besar yang merespons `OK`, node yang memulai election **berhenti mencalonkan diri** dan menunggu pesan `COORDINATOR`.
3. Jika **tidak ada** node ber-ID lebih besar yang merespons dalam batas waktu tertentu, node tersebut menjadi leader dan mem-broadcast `COORDINATOR` ke semua node lain.
4. Semua node mencatat siapa leader saat ini.

### Cara Menjalankan

Buka 5 terminal terpisah (satu per node):
```bash
python3 src/node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
python3 src/node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
python3 src/node.py --id 3 --port 5003 --peers 5001,5002,5004,5005
python3 src/node.py --id 4 --port 5004 --peers 5001,5002,5003,5005
python3 src/node.py --id 5 --port 5005 --peers 5001,5002,5003,5004
```

### Skenario Wajib Diuji & Dicatat

1. **Start normal**: nyalakan node 1–5 hampir bersamaan, catat siapa yang terpilih jadi leader (harusnya node ber-ID tertinggi, yaitu node 5).
2. **Leader mati**: matikan (Ctrl+C) proses node leader (node 5), amati node lain mendeteksi leader hilang dan memicu election baru. Catat leader baru yang terpilih (harusnya node 4).
3. Simpan log terminal (screenshot atau `> log_nodeX.txt` redirect) dari kedua skenario ke folder `bukti/`.

## Struktur Submission

```
tugas-05-koordinasi-konsensus/
├── README.md      # Analisis: kenapa perlu leader, kenapa Bully (vs Raft), hasil 2 skenario
├── JURNAL.md
├── src/
│   └── node.py
└── bukti/          # Log/screenshot skenario start normal & leader mati
```

## Rubrik Penilaian (Tugas 5)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi Bully Algorithm benar | 35% | Election, OK, COORDINATOR message bekerja sesuai aturan algoritma |
| Bukti skenario leader mati → re-election | 30% | Log jelas menunjukkan leader baru terpilih otomatis |
| Analisis (kenapa perlu leader, trade-off Bully vs Raft) | 20% | Dikaitkan ke masalah urutan pesanan di skenario FoodGo |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI tentang gambaran umum algoritma election; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/node.py` (logika `on_message`, `start_election`, `declare_leader`, `monitor_leader`). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menjelaskan kenapa Bully Algorithm selalu memilih node ber-ID tertinggi yang masih hidup, dan apa kelemahannya dibanding algoritma lain (mis. jumlah pesan yang dikirim saat election, single point of failure sebelum leader baru terpilih) — bukan sekadar definisi generik.
