import streamlit as st
import numpy as np
import random
import time

# Function to generate personalized coaching insights
def get_coaching_insights(role):
    insights = {
        "Startup Founder": [
            "🚀 Focus on product-market fit before scaling.",
            "📈 Build a strong company culture from day one.",
            "💡 Secure funding strategically—validate before raising more capital.",
            "🤝 Networking is key—find mentors and advisors.",
            "📊 Track key business metrics and pivot when needed."
        ],
        "CEO / Executive": [
            "🎯 Set a clear vision and align your team with it.",
            "💡 Use data-driven decision-making to reduce bias.",
            "🧘‍♂️ Maintain work-life balance to improve long-term performance.",
            "📊 Delegate effectively—empower your leadership team.",
            "🤝 Build strong relationships with stakeholders and investors."
        ],
        "Leadership Team": [
            "📢 Communication is your superpower—align the team with clear goals.",
            "🔄 Adaptability is key in dynamic business environments.",
            "📈 Lead by example—your actions define company culture.",
            "🧠 Invest in leadership development and continuous learning.",
            "💡 Foster innovation—create a safe space for new ideas."
        ]
    }
    return random.sample(insights.get(role, []), 3)

# Function to provide AI-driven leadership recommendations
def ai_recommendation():
    recs = [
        "📊 Use AI-driven analytics for data-informed decision-making.",
        "🚀 Automate repetitive tasks to improve productivity.",
        "🤖 Leverage AI-powered chatbots for customer engagement.",
        "📉 Analyze market trends using AI prediction models.",
        "🔍 Implement AI-driven talent acquisition strategies."
    ]
    return random.choice(recs)

# Function to simulate a stress management tip
def stress_management_tip():
    tips = [
        "🧘 Practice mindfulness meditation for 5 minutes daily.",
        "🏃 Engage in regular physical exercise to clear your mind.",
        "📅 Set clear boundaries between work and personal time.",
        "💡 Take strategic breaks—work in focused sprints.",
        "📚 Read a book on leadership and resilience."
    ]
    return random.choice(tips)

# Function to simulate leadership coaching chat
def coaching_chatbot(user_input):
    responses = [
        "🔍 Have you tried breaking the problem into smaller steps?",
        "🤝 Consider seeking feedback from your team.",
        "📊 Data-driven decisions often lead to better outcomes.",
        "💡 Innovation comes from embracing failure and learning quickly.",
        "🚀 Keep a growth mindset—every challenge is an opportunity."
    ]
    return random.choice(responses)

# Streamlit UI
st.title("🤖 Executive Coach Agent")
st.write("AI-powered leadership & decision-making support for founders, executives, and leadership teams.")

# Select Role
role = st.selectbox("🎭 Select Your Role", ["Startup Founder", "CEO / Executive", "Leadership Team"])

if role:
    # Coaching Insights
    st.subheader("📌 Personalized Leadership Insights")
    insights = get_coaching_insights(role)
    for insight in insights:
        st.write(insight)

    # AI Recommendation
    st.subheader("🤖 AI-Driven Leadership Recommendation")
    st.write(ai_recommendation())

    # Stress Management Tip
    st.subheader("🧘 Stress Management & Well-being Tip")
    st.write(stress_management_tip())

    # Leadership Chatbot
    st.subheader("💬 Leadership Coaching Chat")
    user_input = st.text_input("Ask a leadership question:")
    if user_input:
        with st.spinner("Thinking..."):
            time.sleep(2)
            st.write("🧠 AI Coach:", coaching_chatbot(user_input))

    st.success("✅ Leadership Coaching Updated!")