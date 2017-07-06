#creating a program that accepts strings of http request and parses it and performs actions
#the job management module

import time
from collections import deque
from random import randint




class Job:
    def __init__(self, id):
        self.id = id
        self.status = None
        self.t = None
        self.starttime = None
        self.endtime = None
        self.remainingtime = None

class Response:
    def __init__(self):
        self.response_message = None
        self.job_id = None
        self.status = None

class Request:
    def __init__(self,request_method,request_uri):
        self.request_method = request_method
        self.request_uri = request_uri



class Server:

    def __init__(self,capacity,jobtime):
        self.capacity = capacity#max no of jobs that will be running at a time
        self.jobs={}
        self.ids=[]
        self.running = []
        self.queue=deque([])
        self.paused=[]
        self.jobtime = jobtime

    def createJob(self):
        # create a job object with a unique random id

        new_id = randint(0,1000)
        while new_id in self.ids:
            print 'regenerating id as id '+str(new_id)+' exists '
            new_id = randint(0,1000)

        self.ids.append(new_id)

        a_job = Job(new_id)
        a_job.t= self.jobtime
        return a_job


    def put(self):
        # check if no of running jobs < capacity
        # assign RUNNING to the job status and add it to running list
        # else assign QUEUED to the job and add it to the queue

        a_job = self.createJob()

        # if theres space for a job in the server
        if len(self.running) < self.capacity:
            a_job.status = "RUNNING"
            a_job.starttime = time.time()
            a_job.endtime = time.time() + a_job.t
            self.running.append(a_job)

        else:
            # add the job to the queue
            a_job.status = "QUEUED"
            self.queue.append(a_job)

        #add the job in a dictionary to maintain records by id
        self.jobs[a_job.id] = a_job
        #response object that must contain "STATUS 200 " and job id, status
        response = Response()
        response.response_message="STATUS 200"
        response.job_id=a_job.id
        response.status=a_job.status

        return response


    def get(self,request_uri):
        #parse through the uri to get the id
        inp = request_uri
        a = inp.split('<')
        b = a[1].split('>')
        id = int(b[0])

        response = Response()
        if id in self.ids:
            response.response_message = "STATUS 200"
            response.job_id=id
            response.status=self.jobs[id].status

        else:
            response.response_message="STATUS 404"


        return response


    def delete(self,request_uri):
        inp = request_uri
        a = inp.split('<')
        b = a[1].split('>')
        id = int(b[0])

        response = Response()

        #if id not found
        if id not in self.ids:
            response.response_message="STATUS 404"
        elif id in self.ids and (self.jobs[id].status==("SUCCESSFUL" or "FAILED")):
            response.response_message="STATUS 403"
            response.job_id=id
            response.status=self.jobs[id].status
        else:
            the_job = self.jobs[id]
            response.response_message="STATUS 200"

            if the_job.status == "DELETED":
                response.status="DELETED"
                response.job_id=the_job.id

            elif the_job.status=="RUNNING":
                the_job.status="DELETED"
                self.running.remove(the_job)

                response.job_id = the_job.id
                response.status = "DELETED"

            elif the_job.status=="PAUSED":
                the_job.status="DELETED"
                #remove from wherever it was stored
                self.paused.remove(the_job)

                response.job_id = the_job.id
                response.status = "DELETED"

            elif the_job.status=="QUEUED":

                the_job.status=="DELETED"
                self.jobs[the_job.id].status = "DELETED"
                if the_job in self.queue:
                    self.queue.remove(the_job)
                response.job_id = the_job.id
                response.status = "DELETED"


        return response

    def post(self,request_uri):
        inp = request_uri
        a = inp.split('<')
        b = a[1].split('>')
        id = int(b[0])
        c = a[2].split('>')
        posttype = c[0]

        response = Response()
        st = self.jobs[id].status
        if posttype=='pause':
            if id not in self.ids:
                response.response_message = "STATUS 404"

            elif id in self.ids and ( st== "SUCCESSFUL" or st== "FAILED" or st== "QUEUED" or st== "DELETED"):
                response.response_message = "STATUS 403"
                response.job_id = id
                response.status = self.jobs[id].status
            else:
                the_job = self.jobs[id]
                response.response_message="STATUS 200"

                if the_job.status=="RUNNING":
                    the_job.status="PAUSED"
                    the_job.remainingtime = the_job.endtime - time.time()

                    self.running.remove(the_job)
                    self.paused.append(the_job)
                    self.jobs[id].status = "PAUSED"
                    self.jobs[id].remainingtime = the_job.remainingtime


                    response.job_id=the_job.id
                    response.status=the_job.status

                elif the_job.status=="PAUSED":
                    response.job_id = the_job.id
                    response.status = the_job.status

        elif posttype=='resume':

            if id not in self.ids:
                response.response_message = "STATUS 404"
            elif id in self.ids and (self.jobs[id].status == ("SUCCESSFUL" or "FAILED" or "QUEUED" or "DELETED")):
                response.response_message = "STATUS 403"
                response.job_id = id
                response.status = self.jobs[id].status
            else:
                the_job = self.jobs[id]
                response.response_message="STATUS 200"

                if the_job.status=="RUNNING":
                    response.job_id=the_job.id
                    response.status=the_job.status

                elif the_job.status=="PAUSED":
                    the_job.status="RUNNING"
                    the_job.endtime = time.time()+the_job.remainingtime

                    self.jobs[the_job.id].status = "RUNNING"
                    self.jobs[the_job.id].endtime = the_job.endtime
                    self.paused.remove(the_job)
                    self.running.append(the_job)


                    response.job_id = the_job.id
                    response.status = the_job.status

        return response








#ONLY TO TEST THIS MODULE , DOESNT RUN WHEN CLIENT SERVER PROGRAMS ARE RUNNING AND CALLING THIS MODULE
if __name__=="__main__":



    #inputstring = raw_input()
    #inputs = inputstring.split(' ')
    #methodname = inputs[0]


    server = Server(4,10)
    response1 = server.put()
    print response1.response_message
    print response1.job_id,response1.status
    print

    print 'TEST PUT METHOD'

    for i in range(10):
        response2 = server.put()
        print response2.response_message,response2.job_id, response2.status
        print

    print
    print
    print 'ALL JOBS'
    for jobid in server.jobs:
        print server.jobs[jobid].id,server.jobs[jobid].status
        print



    print 'TEST GET METHOD'
    inputstring = raw_input()
    inputs = inputstring.split(' ')
    request_method = inputs[0]
    request_uri = inputs[1]
    print request_method
    print request_uri

    get_response=server.get(request_uri)
    print get_response.response_message, get_response.job_id,get_response.status

    print
    todelete = False
    if todelete == True:
        print 'TEST DELETE METHOD'

        for i in range(3):
            print
            print 'TEST DELETE METHOD'
            inputstring = raw_input()
            inputs = inputstring.split(' ')
            request_method = inputs[0]
            request_uri = inputs[1]
            print request_method
            print request_uri

            delete_response = server.delete(request_uri)
            print delete_response.response_message,delete_response.job_id,delete_response.status

        print
        print 'ALL JOBS'
        for jobid in server.jobs:
            print server.jobs[jobid].id, server.jobs[jobid].status
            print

        print
        print 'Queue'
        for obj in server.queue:
            print obj.id , obj.status

        print
        print 'Running'
        for r in server.running:
            print r.id, r.status

            print



#GET /job/<2>
#DELETE /job/<3>


    for i in range(3):
        print
        print 'TEST POST METHOD'
        inputstring = raw_input()
        inputs = inputstring.split(' ')
        request_method = inputs[0]
        request_uri = inputs[1]
        print request_method
        print request_uri

        post_response = server.post(request_uri)
        print post_response.response_message,post_response.job_id,post_response.status

    print
    print 'ALL JOBS'
    for jobid in server.jobs:
        print server.jobs[jobid].id, server.jobs[jobid].status
        print

    print
    print 'PAUSED'
    for obj in server.queue:
        print obj.id , obj.status

    print
    print 'Running'
    for r in server.running:
        print r.id, r.status

    for i in range(3):
        print
        print 'TEST POST METHOD'
        inputstring = raw_input()
        inputs = inputstring.split(' ')
        request_method = inputs[0]
        request_uri = inputs[1]
        print request_method
        print request_uri

        post_response = server.post(request_uri)
        print post_response.response_message,post_response.job_id,post_response.status

    print
    print 'ALL JOBS'
    for jobid in server.jobs:
        print server.jobs[jobid].id, server.jobs[jobid].status
        print

    print
    print 'PAUSED'
    for obj in server.queue:
        print obj.id , obj.status

    print
    print 'Running'
    for r in server.running:
        print r.id, r.status

    for i in range(3):
        print
        print 'TEST POST METHOD'
        inputstring = raw_input()
        inputs = inputstring.split(' ')
        request_method = inputs[0]
        request_uri = inputs[1]
        print request_method
        print request_uri

        post_response = server.post(request_uri)
        print post_response.response_message,post_response.job_id,post_response.status

    print
    print 'ALL JOBS'
    for jobid in server.jobs:
        print server.jobs[jobid].id, server.jobs[jobid].status
        print

    print
    print 'PAUSED'
    for obj in server.queue:
        print obj.id , obj.status

    print
    print 'Running'
    for r in server.running:
        print r.id, r.status

