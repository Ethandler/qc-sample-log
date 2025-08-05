# scripts/collision_demo.py
import threading
from app.allocator import reserve

def reserve_ids(material: str, qty: int, results: list):
    ids = reserve(material, qty)
    results.extend(ids)

def main():
    material = "concrete"
    qty_per_thread = 5
    num_threads = 2
    threads = []
    results = []

    for _ in range(num_threads):
        t = threading.Thread(target=reserve_ids, args=(material, qty_per_thread, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("All reserved IDs:")
    for sid in results:
        print(" ", sid)

    if len(results) != len(set(results)):
        print("❌ Duplicate IDs detected!")
    else:
        print("✅ No collisions — allocator is thread-safe.")

if __name__ == "__main__":
    main()
