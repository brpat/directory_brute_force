import requests
import sys
import time
import threading
import queue


found_dir = queue.Queue()


def main():
	event = threading.Event()
	directory_queue = queue.Queue()
	dir_list = open_dir_file(sys.argv[3])

	for directory in dir_list:	
		directory_queue.put(directory)
	start_time = time.time()
	for i in range(0, 10):
		t = threading.Thread(target=make_requests, args=(sys.argv[1],sys.argv[2],directory_queue, event))
		t.start()
	
	
	time_thread = threading.Thread(target=finish_function, args=(start_time,event))
	time_thread.start()
	time_thread.join()

	
#input function. Takes in 3 arguments: IP, Port, List of directories
def make_requests(ip,port,dir_queue, event):
	while not dir_queue.empty():
		send_get(ip, port, dir_queue.get())
	event.set()


def send_get(ip, port, directory):
	global found_dir
	
	#print(directory, end='')
	response = requests.get(f'http://{ip}:{port}/{directory.strip()}')
	if response.status_code == 200:
		found_dir.put(directory)
	

def finish_function(start_time, event):
	'''Print out time taken after brute force is done'''

	event.wait()
	stop_time = time.time()
	print(f"Time taken = {stop_time - start_time}")

	while not found_dir.empty():
		print(f"Found: {found_dir.get()}")
	event.clear()


#Opens the input files 
def open_dir_file(input_list):
    dir_list = open(input_list)
    return dir_list


if __name__ == "__main__":
	main()








