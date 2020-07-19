# Block suspicious IPs using ML clustering and jenkins
Get the suspicious IPs from apache web server log using Machine Learning clustering technique and block those IPs using Jenkins

There are many tools to perform DDoS attack on the webserver. Use one of them and perform DDoS attack on the webserver. Get the log data from the location where it stored. In my case it it in **/var/log/httpd/**. The webserver log file **access_log** will be like this as shown below

![Log file](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/log.png)


### Extract the required features from access_log file and save in csv file
Following is the python script to extract the features from log file and save in csv file

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


Extracted features from log file using above code

![Extracted_features](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/features.png)

### Form clusters of IPs using KMeans clustering and get the suspicious IPs
Following is the code to form clusters of IPs using KMeans clustering and get the suspicious IPs

    # Read data
    import pandas as pd
    dataset = pd.read_csv('/root/mydata/webserverlog.csv')

    # Label data
    from sklearn.preprocessing import LabelEncoder
    x = dataset.iloc[:, :]
    X = x.values
    label = LabelEncoder()
    ips = label.fit_transform(X[:, 0])
    s_code = label.fit_transform(X[:, 1])
    col1 = pd.DataFrame(ips, columns=["ClientIP_label"])
    col2 = pd.DataFrame(s_code, columns=["Status_code_label"])
    labeled_data = pd.concat([col1, col2], axis=1)

    # Scale data
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    scaled_data = sc.fit_transform(labeled_data)

    # Create clusters of data using KMeans
    from sklearn.cluster import KMeans
    model = KMeans(n_clusters=4)
    pred = model.fit_predict(scaled_data)
    scaled_data = pd.DataFrame(scaled_data,
                               columns=["Scaled_ClientIP", "Scaled_Status_code"])
    scaled_data['Cluster'] = pred

    # Get the suspicious ips
    ips = pd.concat([dataset['ClientIP'], labeled_data['ClientIP_label']], axis=1)
    ipFrequency = ips['ClientIP_label'].value_counts()
    res = []
    for i in range(9):
        if ipFrequency[i] > 200:
            res.append(
                ips['ClientIP'].iloc[ips['ClientIP_label'].tolist().index(i)])

    # Save the ips in a file
    with open('/root/mydata/result.txt', 'w') as file:
        file.writelines("%s\n" % l for l in res)
        file.close()

    
IPs found using above code

![IPs found](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/suspiciousIPs.png)


### Automate the things using Jenkins

![Jobs](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/Jobs.png)

#### Job1: Pull the code from Github

![SCM](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/Job11.png)
![Build trigger](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/Job12.png)
![Build](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/Job13.png)

#### Job2: Extract features from webserver access_log

![Build trigger](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/Job21.png)
![Build](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/Job22.png)

#### Job3: Get the suspicious IPS


![Build trigger](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/Job31.png)
![Build](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/Job32.png)

#### Job4: Block IPs


![Build trigger](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/Job41.png)
![Build](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/Job42.png)

IPs blocked by Job4

![Blocked IPs](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/BlockedIPs.png)

This is the build pipeline view of the Jobs

![Pipeline view](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/pipelineview.png)

Check Blocked IP

![Check Blocked IP](https://github.com/surinder2000/Block-suspicious-IPs-using-ML-clustering-and-jenkins/blob/master/Screenshots/TestBlockedIP.png)


### Thank you
