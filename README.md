# Vehicle Analytics ML Dashboard

A Django-based machine learning dashboard for vehicle price prediction, classification, and clustering analysis.

## Features

- **Regression Analysis**: Predict vehicle selling prices based on year, kilometers driven, seating capacity, and owner income
- **Classification Analysis**: Classify vehicles into income level categories
- **Clustering Analysis**: Group vehicles into Economy, Standard, or Premium segments
- **Exploratory Data Analysis**: Interactive visualizations and dataset insights

## Tech Stack

- Python 3.12
- Django
- scikit-learn
- pandas
- joblib
- Bootstrap 5

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vehicle-analytic-ml
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Train the ML models:
```bash
python model_generators/regression/train_regression.py
python model_generators/classification/train_classifier.py
python model_generators/clustering/train_cluster.py
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Open your browser and navigate to `http://127.0.0.1:8000/`

## Project Structure

```
vehicle-analytic-ml/
├── config/                 # Django project settings
├── predictor/             # Main Django app
│   ├── templates/         # HTML templates
│   ├── views.py          # View functions
│   └── urls.py           # URL routing
├── model_generators/      # ML model training scripts
│   ├── regression/       # Price prediction model
│   ├── classification/   # Income level classification model
│   └── clustering/       # Vehicle segmentation model
├── dummy-data/           # Training dataset
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## Usage

### Regression Analysis
Input vehicle specifications to predict the market price:
- Model Year
- Kilometers Driven
- Number of Seats
- Owner Income

### Classification Analysis
Classify vehicles into income level categories based on the same features.

### Clustering Analysis
Automatically segments vehicles into Economy, Standard, or Premium categories based on predicted price and owner income.

## Model Performance

The dashboard displays evaluation metrics for each model:
- **Regression**: R² Score
- **Classification**: Accuracy Score
- **Clustering**: Silhouette Score

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is for educational purposes.
