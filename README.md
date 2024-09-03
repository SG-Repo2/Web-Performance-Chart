Website Performance Metrics Analysis Tool
Overview
This script is designed to analyze the performance of a list of websites using the Google PageSpeed Insights API. It fetches various performance metrics for each specified URL, saves these metrics into a CSV file, and generates radar charts to visualize the performance of each website.

Features
Fetches performance data for multiple URLs using the Google PageSpeed Insights API.
Collects metrics such as Performance Score, First Contentful Paint, Speed Index, Time to Interactive, Total Blocking Time, Largest Contentful Paint, Cumulative Layout Shift, and Server Response Time.
Saves the collected data into a CSV file.
Generates radar charts to visualize and compare the performance metrics of the websites.
Requirements
Python 3.x
Required Python libraries:
requests
pandas
plotly
You can install the required libraries using the following command:

bash
Copy code
pip install requests pandas plotly
Setup
Replace API Key:

Replace the placeholder YOUR_API_KEY in the script with your actual Google PageSpeed Insights API key.
Specify URLs:

Modify the URLS list in the script to include the URLs of the websites you want to analyze.
How to Use
Run the Script:

Execute the script by running the following command in your terminal:
bash
Copy code
python script_name.py
The script will fetch the performance metrics for each URL and save them in a CSV file named website_performance_metrics.csv.
View the Radar Chart:

The script will generate a radar chart visualizing the performance metrics and save it as radar_plot.html. You can open this file in your web browser to view the chart.
Customization
Retry and Delay Configuration:
You can adjust the number of retries and delay between attempts by modifying the retries and delay parameters in the get_performance_metrics function.
Additional Visualizations:
The script is designed to generate radar charts, but you can extend it to create other types of visualizations as needed.
Notes
Ensure that your Google PageSpeed Insights API key is valid and has sufficient quota.
The radar chart is saved as an HTML file, which can be opened in any modern web browser.
License
This script is provided "as is" without warranty of any kind. You are free to use, modify, and distribute it as you see fit.
