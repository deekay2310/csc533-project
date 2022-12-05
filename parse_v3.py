
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

CLEANR = re.compile('<.*?>')
table_list = list()
key_regex = {"Cloudinary": "cloudinary://.*", "Firebase URL": ".*firebaseio\.com",
             "Slack Token": "(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
             "RSA private key": "-----BEGIN RSA PRIVATE KEY-----",
             "SSH (DSA) private key": "-----BEGIN DSA PRIVATE KEY-----",
             "SSH (EC) private key": "-----BEGIN EC PRIVATE KEY-----",
             "PGP private key block": "-----BEGIN PGP PRIVATE KEY BLOCK-----",
             "Amazon AWS Access Key ID": "AKIA[0-9A-Z]{16}",
             "Amazon MWS Auth Token": "amzn\\.mws\\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
             "AWS API Key": "AKIA[0-9A-Z]{16}",
             "Facebook Access Token": "EAACEdEose0cBA[0-9A-Za-z]+",
             "Facebook OAuth": "[f|F][a|A][c|C][e|E][b|B][o|O][o|O][k|K].*['|\"][0-9a-f]{32}['|\"]",
             "GitHub": "[g|G][i|I][t|T][h|H][u|U][b|B].*['|\"][0-9a-zA-Z]{35,40}['|\"]",
             "Generic API Key": "[a|A][p|P][i|I][_]?[k|K][e|E][y|Y].*['|\"][0-9a-zA-Z]{32,45}['|\"]",
             "Generic Secret": "[s|S][e|E][c|C][r|R][e|E][t|T].*['|\"][0-9a-zA-Z]{32,45}['|\"]",
             "Google API Key": "AIza[0-9A-Za-z\\-_]{35}",
             "Google Cloud Platform API Key": "AIza[0-9A-Za-z\\-_]{35}",
             "Google Cloud Platform OAuth": "[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com",
             "Google Drive API Key": "AIza[0-9A-Za-z\\-_]{35}",
             "Google Drive OAuth": "[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com",
             "Google (GCP) Service-account": "\"type\": \"service_account\"",
             "Google Gmail API Key": "AIza[0-9A-Za-z\\-_]{35}",
             "Google Gmail OAuth": "[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com",
             "Google OAuth Access Token": "ya29\\.[0-9A-Za-z\\-_]+",
             "Google YouTube API Key": "AIza[0-9A-Za-z\\-_]{35}",
             "Google YouTube OAuth": "[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com",
             "Heroku API Key": "[h|H][e|E][r|R][o|O][k|K][u|U].*[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}",
             "MailChimp API Key": "[0-9a-f]{32}-us[0-9]{1,2}",
             "Mailgun API Key": "key-[0-9a-zA-Z]{32}",
             "Password in URL": "[a-zA-Z]{3,10}://[^/\\s:@]{3,20}:[^/\\s:@]{3,20}@.{1,100}[\"'\\s]",
             "PayPal Braintree Access Token": "access_token\\$production\\$[0-9a-z]{16}\\$[0-9a-f]{32}",
             "Picatic API Key": "sk_live_[0-9a-z]{32}",
             "Slack Webhook": "https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}",
             "Stripe API Key": "sk_live_[0-9a-zA-Z]{24}",
             "Stripe Restricted API Key": "rk_live_[0-9a-zA-Z]{24}",
             "Square Access Token": "sq0atp-[0-9A-Za-z\\-_]{22}",
             "Square OAuth Secret": "sq0csp-[0-9A-Za-z\\-_]{43}",
             "Twilio API Key": "SK[0-9a-fA-F]{32}",
             "Twitter Access Token": "[t|T][w|W][i|I][t|T][t|T][e|E][r|R].*[1-9][0-9]+-[0-9a-zA-Z]{40}",
             "Twitter OAuth": "[t|T][w|W][i|I][t|T][t|T][e|E][r|R].*['|\"][0-9a-zA-Z]{35,44}['|\"]"
}
match_list = list()
secret_type_list = list()

data = pd.read_csv('newdata.csv')
for url in data['URL']:
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    table = soup.find('table', attrs={
        'class': 'highlight tab-size js-file-line-container js-code-nav-container js-tagsearch-file'})
    table = re.sub(CLEANR, '', str(table))
    table = re.sub('\n', '', str(table))
    table_list.append(table)

for i in table_list:
    #n = 0
    match = False
    secret_type = 'None'
    for key, val in key_regex.items():
        # print(re.compile(val).search(i))
        if re.compile(val).search(i):
            match = True
            secret_type = key
            continue
            #print(n)
            #print(True)
        #else:
            #print(n)
            #print(False)
        #n += 1
    match_list.append(match)
    secret_type_list.append(secret_type)

data['Match'] = match_list
data['Secret Type'] = secret_type_list
# print(len(table_list))
# print(len(match_list))
# print(len(secret_type_list))
data.to_csv('newdata_matched_with_secret_type.csv', sep='\t', encoding='utf-8')
#url = "https://github.com/apple/turicreate/blob/8896becacde63dd1f27db6d18e8a4025e9b9c50c/deps/src/openssl-1.0.2t/demos/sign/key.pem"
