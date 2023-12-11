import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import silhouette_score
import itertools
import json
import os

# Assuming df is your dataframe with the data
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

features = ['product_brand', 'category', 'harga', 'rating', 'umur', 'skin1', 'skin2', 'skin3', 'purchase_point']

# Generate all possible combinations with a minimum length of 2
all_combinations = []
for r in range(3, len(features) + 1):
    combinations_r = itertools.combinations(features, r)
    all_combinations.extend(combinations_r)

max_silhouette_score = float('-inf')
best_feature_combination = None

for feature_combination in all_combinations:
    selected_features = list(feature_combination)
    
    df_selected = df[selected_features]

    # Convert categorical using LabelEncoder
    label_encoder = LabelEncoder()
    for column in df_selected.select_dtypes(include=['object']).columns:
        df_selected.loc[:, column] = label_encoder.fit_transform(df_selected[column])

    # Convert 'harga' to numeric (remove 'Rp.' and convert to float)
    if 'harga' in df_selected.columns:
        df_selected.loc[:, 'harga'] = df_selected['harga'].replace('[^\d]+', '', regex=True).astype(float)

    # Normalize numeric columns
    numerical_features = df_selected.select_dtypes(include=['float64']).columns
    if numerical_features.size > 0:
        scaler = StandardScaler()
        df_selected.loc[:, numerical_features] = scaler.fit_transform(df_selected.loc[:, numerical_features])

    # Fit KMeans model
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10, init='k-means++')
    df_selected.loc[:, 'cluster'] = kmeans.fit_predict(df_selected)

    # Evaluate with Silhouette Score
    labels = kmeans.labels_
    current_silhouette_score = silhouette_score(df_selected, labels)

    if current_silhouette_score > max_silhouette_score:
        max_silhouette_score = current_silhouette_score
        best_feature_combination = selected_features

# Print the best feature combination and its silhouette score
print("Best Feature Combination:", best_feature_combination)
print("Max Silhouette Score:", max_silhouette_score)