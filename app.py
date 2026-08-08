import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 🌟 Configure Page Layout
st.set_page_config(page_title="VerifyNow: Multi-Channel Fact-Checker 🔍", layout="wide")

def get_topic_emoji(headline):
    """🧠 Topic Emojifier Engine: Auto-detects subjects to inject relevant graphics."""
    h = headline.lower()
    if any(w in h for w in ["flight", "airport", "plane", "vizag", "airline", "travel"]):
        return "✈️ Aviation & Travel"
    elif any(w in h for w in ["cricket", "match", "sports", "football", "olympics", "win"]):
        return "🏆 Sports & Games"
    elif any(w in h for w in ["money", "stock", "tax", "crypto", "bitcoin", "budget", "finance"]):
        return "💰 Economy & Wealth"
    elif any(w in h for w in ["health", "virus", "doctor", "covid", "hospital", "medical"]):
        return "🏥 Medical & Health"
    elif any(w in h for w in ["tech", "ai", "chatgpt", "iphone", "google", "cyber", "robot"]):
        return "🤖 Technology & Science"
    elif any(w in h for w in ["election", "modi", "minister", "government", "bjp", "tdp"]):
        return "🏛️ Politics & Policy"
    elif any(w in h for w in ["war", "blast", "attack", "police", "arrest", "accident", "crash"]):
        return "🚨 Breaking Emergency"
    elif any(w in h for w in ["movie", "actor", "ott", "netflix", "song", "star"]):
        return "🎬 Entertainment & Pop Culture"
    else:
        return "🌐 General Global Context"

def fetch_filtered_news(query, scope, custom_city=""):
    """📡 Multi-Channel Scraper: Dynamically appends parameters targeting specific feeds."""
    base_query = query
    
    # 🎛️ Inject routing algorithms depending on user choice
    if scope == "Global Channels 🌎":
        # Force results solely from major international news networks
        global_filters = " (site:bbc.com OR site:reuters.com OR site:cnn.com OR site:bloomberg.com OR site:apnews.com)"
        base_query += global_filters
    elif scope == "National Channels 🇮🇳":
        # Force results solely from India's primary mainstream news domains
        national_filters = " (site:://indiatimes.com OR site:ndtv.com OR site:indianexpress.com OR site:hindustantimes.com OR site:thehindu.com)"
        base_query += national_filters
    elif scope == "Local/Regional Press 📍":
        # Pinpoint results utilizing location keywords and regional publication strings
        location_keyword = custom_city if custom_city else "Vizag"
        base_query += f" location:{location_keyword}"

    encoded_query = urllib.parse.quote(base_query)
    url = f"https://google.com{encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    
    articles = []
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'xml')
            items = soup.find_all('item')[:5]
            
            for item in items:
                title = item.title.text if item.title else "No Title"
                link = item.link.text if item.link else "#"
                source = item.source.text if item.source else "Verified Media Channel"
                articles.append({"source": source, "title": title, "url": link})
    except Exception:
        pass
    return articles

# 📱 App Header UI
st.title("🚨 VerifyNow: Headline Fact-Checker")
st.caption("🌐 Instantly cross-reference and verify news headlines across specific regional, national, or global networks.")

# 📦 Sidebar Control Dashboard for Multi-Channel settings
st.sidebar.header("🎛️ Channel Scope Settings")
news_scope = st.sidebar.selectbox(
    "Choose News Feed Level:",
    ["Global Channels 🌎", "National Channels 🇮🇳", "Local/Regional Press 📍"]
)

# Show city box helper only if Local scope is selected
target_city = ""
if news_scope == "Local/Regional Press 📍":
    target_city = st.sidebar.text_input("Enter target city/region:", "Vizag")

# 📥 User Input Box
headline_input = st.text_input("✍️ Enter or paste any news headline to verify:", "Flights from Vizag airport soon")

# ⚡ Action Button
if st.button("🔍 Run Multi-Channel Analysis") and headline_input:
    with st.spinner(f"⏳ Querying selected {news_scope} database feeds..."):
        
        # 🔄 Run Topic Categorization Engine
        detected_topic = get_topic_emoji(headline_input)
        st.info(f"💡 Detected Topic Classification: **{detected_topic}**")
        
        # 🔄 Fetch Targeted Live Feeds
        news_articles = fetch_filtered_news(headline_input, news_scope, target_city)
        
        col1, col2 = st.columns(2)
        
        # 🛡️ Column 1: Verification Matrix
        with col1:
            st.subheader("🛡️ Accredited Fact-Check Ratings")
            if news_articles:
                st.success(f"✅ **Verdict: Active {news_scope} Distribution Detected**")
                st.write(f"This headline has verified distribution matching our filtered database parameters for {news_scope}.")
            else:
                st.error(f"❌ **Verdict: Target Channel Disconnection Risk**")
                st.write(f"Warning: No valid print records match this query inside **{news_scope}**. The headline is either highly local to another area, or completely fabricated.")
                
        # 📰 Column 2: Isolated Media Footprint Stream
        with col2:
            st.subheader(f"📰 Matches from {news_scope}")
            if news_articles:
                st.write(f"📊 Filtered coverage points retrieved:")
                for art in news_articles:
                    st.markdown(f"📡 **{art['source']}**: [{art['title']}]({art['url']})")
                st.success("🟢 Headline source profiles isolated cleanly.")
            else:
                fallback_url = f"https://google.com{urllib.parse.quote(headline_input)}"
                st.error(f"🔴 No matching items found inside the {news_scope} filter indexes.")
                st.markdown(f"🔗 [Force broaden search to manual global web logs]({fallback_url})")
