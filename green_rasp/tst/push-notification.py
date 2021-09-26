import requests
import json
import pickle


def read_pickle_file(fn):
    with open(fn, 'rb') as handle:
        val = pickle.load(handle)
    return val

fn = '/home/pi/key/one_sig_creds.pickle'
creds = read_pickle_file(fn)

header = {"Content-Type": "application/json; charset=utf-8",
          "Authorization": creds['authorization']}

payload = {"app_id": creds['app_id'],
           "included_segments": ["Subscribed Users"],
           "contents": {"en": "Water Sprinkler Switched On"}, "headings": {"en": "💦"}, "priority": 10}
 
req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
 
print(req.status_code, req.reason)
