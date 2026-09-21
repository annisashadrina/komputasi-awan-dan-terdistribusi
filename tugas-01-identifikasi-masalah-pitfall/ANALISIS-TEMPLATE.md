# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Annisa Nur Shadrina] | [103072400134] | [semua modul berebut resource yang sama] |
| [Fadia Nabila Shifa] | [103072400066] | [pitfall/bagian yang dikerjakan] |
| [Aryo Abdillah Ainnurrofiq] | [103072400006] | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: [semua modul berebut resource yang sama] — ditulis oleh [Annisa N Shadrina]

**Bukti di skenario:** Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama

**Kenapa ini keliru:** Dari kalimat tersebut, yang menarik menurut saya bukan cuma servernya "kewalahan", tetapi kenapa satu peningkatan traffic bisa membuat beberapa bagian sistem ikut terdampak, walaupun sebenarnya belum tentu semua modul sedang sibuk dengan tingkat yang sama
sebelum traffic meningkat, sistemnya yang kami lihat seperti ini :
user - foodgo server, lalu membawahi order, payment, dan notification. yang menyebabkan ketiga fungsi itu berada dalam satu server dan satu proses, jadi foofgo belum memisahkan resource untuk masing-masing fungsi


**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
