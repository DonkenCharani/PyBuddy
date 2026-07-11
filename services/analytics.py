import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from services.database import get_quiz_results, get_practice_results, get_concept_history

# Theme constant colors
COLOR_PRIMARY = "#FFE082"    # Yellow accent
COLOR_SECONDARY = "#3776AB"  # Python Blue
COLOR_BG = "#1E293B"         # Dark card background
COLOR_TEXT = "#F8FAFC"       # Light gray text
COLOR_GRID = "#334155"       # Grid line color

def _apply_theme(fig):
    """Helper to apply the uniform dark theme styling to Plotly figures."""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', # transparent
        plot_bgcolor='rgba(0,0,0,0)',  # transparent
        font=dict(color=COLOR_TEXT, family="sans-serif"),
        title_font=dict(color=COLOR_PRIMARY, size=16),
        legend=dict(
            font=dict(color=COLOR_TEXT),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=COLOR_GRID,
        linecolor=COLOR_GRID,
        tickfont=dict(color=COLOR_TEXT)
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=COLOR_GRID,
        linecolor=COLOR_GRID,
        tickfont=dict(color=COLOR_TEXT)
    )
    return fig

def get_quiz_history_chart(username: str):
    """
    Generates a line chart tracking quiz scores over time.
    """
    raw_data = get_quiz_results(username)
    if not raw_data:
        return None
        
    df = pd.DataFrame(raw_data)
    # Parse dates
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["Percentage"] = (df["score"] / df["total_questions"]) * 100
    df = df.sort_values(by="created_at")
    
    fig = px.line(
        df, 
        x="created_at", 
        y="Percentage", 
        color="difficulty",
        title="Quiz Scores Trend Over Time (%)",
        hover_data=["quiz_topic", "score", "total_questions"],
        markers=True,
        color_discrete_map={"Easy": "#4ade80", "Medium": "#facc15", "Hard": "#f87171"}
    )
    
    fig.update_traces(line=dict(width=3))
    return _apply_theme(fig)

def get_exercise_stats_chart(username: str):
    """
    Generates a grouped bar chart displaying number of coding practice exercises
    passed vs failed grouped by difficulty level.
    """
    raw_data = get_practice_results(username)
    if not raw_data:
        return None
        
    df = pd.DataFrame(raw_data)
    df["Status"] = df["passed"].apply(lambda x: "Passed" if x == 1 else "Needs Work")
    
    # Aggregate data
    agg_df = df.groupby(["difficulty", "Status"]).size().reset_index(name="Count")
    
    fig = px.bar(
        agg_df,
        x="difficulty",
        y="Count",
        color="Status",
        barmode="group",
        title="Coding Exercises Status by Difficulty",
        color_discrete_map={"Passed": "#4ade80", "Needs Work": "#f87171"}
    )
    
    return _apply_theme(fig)

def get_topics_learning_distribution(username: str):
    """
    Generates a horizontal bar chart summarizing the volume of activities 
    completed per Python topic (concept readings + exercises + quizzes).
    """
    concepts = get_concept_history(username)
    quizzes = get_quiz_results(username)
    practices = get_practice_results(username)
    
    topic_counts = {}
    
    # Process concepts read
    for c in concepts:
        topic = c["topic"]
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
    # Process quizzes taken
    for q in quizzes:
        topic = q["quiz_topic"]
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
    # Process practices coded
    for p in practices:
        # Match practice title roughly back to topics if possible, or use exercise_title
        # Let's count them simply
        title = p["exercise_title"]
        topic_counts[title] = topic_counts.get(title, 0) + 1
        
    if not topic_counts:
        return None
        
    df = pd.DataFrame(list(topic_counts.items()), columns=["Topic", "Activity Count"])
    df = df.sort_values(by="Activity Count", ascending=True)
    
    fig = px.bar(
        df,
        x="Activity Count",
        y="Topic",
        orientation="h",
        title="Learning Activities Map by Topic",
        color="Activity Count",
        color_continuous_scale=["#3776AB", "#FFE082"] # Blue to Yellow
    )
    
    fig.update_layout(coloraxis_showscale=False)
    return _apply_theme(fig)
