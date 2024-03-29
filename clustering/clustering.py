import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import plotly.graph_objs as go
import plotly as py

data_dict = []

## GET DATA
json_file_path = '../scrape_result_fix.json'
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data_dict = json.load(json_file)
    print("Successfully loaded JSON data.")
else:
    print(f"Error: JSON file not found at {json_file_path}. Please check the file path.")

## PREPROCESSING
df = pd.DataFrame(data_dict)
# selected_features = ['product_brand', 'category', 'harga', 'rating', 'umur', 'skin1', 'skin2', 'skin3', 'purchase_point']
selected_features = ['product_brand','skin1', 'category', 'harga']


df_selected = df[selected_features]
print('before',df_selected)
# Convert categorical pakai LabelEncoder and OneHotEncoder
label_encoder = LabelEncoder()
one_hot_encoder = OneHotEncoder(sparse_output=False)
for column in ['product_brand', 'skin1','category']:
    df_selected.loc[:, column]  = label_encoder.fit_transform(df_selected[column])

# Convert 'harga' to jadi angka (hapus 'Rp.' dan convert to float)
df_selected.loc[:,'harga'] = df_selected['harga'].replace('[^\d]+', '', regex=True).astype(float)
print('harga', df_selected['harga'])
# Normalize column angka
numerical_features = ['harga']
scaler = StandardScaler()
df_selected.loc[:, numerical_features] = scaler.fit_transform(df_selected.loc[:, numerical_features])
print('after2',df_selected)


# Fit KMeans model
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_selected.loc[:,'cluster'] = kmeans.fit_predict(df_selected)

print('cluster center', kmeans.cluster_centers_)
print("Number of iterations:", kmeans.n_iter_)

# Distance to Cluster
features_for_clustering = df_selected.drop('cluster', axis=1)
inertia = -kmeans.score(features_for_clustering)
print('Score',inertia)

# CLuster count
print('skin 1',df_selected['cluster'].value_counts())
cluster_2_rows = df_selected[df_selected['skin1'] == 0]
print('skin1 ',cluster_2_rows)

# Evaluatin with Silhoutte Score (Jumlah K Paling bagus)
labels = kmeans.labels_
print(silhouette_score(df_selected,labels))
silhoutte = {}
for k in range(2,8):
    km = KMeans(n_clusters=k, max_iter=1000, random_state=42, n_init=10)
    km.fit(df_selected)
    silhoutte[k] = silhouette_score(df_selected, km.labels_)
sns.pointplot(x=list(silhoutte.keys()), y=list(silhoutte.values()))
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Score")
plt.title('Silhouette Score for Optimal K')
plt.show()

## Visualisasi Cluster 2D
centroids = kmeans.cluster_centers_
print(centroids)
color = ['red', 'green', 'blue']
df_selected.loc[:,'color'] = df_selected['cluster'].map(lambda p: color[p])
plt.figure(figsize=(10,10))
plt.scatter(
    df_selected['product_brand'], 
    df_selected['skin1'], 
    c=df_selected['color'])
# plt.scatter(centroids[:,2],centroids[:,3], c='green',s=250)
plt.show()

# Visualisasi Cluster 3D
labels = kmeans.labels_
centroids = kmeans.cluster_centers_
df_selected.loc[:,'labels'] = labels
trace = go.Scatter3d(
    x = df_selected['product_brand'],
    y = df_selected['skin1'],
    z = df_selected['category'],
    mode = 'markers',
    marker=dict(color=df_selected['labels'], size=5, line=dict(color=df_selected['labels'], width=12), opacity=0.8)
)
data = [trace]
layout = go.Layout(
    title = 'Clusters',
    scene = dict(
        xaxis = dict(title='product_brand'),
        yaxis = dict(title='skin1'),
        zaxis = dict(title='category')
    )
)
fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig)
plt.show()
print('done')