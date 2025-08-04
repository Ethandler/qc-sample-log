# tests/test_allocator.py
import threading
from app.allocator import reserve

def test_concurrent_reservation():
    results = []

    def worker():
        ids = reserve("concrete", 5)
        results.extend(ids)

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for t in threads: t.start()
    for t in threads: t.join()

    assert len(set(results)) == 10, "Duplicate IDs detected"
