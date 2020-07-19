import pandas as pd
import re
ip = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
status = re.compile(r" \b\d\d\d\b ")
with open('/root/mydata/access_log', 'r') as file:
    ipList = []
    statusList = []
    for line in file.readlines():
        ipaddr = ip.findall(line)
        scode = status.findall(line)
        if ipaddr and scode:
            ipList.append(ipaddr[0])
            statusList.append(scode[0])
        else:
            pass

col1 = pd.DataFrame(ipList, columns=['ClientIP'])
col2 = pd.DataFrame(statusList, columns=['Status_code'])

dataset = pd.concat([col1, col2], axis=1)

dataset.to_csv('webserverlog.csv', index=False)
