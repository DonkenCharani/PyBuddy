import streamlit as st
import json
from services.database import (
    get_or_create_user,
    get_quiz_results,
    get_practice_results,
    get_concept_history,
    save_study_plan,
    get_study_plans,
    update_study_plan_tasks,
    delete_study_plan
)
from services.analytics import (
    get_quiz_history_chart,
    get_exercise_stats_chart,
    get_topics_learning_distribution
)
from services.gemini_service import generate_response, is_api_configured
from prompts.explain import STUDY_PLANNER_PROMPT

# Headers
st.markdown("<h1 class='gradient-header'>📊 Progress Tracker</h1>", unsafe_allow_html=True)
st.markdown("<p class='gradient-subheader'>View your learning dashboard, metrics, and manage your AI Study Plans</p>", unsafe_allow_html=True)

username = st.session_state["username"]
user_data = get_or_create_user(username)

# Stat Box Column Header Grid
st.markdown("### 🏆 Accomplishments Overview")
s_col1, s_col2, s_col3, s_col4 = st.columns(4)

concepts_read = len(get_concept_history(username))
quizzes_taken = len(get_quiz_results(username))
exercises_done = len(get_practice_results(username))

with s_col1:
    st.metric(label="Active Streak", value=f"🔥 {user_data['streak_days']} Days")
with s_col2:
    st.metric(label="Total XP", value=f"🏆 {user_data['xp']} XP")
with s_col3:
    st.metric(label="Concepts Studied", value=f"📚 {concepts_read}")
with s_col4:
    st.metric(label="Assessments Finished", value=f"✏️ {quizzes_taken + exercises_done}")

st.markdown("---")

# Layout: Plots & Analytics Charts
tab_charts, tab_planner = st.tabs(["📈 Performance Charts", "📅 AI Study Planner"])

with tab_charts:
    st.markdown("### 🔍 Analytics Visualization")
    
    # 1. Learning activities map
    fig_topics = get_topics_learning_distribution(username)
    if fig_topics:
        st.plotly_chart(fig_topics, use_container_width=True)
    else:
        st.info("No learning activities logged yet. Read a topic or take a quiz to populate this graph!")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        # 2. Quiz scores trend
        fig_quizzes = get_quiz_history_chart(username)
        if fig_quizzes:
            st.plotly_chart(fig_quizzes, use_container_width=True)
        else:
            st.info("Quiz history empty. Take a quiz on the Quiz page to view your performance trend.")
            
    with col_c2:
        # 3. Practice stats
        fig_practice = get_exercise_stats_chart(username)
        if fig_practice:
            st.plotly_chart(fig_practice, use_container_width=True)
        else:
            st.info("Practice exercises empty. Complete coding challenges to see your status breakdown.")

with tab_planner:
    st.markdown("### 📅 Personalized Learning Roadmap")
    st.write("Need structure? Ask PyBuddy to design a weekly curriculum step-by-step for any target python topic or library.")
    
    # Study Plan Input controls
    p_col1, p_col2 = st.columns([2, 1])
    with p_col1:
        goal_input = st.text_input("What is your Python learning goal?", placeholder="e.g., Master Django Web Development, Learn Data Analysis with Pandas")
    with p_col2:
        duration_weeks = st.slider("Duration (Weeks):", min_value=1, max_value=8, value=4)
        
    btn_planner = st.button("🌟 Generate Custom Study Plan", use_container_width=True)
    
    if btn_planner:
        if not goal_input.strip():
            st.warning("Please define a learning goal first.")
        else:
            with st.spinner("🤖 PyBuddy is scheduling your tasks..."):
                try:
                    planner_prompt = STUDY_PLANNER_PROMPT.format(goal=goal_input, weeks=duration_weeks)
                    
                    if is_api_configured():
                        response_text = generate_response(planner_prompt, json_mode=True)
                        clean_text = response_text.strip()
                        if clean_text.startswith("```"):
                            clean_text = clean_text.split("```json")[-1].split("```")[0].strip()
                        plan_data = json.loads(clean_text)
                    else:
                        # Demo Mode Planner template
                        plan_data = [
                            {
                                "week": w,
                                "title": f"Week {w}: Getting started with {goal_input}",
                                "topics": [f"Introduction to {goal_input} concepts", "Setup environments"],
                                "tasks": [f"Build a basic script using {goal_input}", "Review documentation syntax"],
                                "challenge": f"Complete a mini challenge on week {w} topics."
                            } for w in range(1, duration_weeks + 1)
                        ]
                        
                    # Save plan to DB
                    save_study_plan(username, goal_input, duration_weeks, json.dumps(plan_data))
                    st.success("🎉 Plan generated successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error creating plan: {str(e)}")
                    
    # Render active study plans
    st.markdown("---")
    st.markdown("### 📂 Your Current Study Plans")
    plans = get_study_plans(username)
    
    if not plans:
        st.info("No study roadmaps created yet. Set a goal above to get started!")
    else:
        for idx, plan in enumerate(plans):
            # Expander for each roadmap
            with st.expander(f"📋 Goal: {plan['goal']} ({plan['duration']} Weeks)", expanded=(idx == 0)):
                
                # Delete Plan button
                if st.button("🗑️ Delete Plan", key=f"del_plan_{plan['id']}", use_container_width=True):
                    delete_study_plan(plan["id"])
                    st.toast("Plan deleted!")
                    st.rerun()
                    
                # Load JSON
                plan_weeks = json.loads(plan["plan_json"])
                completed_tasks = json.loads(plan["completed_tasks"])
                
                new_completed = list(completed_tasks)
                
                # Render content weekly
                for week in plan_weeks:
                    st.markdown(f"#### 📅 Week {week['week']}: {week['title']}")
                    st.markdown("**Topics to learn**:")
                    for top in week["topics"]:
                        st.markdown(f"- {top}")
                        
                    st.markdown("**Checklist Tasks**:")
                    for task in week["tasks"]:
                        # Unique identifier for the checkbox state
                        task_key = f"task_{plan['id']}_w{week['week']}_{task[:20]}"
                        is_checked = task in completed_tasks
                        
                        checked = st.checkbox(task, value=is_checked, key=task_key)
                        
                        if checked and task not in new_completed:
                            new_completed.append(task)
                        elif not checked and task in new_completed:
                            new_completed.remove(task)
                            
                    st.markdown(f"**🎯 Challenge**: {week['challenge']}")
                    st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
                    
                # Update DB state if changes occurred
                if sorted(new_completed) != sorted(completed_tasks):
                    update_study_plan_tasks(plan["id"], new_completed)
                    st.rerun()
