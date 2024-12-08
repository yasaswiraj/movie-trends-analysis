
# Callback to handle state transitions and manage app logic
def handle_state(key, value):
    st.session_state[key] = value
import streamlit as st
import pymysql
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# Initialize session state for the landing page logic
if "explore_clicked" not in st.session_state:
    handle_state("explore_clicked", False)
if "quote_index" not in st.session_state:
    st.session_state["quote_index"] = 0

# Define the about section content
about_content = """
<h3 style="text-align:center; margin-bottom:20px;">About The Project</h3>
<p style="text-align:justify; font-size:16px; line-height:1.6;">
This project presents an in-depth analysis of movie data, combining advanced machine learning techniques and interactive tools to uncover meaningful trends and insights. By utilizing data from IMDb and Rotten Tomatoes, we explored the intricate relationships between critic reviews, audience ratings, genres, director performance, and other factors that contribute to a movie's success. Through detailed analysis, we revealed how critic and audience ratings align, how genres evolve over time, and how certain directors consistently produce highly rated films.

A core feature of the project is the classification of directors into performance clusters, such as "Elite Directors" and "Moderate Performers," based on their historical ratings and success metrics. Additionally, machine learning models were employed to predict the likelihood of a movie achieving a high rating, providing actionable insights for filmmakers and marketers. The analysis also revealed key trends in genre popularity and demonstrated how runtime impacts audience engagement, with medium-length films showing the highest levels of satisfaction.

To make these findings accessible, we developed an interactive web application. This tool allows users to explore data trends, generate predictions, and interact with the movie dataset in a user-friendly interface. With its comprehensive approach, the project offers a valuable resource for understanding the dynamics of the film industry and what drives audience preferences.
</p>
"""

# List of rotating quotes
quotes = [
    "Cinema is a matter of what's in the frame and what's out. – Martin Scorsese",
    "Movies are dreams that you never forget. – Steven Spielberg",
    "Every frame of a movie is an idea. – Quentin Tarantino",
    "Film is the most powerful medium to tell a story. – Christopher Nolan",
]

# Injecting custom CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Open+Sans:wght@300;400;600&family=Roboto:wght@500&display=swap');

    /* Background Image */
    body {
        background: url("https://preview.redd.it/2jhtmqhg4mo81.png?width=1080&crop=smart&auto=webp&s=8c8178a80c74b575cf49089d77b66935337425c0") no-repeat center center fixed;
        background-size: cover;
        color: #FFFFFF;
        font-family: 'Open Sans', sans-serif;
    }

    /* Central Box Styling */
    .block-container {
        padding: 30px 50px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
        margin-top: 10%;
        animation: fadeIn 2s ease-in-out;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        background-color: rgba(0, 0, 0, 0.7); /* Add slight overlay for readability */
    }

    /* Title Styling */
    h1 {
        font-family: 'Bebas Neue', sans-serif;
        color: #E50914;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        margin-bottom: 20px;
        font-size: 2.8rem;
        animation: slideIn 2s ease-out;
    }

    /* Subtitle Styling */
    h3 {
        font-family: 'Bebas Neue', sans-serif;
        color: #F50057;
        text-align: center;
        animation: fadeIn 1.5s ease-in-out;
    }

    /* Button Styling */
    .stButton button {
        background: linear-gradient(to right, #E50914, #F50057);
        border: none;
        color: #FFFFFF;
        font-family: 'Bebas Neue', sans-serif;
        font-weight: 700;
        padding: 0.7em 1.5em;
        border-radius: 8px;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(229, 9, 20, 0.4);
        transition: transform 0.3s, box-shadow 0.3s;
        width: 100%;
        max-width: 300px;
        margin: 0 auto;
        display: block;
    }

    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(229, 9, 20, 0.6);
    }

    /* Floating Quote Card */
    .quote-card {
        margin: 20px auto;
        padding: 20px;
        background-color: rgba(0, 0, 0, 0.8);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        color: #FFD700;
        text-align: center;
        font-family: 'Open Sans', sans-serif;
        font-size: 18px;
        font-style: italic;
        max-width: 600px;
        animation: fadeInUp 1.5s ease-in-out;
    }

    /* Animations */
    @keyframes fadeInUp {
        from {
            transform: translateY(20px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }

    @keyframes slideIn {
        from {
            transform: translateX(-30px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Landing Page
if not st.session_state["explore_clicked"]:
    st.title("TITLE IS MOVIE DATA ANALYSIS")
    st.markdown(about_content, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Let's Explore the Project"):
            handle_state("explore_clicked", True)
            

    # Display a single rotating quote
    current_quote = quotes[st.session_state["quote_index"]]
    st.markdown(f"""
        <div class="quote-card">
            "{current_quote}"
        </div>
        """, unsafe_allow_html=True)

    # Rotate the quote every 5 seconds
    time.sleep(5)
    st.session_state["quote_index"] = (st.session_state["quote_index"] + 1) % len(quotes)

# Main Page
if st.session_state["explore_clicked"]:
    back_col, title_col = st.columns([0.1, 0.9])
    with back_col:
        if st.button("←", key="back_button"):
            handle_state("explore_clicked", False)
            

    title_col.title("3D Cluster Visualization with Director Highlighting")

    # Cluster mapping and colors
    cluster_labels = {
        0: "Elite Directors",
        1: "Mixed Legends",
        2: "Moderate Performers",
        3: "Inconsistent Output",
        4: "Little Inconsistent",
    }

    cluster_colors = {
        "Elite Directors": "red",
        "Mixed Legends": "darkblue",
        "Moderate Performers": "yellow",
        "Inconsistent Output": "darkgreen",
        "Little Inconsistent": "orange",
    }

    # Dropdown menu
    questions = [
        "1. What are the top 10 highest-rated movies on IMDb?",
        "2. Which group of directors does a director belong to, and how successful are they?",
        "3. Given the runtime, year, and genre, predict movie success",
        "4. What are the trends in movie releases over the years?",
    ]

    selected_question = st.selectbox("Select a question to analyze:", questions)

    def fetch_directors(partial_name):
        db_config = {
            'user': 'root',
            'password': 'qwerty1234',
            'host': 'localhost',
            'database': 'DIC',
        }
        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            query = "SELECT DISTINCT director FROM movies WHERE LOWER(director) LIKE LOWER(%s) LIMIT 10"
            cursor.execute(query, (f"{partial_name}%",))
            directors = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()
            return directors
        except Exception as e:
            st.error(f"Database connection error: {e}")
            return []

    def generate_cluster_data(num_points=500):
        clusters = []
        np.random.seed(42)
        for cluster_id, label in cluster_labels.items():
            x = np.random.normal(loc=cluster_id * 10, scale=2, size=num_points)
            y = np.random.normal(loc=cluster_id * 15, scale=3, size=num_points)
            z = np.random.normal(loc=cluster_id * 20, scale=4, size=num_points)
            cluster = pd.DataFrame({"X": x, "Y": y, "Z": z, "Cluster": label})
            clusters.append(cluster)
        return pd.concat(clusters, ignore_index=True)

    if selected_question == "2. Which group of directors does a director belong to, and how successful are they?":
        st.text_area(
            "Question Description",
            """
            Discover which group a director is part of, based on how successful their movies have been. The groups are created using data like audience ratings, the number of hit movies, and overall feedback. This helps us see if the director is among the best, moderately successful, or needs improvement.
            """,
            height=120,
        )

        if "current_input" not in st.session_state:
            st.session_state["current_input"] = ""
        if "suggestions" not in st.session_state:
            st.session_state["suggestions"] = []

        director_name = st.text_input(
            "Type a director's name (Press Enter to search):",
            value=st.session_state["current_input"],
            placeholder="Press Enter to search the director",
            key="input_field",
        )

        if director_name and director_name != st.session_state["current_input"]:
            st.session_state["current_input"] = director_name
            st.session_state["suggestions"] = fetch_directors(director_name)

        if st.session_state["suggestions"]:
            st.write("Suggestions:")
            for suggestion in st.session_state["suggestions"]:
                if st.button(suggestion, key=suggestion):
                    st.session_state["current_input"] = suggestion
                    st.session_state["suggestions"] = []

        predict_clicked = st.button("Get Prediction")

        if predict_clicked:
            if director_name:
                api_url = "http://127.0.0.1:5000/predict-director-cluster"
                try:
                    response = requests.post(api_url, json={"director": director_name})
                    if response.status_code == 200:
                        api_output = response.json().get("prediction", "Unknown Cluster")
                        cluster_name = api_output.split(": ")[1] if ": " in api_output else "Unknown Cluster"
                        st.success(f"Director '{director_name}' belongs to: {cluster_name}")

                        if cluster_name == "Unknown Cluster":
                            st.warning("No graph data available for the selected director.")
                        else:
                            cluster_data = generate_cluster_data(num_points=500)
                            director_data = cluster_data[cluster_data["Cluster"] == cluster_name].sample(1)
                            director_data["Cluster"] = cluster_name
                            director_data["Director"] = director_name

                            fig = go.Figure()
                            for cluster, cluster_df in cluster_data.groupby("Cluster"):
                                fig.add_trace(
                                    go.Scatter3d(
                                        x=cluster_df["X"],
                                        y=cluster_df["Y"],
                                        z=cluster_df["Z"],
                                        mode="markers",
                                        marker=dict(size=4, color=cluster_colors[cluster]),
                                        name=cluster,
                                    )
                                )
                            fig.add_trace(
                                go.Scatter3d(
                                    x=director_data["X"],
                                    y=director_data["Y"],
                                    z=director_data["Z"],
                                    mode="markers+text",
                                    marker=dict(size=8, color="black", symbol="circle"),
                                    text=[f"{director_name} ({cluster_name})"],
                                    textposition="top center",
                                    showlegend=False,
                                )
                            )

                            fig.update_layout(
                                title=f"3D Cluster Visualization with {director_name} Highlighted",
                                scene=dict(
                                    xaxis_title="Dimension X",
                                    yaxis_title="Dimension Y",
                                    zaxis_title="Dimension Z",
                                ),
                                legend_title="Clusters",
                            )

                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("Failed to fetch prediction from the API.")
                except requests.exceptions.RequestException as e:
                    st.error(f"API error: {e}")
            else:
                st.warning("Please enter or select a director's name before fetching predictions.")

    if selected_question == "3. Given the runtime, year, and genre, predict movie success":
        st.subheader("Enter Movie Details")

        runtime = st.text_input("Enter the runtime (in minutes):", value="")
        year = st.text_input("Enter the year of release:", value="")
        genre = st.text_input("Enter the genre (comma-separated):", value="")

        predict_clicked = st.button("Predict Movie Success")

        if predict_clicked:
            if runtime and year and genre:
                try:
                    # Convert inputs to appropriate types
                    runtime = int(runtime)
                    year = int(year)
                    genres = genre.split(",")

                    # Make API request
                    api_url = "http://127.0.0.1:5000/predict-movie-success"
                    response = requests.post(
                        api_url,
                        json={"runtimeMinutes": runtime, "startYear": year, "genres_list": str(genres)}
                    )

                    if response.status_code == 200:
                        api_output = response.json()
                        predicted_success = api_output.get("predicted_success", 0)
                        success_probability = api_output.get("success_probability", 0.0)

                        # Display success or failure prediction
                        if predicted_success == True:
                            st.success(f"Hurray! The movie will be a hit! 🎉 (Success Probability: {success_probability:.2%})")
                        else:
                            st.error(f"Omg! The movie might not succeed. 😢 (Success Probability: {success_probability:.2%})")

                        # Fetch movies from the database
                        try:
                            db_config = {
                                'user': 'root',
                                'password': 'qwerty1234',
                                'host': 'localhost',
                                'database': 'DIC',
                            }
                            conn = pymysql.connect(**db_config)

                            # Query movies based on success prediction
                            query = """
                                SELECT originalTitle, startYear, runtimeMinutes, averageRating 
                                FROM movies 
                                WHERE startYear = %s AND averageRating {} 7.5
                            """.format(">=" if predicted_success == 1 else "<=")

                            with conn.cursor() as cursor:
                                cursor.execute(query, (year,))
                                movies = cursor.fetchall()

                            # Display query results
                            if movies:
                                result_label = "successful" if predicted_success == 1 else "unsuccessful"
                                st.write(f"Here are some {result_label} movies from the same year:")
                                df = pd.DataFrame(movies, columns=["Title", "Year", "Runtime (minutes)", "Rating"])
                                st.dataframe(df)
                            else:
                                st.warning("No movies found matching the criteria.")

                        except Exception as e:
                            st.error(f"Error fetching movies from the database: {e}")
                        finally:
                            if 'conn' in locals() and conn:
                                conn.close()
                    else:
                        st.error("Failed to fetch prediction from the API.")
                except ValueError:
                    st.error("Invalid input! Please ensure runtime and year are numbers.")
                except requests.exceptions.RequestException as e:
                    st.error(f"API error: {e}")
            else:
                st.warning("Please fill in all fields to predict the movie's success.")

    if selected_question == "4. What are the trends in movie releases over the years?":
            import time
            import random

            # Creative greetings
            greetings = [
                "Lights, Camera, Action!",
                "Your Cinematic Journey Begins!",
                "Embrace Your Inner Screenwriter!",
                "Set the Stage for Your Blockbuster!",
                "Prepare to Captivate Audiences!"
            ]
            selected_greeting = random.choice(greetings)

            # Function to update word count whenever text area changes
            def update_word_count():
                text = st.session_state.get('plot_input', '').strip()
                st.session_state['word_count'] = len(text.split())

            # Ensure word_count is initialized
            if "word_count" not in st.session_state:
                st.session_state["word_count"] = 0

            # Custom CSS and styling
            # Updated color scheme matched with uploaded theme
            st.markdown(
                """
                <style>
                @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Outfit:wght@400;500;600&display=swap');

                html, body {
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                    background: #000000 !important;
                }

                .video-bg {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    object-fit: cover;
                    z-index: 0;
                }

                .stage {
                    position: relative;
                    width: 90%;
                    max-width: 1200px;
                    margin: 3rem auto;
                    border-radius: 15px;
                    overflow: hidden;
                    background: #141414;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
                    z-index: 2;
                }

                .curtain-container {
                    position: relative;
                    width: 100%;
                    padding-bottom: 56.25%; 
                    overflow: hidden;
                    z-index: 2;
                }

                .curtain {
                    position: absolute;
                    top: 0;
                    width: 50%;
                    height: 100%;
                    background: linear-gradient(to right, #b20710, #e50914, #b20710);
                    animation: curtain-open 3s forwards;
                    z-index: 3;
                }

                .curtain.left {
                    left: 0;
                }
                .curtain.right {
                    right: 0;
                }

                @keyframes curtain-open {
                    0% { width: 50%; }
                    100% { width: 0%; }
                }

                .welcome-text {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    color: #ffffff;
                    font-family: 'Space Grotesk', sans-serif;
                    font-size: 2rem;
                    text-align: center;
                    z-index: 4;
                    opacity: 1;
                    animation: fade-out 3s forwards;
                }

                @keyframes fade-out {
                    0% { opacity: 1; }
                    80% { opacity: 0.5; }
                    100% { opacity: 0; }
                }

                .custom-container {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    padding: 3rem;
                    box-sizing: border-box;
                    background: rgba(20, 20, 20, 0.9);
                    backdrop-filter: blur(5px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    overflow-y: auto;
                    opacity: 0;
                    animation: reveal 3s forwards 3s;
                    z-index: 5;
                }

                @keyframes reveal {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }

                .title-gradient {
                    background: linear-gradient(90deg, #e50914, #b20710);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-family: 'Space Grotesk', sans-serif;
                    font-weight: 700;
                    text-align: center;
                    margin-bottom: 2rem;
                    font-size: 2.5rem;
                }

                .stTextArea textarea {
                    background: #333333 !important;
                    border: 1px solid rgba(255, 255, 255, 0.2) !important;
                    border-radius: 10px !important;
                    color: white !important;
                    font-family: 'Outfit', sans-serif !important;
                    font-size: 1.1rem !important;
                }

                .stButton > button {
                    background: linear-gradient(90deg, #e50914, #b20710) !important;
                    color: white !important;
                    font-weight: 600 !important;
                    padding: 0.75rem 1.5rem !important;
                    border-radius: 10px !important;
                    border: none !important;
                    width: 100% !important;
                    transition: all 0.3s ease !important;
                    font-size: 1rem !important;
                }

                .stButton > button:hover {
                    transform: translateY(-2px) !important;
                    box-shadow: 0 4px 12px rgba(229, 9, 20, 0.5) !important;
                }

                .feedback-box {
                    background: #141414;
                    border-radius: 10px;
                    padding: 2rem;
                    margin: 2rem auto;
                    border: 1px solid #e50914;
                    color: #ffffff;
                    max-width: 800px;
                    text-align: center;
                }

                .word-count {
                    text-align: right; 
                    color: #ffffff; 
                    font-family: 'Outfit', sans-serif; 
                    font-size: 0.9rem; 
                    margin-top: 0.5rem;
                }

                .input-container {
                    max-width: 800px;
                    margin: 2rem auto;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

        # The rest of your logic remains unchanged!

            st.markdown("""
            <script>
                // Scroll to the text area on load
                function scrollToTextArea() {
                    const plotInput = document.getElementById("plot_input");
                    if (plotInput) {
                        plotInput.scrollIntoView({behavior: "smooth"});
                    }
                }

                // Function to scroll to the GIF section
                function scrollToGIF() {
                    const gifElement = document.getElementById("loading_gif");
                    if (gifElement) {
                        gifElement.scrollIntoView({behavior: "smooth"});
                    }
                }

                // Function to scroll to the results section
                function scrollToResults() {
                    const resultElement = document.getElementById("analysis_results");
                    if (resultElement) {
                        resultElement.scrollIntoView({behavior: "smooth"});
                    }
                }
            </script>
            """, unsafe_allow_html=True)

            # Stage and Curtain with dynamic greeting
            st.markdown(f"""
            <div class="stage">
                <div class="curtain-container">
                    <div class="curtain left"></div>
                    <div class="curtain right"></div>
                    <div class="welcome-text">{selected_greeting}</div>
                    <div class="custom-container">
                        <h1 class="title-gradient">Unveil Your Plot's Potential</h1>
                        <p style="color: #e2e8f0; text-align: center; font-size: 1.1rem; margin-bottom: 3rem;">
                            Transform your story into cinematic success with our AI-powered analysis
                        </p>
                        <div class="input-container">
            """, unsafe_allow_html=True)

            # Minimum and maximum word limits
            MIN_WORDS = 100
            MAX_WORDS = 1500

            # Fixed text area: provide a label and hide it
        # Text Area
            story_plot = st.text_area(
                "Describe your plot",  
                height=300,
                placeholder="Describe your movie plot here... At least 100 words and up to 1500 words 🎬",
                key="plot_input",
                on_change=update_word_count,
                label_visibility="collapsed"
            )

            # Automatically scroll to the text area on load
            st.markdown("<script>scrollToTextArea();</script>", unsafe_allow_html=True)


            word_count = st.session_state.get('word_count', 0)

            # Show word count
            st.markdown(f"<div class='word-count'>Words: {word_count}/{MAX_WORDS}</div>", unsafe_allow_html=True)

            # Check length criteria
            plot_too_short = word_count > 0 and word_count < MIN_WORDS
            plot_too_long = word_count > MAX_WORDS

            # Show warnings if needed
            if plot_too_short:
                st.warning(f"Your plot is too short! Please write at least {MIN_WORDS} words.")
            elif plot_too_long:
                st.warning(f"Your plot is too long! Please limit to {MAX_WORDS} words.")

            predict_clicked = st.button("✨ Analyze Plot")

            # Close the HTML containers
            st.markdown("</div></div></div></div>", unsafe_allow_html=True)
            
            if predict_clicked:
                print("clicked")
                # Only proceed if within word limits
                if not plot_too_short and not plot_too_long and word_count >= MIN_WORDS:
                    if story_plot.strip():
                        # Show custom loading animation
                        st.markdown("""
                        <center>
                        <img src="https://media.giphy.com/media/l0IylOPCNkiqOgMyA/giphy.gif" 
                            alt="Meme GIF" 
                            width="400px" 
                            style="margin-bottom: 1rem;"/>
                        </center>
                        """, unsafe_allow_html=True)




                        progress = st.progress(0)
                        status_text = st.empty()

                        messages = [
                            "🍿 Grabbing popcorn from the lobby...",
                            "💡 Brightening the storyline...",
                            "🎉 Hearing applause echo through the theatre...",
                            "🎬 Final take! Polishing the narrative..."
                        ]

                        # Simulate loading steps
                        for idx, msg in enumerate(messages):
                            status_text.text(msg)
                            for i in range(25):
                                progress.progress((idx * 25 + i + 1))
                                time.sleep(0.02)

                        try:
                            # Make the API call with the user's plot
                            print("calling api")
                            api_url = "http://127.0.0.1:5000/predict"
                            payload = {"plot": story_plot}
                            response = requests.post(api_url, json=payload)

                            # Clear progress indicators
                            progress.empty()
                            status_text.empty()
                            print(response)
                            # Check for successful response
                            if response.status_code == 200:
                                result = response.json()
                                print(result)
                                # Extract the success probability from the API response
                                success_value_str = result.get("success_probability", "0")
                                success_value_str = success_value_str.replace('%', '')  # now success_value_str = "39.06"
                                success_value = float(success_value_str)

                                # Anchor to scroll into view
                                st.markdown("<div id='analysis_results'></div>", unsafe_allow_html=True)

                                # Determine message and color
                                
                                if success_value >= 0:
                                        
                                        st.balloons()
            # Add a confetti blast effect from each corner
            # Feel free to replace the Giphy URL with another confetti-like GIF that loops nicely.
                                        st.markdown("""
                                        <style>
                                        .confetti-corner {
                                            position: fixed;
                                            width: 100px;
                                            height: 100px;
                                            z-index: 9999;
                                            background-size: cover;
                                            background-repeat: no-repeat;
                                        }


                                        </style>
                                        <div class="confetti-corner top-left-confetti"></div>
                                        <div class="confetti-corner top-right-confetti"></div>
                                        <div class="confetti-corner bottom-left-confetti"></div>
                                        <div class="confetti-corner bottom-right-confetti"></div>
                                        """, unsafe_allow_html=True)
                                        color = "#4ade80"
                                        message = "🌟 Oscar-Worthy Potential!"
                                        st.balloons()
                                elif success_value >= 60:
                                    color = "#60a5fa"
                                    message = "✨ Box Office Promise"
                                else:
                                    color = "#f472b6"
                                    message = "💫 Diamond in the Rough"

                                # Single large feedback box
                                st.markdown(f"""
                                    <div class="feedback-box">
                                        <h2 style="color: #60a5fa; font-size: 2rem; margin-bottom: 2rem;">
                                            Analysis Results
                                        </h2>
                                        <h3 style="color: {color}; font-size: 1.8rem; margin-bottom: 1.5rem;">
                                            {message}
                                        </h3>
                                        <div style="font-size: 3rem; color: {color}; margin-bottom: 1rem;">
                                            {success_value}%
                                        </div>
                                        <p style="color: #e2e8f0; font-size: 1rem;">
                                            Success Probability
                                        </p>
                                    </div>
                                """, unsafe_allow_html=True)

                                # Scroll down to analysis results
                                st.markdown("""
                                <script>
                                document.getElementById("analysis_results").scrollIntoView({behavior: "smooth"});
                                </script>
                                """, unsafe_allow_html=True)
                            else:
                                st.error("API call failed. Please try again.")

                        except Exception as e:
                            print(e)
                            st.markdown("""
                                <div class="feedback-box" style="border-color: rgba(239, 68, 68, 0.2);">
                                    <h4 style="color: #ef4444;">⚠️ Analysis Error</h4>
                                    <p style="color: #f87171;">Unable to complete analysis. Please try again.</p>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                            <div class="feedback-box" style="border-color: rgba(234, 179, 8, 0.2); max-width:800px; margin:auto;">
                                <h4 style="color: #eab308;">📝 Plot Required</h4>
                                <p style="color: #fbbf24;">Please describe your plot before requesting analysis.</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    # If out of word range and user still clicked Analyze
                    if word_count < MIN_WORDS:
                        st.warning(f"Your plot is too short! Please have at least {MIN_WORDS} words.")
                    elif word_count > MAX_WORDS:
                        st.warning(f"Your plot is too long! Please limit to {MAX_WORDS} words.")