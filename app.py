import streamlit as st
import pandas as pd
from log_analyzer import analyze_logs

# Page config
st.set_page_config(page_title="IntelliResolve", layout="wide")

# Custom styling
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: #00ADB5;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("IntelliResolve 🚀")
st.subheader("AI-Powered Intelligent Error Monitoring Platform")
st.caption("AI-based log analysis with anomaly detection and smart suggestions")

# Sidebar
st.sidebar.title("IntelliResolve")
st.sidebar.write("AI Monitoring Dashboard")

st.sidebar.write("Features:")
st.sidebar.write("• Log Analysis")
st.sidebar.write("• AI Anomaly Detection")
st.sidebar.write("• Smart Fix Suggestions")
st.sidebar.write("• System Health Monitoring")

# Upload
uploaded_file = st.file_uploader("Upload Log File")

if uploaded_file:

    logs = uploaded_file.read().decode().split("\n")

    with st.spinner("Analyzing logs..."):
        results = analyze_logs(logs)

    st.success("Logs analyzed successfully!")

    # Convert to table
    data = []
    for log, severity, fix in results:
        data.append({
            "Log Message": log,
            "Severity": severity,
            "Suggested Fix": fix
        })

    df = pd.DataFrame(data)

    # Table
    st.subheader("Analysis Results")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # Summary
    high = df[df["Severity"] == "High"].shape[0]
    medium = df[df["Severity"] == "Medium"].shape[0]
    low = df[df["Severity"] == "Low"].shape[0]

    st.subheader("System Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("High Severity Issues", high)
    col2.metric("Medium Severity Issues", medium)
    col3.metric("Low Severity Issues", low)

    st.divider()

    # Graph
    st.subheader("System Health Overview")

    chart_data = {
        "Severity": ["High", "Medium", "Low"],
        "Count": [high, medium, low]
    }

    chart_df = pd.DataFrame(chart_data)
    st.bar_chart(chart_df.set_index("Severity"))

    st.divider()

    # Alerts
    st.subheader("Detected Issues")

    for log, severity, fix in results:

        if severity == "High":
            st.error(f"{log} | Fix: {fix}")

        elif severity == "Medium":
            st.warning(f"{log} | Fix: {fix}")

        elif severity == "Low":
            st.info(f"{log} | Fix: {fix}")

    st.divider()

    # AI Assistant
    st.subheader("AI Log Assistant 🤖")

    question = st.text_input("Ask something about the logs")

    def answer_question(question):
        question = question.lower()

        if "database" in question:
            return "Database connection failed. This may be due to server downtime or incorrect credentials."

        elif "memory" in question:
            return "Memory overflow means system RAM is full. Close unnecessary processes."

        elif "cpu" in question:
            return "High CPU usage indicates heavy processes running."

        elif "error" in question:
            return "Errors indicate failed operations that require investigation."

        elif "critical" in question:
            return "Critical issues need immediate attention to avoid system failure."

        else:
            return "Check logs for warnings, errors, or anomalies."

    if question:
        st.success(answer_question(question))

# Footer
st.divider()
st.caption("Developed by Nexus Team | IntelliResolve AI Monitoring System")