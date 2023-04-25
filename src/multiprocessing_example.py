import multiprocessing
import time

def initialize_pool(pool_global: multiprocessing.Queue):
	global pool_buffer
	pool_buffer = pool_global

def process(value: int) -> None:
	# time.sleep(0.0000001)
	pool_buffer.put(value)

def show() -> None:
	while True:
		if pool_buffer.empty():
			continue
		value = pool_buffer.get()
		if value is None:
			break
		print(f"value: {value}")

if __name__ == "__main__":
	pool_buffer = multiprocessing.Queue()
	pool = multiprocessing.Pool(processes=6, initializer=initialize_pool, initargs=(pool_buffer,))

	show_task_future = pool.apply_async(func=show, args=(), callback=None, error_callback=None)

	bigg_num: int = 1000
	counter: int = 0

	futures = []
	while counter <= bigg_num:
		f = pool.apply_async(func=process, args=(counter,), callback=None, error_callback=None)
		futures.append(f)
		# time.sleep(0.0025)
		counter += 1

	for f in futures:
		f.get()

	pool_buffer.put(None)
	show_task_future.get()

	print("[DONE]")