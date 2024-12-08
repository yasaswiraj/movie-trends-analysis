# Movie Trends Analysis

This project explores various hypotheses about trends in the movie industry, using data from IMDb and Rotten Tomatoes. It includes backend and frontend components to enable analysis, visualizations, and predictions.

---

## Project Structure

- **backend/venv/**: Virtual environment for the backend.
- **frontend.py**: Frontend implementation using Streamlit.
- **loadDB.py**: Script to load the database with cleaned data.
- **cleaned_movies_dataset.csv**: Dataset used for analysis.
- **MovieTrendAnalysis1.ipynb**: Jupyter Notebook with exploratory analysis and visualizations.
- **script_DIC.ipynb**: Hypothesis testing and data exploration.
- **script.ipynb**: Additional analysis scripts.

---

## Team Members

- **Aravind Mohan** - 50611294 - amohan22@buffalo.edu
- **Teja Chalikanti** - 50579526 - tejachal@buffalo.edu
- **Yasaswi Raj Madari** - 50608811 - yasaswir@buffalo.edu
- **Sai Kumar Domakonda** - 50604883 - sdomakon@buffalo.edu

---

## Hypotheses and Objectives

### **Aravind Mohan**

1. **Hypothesis 1**: Movies with better critic rankings tend to have better audience ratings as well.
2. **Hypothesis 2**: Audience ratings differ based on genre.

### **Teja Chalikanti**

1. **Hypothesis 1**: Movies with a higher number of votes (`numVotes`) have higher average ratings (`averageRating`).
2. **Hypothesis 2**: Movies with sub-genres tend to have better `audienceRating` compared to movies with only one genre.

### **Yasaswi Raj Madari**

1. **Hypothesis 1**: How do genres change over time based on IMDb ratings?
2. **Hypothesis 2**: Which genre has been consistent among audiences?

### **Sai Kumar Domakonda**

1. **Hypothesis 1**: Do well-known directors (as measured by audience vote counts) receive higher and more consistent IMDb ratings compared to less popular directors?
2. **Hypothesis 2**: Do longer runtime movies receive more audience engagement?

---

## How to Run the Project

### **Prerequisites**

- Python 3.8 or higher
- MySQL Server (for the database)
- `pip` for managing dependencies

---

### **1. Clone the Repository**

```bash
git clone https://github.com/your-repo-name/movie-trends-analysis.git
cd movie-trends-analysis
```

## 2. Setup the Backend

1. **Navigate to the backend directory**:

   ```bash
   cd backend
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**:

   - Update the database connection details in `loadDB.py` and `app.py` (e.g., `db_config`).

5. **Load the database**:

   ```bash
   python loadDB.py
   ```

6. **Run the Flask backend**:

   ```bash
   python app.py
   ```

   - The backend will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 3. Setup the Frontend

1. **Navigate back to the main directory**:

   ```bash
   cd ..
   ```

2. **Install dependencies for the frontend**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit frontend**:

   ```bash
   streamlit run frontend.py
   ```

   - The frontend will be accessible in your browser at [http://localhost:8501](http://localhost:8501).

---

## API Endpoints

### Backend API

#### **Predict Movie Success**:

- **Endpoint**: `POST /predict-movie-success`
- **Payload**:
  ```json
  {
    "runtimeMinutes": 120,
    "startYear": 2021,
    "genres_list": "['Drama', 'Comedy']"
  }
  ```
- **Response**:
  ```json
  {
    "predicted_success": 1,
    "success_probability": 0.85
  }
  ```

#### **Predict Director Cluster**:

- **Endpoint**: `POST /predict-director-cluster`
- **Payload**:
  ```json
  {
    "director": "Christopher Nolan"
  }
  ```
- **Response**:
  ```json
  {
    "prediction": "Director 'Christopher Nolan' belongs to: Elite Directors"
  }
  ```

---

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:

   - Verify database credentials in `loadDB.py` and `app.py`.
   - Ensure MySQL Server is running and the database schema is loaded correctly.

2. **Backend Not Running**:

   - Ensure Flask is running on the correct port (`5000` by default).
   - Check for dependency issues in the backend virtual environment.

3. **Frontend Errors**:
   - Ensure all dependencies are installed in the main directory.
   - Verify the backend is running and accessible.
