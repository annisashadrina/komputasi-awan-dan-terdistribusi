
"""Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)
Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        # TODO 1: tambahkan node_id -> node_ip ke self.nodes.
        if node_id in self.nodes:
            print(f"[INFO] Node '{node_name}' sudah ada.")
            return

        # TODO 2: cari successor LAMA dari node_id ini (successor sebelum node
        # baru bergabung, gunakan find_successor() dengan node_id INI dikecualikan
        # dulu dari self.nodes saat mencari).
        old_successor = None
        if self.nodes:
            old_successor = self.find_successor(node_id)

        old_successors = {}
        for key_hash in self.data:
            if self.nodes:
                old_successors[key_hash] = self.find_successor(key_hash)

        self.nodes[node_id] = node_ip

        # TODO 3: pindahkan semua key di self.data yang seharusnya menjadi
        # tanggung jawab node baru (key dengan hash <= node_id, tapi masih
        # dipegang oleh successor lama) ke bawah tanggung jawab node baru.
        # (Untuk simulasi sederhana, cukup print log siapa mengambil alih apa -
        # tidak perlu benar-benar memindahkan struktur data kompleks.)
        print(f"[TODO] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        for key_hash, previous_node in old_successors.items():
            new_successor = self.find_successor(key_hash)

            if new_successor == node_id:
                print(
                    f"[TRANSFER] Data hash {key_hash} "
                    f"berpindah dari node {previous_node} ke node {node_id}"
                )

        if old_successor is not None:
            print(
                f"[INFO] Successor lama node baru: {old_successor}"
            )

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)

        # TODO 4: hapus node_id dari self.nodes.
        if node_id not in self.nodes:
            print(f"[INFO] Node '{node_name}' tidak ditemukan.")
            return

        affected_keys = []
        for key_hash in self.data:
            if self.find_successor(key_hash) == node_id:
                affected_keys.append(key_hash)

        del self.nodes[node_id]

        # TODO 5: cari successor BARU untuk tiap key yang tadinya dipegang
        # node ini, pindahkan ke successor tersebut.
        if self.nodes:
            for key_hash in affected_keys:
                new_successor = self.find_successor(key_hash)
                print(
                    f"[TRANSFER] Data hash {key_hash} "
                    f"berpindah dari node {node_id} "
                    f"ke node {new_successor}"
                )
        else:
            print("[INFO] Ring kosong. Tidak ada successor.")

        print(f"[TODO] Node '{node_name}' (id={node_id}) keluar dari ring")

    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        # TODO 6: implementasikan logika successor di atas menggunakan
        # self.nodes.keys(). Kembalikan node_id (bukan IP).
        if not self.nodes:
            raise ValueError("Ring belum memiliki node.")

        sorted_nodes = sorted(self.nodes.keys())

        for node_id in sorted_nodes:
            if node_id >= key_hash:
                return node_id

        return sorted_nodes[0]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        # TODO 7: panggil find_successor(key_hash) untuk menentukan node
        # penanggung jawab, lalu simpan (kurir_id, ip_kurir) ke self.data[key_hash].
        responsible_node = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)

        print(
            f"[REGISTER] {kurir_id} (hash={key_hash}) "
            f"disimpan pada node {responsible_node}"
        )

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        # TODO 8: gunakan find_successor(key_hash) untuk menemukan node
        # penanggung jawab, lalu kembalikan ip_kurir dari self.data jika ada.
        responsible_node = self.find_successor(key_hash)
        result = self.data.get(key_hash)

        if result is None or result[0] != kurir_id:
            return None

        return result[1]


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Daftarkan beberapa kurir
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    # Data pengujian untuk membuktikan transfer ketika node bergabung.
    # Hash dicari secara otomatis pada rentang 102 sampai 123.
    join_test_id = next(
        (
            f"kurir-uji-join-{i}"
            for i in range(10000)
            if hash_id("node-jakarta-2") < hash_id(f"kurir-uji-join-{i}")
            <= hash_id("node-medan-1")
        ),
        None
    )

    if join_test_id is not None:
        ring.register_kurir(join_test_id, "192.168.1.99")

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    # Data pengujian untuk membuktikan transfer ketika node keluar.
    # Hash dicari pada rentang 136 sampai 177.
    leave_test_id = next(
        (
            f"kurir-uji-leave-{i}"
            for i in range(10000)
            if hash_id("node-surabaya-1") < hash_id(f"kurir-uji-leave-{i}")
            <= hash_id("node-jakarta-1")
        ),
        None
    )

    if leave_test_id is not None:
        ring.register_kurir(leave_test_id, "192.168.1.100")

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()
