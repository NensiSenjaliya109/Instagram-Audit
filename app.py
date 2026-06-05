import streamlit as st
import requests
import pandas as pd
import io
from datetime import datetime
import plotly.graph_objects as go

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Instagram Influencer Audit",
    page_icon="📸",
    layout="wide",
)

# ── Custom CSS (dark theme matching screenshots) ───────────────────────────────
st.markdown("""
<style>
  /* ---------- global ---------- */
  [data-testid="stAppViewContainer"] {
    background: #0d0f14;
    color: #ffffff;
  }
  [data-testid="stHeader"] { background: #0d0f14; }
  section[data-testid="stSidebar"] { display: none; }

  /* ---------- typography ---------- */
  h1 { font-size: 2.6rem !important; font-weight: 800 !important; color: #fff !important; }
  h2 { font-size: 1.6rem !important; font-weight: 700 !important; color: #fff !important; margin-top: 1.6rem !important; }
  h3 { font-size: 1.1rem !important; font-weight: 600 !important; color: #fff !important; }
  p, li, label, .stMarkdown { color: #cccccc !important; }

  /* ---------- input ---------- */
  [data-testid="stTextInput"] input {
    background: #1a1d26 !important;
    color: #ffffff !important;
    border: 1px solid #2a2d3a !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
  }

  /* ---------- primary button ---------- */
  .stButton > button {
    background: #ff4d4d !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: background 0.2s;
  }
  .stButton > button:hover { background: #e03333 !important; }

  /* ---------- download button ---------- */
  .stDownloadButton > button {
    background: #ff4d4d !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
  }
  .stDownloadButton > button:hover { background: #e03333 !important; }

  /* ---------- metric cards ---------- */
  [data-testid="metric-container"] {
    background: #1a1d26 !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    border: 1px solid #2a2d3a !important;
  }
  [data-testid="metric-container"] label { color: #888 !important; font-size: 0.85rem !important; }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
  }

  /* ---------- dataframe ---------- */
  [data-testid="stDataFrame"] {
    background: #1a1d26 !important;
    border-radius: 10px !important;
    border: 1px solid #2a2d3a !important;
  }

  /* ---------- tabs ---------- */
  [data-testid="stTabs"] [role="tab"] {
    color: #888 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.2rem !important;
  }
  [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #ff4d4d !important;
    border-bottom: 2px solid #ff4d4d !important;
  }
  [data-testid="stTabs"] { border-bottom: 1px solid #2a2d3a !important; }

  /* ---------- expander ---------- */
  [data-testid="stExpander"] {
    background: #1a1d26 !important;
    border: 1px solid #2a2d3a !important;
    border-radius: 8px !important;
    margin-bottom: 0.5rem !important;
  }
  [data-testid="stExpander"] summary { color: #fff !important; font-weight: 600 !important; }

  /* ---------- recommendation cards ---------- */
  .rec-card {
    background: #1a2540;
    border: 1px solid #243058;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
    color: #a8c0ff;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
  }

  /* ---------- divider ---------- */
  hr { border-color: #2a2d3a !important; margin: 2rem 0 !important; }

  /* ---------- spinner ---------- */
  [data-testid="stSpinner"] { color: #ff4d4d !important; }

  /* ---------- code blocks ---------- */
  code { background: #1a1d26 !important; color: #ff8080 !important; border-radius: 4px; padding: 2px 6px; }
</style>
""", unsafe_allow_html=True)

# ── Webhook URL (edit here if needed) ─────────────────────────────────────────
WEBHOOK_URL = "https://n8nnensi.app.n8n.cloud/webhook/instagram-audit"

# ── Helper: call the n8n webhook ──────────────────────────────────────────────
def run_audit(username: str) -> dict:
    payload = {"username": username}
    resp = requests.post(WEBHOOK_URL, json=payload, timeout=180)
    resp.raise_for_status()
    return resp.json()

# ── Helper: build Excel download bytes ────────────────────────────────────────
def build_excel(data: dict, username: str) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        # Sheet 1 – Profile Summary
        profile = data.get("report", {}).get("profile_summary", {})
        prof_df = pd.DataFrame([{
            "username": profile.get("username", username),
            "full_name": profile.get("full_name", ""),
            "category": profile.get("category", ""),
            "followers_count": profile.get("followers_count", ""),
            "following_count": profile.get("following_count", ""),
            "total_posts": profile.get("total_posts", ""),
            "verified": profile.get("verified", ""),
            "biography": profile.get("biography", ""),
        }])
        prof_df.to_excel(writer, sheet_name="Profile Summary", index=False)

        # Sheet 2 – Analytics
        analytics = data.get("report", {}).get("analytics", {})
        an_df = pd.DataFrame([{
            "avg_likes": analytics.get("avg_likes", ""),
            "avg_comments": analytics.get("avg_comments", ""),
            "avg_views": analytics.get("avg_views", ""),
            "avg_engagement_rate": analytics.get("avg_engagement_rate", ""),
            "total_posts_analyzed": analytics.get("total_posts", ""),
            "total_views": analytics.get("total_views", ""),
            "best_posting_day": analytics.get("best_posting_day", ""),
        }])
        an_df.to_excel(writer, sheet_name="Analytics", index=False)

        # Sheet 3 – Recent Posts
        posts = data.get("report", {}).get("posts", [])
        if posts:
            posts_df = pd.DataFrame(posts)
            posts_df.to_excel(writer, sheet_name="Recent Posts", index=False)

        # Sheet 4 – AI Recommendations
        recs = data.get("report", {}).get("recommendations", [])
        if recs:
            rec_df = pd.DataFrame({"recommendation": recs})
            rec_df.to_excel(writer, sheet_name="AI Recommendations", index=False)

        # Sheet 5 – Top Performing
        top = data.get("report", {}).get("top_posts", [])
        if top:
            pd.DataFrame(top).to_excel(writer, sheet_name="Top Posts", index=False)

        # Sheet 6 – Low Performing
        low = data.get("report", {}).get("low_posts", [])
        if low:
            pd.DataFrame(low).to_excel(writer, sheet_name="Low Posts", index=False)

    return output.getvalue()

# ── Helper: bar chart (dark theme) ────────────────────────────────────────────
def dark_bar(x_vals, y_vals, title=""):
    fig = go.Figure(go.Bar(
        x=x_vals, y=y_vals,
        marker_color="#7ec8e3",
        marker_line_width=0,
    ))
    fig.update_layout(
        title=title,
        title_font_color="#fff",
        paper_bgcolor="#0d0f14",
        plot_bgcolor="#0d0f14",
        font_color="#ccc",
        xaxis=dict(tickfont_color="#ccc", gridcolor="#1e2130", linecolor="#2a2d3a"),
        yaxis=dict(tickfont_color="#ccc", gridcolor="#1e2130", linecolor="#2a2d3a"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=300,
    )
    return fig

# ══════════════════════════════════════════════════════════════════════════════
#  LANDING / INPUT SECTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.title("Instagram Influencer Audit")
st.markdown(
    "Paste a handle, <code>@username</code>, or full Instagram profile URL. "
    "The app normalises it, calls Apify, and shows the audit output.",
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

profile_input = st.text_input(
    "Profile input",
    placeholder="Example: @nike or https://www.instagram.com/nike/",
    label_visibility="visible",
)

run_clicked = st.button("Run audit")

# ── session state ─────────────────────────────────────────────────────────────
if "audit_data" not in st.session_state:
    st.session_state.audit_data = None
if "audit_username" not in st.session_state:
    st.session_state.audit_username = ""

# ══════════════════════════════════════════════════════════════════════════════
#  TRIGGER AUDIT
# ══════════════════════════════════════════════════════════════════════════════
if run_clicked and profile_input.strip():
    with st.spinner("Running Instagram audit…"):
        try:
            result = run_audit(profile_input.strip())
            st.session_state.audit_data = result
            st.session_state.audit_username = profile_input.strip()
        except requests.exceptions.HTTPError as e:
            st.error(f"Audit failed: {e.response.status_code} – {e.response.text[:300]}")
        except Exception as e:
            st.error(f"Error: {e}")

elif run_clicked and not profile_input.strip():
    st.warning("Please enter a username or URL.")

# ══════════════════════════════════════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════════════════════════════════════
data = st.session_state.audit_data

if data:
    st.markdown("---")
    report     = data.get("report", data)          # support both wrapped & flat
    profile    = report.get("profile_summary", {})
    analytics  = report.get("analytics", {})
    posts      = report.get("posts", [])
    top_posts  = report.get("top_posts", [])
    low_posts  = report.get("low_posts", [])
    recs       = report.get("recommendations", [])
    ai_intel   = report.get("ai_intelligence", {})

    tab1, tab2, tab3 = st.tabs(["📊 Profile & Analytics", "📷 Recent Posts", "🤖 AI Intelligence"])

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 1 – Profile & Analytics
    # ─────────────────────────────────────────────────────────────────────────
    with tab1:
        st.markdown("## Profile summary")
        cols = ["username", "full_name", "category", "followers_count",
                "following_count", "total_posts", "verified"]
        prof_row = {c: profile.get(c, "—") for c in cols}
        st.dataframe(pd.DataFrame([prof_row]), use_container_width=True, hide_index=True)

        bio = profile.get("biography", "")
        if bio:
            st.markdown(f"*{bio}*")
        ext = profile.get("external_url", "")
        if ext:
            st.markdown(f"[{ext}]({ext})")

        st.markdown("---")
        st.markdown("## Analytics")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Avg likes",       f"{analytics.get('avg_likes', '—'):,}" if isinstance(analytics.get('avg_likes'), (int, float)) else "—")
        c2.metric("Avg comments",    f"{analytics.get('avg_comments', '—'):,}" if isinstance(analytics.get('avg_comments'), (int, float)) else "—")
        c3.metric("Avg views",       f"{analytics.get('avg_views', '—'):,}" if isinstance(analytics.get('avg_views'), (int, float)) else "—")
        c4.metric("Avg engagement",  f"{analytics.get('avg_engagement_rate', '—')}%" if analytics.get('avg_engagement_rate') else "—")

        st.markdown("---")
        st.markdown("## Dashboard metrics")
        d1, d2, d3 = st.columns(3)
        d1.metric("Total posts",     analytics.get("total_posts", "—"))
        d2.metric("Total views",     f"{analytics.get('total_views', 0):,}" if isinstance(analytics.get('total_views'), (int, float)) else "—")
        d3.metric("Best posting day", analytics.get("best_posting_day", "—"))

        # Top / low performing post accordions
        st.markdown("---")
        st.markdown("## Top and low-performing posts")
        with st.expander("⭐ Top-performing posts"):
            if top_posts:
                st.dataframe(pd.DataFrame(top_posts), use_container_width=True, hide_index=True)
            else:
                st.info("No top-performing posts data available.")

        with st.expander("📉 Low-performing posts"):
            if low_posts:
                st.dataframe(pd.DataFrame(low_posts), use_container_width=True, hide_index=True)
            else:
                st.info("No low-performing posts data available.")

        # Download
        st.markdown("---")
        excel_bytes = build_excel(data, st.session_state.audit_username)
        fname = f"audit_{profile.get('username', 'report')}_{datetime.today().strftime('%Y%m%d')}.xlsx"
        st.download_button(
            label="📥  Download Audit Report (Excel)",
            data=excel_bytes,
            file_name=fname,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 2 – Recent Posts
    # ─────────────────────────────────────────────────────────────────────────
    with tab2:
        st.markdown("## Recent posts")
        if posts:
            with st.expander("View all recent posts", expanded=True):
                posts_df = pd.DataFrame(posts)
                # rename cols for display
                rename_map = {
                    "shortcode": "shortcode", "type": "post_type",
                    "likes": "likes", "comments": "comments",
                    "views": "views", "engagement_rate": "engagement_rate",
                    "performance_label": "performance_label", "timestamp": "timestamp",
                }
                display_cols = [c for c in rename_map.values() if c in posts_df.columns]
                st.dataframe(posts_df[display_cols] if display_cols else posts_df,
                             use_container_width=True, hide_index=True)
        else:
            st.info("No recent posts data returned.")

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 3 – AI Intelligence
    # ─────────────────────────────────────────────────────────────────────────
    with tab3:
        st.markdown("## Audit intelligence")
        ai1, ai2, ai3, ai4 = st.columns(4)
        ai1.metric("Total posts",    analytics.get("total_posts", "—"))
        ai2.metric("Total views",    f"{analytics.get('total_views', 0):,}" if isinstance(analytics.get('total_views'), (int, float)) else "—")
        ai3.metric("Avg views",      f"{analytics.get('avg_views', '—'):,}" if isinstance(analytics.get('avg_views'), (int, float)) else "—")
        ai4.metric("Avg engagement", f"{analytics.get('avg_engagement_rate', '—')}%" if analytics.get('avg_engagement_rate') else "—")

        st.markdown("---")
        # Top 3 / Bottom 3
        tc, bc = st.columns(2)
        with tc:
            st.markdown("**Top 3 performing posts**")
            if top_posts:
                t_df = pd.DataFrame(top_posts[:3])
                cols_show = [c for c in ["shortcode","post_type","engagement_rate","content_type"] if c in t_df.columns]
                st.dataframe(t_df[cols_show] if cols_show else t_df, use_container_width=True, hide_index=True)
            else:
                st.info("No data")
        with bc:
            st.markdown("**Bottom 3 performing posts**")
            if low_posts:
                b_df = pd.DataFrame(low_posts[:3])
                cols_show = [c for c in ["shortcode","post_type","engagement_rate","content_type"] if c in b_df.columns]
                st.dataframe(b_df[cols_show] if cols_show else b_df, use_container_width=True, hide_index=True)
            else:
                st.info("No data")

        # Posting day chart
        post_by_day = analytics.get("posts_by_day", {})
        if post_by_day:
            st.markdown("---")
            best_day  = analytics.get("best_posting_day", "")
            worst_day = analytics.get("worst_posting_day", "")
            st.markdown(f"**Best day:** {best_day} &nbsp;|&nbsp; **Worst day:** {worst_day}", unsafe_allow_html=True)
            days = list(post_by_day.keys())
            counts = [post_by_day[d] for d in days]
            st.plotly_chart(dark_bar(days, counts), use_container_width=True)

        # Content classification & hook analysis (side by side)
        content_class = analytics.get("content_classification", {})
        hook_analysis = analytics.get("hook_analysis", {})
        if content_class or hook_analysis:
            cc_col, ha_col = st.columns(2)
            with cc_col:
                st.markdown("**Content classification**")
                if content_class:
                    st.plotly_chart(dark_bar(list(content_class.keys()), list(content_class.values())), use_container_width=True)
                else:
                    st.info("No content classification data.")
            with ha_col:
                st.markdown("**Hook analysis**")
                if hook_analysis:
                    st.plotly_chart(dark_bar(list(hook_analysis.keys()), list(hook_analysis.values())), use_container_width=True)
                else:
                    st.info("No hook analysis data.")

        # AI recommendations
        st.markdown("---")
        st.markdown("### 📈 Baseline Business Recommendations")
        if recs:
            for rec in recs:
                st.markdown(f"""
                <div class="rec-card">
                  <span style="font-size:1.3rem">💡</span>
                  <span>{rec}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="rec-card" style="color:#6b7fa8;font-style:italic;">
              AI outputs are unavailable for this run, so only numeric analytics are shown.
            </div>""", unsafe_allow_html=True)

        # Full AI intelligence block (if present)
        if ai_intel:
            st.markdown("---")
            st.markdown("### Full AI Analysis")
            for section, content in ai_intel.items():
                with st.expander(section.replace("_", " ").title()):
                    if isinstance(content, dict):
                        st.json(content)
                    else:
                        st.write(content)
