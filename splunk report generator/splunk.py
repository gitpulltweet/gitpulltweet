import splunklib.client as client
from time import sleep
import sys
import json
from pprint import pprint
HOST = {"<<key identifier>>":"<<Splunk host ip/hostname>>"}
PORT = 8089
USERNAME = "<<splunk username>>"
PASSWORD = "<<Splunk password>>"

docm1={}
for key, value in HOST.items():
        #print key
        # Create a Service instance and log in
        service = client.connect(
                host=value,
                port=PORT,
                username=USERNAME,
                password=PASSWORD)

        docm={}
        mysavedsearch = service.saved_searches["<<saved report name>>"]
        job = mysavedsearch.dispatch()
        sleep(2)

        while True:
                while not job.is_ready():
                        pass
                stats = {"isDone": job["isDone"],
            "doneProgress": float(job["doneProgress"])*100,
             "scanCount": int(job["scanCount"]),
             "eventCount": int(job["eventCount"]),
             "resultCount": int(job["resultCount"])}
                status = ("\r%(doneProgress)03.1f%%   %(scanCount)d scanned   "
              "%(eventCount)d matched   %(resultCount)d results") % stats

                #sys.stdout.write(status)
                #sys.stdout.flush()
                if stats["isDone"] == "1":
                #sys.stdout.write("\n\nDone!\n\n")
                        break
                sleep(2)



        #print jobresults
        doc = job.results(output_mode="json")


        data = json.load(doc)
        docm['consolidated'] = data['results']
        docm1[key] = docm
print json.dumps(docm1)
