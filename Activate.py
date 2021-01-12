import json
def userpassGetter():
    from getmac import get_mac_address as gma
    import requests
    macAddres = gma().replace(":", "").upper()
    with open("data.json") as f:
        data = json.load(f)
        s = data["API ID"] + data["API Hash"]
    key = s+macAddres

    session = requests.session()
    req = session.get("https://www.dropbox.com/s/ry3jbzsfrgizyb2/Licensekey.txt?dl=0")
    realLink = req.text.split('"htmlified_link": "')[1].split('",')[0]
    req = requests.get(realLink)
    activationKeys = req.text.split('pre><span></span>')[1].split('</pre>')[0].strip()
    if key in activationKeys: #50E085B92120
        return True, ''
    else:
        #return True, ''
        #sys.exit()
        return False, key



