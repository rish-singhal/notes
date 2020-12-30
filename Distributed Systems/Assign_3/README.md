## Distributed System Assignment - 4

Author: Rishabh Singhal    
Roll No: 20171213


- Basic Input, Output 
	This is implemented by taking the input as a string from the INPUT file, and then it is splitted on the basis of " " & "\n" character is removed, further list of integers in form of string is obtained (for e.g. ["0", "1", "-1"] ), then it is converted into [ 0, 1, -1] by some inbuilt function and send back to the main function. i.e. "start".


- Question1 " Ring of Processes "
    For this question -
	1. First N number of processes are spawned and each one is assigned MyID i.e. 0,1,2..
	   ( and each process calls a function nodefun with argmuments as MyID).
	2. Then for passing the token once along complete ring, array of PID ( Process Ids) of N 
Processes is transformed into pairs of PIDS i.e. { PID1, PID2 } where PID1 is the sender of the token, and PID2 is the receiver of the token.
	3. Then to start the message starting process, a function is called to init the message passing, and sends message to "Process 0", so it can start passing messages to the next PID in the ring.
	4. Once a token is recieved by the current Process, it passes to the next Process in the ring, and the count of total number of message passes ( CNT ) is decremented each time.
	5. At last, when Process 0 inturn recieves the from Nth node, CNT becomes 0 and last message is printed and further passing of tokens is stopped.



- Question2 " Parallel Merge Sort"
    For this question - 
	1. Firstly, the main function spawns a process " main process" and calls msort ( mergesort implementation ) with parameter as the array given ( obtained after parsing input file).
	2. Now, in the implementation of msort (mergesort function), base condition is added, such that if the size of the array "list in erlang" is <= 1, then directly return the array.
	3. If it is >= 1, then the array is split into 2 subarrays, first half and the right half.
	4. In the implementation of split function " it is done reccursively ", by passing the length to split on & array.
	5. Then, 2 processes are spawned, one for the left array and other for the right array.
	6. After they are done with processing of the array, 2 arrays are recieved " each sorted ", one left and the other.
	7. After this, merge function is called " which is also implemented reccursively",
	[ mergefun/2, mergefun/3 ]. mergefun/2 for the initializing the result array " or merge array" to be returned to "[]" ( empty ) and then in mergefun/3, first element of both the arrays are checked and the one having lesser value is appended to the result array and, the function is again called
	8. There are 3 instances for 3 conditions for merging i.e (A,[]), ([], B), ([],[]), after first processing is done and atleast one array is empty.
	9. Now, for printing the list element into output file, a recursive function is implemented " namely 'print' ", which goes through each array element one by one.

For Complexity Part, there is a time constant for spawning a process, and as non-parallel merge sort works in O(nlogn), in this case as the 2 processes run concurrently one for each left and right array before merge, it should be O(N), merge function is also O(N), and split function too.

So, complexity -> O( const\*(Process Spawn) + N )

where N = size of the array.  
