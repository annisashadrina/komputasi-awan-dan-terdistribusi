B. SEQUENCE DIAGRAM URUTAN KOMUNIKASI END-TO=END
![gambar](../diagram/DIAGRAM%20URUTAN%20KOMUNIKASI.drawio.png)
Kenapa alurnya dibuat seperti ini ?
Ada alasan untuk membedakan komunikasi sinkron dan asinkron
1. Pesanan minta data menu (sinkron) : karena pesanan perlu tau "apakah menu tersedia dan berapa harganya?"
2. Pesanan minta pembayaran (sinkron) : karena pesanan perlu ngedapetin hasil pembayaran sebelum nentuin status pembayaran
3. Pesanan melakukan "OrderPaid" (asinkron) : sesudah pembayaran di konfirmasi , informasi bisa disampaikan tanpa nunggu seluruh layanan lain selesai
4. Resto menerima "OrderPaid" (asinkron) : resto bisa memproses pesanan secara terpisah
5. Kurir menerima "Order-Ready" (asinkron) : kurir bisa ditugaskan setelah restoran memberitahu pesanan siap

