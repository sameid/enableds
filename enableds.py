import requests
import json
import time as t
import os

print 'enableds - running'

cert ='cacert.pem'
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.getcwd(), cert)

config = open('./config.json').read()
config = json.loads(config)

current_milli_time = lambda: int(round(t.time() * 1000))

start = current_milli_time()

HOST = 'https://app.klipfolio.com/api/1'
USERNAME = config['user']
PASSWORD = config['pass']

try:
    CLIENT_ID = config['cid']
    print 'Client ID was provided, retrieving all datasources'
except KeyError:
    CLIENT_ID = None
    print 'No Client ID provided, retrieving all datasources'

def get(req, host = HOST):
    res = requests.get(host+req, auth=(USERNAME,PASSWORD), verify=False)  
    return res.json()

##def put(req, data, headers, host=HOST):
##    res = requests.put(host+req, auth=(USERNAME, PASSWORD), data=json.dumps(data),headers=headers, verify=False )
##    return res.json()
            
def post(req, host=HOST):
    res = requests.post(host+req, auth=(USERNAME,PASSWORD), verify=False)  
    return res.json()

def delete(req, host=HOST):
    res = requests.delete(host+req,auth=(USERNAME,PASSWORD), verify=False)
    return res.json()

def pprint(data, sort=True):
    print ((json.dumps(data, sort_keys=sort, indent=2, separators=(',', ': '))))
    return;

if CLIENT_ID:
    req = get('/datasources?client_id='+CLIENT_ID)
else:
    req = get('/datasources')
s
##pprint(req)
ds = req['data']['datasources']

print 'Enabling and Refreshing Datasources ...'
for i in ds:
    _id = i['id']
    data = get('/datasources/'+_id+'?full=true')
    if (data['meta']['success'] == True):
        data = data['data']
        if data['is_dynamic'] == True:
            t.sleep(0.01)
        else:
            ds_instances = get('/datasource-instances?datasource_id='+_id)['data']['instances']
            for j in ds_instances:
                if (j['refresh_fail_count'] > 0):
                    pprint(j)
                    pprint(data)       
                    post('/datasources/'+_id+'/@/enable')
                    post('/datasources/'+_id+'/@/refresh')
                    t.sleep(0.01)        
        
end = current_milli_time()
delta = (end - start)/1000
print '... Done!'
print "Script took " + str(delta) + " seconds"
