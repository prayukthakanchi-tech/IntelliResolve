from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest


def suggest_fix(log):
    log = log.lower()

    if "database" in log:
        return "Check database connection and restart DB service"
    elif "memory" in log:
        return "Check running processes and free system memory"
    elif "cpu" in log:
        return "Optimize CPU usage or restart heavy processes"
    elif "file not found" in log:
        return "Verify file path or check file permissions"
    else:
        return "Investigate system logs for root cause"


def analyze_logs(logs):

    logs = [log for log in logs if log.strip() != ""]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(logs)

    model = IsolationForest(contamination=0.3, random_state=42)
    model.fit(X)

    predictions = model.predict(X)

    results = []

    for log, pred in zip(logs, predictions):

        if pred == -1:
            severity = "High"
        else:
            severity = "Normal"

        fix = suggest_fix(log)

        results.append((log, severity, fix))

    return results