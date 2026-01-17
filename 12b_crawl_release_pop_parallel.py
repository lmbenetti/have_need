import discogs_client, time, gzip, sys, requests
import pandas as pd
from lxml import etree
from datetime import datetime

def print_current_datetime():
    now = datetime.now()
    print(now.strftime("%d-%m %H:%M"))
    
def count_lines_in_file(filename):
    with open(filename, 'r') as file:
        return sum(1 for line in file)

total = count_lines_in_file('ids_todo_lisandro.txt')
count = 0


# client = discogs_client.Client(
#    "",
#    consumer_key = "iufWvgIynwXXrgQaruCy",
#    consumer_secret = "AYCpGkIlmZVBabEbnwiihDZvfIuphkDn",
#    token = u"WZRCRDqNMpLSbcVqQUyiIhrlaIWRgESiaIKvdpqj",
#    secret = u""
# )

# client.get_authorize_url()
# code = "cJCXKxTxSE"
# client.get_access_token('cJCXKxTxSE')

TOKEN = open("token.txt").read().strip()

client = discogs_client.Client(
    "MyDiscogsApp/1.0",
    user_token=TOKEN
)

try:
    identity = client.identity()
    print("Connected as:", identity.username)
except Exception as e:
    print("Not connected:", e)
    

already_done = set(pd.read_csv("releases_have_want.tsv", sep = '\t')["release"])
last_printed_pct = -1.0
with open("ids_todo_lisandro.txt", 'r') as fin, open("releases_have_want.tsv", 'a') as fout:
    for line in fin:
        count += 1
        
		 
        pct = round((count / total) * 100, 2)
        if pct != last_printed_pct:
            print_current_datetime()
            print(f"{pct:.2f}% done ({count}/{total})")
            last_printed_pct = pct
            
        release_id = int(line.strip())
        if release_id not in already_done:
            try:
                release = client.release(release_id).community
                fout.write(f"{release_id}\t{release.have}\t{release.want}\n")
                fout.flush()
            except ValueError:
                fout.write(f"{release_id}\t0\t0\n")
                fout.flush()
            except discogs_client.exceptions.HTTPError:
                fout.write(f"{release_id}\t0\t0\n")
                fout.flush()
            except requests.exceptions.ConnectionError:
                time.sleep(10)
                continue
            time.sleep(1)

