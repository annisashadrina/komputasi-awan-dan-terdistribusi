# Tugas 3 (Pekan 3) — Efisiensi Proses & Kontainer

**Materi terkait:** Threading, Virtualization, Containers.

**Kelompok:** [Nama Kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| Annisa Nur Shadrina | 103072400134 | Implementasi Multithreading & Analisis Efisiensi Proses (No. 1) |
| Fadia Nabila Shifa | 103072400066 | Analisis Teknis Race Condition & Perbaikan Lock (No. 2) |
| Aryo Abdillah Ainnurrofiq | 103072400006 | Konfigurasi Dockerfile & Pengujian Kontainer (No. 3 & 4) |

## Studi Kasus

Server FoodGo boros sumber daya karena setiap permintaan pesanan masuk diproses sebagai **proses baru yang berat** (mis. `fork()` proses OS penuh per request). Saat 100 pesanan masuk bersamaan, server kehabisan memori karena tiap proses membawa overhead-nya sendiri.

## Tugas Kelompok

1. Implementasikan **simulasi pesanan masuk** di Python (`src/order_simulator.py`) yang memproses banyak pesanan **secara konkuren memakai multithreading** (bukan multiprocessing, bukan sekuensial biasa).

**Jawab :**
**A. Implementasi Arsitektur Konkurensi (`src/order_simulator.py`)**
- Simulasi dirancang untuk menangani `NUM_ORDERS = 100` pesanan yang didistribusikan ke `NUM_WORKERS = 10` worker thread secara konkuren.
- Daftar order (`order_ids = list(range(1, 101))`) dibagi secara merata menjadi 10 partisi/chunk (masing-masing 10 pesanan per worker).
- Setiap chunk ditugaskan ke sebuah thread mandiri menggunakan modul standard library `threading.Thread(target=worker, args=(chunk,))`.
- Semua thread dimulai secara bersamaan menggunakan metode `.start()`, lalu fungsi utama menunggu seluruh thread menyelesaikan tugasnya menggunakan `.join()` sebelum melakukan verifikasi agregasi hasil akhir pada counter bersama (`processed_count`).

**B. Analisis Efisiensi: Mengapa Multithreading (Bukan Proses Berat OS / Multiprocessing)?**
Mengaitkan kembali ke studi kasus di mana server FoodGo kehabisan memori akibat setiap pesanan diproses sebagai proses OS penuh (`fork()`):

1. **Efisiensi Alokasi & Berbagi Memori (Shared Memory Space vs. Isolated Address Space):**
   - **Model Lama (OS Process / Fork):** Pada model pembuatan proses OS penuh (`fork()`), sistem operasi mengalokasikan ruang alamat virtual (*isolated address space*) yang terpisah untuk setiap proses baru. Tiap proses membawa struktur data OS tersendiri: *Process Control Block (PCB)*, tabel file descriptor, page table, serta duplikasi runtime environment. Ketika 100 pesanan masuk serentak, tercipta 100 proses OS terpisah yang masing-masing mengonsumsi memori belasan hingga puluhan megabyte, sehingga memicu *memory exhaustion* dan *Out of Memory (OOM) Killer*.
   - **Model Baru (Multithreading):** Seluruh 10 worker thread berjalan di dalam **satu proses OS yang sama** dan saling berbagi segmen memori yang sama (*code segment*, *global data*, dan *heap space*). Setiap thread hanya membutuhkan struktur minimal berupa *Thread Control Block (TCB)* dan alokasi call stack pribadi yang relatif sangat kecil (hanya beberapa kilobyte). Overhead memori untuk menangani 100 pesanan turun drastis hingga lebih dari 90% dibandingkan pendekatan *fork()*.

2. **Overhead Pergantian Konteks (Context Switching Cost):**
   - **Process Context Switch:** Pergantian antar-proses membutuhkan intervensi kernel tingkat tinggi, pergantian *page directory*, pengosongan cache virtual memory (*TLB - Translation Lookaside Buffer flush*), serta invalidasi cache CPU L1/L2. Hal ini menghabiskan banyak siklus komputasi CPU hanya untuk urusan pergantian konteks.
   - **Thread Context Switch:** Karena seluruh thread berada dalam ruang alamat memori yang sama, CPU tidak perlu melakukan *flush* pada TLB atau mengubah tabel pemetaan memori virtual. Pergantian konteks antar-thread berlangsung jauh lebih cepat dan ringan, sehingga utilisasi CPU benar-benar difokuskan untuk memproses logika pesanan.

3. **Karakteristik Beban Kerja (I/O-Bound vs CPU-Bound):**
   - Proses transaksi pesanan makanan pada FoodGo (validasi pesanan, kalkulasi total, pemanggilan API payment, dan notifikasi mitra) pada dasarnya adalah operasi yang bersifat **I/O-Bound** (disimulasikan dengan `time.sleep()`).
   - Pada operasi I/O-bound di Python, multithreading sangat efektif. Ketika suatu thread masuk ke kondisi tunggu I/O (seperti menunggu respons jaringan atau disk), thread tersebut secara sukarela melepaskan *Global Interpreter Lock (GIL)*, sehingga thread lain dapat langsung dieksekusi oleh interpreter tanpa tertahan. Ini memberikan konkurensi nyata tanpa memerlukan beban berat dari *multiprocessing*.

---

2. Program harus mensimulasikan **race condition yang sengaja dibuat lalu diperbaiki** — buktikan pemahaman kalian tentang `Lock`/sinkronisasi dengan cara:
   - Jalankan dulu versi TANPA lock, tunjukkan hasil counter yang salah (screenshot/log).
   - Perbaiki dengan `threading.Lock()`, tunjukkan hasil counter yang benar.
   - Tulis perbandingan ini di `JURNAL.md`.

**Jawab :**
**A. Mekanisme Terjadinya Race Condition (Analisis Tingkat Bytecode Python)**
- Masalah inkonsistensi data terjadi pada variabel global bersama: `processed_count`.
- Dalam kode Python, operasi penambahan counter tampak seperti satu baris sederhana:
  ```python
  processed_count += 1
  ```
- Namun, di tingkat *Python Virtual Machine (bytecode)*, operasi ini **bukan operasi atomik (non-atomic)**. Operasi tersebut dipecah menjadi 4 tahapan instruksi CPU/interpreter:
  1. `LOAD_GLOBAL (processed_count)` : Membaca nilai variabel dari memori heap ke evaluation stack thread.
  2. `LOAD_CONST (1)` : Memuat konstanta angka 1 ke stack.
  3. `BINARY_OP (+)` : Menjumlahkan kedua nilai di stack.
  4. `STORE_GLOBAL (processed_count)` : Menuliskan kembali hasil penjumlahan dari stack ke variabel global di memori.

- **Skenario Tabrakan Data (*Lost Update*):**
  Ketika 10 thread berjalan bersamaan tanpa sinkronisasi, *context switch* dapat terjadi di antara instruksi `LOAD_GLOBAL` dan `STORE_GLOBAL`:
  1. Misalkan nilai `processed_count` saat ini adalah **50**.
  2. **Thread 1** membaca nilai **50** (`LOAD_GLOBAL`). Tepat setelah itu, giliran CPU Thread 1 habis atau berpindah (*context switch*).
  3. **Thread 2** masuk dan membaca nilai `processed_count` yang masih bernilai **50**.
  4. **Thread 2** menambahkan nilai menjadi **51** lalu menyimpannya kembali ke memori global (`STORE_GLOBAL`).
  5. Giliran berpindah kembali ke **Thread 1**. Thread 1 melanjutkan instruksinya dengan nilai lama yang sudah dimuat (50), menambahkan 1 menjadi **51**, lalu menuliskan **51** ke memori.
  6. **Dampak:** Dua pesanan nyata telah selesai diproses oleh dua worker berbeda, tetapi nilai counter hanya bertambah satu. Terjadi *lost update* berulang kali selama simulasi, sehingga hasil akhir `processed_count` meleset jauh dari 100 (misalnya hanya tercatat 80–90).

**B. Mekanisme Perbaikan dengan `threading.Lock()` (Mutual Exclusion / Mutex)**
- Untuk memperbaiki kondisi di atas, area modifikasi variabel bersama didefinisikan sebagai **Critical Section** yang dilindungi oleh objek `threading.Lock()`.
- Implementasi dilakukan dengan membungkus operasi increment menggunakan context manager:
  ```python
  with lock:
      processed_count += 1
  ```
- **Cara Kerja:**
  - Metode `with lock` secara otomatis memanggil `lock.acquire()` saat masuk dan `lock.release()` saat keluar (bahkan jika terjadi error/exception).
  - Objek lock menerapkan prinsip **Mutual Exclusion (Mutex)**: hanya ada satu thread yang diizinkan memegang kunci kepemilikan lock dalam satu waktu.
  - Jika Thread 1 sedang berada di dalam blok `with lock:`, maka Thread 2 hingga Thread 10 yang mencoba mengakses kode tersebut akan dipaksa menunggu (*blocked*) hingga Thread 1 selesai dan melepaskan lock.
  - Hal ini menjamin bahwa seluruh rangkaian instruksi *Read-Modify-Write* dieksekusi secara terisolasi dan atomik, mencegah *lost update*, serta menjamin total pesanan terhitung tepat **100 dari 100 pesanan**.

**C. Ringkasan Perbandingan Hasil Eksekusi**
| Skenario | Mekanisme Sinkronisasi | Hasil `processed_count` | Status Sistem |
|---|---|---|---|
| **Sebelum Perbaikan** | Tanpa Lock (`processed_count += 1` langsung) | `< 100` (sering kali bernilai acak ~70 s.d. ~95) | `RACE CONDITION TERDETEKSI` (Terjadi lost update) |
| **Sesudah Perbaikan** | Menggunakan `with lock:` (`threading.Lock()`) | **Tepat 100** | Sukses konsisten (Semua order tercatat akurat) |

*(Log rincian eksperimen dicatat pada `JURNAL.md` dan bukti tangkapan layar terminal disimpan pada folder `bukti/`)*

---

3. Paketkan program ke dalam **Docker container** (`Dockerfile` disediakan skeleton-nya, lengkapi bagian yang kosong).

**Jawab :**
**A. Konfigurasi `Dockerfile` yang Diimplementasikan**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["python3", "src/order_simulator.py"]
```

**B. Rationale & Best Practice Desain Kontainer**
1. **Pemilihan Base Image (`python:3.11-slim`):**
   - Menggunakan varian resmi Debian-slim (`3.11-slim`) yang memiliki footprint memori sangat kecil (~150 MB) dibandingkan image Python default yang ukurannya mencapai >1 GB karena membawa compiler C/C++ yang tidak diperlukan.
   - Varian *slim* tetap membawa *glibc* standar Linux yang menjamin stabilitas dan kompatibilitas penuh dengan modul threading Python (berbeda dengan varian Alpine yang berbasis `musl` libc yang terkadang menimbulkan kendala alokasi stack pada eksekusi multithread).
2. **Efisiensi Layer Caching:**
   - Baris `COPY requirements.txt .` dan `RUN pip install ...` diletakkan sebelum penyalinan source code `src/`. Hal ini memastikan bahwa layer instalasi dependensi akan di-*cache* oleh Docker engine. Ketika terjadi perubahan kode pada `src/order_simulator.py`, Docker tidak perlu mengulang proses `pip install`, sehingga proses build ulang berlangsung instan.
3. **Optimasi Image Size (`--no-cache-dir`):**
   - Menambahkan flag `--no-cache-dir` pada perintah `pip install` untuk mencegah file cache package tersimpan di layer kontainer, menjaga ukuran image tetap ramping.
4. **Instruksi `CMD` (Exec Form):**
   - Ditulis menggunakan sintaks *exec form* `["python3", "src/order_simulator.py"]` agar Python berjalan langsung sebagai PID 1 di dalam namespace kontainer, sehingga proses dapat menerima sinyal OS (*SIGTERM* / *SIGINT*) secara bersih (*graceful shutdown*).

---

4. Jalankan container di laptop, buktikan program tetap berjalan benar di dalam container (screenshot/video di `bukti/`).

**Jawab :**
**A. Langkah Eksekusi Kontainer**
1. **Build Image:**
   ```bash
   docker build -t foodgo-order-sim .
   ```
   Docker berhasil mengunduh base image `python:3.11-slim`, mengeksekusi tahapan instruksi, dan menghasilkan image bernama `foodgo-order-sim:latest`.
2. **Menjalankan Kontainer:**
   ```bash
   docker run --rm foodgo-order-sim
   ```
   Flag `--rm` digunakan agar kontainer otomatis dibersihkan dan dihapus dari memori setelah proses selesai dieksekusi.

**B. Hasil Eksekusi & Validasi**
- Di dalam kontainer Docker, program berhasil mengeksekusi 100 pesanan menggunakan 10 worker thread secara konkuren dan menampilkan output yang sama persis seperti pada host lokal:
  ```text
  Total pesanan diproses: 100 (seharusnya 100)
  ```
- **Kesimpulan:** Implementasi `threading.Lock()` berhasil menjamin keamanan konkurensi data (*thread-safety*) baik di level host OS Windows maupun di dalam lingkungan terisolasi Linux Docker Container.
- Tangkapan layar bukti eksekusi build dan run kontainer disimpan pada file `bukti/03_docker_run_success.png`.


## Skeleton yang Disediakan

- `src/order_simulator.py` — kerangka program dengan `# TODO` di bagian logika inti (worker function, penggunaan lock, agregasi hasil). **Kalian wajib mengisi bagian TODO sendiri** — ini bagian penilaian utama.
- `requirements.txt` — kosong/minimal (program ini sengaja hanya pakai standard library Python, tidak perlu dependency eksternal).
- `Dockerfile` — kerangka dengan beberapa baris `# TODO`, lengkapi agar image bisa di-build dan dijalankan.

## Cara Menjalankan (Setelah Skeleton Dilengkapi)

Tanpa Docker (langsung di laptop, untuk debugging cepat):
```bash
cd tugas-03-multithreading-container
python3 src/order_simulator.py
```

Dengan Docker (wajib untuk submission akhir):
```bash
cd tugas-03-multithreading-container
docker build -t foodgo-order-sim .
docker run --rm foodgo-order-sim
```

## Struktur Submission

```
tugas-03-multithreading-container/
├── README.md          # Analisis: race condition, perbaikan, kenapa threading (bukan multiprocessing/proses OS)
├── JURNAL.md           # Log sebelum/sesudah lock, error yang ditemui saat build Docker
├── Dockerfile
├── requirements.txt
├── src/
│   └── order_simulator.py
└── bukti/              # Screenshot/video: hasil counter salah (tanpa lock), hasil benar (dengan lock), container jalan
```

## Rubrik Penilaian (Tugas 3)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi multithreading benar | 30% | Worker benar-benar konkuren (bukan `time.sleep` yang menyamarkan sekuensial), pakai `threading` |
| Bukti race condition & perbaikan lock | 25% | Ada bukti nyata (log/screenshot) sebelum & sesudah, bukan cuma klaim di teks |
| Dockerfile & eksekusi container | 20% | Image ter-build, container jalan dan hasilkan output yang sama seperti tanpa Docker |
| Analisis (kenapa threading, bukan proses berat) | 15% | Mengaitkan balik ke masalah "server boros resource" di studi kasus |
| Proses & kontribusi kelompok | 10% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI soal opsi umum menangani race condition (mis. "apa saja cara sinkronisasi thread di Python"); **tidak boleh** meminta AI menuliskan isi bagian `# TODO` di `order_simulator.py`/`Dockerfile`. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Bagian `# TODO` di `order_simulator.py` dan `Dockerfile` sengaja dikosongkan — solusi yang identik persis antar kelompok (termasuk nama variabel, komentar) akan diperiksa lebih lanjut.
- `JURNAL.md` wajib menunjukkan bukti nyata percobaan **sebelum** (race condition muncul) dan **sesudah** (`Lock()` dipasang) — bukan cuma klaim tanpa data pembanding.
