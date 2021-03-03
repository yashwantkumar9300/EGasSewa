import requests
import json

def sendASMS(contactno = "9691060747",message="Sorry Message not Available"):

    url = "https://www.fast2sms.com/dev/bulk"

    payload = "sender_id=FSTSMS&message="+message+"&language=english&route=p&numbers="+contactno


    headers = {
        'authorization': "5fAEdmWwujGsPCKHQTaM1YShV8ODxqycg9NBZv3zbeFrp7IinLsS162wBjUHecp3qzmyIFxEAKuNa7Jg",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)

    return json.loads(response.text)