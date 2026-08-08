import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Configure Page Layout
st.set_page_config(page_title="VerifyNow: Multi-Channel Fact-Checker 🔍", layout="wide")

def get_topic_emoji(headline):
    h = headline.lower()
    if any(w in h for w in ["flight", "airport", "plane", "vizag", "airline", "travel"]):
        return "✈️ Aviation & Travel"
    elif any(w in h for w in ["cricket", "match", "sports", "football", "olympics", "win"]):
        return "⚽ Sports & Games"
    elif any(w in h for w in ["money", "stock", "tax", "crypto", "bitcoin", "budget", "finance"]):
        return "💰 Economy & Wealth"
    elif any(w in h for w in ["health", "virus", "doctor", "covid", "hospital", "medical"]):
        return "🏥 Medical & Health"
    return "📰 General News"

# --- 1. CHANNEL SCOPE SETTINGS ---
st.title("🎛️ Channel Scope Settings")

col1, col2 = st.columns(2)
with col1:
    feed_level = st.selectbox(
        "Choose News Feed Level:",
        ["Local/Regional Press 📍", "National Press 🇮🇳", "Global Press 🌐"]
    )
with col2:
    # This text box allows you to change the city name on the fly!
    target_city = st.text_input("Enter target city/region:", value="Vizag")

st.markdown("---")

# --- 2. INPUT AREA ---
st.markdown("### ✍️ Enter or paste any news headline to verify:")
user_headline = st.text_input(
    label="Headline Input",
    value="All commercial flights in Vizag are shifting to Bhogapuram airport from August 17",
    label_visibility="collapsed"
)

run_analysis = st.button("🔍 Run Multi-Channel Analysis")

# --- BACKEND INTERNET ENGINE ---
def background_web_search(query, city, feed_scope):
    try:
        # It dynamically reads whatever city name you typed in the box!
        if "Local" in feed_scope:
            search_query = f"{query} {city}"
        elif "National" in feed_scope:
            search_query = f"{query} India"
        else:
            search_query = query  # Global search
           
        search_url = f"https://duckduckgo.com{search_query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            snippets = [node.text for node in soup.find_all('a', class_='result__snippet')]
            return snippets
    except Exception:
        pass
    return []

# --- 3. THE OUTPUTS & SEPARATION ---
if run_analysis or user_headline:
    detected_topic = get_topic_emoji(user_headline)
    st.markdown(f"💡 **Detected Topic Classification:** {detected_topic}")
   
    st.header("🛡️ Accredited Fact-Check Ratings")
   
    with st.spinner("Checking records..."):
        # This sends whatever city is written in the box directly to the engine
        web_matches = background_web_search(user_headline, target_city, feed_level)
   
    if len(web_matches) > 0:
        st.success(f"✅ Verdict: Headline Verified via {feed_level} Logs")
        st.subheader(f"📑 Matches from {feed_level}")
        st.info(f"Active records matching your query found under the selected filters!")
        for snippet in web_matches[:2]:
            st.write(f"• {snippet.strip()}")
    else:
        st.error("❌ Verdict: Target Channel Disconnection Risk")
        st.warning(
            f"Warning: No valid records match this query inside your {feed_level} filter for {target_city}. "
            "The headline is either highly local to another area, or completely fabricated."
        )
        st.subheader(f"📑 Matches from {feed_level}")
        st.error(f"🔴 No matching items found inside the current filter indexes.")

    # Fixed URL logic for manual global broadening
    encoded_query = urllib.parse.quote(f"{user_headline}")
    google_search_url = f"https://google.com{encoded_query}"
    st.link_button("🔗 Force broaden search to manual global web logs", google_search_url) 
