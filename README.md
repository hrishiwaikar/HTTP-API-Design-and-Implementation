# HTTP-API-Design-and-Implementation
Wrote the HTTP protocol from scratch and designed and implemented it as an api in a Client Server Architecture


I have implemented the http protocol from scratch .  I have simulated the use of the api by building client-server architecture , where in the client  sends http request (eg PUT /job) to the server using tcp socket library . The server manages certiain jobs and their lifecycle using multithreading.

The server receives the request and based on it calls corresponding method PUT/DELETE/POST/GET which are defined inside the Server class in mainserver module.
The generated response by the method is sent back to the client . (Note: client and server are run on two different terminals)

Finally , a separate thread manages the Job lifecycle by constantly checking for change of state of running threads and transferring jobs from queue to running state.


1. There are three modules - mainserver.py , server.py and client.py

--mainserver.py  -  Contains the class Server which contains defined http methods - get, put, delete , post as per requirements in assignment. All the datastructures for creating managing the jobs lifecycle are also here
Inside __name__==__main__ : code for testing and debugging the http functions exists

 	--server.py - hosts the server on localhost and contains multhreaded functions for hosting the server and simultaneously manage the job life cycle like changing from running to successful after job completion .

-client.py - sends request to the server via the network and seeks response from the server


Attachments also contain different output files showcasing how the code is run and generates output for different http methods.


IMPLEMENTATION of CODE :
   How to run :

1. Open new terminal . Run server.py
		- Enter N - max no. of jobs
- Enter t - time of each job
The server is running on localhost:10025(you can change the port in the code)

    
 2.  Open another new terminal , Run client.py
		-Enter the correct server url which is : http://localhost:10025/
		-The client gets connected to the server
		-Keep entering Http request uri’s as mentioned in the assignment
		eg
			-PUT /job
			-GET /job/<5>
			-DELETE /job/<5>
			And POST 
		-You will see response per request from the server on the client screen
	
    
    


