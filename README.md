# Predicting Urban Job Accessibility
This repository contains the code and analysis for a thesis investigating urban job accessibility. The project leverages a diverse set of geospatial and socio-economic data to build and interpret machine learning models that predict accessibility at the census tract level for several major US cities, including Atlanta, New York, Denver, and Boston.

The core of the project involves two distinct modeling approaches: a traditional gradient boosting model (XGBoost) and a Graph Neural Network (GraphSAGE).

## Repository Structure

*   `notebooks/`: Contains the end-to-end Jupyter notebooks that form the analysis pipeline, from data collection to model explanation.
*   `src/`: Contains reusable Python modules for data fetching (ACS, OSM), feature computation, and dataset construction.

## Workflow

The analysis is structured across a series of notebooks, intended to be run sequentially:

1.  **`01_data_collection.ipynb`**: Fetches and processes all predictor variables, including ACS demographics, road network data, and amenity data from OSM.
2.  **`02_target_variable_collection.ipynb`**: Computes the job accessibility index using LODES data and `r5py` for travel time analysis.
3.  **`03_XGBoost_model.ipynb`**: Trains and evaluates the XGBoost model using spatial cross-validation.
4.  **`04_shap_analysis.ipynb`**: Computes and visualizes SHAP values to explain the trained XGBoost models.
5.  **`05_GraphSAGE_model.ipynb`**: Constructs a spatial graph, trains the GraphSAGE model, and performs initial explainability with GNNExplainer.
6.  **`06_gnnexplainer_analysis.ipynb`**: Aggregates and visualizes global feature importance from GNNExplainer across all cities.
