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
from sklearn.manifold import TSNE

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
selected_features = ['skin1', 'skin3']
# selected_features = ['product_brand', 'category', 'harga', 'rating', 'umur', 'skin1', 'skin2', 'skin3','purchase_point']
# selected_features = ['product_brand','skin1', 'category', 'harga']


df_selected = df[selected_features]
print('before',df_selected)
# Convert categorical pakai LabelEncoder and OneHotEncoder
label_encoder = LabelEncoder()
one_hot_encoder = OneHotEncoder(sparse_output=False)
for column in selected_features:
    df_selected.loc[:, column]  = label_encoder.fit_transform(df_selected[column])

# Fit KMeans model
kmeans = KMeans(n_clusters=7, random_state=42, n_init=10, init='k-means++')
df_selected.loc[:,'cluster'] = kmeans.fit_predict(df_selected)

print('cluster center', kmeans.cluster_centers_)
print("Number of iterations:", kmeans.n_iter_)

# Distance to Cluster
features_for_clustering = df_selected.drop('cluster', axis=1)
inertia = -kmeans.score(features_for_clustering)
print('Score',inertia)

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
color = ['red', 'green','blue','yellow','purple','pink','orange','black','grey','brown']
df_selected.loc[:,'color'] = df_selected['cluster'].map(lambda p: color[p])
plt.figure(figsize=(10,10))
plt.scatter(
    df_selected['skin1'], 
    df_selected['skin3'], 
    c=df_selected['color'])
# plt.scatter(centroids[:,0],centroids[:,1], c='green',s=250)
plt.xlabel('skin1')
plt.ylabel('skin3')
plt.title('Clustering Visualisation Skin1 and Skin3')
plt.show()


# Visualisasi TSNE 2D
tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300, init='random')
tsne_result = tsne.fit_transform(df_selected.drop('cluster', axis=1).drop('color', axis=1).drop('labels', axis=1))
plt.figure(figsize=(10,8))
plt.scatter(tsne_result[:,0], tsne_result[:,1], c=df_selected['cluster'], cmap='viridis', alpha=0.5)
plt.colorbar()
plt.show()