Tutorials : https://docs.google.com/document/d/1eFaPnQ1HBrncs7NnMOq4V3Q6qHB00jyYjGvJojYuV44/edit

Miscellaneous :
--------------
1. Assume you are remotely logged-in to a server with SSH and training an ML model in the Server. Unfortunately, your SSH connection gets disconnected, which will result in the termination of model training. How to make that process (model training) to run in background irrespective of the SSH connection?
	python train.py &> out.txt &
	jobs
	disown -a
	jobs
  Explanation : python train.py > out.txt ===> only redirects the stdout and not the stderr. To redirect both, use &> instead of >.
		<command> & ===> makes the command to run in the background
		disown -a ===> It detaches the processes or jobs from the shell; even if you terminate the shell, the background jobs are not killed
  Note : if you use '>', instead of '&>', whenever the background process throws an error, it tries to print stderr on the terminal (default behaviour); if your terminal is closed (SSH connection is terminated) then the background process is killed immediately.

2. See how much CPU percentage your processes are using (100% ~ 1 whole CPU or 1 whole core)
	top -n 1 | grep katari15 | awk '{print $10}' | awk 'BEGIN{s=0}{s+=$1}END{print s}'
   Explanation : top -n 1 ===>  top runs for 1 iteration
		grep katari15 ===> only those rows are printed which have katari15 in them
		awk '{print $10}' ===> extracts 10th column (Delimiter is " ")
		awk 'BEGIN{s=0}{s=s+$1}END{print s}' ===> Before anything {s=0} is executed. In each iteration, {s=s+$1} is executed. At the end, {print s} is executed
