"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    # TODO 1: buat ServerProxy ke http://localhost:8000
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

    try:
        print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
        start = time.time()
        # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
        #         (buktikan client BENAR-BENAR menunggu sampai server membalas)
        saldo = proxy.cek_saldo("user1")
        durasi = time.time() - start
        print(f"Saldo user1: {saldo} (waktu tunggu: {durasi:.4f} detik)")

        print("\nMemanggil proses_pembayaran('user1', 20000) ...")
        # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya
        hasil = proxy.proses_pembayaran("user1", 20000)
        print(f"Hasil pembayaran: {hasil}")

        # Cek saldo setelah pembayaran
        saldo_terbaru = proxy.cek_saldo("user1")
        print(f"Saldo user1 setelah pembayaran: {saldo_terbaru}")

        # Percobaan pembayaran yang melebihi saldo
        print("\nMemanggil proses_pembayaran('user1', 50000) ...")
        hasil_gagal = proxy.proses_pembayaran("user1", 50000)
        print(f"Hasil pembayaran: {hasil_gagal}")

    except ConnectionRefusedError:
        print("\nError: Koneksi ke RPC server gagal (server belum aktif atau mati).")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
