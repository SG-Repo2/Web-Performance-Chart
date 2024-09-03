import csv
import requests
import time
import pandas as pd
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objects as go

# Replace with your Google PageSpeed Insights API key
API_KEY = ""
URLS = [
    "https://hydroinc.com/centaur-iiot/",
    "https://kcftech.com/",
    "https://petasense.com",
    "https://www.nikola.tech/",
    "https://sensors.waites.net/condition-monitoring/",
    "https://www.i-alert.com/"
]

def get_score_explanation(score):
    """Returns a performance score explanation."""
    if score >= 90:
        return "Good: The page performs well and meets most performance best practices."
    elif score >= 50:
        return "Needs Improvement: The page's performance could be improved by optimizing certain aspects."
    return "Poor: The page performs poorly and requires significant optimization to improve performance."

def get_performance_metrics(url, api_key, retries=3, delay=5):
    """Fetches performance metrics for a given URL using the PageSpeed Insights API."""
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={api_key}"
    
    for attempt in range(retries):
        response = requests.get(api_url)
        if response.status_code == 200:
            try:
                data = response.json()
                lighthouse_result = data["lighthouseResult"]
                performance_score = lighthouse_result["categories"]["performance"]["score"] * 100
                metrics = {
                    "URL": url,
                    "Performance Score": performance_score,
                    "Score Explanation": get_score_explanation(performance_score),
                    "First Contentful Paint": lighthouse_result["audits"]["first-contentful-paint"]["displayValue"],
                    "Speed Index": lighthouse_result["audits"]["speed-index"]["displayValue"],
                    "Time to Interactive": lighthouse_result["audits"]["interactive"]["displayValue"],
                    "Total Blocking Time": lighthouse_result["audits"]["total-blocking-time"]["displayValue"],
                    "Largest Contentful Paint": lighthouse_result["audits"]["largest-contentful-paint"]["displayValue"],
                    "Cumulative Layout Shift": lighthouse_result["audits"]["cumulative-layout-shift"]["displayValue"],
                    "Server Response Time": lighthouse_result["audits"]["server-response-time"]["displayValue"],
                }
                return metrics
            except KeyError as e:
                print(f"Error processing data for {url}: {e}")
                return None
        else:
            print(f"Error fetching data for {url} (attempt {attempt + 1}): {response.status_code} - {response.text}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return None

def write_metrics_to_csv(metrics_list, output_file):
    """Writes performance metrics to a CSV file."""
    fieldnames = [
        "URL", 
        "Performance Score", 
        "Score Explanation", 
        "First Contentful Paint", 
        "Speed Index", 
        "Time to Interactive", 
        "Total Blocking Time", 
        "Largest Contentful Paint", 
        "Cumulative Layout Shift", 
        "Server Response Time"
    ]
    
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metrics_list)

def generate_radar_charts(data):
    """Generates radar charts to visualize website performance metrics."""
    df = pd.DataFrame(data)

    numeric_columns = [
        "Performance Score",
        "First Contentful Paint",
        "Speed Index",
        "Time to Interactive",
        "Total Blocking Time",
        "Largest Contentful Paint",
        "Cumulative Layout Shift",
        "Server Response Time",
    ]

    # Convert numeric columns to string before extracting numeric values
    for col in numeric_columns:
        df[col] = df[col].astype(str).str.extract(r"([\d\.]+)").astype(float)

    # Generate radar chart
    fig = go.Figure()
    colors = px.colors.qualitative.Plotly

    for i, row in df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=row[numeric_columns],
            theta=numeric_columns,
            fill='toself',
            name=row["URL"],
            line_color=colors[i % len(colors)]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Website Performance Metrics Radar Chart"
    )

    plot_filename = "radar_plot.html"
    pyo.plot(fig, filename=plot_filename)
    print(f"Radar chart saved to {plot_filename}")

def main():
    metrics_list = []
    for url in URLS:
        metrics = get_performance_metrics(url, API_KEY)
        if metrics:
            metrics_list.append(metrics)

    output_file = "website_performance_metrics.csv"
    write_metrics_to_csv(metrics_list, output_file)
    print(f"Metrics saved to {output_file}")

    generate_radar_charts(metrics_list)

if __name__ == "__main__":
    main()
