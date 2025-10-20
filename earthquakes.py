# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np



def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc",
            "format": "geojson"
            }
    )

    data = json.loads(response.text)
    print(json.dumps(data, indent=2)[:1000])
    return data

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    ...

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return ...

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data["features"])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    coords = earthquake["geometry"]["coordinates"]
    return coords[1], coords[0]  # (latitude, longitude)


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    features = data["features"]
    strongest = max(features, key=lambda eq: get_magnitude(eq))
    max_magnitude = get_magnitude(strongest)
    max_location = get_location(strongest)
    return max_magnitude, max_location



# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

from datetime import datetime

#同时提取年份与震级
def extract_year_and_magnitude(data):
    years = []
    magnitudes = []
    for eq in data["features"]:
        timestamp = eq["properties"]["time"] / 1000  # 毫秒转秒
        year = datetime.fromtimestamp(timestamp).year
        mag = eq["properties"]["mag"]
        if mag is not None:
            years.append(year)
            magnitudes.append(mag)
    return years, magnitudes


#统计每年的数量与平均震级
def analyse_yearly_stats(years, magnitudes):
    unique_years = np.unique(years)
    freq_per_year = []
    avg_mag_per_year = []
#enumerate() 是 Python 的一个内置函数，它能同时遍历索引和值。
    for y in unique_years:
        mags = [m for i, m in enumerate(magnitudes) if years[i] == y]
        freq_per_year.append(len(mags))
        avg_mag_per_year.append(np.mean(mags))
    
    return unique_years, freq_per_year, avg_mag_per_year


import matplotlib.pyplot as plt
# 提取年份和震级
years, magnitudes = extract_year_and_magnitude(data)

# 统计每年的数量和平均震级
years, freq_per_year, avg_mag_per_year = analyse_yearly_stats(years, magnitudes)

print("Years:", years)
print("Average magnitude per year:", avg_mag_per_year)

# 每年地震数量
plt.figure(figsize=(8,5))
plt.plot(years, freq_per_year, 'o-', label="Frequency per year", color='blue')
plt.xlabel("Year")
plt.ylabel("Number of earthquakes")
plt.title("Earthquake frequency per year (UK)")
plt.legend()
plt.grid(True)
plt.savefig("earthquake_frequency.png")   # ✅ 一定要在 show 前！
plt.show()

# 每年平均震级
plt.figure(figsize=(8,5))
plt.plot(years, avg_mag_per_year, 'o-', label="Average magnitude", color='orange')
plt.xlabel("Year")
plt.ylabel("Average magnitude")
plt.title("Average earthquake magnitude per year (UK)")
plt.legend()
plt.grid(True)
plt.savefig("earthquake_magnitude.png")   # ✅ 一定要在 show 前！
plt.show()
