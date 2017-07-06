import socket
import sys
import struct
import time
from mainserver import Server
import threading

server = None

class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

lock = threading.Lock()


def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data




def manage_jobs():
    #1. When job starts running - thats starttime , endtime = st +10
    #2. If job is paused , calculate remaining time . Transfer the job from paused to running
    #3. When job is resumed ,calculate remaining time and therefore the endtime . and put it from paused to running
    #4. Loop through all the jobs in running list and if current time exceeds a job's endtime , it is SUCCESSFUL
    global server
    while True:
        time.sleep(server.jobtime - 1)
        currenttime=time.time()
        removelist =[]
        with lock:

            for job in server.running:
                if currenttime>=job.endtime:
                    job.status="SUCCESSFUL"
                    removelist.append(job)
                    server.jobs[job.id].status = "SUCCESSFUL"

            #removing the jobs in removelist from running list
            for job in removelist:
                server.running.remove(job)

            #transferring from queue to running until len of running =N
            while(len(server.running)<server.capacity and len(server.queue)>0):
                    a_job = server.queue.popleft()
                    server.running.append(a_job)









def host_server():
    # Create a TCP/IP socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 10025)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)


    # Listen for incoming connections
    sock.listen(1)

    global server
    while True:
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()

        try:
            print >> sys.stderr, 'connection from', client_address

            # Receive the data
            data = recv_msg(connection)
            print >> sys.stderr, 'received "%s"' % data
            print
            # PROCESS THE MESSAGE FROM CLIENT HERE

            inputstring = data
            inputs = inputstring.split(' ')
            request_method = inputs[0]
            request_uri = inputs[1]
            print request_method
            print request_uri

            #TEST PUT
            if request_method=='PUT':
                print 'PUT Method'
                with lock:
                    print 'Inside put with lock'
                    response = server.put()
                print response.response_message
                print response.job_id, response.status
                print
            #TEST GET
            if request_method=='GET':
                print 'GET METHOD'
                with lock:
                    response = server.get(request_uri)
                print response.response_message, response.job_id, response.status
                print

            if request_method=='DELETE':
                with lock:
                    response = server.delete(request_uri)
                print response.response_message, response.job_id, response.status
                print

            if request_method=='POST':
                with lock:
                    response = server.post(request_uri)
                print response.response_message, response.job_id, response.status
                print


                # CREATE RESPONSE IN msg
            response_string = str(response.response_message)+'  job id = '+str(response.job_id)+' job status = '+str(response.status)
            msg = response_string
            send_msg(connection,msg)

        finally:
            # Clean up the connection
            connection.close()
            print 'Closing connection'


def main():
    global server
    print 'Enter Server Specification'
    N = int(raw_input('N (max no. of running jobs): '))
    t  = int(raw_input('Time per job : '))


    server = Server(N,t)
    hostservercode = Thread(host_server)
    managejobscode = Thread(manage_jobs)


if __name__ == '__main__':
    main()

