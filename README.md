# 📸 Instagram Influencer Audit

Welcome to the **Instagram Influencer Audit** dashboard! This is a powerful, interactive web application built with Streamlit that allows you to instantly generate deep analytical audits for any public Instagram profile.

🔗 **Live Website:** [nensi-instagram-audit.streamlit.app](https://nensi-instagram-audit.streamlit.app/)

## 🚀 Use Case
This tool is designed for marketers, brand managers, and agencies who need to quickly evaluate an Instagram influencer before collaborating. It provides:
- **Profile Summaries:** Follower/following ratios, verified status, and category.
- **Deep Analytics:** Average likes, comments, views, and overall engagement rates.
- **Post Performance:** Identification of the best and worst performing posts.
- **AI Intelligence & Recommendations:** Automated business suggestions based on the influencer's metrics and posting habits (e.g., best day to post, content classification, hook analysis).
- **Exportable Reports:** Download the entire audit as a multi-sheet Excel file.

---

## 🔄 Project Flow
Here is how the data flows from the user input to the final dashboard:

1. **User Input:** You enter an Instagram username (e.g., `@nike`) or profile URL into the Streamlit user interface.
2. **Webhook Trigger:** The Streamlit app sends a `POST` request containing the username to an **n8n Webhook**.
3. **Backend Processing (n8n):** 
   - The n8n workflow receives the request.
   - n8n triggers the **Apify API** to scrape real-time data from the requested Instagram profile.
   - n8n formats, cleans, and structures the data (and potentially runs it through an AI model for intelligence).
4. **Data Delivery:** n8n returns the structured JSON report back to the Streamlit application.
5. **Visualization:** Streamlit parses the JSON and renders dynamic metrics, Plotly charts, and downloadable DataFrames for the user.

---

## 🔌 APIs & Technologies Used
- **Frontend:** [Streamlit](https://streamlit.io/) (Python web framework), Pandas, Plotly.
- **Integration/Backend:** [n8n](https://n8n.io/) (Workflow automation).
- **Data Extraction API:** [Apify](https://apify.com/) (Used internally inside the n8n flow to fetch Instagram data).

*(Note: Because the Apify token is stored securely inside the n8n workflow, the Streamlit frontend does not require any local API keys or `.env` files to run!)*

---

## 💻 How to Run Locally

Follow these steps to run the dashboard on your own machine.

### 1. Prerequisites
Make sure you have Python installed on your computer. 

### 2. Install Dependencies
Open your terminal or command prompt, navigate to the project folder, and install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Start the Application
Once the installation is complete, start the Streamlit server by running:

```bash
streamlit run app.py
```

### 4. View in Browser
The terminal will provide a local network URL. Your default web browser should automatically open to `http://localhost:8501`, displaying the app.

---

## ☁️ Deployment
This project is deployed and running on [Streamlit Community Cloud](https://share.streamlit.io/).

🔗 **Live Link:** [https://nensi-instagram-audit.streamlit.app/](https://nensi-instagram-audit.streamlit.app/)

Simply push this repository to your GitHub account and connect it to Streamlit Cloud using `app.py` as your main file path!
