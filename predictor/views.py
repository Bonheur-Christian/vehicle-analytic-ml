import pandas as pd
from django.shortcuts import render
from predictor.data_exploration import dataset_exploration, data_exploration
from predictor.plotly_dashboards import rwanda_vehicle_map_with_labels, rwanda_district_summary, generate_rwanda_map
import joblib
from model_generators.clustering.train_cluster import evaluate_clustering_model
from model_generators.classification.train_classifier import evaluate_classification_model
from model_generators.regression.train_regression import evaluate_regression_model

# Load models once
regression_model = joblib.load("model_generators/regression/regression_model.pkl")
classification_model = joblib.load("model_generators/classification/classification_model.pkl")
clustering_model = joblib.load("model_generators/clustering/clustering_model.pkl")

def data_exploration_view(request):
    df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")
    
    context = {
        "dataset_exploration": dataset_exploration(df),
        "data_exploration": data_exploration(df),
        "rwanda_map": generate_rwanda_map(df),
        "district_summary": rwanda_district_summary()
    }
    
    return render(request, "predictor/exploratory_data_analysis.html", context)

def regression_analysis(request):
    context = {
        "evaluations": evaluate_regression_model()
    }
    
    if request.method == "POST":
        year = int(request.POST["year"])
        km = float(request.POST["km"])
        seats = int(request.POST["seats"])
        income = float(request.POST["income"])
        
        # Use DataFrame with feature names to avoid sklearn warning
        input_data = pd.DataFrame([[year, km, seats, income]], 
                                  columns=["year", "kilometers_driven", "seating_capacity", "estimated_income"])
        prediction = regression_model.predict(input_data)[0]
        context["price"] = round(prediction, 2)
    
    return render(request, "predictor/regression_analysis.html", context)

def classification_analysis(request):
    context = {
        "evaluations": evaluate_classification_model()
    }
    
    if request.method == "POST":
        year = int(request.POST["year"])
        km = float(request.POST["km"])
        seats = int(request.POST["seats"])
        income = float(request.POST["income"])
        
        # Use DataFrame with feature names to avoid sklearn warning
        input_data = pd.DataFrame([[year, km, seats, income]], 
                                  columns=["year", "kilometers_driven", "seating_capacity", "estimated_income"])
        prediction = classification_model.predict(input_data)[0]
        context["prediction"] = prediction
    
    return render(request, "predictor/classification_analysis.html", context)

def clustering_analysis(request):
    context = {
        "evaluations": evaluate_clustering_model()
    }
    
    if request.method == "POST":
        try:
            import joblib
            from sklearn.preprocessing import MinMaxScaler
            
            year = int(request.POST["year"])
            km = float(request.POST["km"])
            seats = int(request.POST["seats"])
            income = float(request.POST["income"])
            
            # Step 1: Predict price using DataFrame with feature names
            input_data = pd.DataFrame([[year, km, seats, income]], 
                                      columns=["year", "kilometers_driven", "seating_capacity", "estimated_income"])
            predicted_price = regression_model.predict(input_data)[0]
            
            # Step 2: Predict cluster with scaling and engineered features
            try:
                scaler = joblib.load("model_generators/clustering/scaler.pkl")
                pca = joblib.load("model_generators/clustering/pca.pkl")
            except:
                # Fallback if files don't exist
                from sklearn.preprocessing import MinMaxScaler
                from sklearn.decomposition import PCA
                scaler = MinMaxScaler()
                pca = PCA(n_components=4, random_state=42)
            
            # Create engineered features (same as in training)
            age = 2024 - year
            km_per_year = km / (age + 1)
            price_to_income_ratio = predicted_price / (income + 1)
            luxury_score = (seats * 10 + predicted_price / 10000)
            
            # Use the same features as in training
            cluster_input = pd.DataFrame([[income, predicted_price, price_to_income_ratio, 
                                          km_per_year, seats, luxury_score]], 
                                        columns=["estimated_income", "selling_price", "price_to_income_ratio",
                                                "km_per_year", "seating_capacity", "luxury_score"])
            cluster_input_scaled = scaler.transform(cluster_input)
            cluster_input_pca = pca.transform(cluster_input_scaled)
            cluster_id = clustering_model.predict(cluster_input_pca)[0]
            
            # Get cluster mapping from the evaluation data
            evaluations = context["evaluations"]
            best_k = evaluations.get("best_k", 3)
            
            # Create dynamic mapping based on actual clusters
            mapping = {}
            if best_k == 2:
                mapping = {0: "Economy", 1: "Premium"}
            elif best_k == 3:
                mapping = {0: "Economy", 1: "Standard", 2: "Premium"}
            elif best_k == 4:
                mapping = {0: "Economy", 1: "Standard", 2: "Premium", 3: "Luxury"}
            elif best_k == 5:
                mapping = {0: "Economy", 1: "Standard", 2: "Premium", 3: "Luxury", 4: "Ultra-Luxury"}
            elif best_k == 6:
                mapping = {i: f"Segment_{i+1}" for i in range(best_k)}
            else:
                mapping = {i: f"Segment_{i+1}" for i in range(best_k)}
            
            context.update({
                "prediction": mapping.get(cluster_id, "Unknown"),
                "price": round(predicted_price, 2)
            })
        except Exception as e:
            context["error"] = str(e)
    
    return render(request, "predictor/clustering_analysis.html", context)