"""
Tugas 4 - Jalur A: RPC Server (simulasi modul Pembayaran)
Memakai xmlrpc.server dari Python standard library - tidak perlu install apa pun.
"""

from xmlrpc.server import SimpleXMLRPCServer

# Simulasi "database" saldo user
saldo_user = {
    "user1": 50000,
    "user2": 120000,
}


def cek_saldo(user_id: str) -> float:
    """Kembalikan saldo user_id saat ini."""
    # TODO 1: kembalikan saldo dari dict `saldo_user`.
    # Jika user_id tidak ada, kembalikan 0.0
    if user_id in saldo_user:
        print(f"Cek saldo {user_id}: {saldo_user[user_id]}", flush=True)
        return float(saldo_user[user_id])
    print(f"User {user_id} tidak ditemukan", flush=True)
    return 0.0


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    """Kurangi saldo user sejumlah `jumlah`. Kembalikan status hasil."""
    # TODO 2: validasi saldo cukup, kurangi saldo_user[user_id], dan kembalikan
    # dict berisi minimal {"status": "sukses"/"gagal", "saldo_akhir": ...}
    if user_id not in saldo_user:
        return {"status": "gagal", "pesan": "user tidak ditemukan", "saldo_akhir": 0.0}

    if saldo_user[user_id] < jumlah:
        print(f"Pembayaran gagal: saldo {user_id} tidak cukup ({saldo_user[user_id]} < {jumlah})", flush=True)
        return {
            "status": "gagal",
            "pesan": "saldo tidak cukup",
            "saldo_akhir": float(saldo_user[user_id]),
        }

    saldo_user[user_id] -= jumlah
    print(f"Pembayaran berhasil: {user_id} bayar {jumlah}, sisa saldo {saldo_user[user_id]}", flush=True)
    return {
        "status": "sukses",
        "saldo_akhir": float(saldo_user[user_id]),
    }


def main():
    # TODO 3: buat SimpleXMLRPCServer di localhost port 8000,
    # daftarkan fungsi cek_saldo & proses_pembayaran, lalu serve_forever().
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    server.register_function(cek_saldo, "cek_saldo")
    server.register_function(proses_pembayaran, "proses_pembayaran")

    print("RPC server modul Pembayaran berjalan di port 8000...", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dimatikan.", flush=True)


if __name__ == "__main__":
    main()
