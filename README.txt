Tutorials : https://docs.google.com/document/d/1eFaPnQ1HBrncs7NnMOq4V3Q6qHB00jyYjGvJojYuV44/edit

Observations :
------------
1. If you are not visualizing data, don't use PCA i.e it doesn't make sense to reduce the dimensions of data to, say, 2 when you don't want to visualize data

Miscellaneous :
--------------
1. Assume you are remotely logged-in to a server with SSH and training an ML model in the Server. Unfortunately, your SSH connection gets disconnected, which will result in the termination of model training. How to make that process (model training) to run in background irrespective of the SSH connection?
	python train.py > out.txt &
	jobs
	disown -a
	jobs

2. See how much CPU percentage your processes are using (100% ~ 1 whole CPU or 1 whole core)
	top -n 1| grep katari | awk '{print $9}' | awk '{s=s+$1}END{print s}'
