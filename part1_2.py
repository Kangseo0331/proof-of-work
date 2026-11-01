
import hashlib
import time
import csv

T_star = 2433849096262126601305031626558662622707783392882157128131455873201182

class Block:
    def __init__(self, index, prev_hash, data, T):
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.nonce = 0
        self.hash = None
        self.target = T

    def encode(self):
        return (
            f"{self.index}|{self.data}|{self.prev_hash.hex()}|{self.target}|{self.nonce}"
        ).encode("utf-8")

    def calNonce(self):
        trial = 0

        while True:
            hashed_data = hashlib.sha256(self.encode())
            digest = hashed_data.digest()
            H = int.from_bytes(digest, "big")
            trial += 1

            if H < self.target:
                self.hash = digest
                return trial

            self.nonce += 1



times = []
total_trial = 0

with open("part1_2.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["target", "trial0", "trial1", "trial2", "trial3", "trial4", "avg", "total_trial"])

    for i in range(5):

        b = Block(i, bytes(32), i, T_star)

        start = time.perf_counter()
        trial = b.calNonce()
        elapsed = time.perf_counter() - start

        times.append(elapsed)
        total_trial += trial

        print(f"실험 {i + 1}: {elapsed}초, "
              f"hash 횟수 = {trial}")

    avg = sum(times) / len(times)

    writer.writerow([
        T_star, *times, avg, total_trial
    ])

print(f"\navg time: {avg}")
print(f"total_trial: {total_trial}")

