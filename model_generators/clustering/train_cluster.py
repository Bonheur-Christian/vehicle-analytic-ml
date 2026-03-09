import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
import joblib
import numpy as np
from sklearn.decomposition import PCA

# Use engineered features for better clustering
df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")

# Feature engineering: create meaningful features that increase separation
df['price_to_income_ratio'] = df['selling_price'] / (df['estimated_income'] + 1)
df['age'] = 2024 - df['year']  # Vehicle age
df['km_per_year'] = df['kilometers_driven'] / (df['age'] + 1)
df['luxury_score'] = (df['seating_capacity'] * 10 + df['selling_price'] / 10000)

SEGMENT_FEATURES = [
    "estimated_income", 
    "selling_price", 
    "price_to_income_ratio",
    "km_per_year",
    "seating_capacity",
    "luxury_score"
]

# Remove any rows with missing values or infinite values
df = df.dropna(subset=SEGMENT_FEATURES)
df = df[~df[SEGMENT_FEATURES].isin([np.inf, -np.inf]).any(axis=1)]

X = df[SEGMENT_FEATURES].copy()

# Use MinMaxScaler for better outlier handling with engineered features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA with more components to capture more variance
pca = PCA(n_components=4, random_state=42)
X_pca = pca.fit_transform(X_scaled)

print(f"PCA Explained Variance Ratio: {pca.explained_variance_ratio_}")
print(f"Cumulative Variance: {sum(pca.explained_variance_ratio_):.4f}\n")

# Find optimal number of clusters
best_silhouette = -1
best_k = 2
silhouette_scores = []
davies_bouldin_scores = []
best_k_range = range(2, 7)

for k in best_k_range:
    # Increased iterations and initialization attempts
    kmeans_temp = KMeans(n_clusters=k, random_state=42, n_init=100, max_iter=1000, algorithm='elkan')
    labels_temp = kmeans_temp.fit_predict(X_pca)
    
    sil_score = silhouette_score(X_pca, labels_temp)
    db_score = davies_bouldin_score(X_pca, labels_temp)
    
    silhouette_scores.append(sil_score)
    davies_bouldin_scores.append(db_score)
    
    print(f"k={k}: Silhouette={sil_score:.4f}, Davies-Bouldin={db_score:.4f}")
    
    if sil_score > best_silhouette:
        best_silhouette = sil_score
        best_k = k

# Train the final model with optimal k using PCA-transformed data
print(f"\nOptimal number of clusters: {best_k}")
print(f"Best Silhouette Score: {round(best_silhouette, 4)}")

# Final training
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=100, max_iter=1000, algorithm='elkan')
df["cluster_id"] = kmeans.fit_predict(X_pca)

# For mapping, calculate cluster centers in original feature space
cluster_centers_income = []
for i in range(best_k):
    cluster_data = df[df["cluster_id"] == i]
    avg_income = cluster_data["estimated_income"].mean()
    cluster_centers_income.append((i, avg_income))

# Sort clusters by income
sorted_clusters = sorted(cluster_centers_income, key=lambda x: x[1])
sorted_cluster_ids = [c[0] for c in sorted_clusters]

# Create mapping based on number of clusters
if best_k == 2:
    cluster_mapping = {
        sorted_cluster_ids[0]: "Economy",
        sorted_cluster_ids[1]: "Premium",
    }
elif best_k == 3:
    cluster_mapping = {
        sorted_cluster_ids[0]: "Economy",
        sorted_cluster_ids[1]: "Standard",
        sorted_cluster_ids[2]: "Premium",
    }
elif best_k == 4:
    cluster_mapping = {
        sorted_cluster_ids[0]: "Economy",
        sorted_cluster_ids[1]: "Standard",
        sorted_cluster_ids[2]: "Premium",
        sorted_cluster_ids[3]: "Luxury",
    }
else:
    # For other k values, create generic names
    cluster_mapping = {sorted_cluster_ids[i]: f"Segment_{i+1}" for i in range(best_k)}

df["client_class"] = df["cluster_id"].map(cluster_mapping)

# Save models
joblib.dump(kmeans, "model_generators/clustering/clustering_model.pkl")
joblib.dump(scaler, "model_generators/clustering/scaler.pkl")
joblib.dump(pca, "model_generators/clustering/pca.pkl")

silhouette_avg = round(silhouette_score(X_pca, df["cluster_id"]), 4)

print(f"\nFinal Silhouette Score: {silhouette_avg}")
if silhouette_avg >= 0.9:
    print("✅ Excellent clustering quality achieved!")
elif silhouette_avg >= 0.7:
    print("⚠️ Good clustering quality achieved")
elif silhouette_avg >= 0.5:
    print("ℹ️ Fair clustering quality")
else:
    print("⚠️ Clustering quality needs improvement")

# Calculate Coefficient of Variation (CV) for each cluster
def calculate_cv(data):
    """Calculate coefficient of variation: (std / mean) * 100"""
    # Handle edge cases (zero or negative means)
    if data.mean() == 0 or data.mean() < 0:
        return 0
    return (data.std() / abs(data.mean())) * 100

# Use original features for CV calculation (not engineered ones)
ORIGINAL_FEATURES = ["estimated_income", "selling_price", "year", "kilometers_driven", "seating_capacity"]

cluster_summary = df.groupby("client_class")[ORIGINAL_FEATURES].agg(['mean', 'std', 'count'])
cluster_summary.columns = ['_'.join(col).strip() for col in cluster_summary.columns.values]

# Calculate CV for each feature in each cluster
cv_data = []
for cluster in sorted(df["client_class"].unique()):
    cluster_data = df[df["client_class"] == cluster][ORIGINAL_FEATURES]
    cv_row = {"Segment": cluster}
    for feature in ORIGINAL_FEATURES:
        cv = calculate_cv(cluster_data[feature])
        cv_row[f"{feature}_CV"] = cv
    cv_data.append(cv_row)

cv_df = pd.DataFrame(cv_data)

# Calculate overall CV for the entire dataset
overall_cv_data = []
for feature in ORIGINAL_FEATURES:
    cv = calculate_cv(df[feature])
    overall_cv_data.append({
        "Metric": feature,
        "Coefficient of Variation (%)": cv
    })

overall_cv_df = pd.DataFrame(overall_cv_data)

# Calculate overall CV across all features
overall_mean_cv = overall_cv_df["Coefficient of Variation (%)"].mean()
overall_cv_df.loc[len(overall_cv_df)] = {
    "Metric": "Overall",
    "Coefficient of Variation (%)": overall_mean_cv
}

cluster_counts = df["client_class"].value_counts().reset_index()
cluster_counts.columns = ["client_class", "count"]
cluster_summary = df.groupby("client_class")[ORIGINAL_FEATURES].mean()
cluster_summary = cluster_summary.merge(cluster_counts, on="client_class")

comparison_df = df[["client_name", "estimated_income", "selling_price", "client_class"]].copy()

def evaluate_clustering_model():
    return {
        "silhouette": silhouette_avg,
        "best_k": best_k,
        "silhouette_history": silhouette_scores,
        "davies_bouldin_history": davies_bouldin_scores,
        "cv_by_cluster": cv_df.to_html(
            classes="table table-bordered table-striped table-sm",
            float_format="%.2f",
            justify="center",
            index=False,
        ),
        "overall_cv": overall_cv_df.to_html(
            classes="table table-bordered table-striped table-sm",
            float_format="%.2f",
            justify="center",
            index=False,
        ),
        "summary": cluster_summary.to_html(
            classes="table table-bordered table-striped table-sm",
            float_format="%.2f",
            justify="center",
            index=False,
        ),
        "comparison": comparison_df.head(10).to_html(
            classes="table table-bordered table-striped table-sm",
            float_format="%.2f",
            justify="center",
            index=False,
        ),
    }