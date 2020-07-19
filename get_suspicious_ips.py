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
