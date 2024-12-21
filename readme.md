# Movie Trends Analysis

This project explores various hypotheses about trends in the movie industry, using data from IMDb and Rotten Tomatoes. It includes backend and frontend components to enable analysis, visualizations, and predictions.

---

## Project Structure

everything is under app folder

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

## Hypotheses and Objectives In the Phase 3

### **Aravind Mohan**

### Question 1: Trends in Movie Releases Over Time

What is this about?
This question looks at how many movies were released each year and predicts future trends.

Inputs:
Year of Release (startYear): This tells us when a movie was released.
Model Used: ARIMA (AutoRegressive Integrated Moving Average)
This model predicts trends based on time (like years). It works in three steps:

AR (AutoRegressive): Looks at how the number of movies released in one year depends on the previous years.
I (Integrated): Removes any long-term trends (like if releases are increasing every year).
MA (Moving Average): Fixes errors by looking at patterns in past mistakes.

What’s the Output?
A line graph showing how movie releases have changed over time.
A prediction line showing how many movies might be released in future years.

How is it shown in the app?
When users ask about trends in movie releases, the app creates a graph showing past data and predictions for the future.

### previous hypotheses

1. **Hypothesis 1**: Movies with better critic rankings tend to have better audience ratings as well.
2. **Hypothesis 2**: Audience ratings differ based on genre.

### **Teja Chalikanti**

### Question 2: Grouping Directors Based on Success

What is this about?
This question divides directors into groups based on how successful they are.

Inputs:
Director’s Name: You enter a director’s name.
Success Metrics: Data about how well their movies performed (e.g., ratings, number of hit movies).
Model Used: K-Means Clustering
This model groups directors based on patterns in their performance. It forms groups like:

Elite Directors: Directors with lots of successful movies.
Moderate Performers: Directors with some good movies.
Inconsistent Output: Directors with mixed or poor results.

What’s the Output?
A 3D scatter plot with directors in different groups (clusters).
The chosen director’s group is highlighted on the graph.
How is it shown in the app?
You type in a director’s name, and the app predicts their group. It also shows their position in the graph, making it easy to see how they compare to others.

### previous hypotheses

1. **Hypothesis 1**: Movies with a higher number of votes (`numVotes`) have higher average ratings (`averageRating`).
2. **Hypothesis 2**: Movies with sub-genres tend to have better `audienceRating` compared to movies with only one genre.



### **Yasaswi Raj Madari**


### Question 3: Predicting Movie Ratings


What is this about?
This question predicts the rating of a movie based on its details like genre, runtime, and year of release.

Inputs:
Runtime (runtimeMinutes): How long the movie is.
Year (startYear): When the movie was released.
Genres (genres_list): The type of movie (e.g., Comedy, Drama).
Model Used: Gradient Boosting (LightGBM)
This model looks at all the details of a movie and predicts its rating. It uses:

Genres: To understand how different types of movies are rated.
Runtime: To check if longer or shorter movies are rated higher.
Year: To see if ratings change over time.


What’s the Output?
A predicted rating for the movie.
Insights into how genre or runtime affects the rating.


How is it shown in the app?
You enter the movie’s details, and the app predicts its rating. It also shows graphs comparing movies with similar details.


### previous hypotheses

1. **Hypothesis 1**: How do genres change over time based on IMDb ratings?
2. **Hypothesis 2**: Which genre has been consistent among audiences?



### **Sai Kumar Domakonda**


### Question 4: Predicting a Movie’s Success Based on Its Plot

What is this about?
This question predicts whether a movie will be successful or not based on its plot (story).

Inputs:
Plot: The description of the movie’s story.
Model Used: BERT (Bidirectional Encoder Representations from Transformers)
This model is trained to understand text and predict whether the plot is good enough for a successful movie. It works by:

Reading and understanding the plot text.
Scoring the plot on how likely it is to lead to a successful movie.

What’s the Output?
A success probability (e.g., "85% chance of success").
A color-coded result:
Green: Likely a blockbuster.
Blue: Has good potential.
Pink: Needs improvement.


How is it shown in the app?
You type the movie’s plot, and the app predicts how successful it will be. It also gives detailed feedback with a percentage and colorful visuals.

### previous hypotheses

1. **Hypothesis 1**: Do well-known directors (as measured by audience vote counts) receive higher and more consistent IMDb ratings compared to less popular directors?
2. **Hypothesis 2**: Do longer runtime movies receive more audience engagement?

---

## How to Run the Project

### **Prerequisites**

- Python 3.8 or higher
- MySQL Server (for the database)
- `pip` for managing dependencies

---

## 2. Setup the Backend

1. **Load the database**:

   ```bash
   pip install -r requirements.txt
   python loadDB.py
   ```

2. **Navigate to the backend directory**:

   ```bash
   cd backend
   ```

3. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows, use venv\Scripts\activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure the database**:

   - Update the database connection details in `loadDB.py` and `app.py` (e.g., `db_config`).

6. **Run the Flask backend**:

   ```bash
   cd venv/Scripts/
   python app.py
   ```

   - The backend will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 3. Setup the Frontend

1. **Navigate back to the main directory**:
   Open a new terminal with the main directory

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

## Setup the CRUD Frontend (React)

1. **Navigate to the React frontend folder**:
   ```bash
   cd frontend/movie-app
   ```
2. **Install dependencies**:
   Ensure that you have Node.js and npm installed on your machine.
   Run the following command to install all required dependencies from the package.json file:
   ```bash
   npm install
   ```
3. **Run the React app**:
   Start the development server:
   ```bash
   npm start
   ```
   The React CRUD frontend will be accessible in your browser at http://localhost:3000.
   **Build for Production (Optional)**:
   To create a production-ready build of the app:
   ```bash
      npm run build
   ```
   The production build will be created in the build/ directory. 5. **Environment Variables (Optional)**:
   If the React app requires environment-specific configurations (e.g., API endpoints), create a .env file in the project root and define variables like:
   ```bash
   REACT_APP_API_URL=http://localhost:5001
   ```
   Use these variables in the app as:
   const apiUrl = process.env.REACT_APP_API_URL; \n

---

## Setup the CRUD Backend

1. **Load the database**:

   ```bash
   cd crud
   pip install -r requirements.txt
   python loadDB.py
   ```

2. **Navigate to the backend directory**:

   ```bash
   cd backend
   ```

3. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows, use venv\Scripts\activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure the database**:

   - Update the database connection details in `loadDB.py` and `app.py` (e.g., `db_config`).

6. **Run the Flask backend**:

   ```bash
   cd venv/Scripts/
   python app.py
   ```

   - The backend will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

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
