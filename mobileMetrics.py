import csv
import requests
import time
import pandas as pd
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objects as go

# Replace with your Google PageSpeed Insights API key
API_KEY = "AIzaSyB5JFVZS5T0RqKJXK1XpUJpESlSpE3v2S8"

URLS = [
    "https://hydroinc.com/centaur-iiot/",
    "https://kcftech.com/",
    "https://petasense.com",
    "https://www.nikola.tech/",
    "https://sensors.waites.net/condition-monitoring/",
    "https://www.i-alert.com/"
]

def get_score_explanation(score):
    if score >= 90:
        return "Good: The page performs well and meets most performance best practices."
    elif score >= 50:
        return "Needs Improvement: The page's performance could be improved by optimizing certain aspects."
    else:
        return "Poor: The page performs poorly and requires significant optimization to improve performance."


def get_performance_metrics(url, api_key, retries=3, delay=5):
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={api_key}"
    
    for i in range(retries):
        response = requests.get(api_url)
        if response.status_code == 200:
            try:
                data = response.json()
                performance_score = data["lighthouseResult"]["categories"]["performance"]["score"] * 100
                metrics = {
                    "URL": url,
                    "Performance Score": performance_score,
                    "Score Explanation": get_score_explanation(performance_score),
                    "First Contentful Paint": data["lighthouseResult"]["audits"]["first-contentful-paint"]["displayValue"],
                    "Speed Index": data["lighthouseResult"]["audits"]["speed-index"]["displayValue"],
                    "Time to Interactive": data["lighthouseResult"]["audits"]["interactive"]["displayValue"],
                    "Total Blocking Time": data["lighthouseResult"]["audits"]["total-blocking-time"]["displayValue"],
                    "Largest Contentful Paint": data["lighthouseResult"]["audits"]["largest-contentful-paint"]["displayValue"],
                    "Cumulative Layout Shift": data["lighthouseResult"]["audits"]["cumulative-layout-shift"]["displayValue"],
                    "Server Response Time": data["lighthouseResult"]["audits"]["server-response-time"]["displayValue"],
                }
                return metrics
            except KeyError as e:
                print(f"Error processing data for {url}: {e}")
                return None
        else:
            print(f"Error fetching data for {url} (attempt {i + 1}): {response.status_code} - {response.text}")
            if i < retries - 1:
                time.sleep(delay)
            else:
                return None

def write_metrics_to_csv(metrics_list, output_file):
    with open(output_file, "w", newline="") as csvfile:
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

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for metrics in metrics_list:
            writer.writerow(metrics)


def generate_radar_charts(data):
    df = pd.DataFrame(data)

    # Define distinct colors for each URL
    colors = px.colors.qualitative.Plotly

    # Add an 'Index' column to df for color coding
    df['Index'] = df.index % len(colors)  # If more websites than colors, cycle through colors again

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

    for col in numeric_columns:
        df[col] = df[col].astype(str).str.extract(r"([\d\.]+)").astype(float)

    fig = go.Figure()

    for i, row in df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=row[numeric_columns],
            theta=numeric_columns,
            fill='toself',
            name=row["URL"],
            line_color=colors[row['Index']]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True
    )

    plot_filename = "radar_plot.html"
    pyo.plot(fig, filename=plot_filename)
    print(f"Plot saved to {plot_filename}")




def generate_parallel_coordinates_plot(data):
    df = pd.DataFrame(data)

    # Define distinct colors for each URL
    colors = px.colors.qualitative.Plotly

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

    for col in numeric_columns:
        df[col] = df[col].astype(str).str.extract(r"([\d\.]+)").astype(float)

    # Create a plotly figure
    fig = go.Figure()

    for idx, row in df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=row[numeric_columns].values,
            theta=numeric_columns,
            fill='toself',
            name=row['URL'],  # This will be the legend entry
            line_color=colors[idx % len(colors)]  # Cycle through colors if more websites than colors
        ))

    # Update layout to include URL names in the legend
    fig.update_layout(
        title="Website Performance Metrics",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True
    )

    plot_filename = "parallel_coordinates_plot.html"
    fig.write_html(plot_filename)
    print(f"Plot saved to {plot_filename}")

    # Update traces to reflect new color scheme
    fig.update_traces(line=dict(color='rgba(0,0,0,0.7)'))

    plot_filename = "parallel_coordinates_plot.html"
    pyo.plot(fig, filename=plot_filename)
    print(f"Plot saved to {plot_filename}")

def main():
    metrics_list = []
    for url in URLS:
        metrics = get_performance_metrics(url, API_KEY)
        if metrics:
            metrics_list.append(metrics)

    output_file = "website_performance_metrics.csv"
    write_metrics_to_csv(metrics_list, output_file)
    print(f"Metrics saved to {output_file}")

    #generate_parallel_coordinates_plot(metrics_list)
    generate_radar_charts(metrics_list)

if __name__ == "__main__":
    main()
