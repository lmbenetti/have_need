import discogs_client, time, gzip, sys, requests
import pandas as pd
from lxml import etree


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

with open("ids_todo_lisandro.txt", 'r') as fin, open("releases_have_want.tsv", 'a') as fout:
    for line in fin:
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

