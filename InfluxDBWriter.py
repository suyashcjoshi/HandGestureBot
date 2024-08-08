# Write to InfluxDB
# Author: Suyash Joshi

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

class InfluxDBWriter:
  def __init__(self, url, token, org, bucket):
    self.url = url
    self.token = token
    self.org = org
    self.bucket = bucket
    self.client = influxdb_client.InfluxDBClient(url=self.url, token=self.token, org=self.org)
    self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

  def write_gesture(self, gesture, timestamp):
    # Convert timestamp from milliseconds to nanoseconds
    timestamp_ns = timestamp * 1000000
    
    # Create the point
    point = influxdb_client.Point("gesture_data") \
      .tag("gesture", gesture) \
      .field("gesture_name", gesture) \
      .time(timestamp_ns)

    # Write the point to InfluxDB
    self.write_api.write(bucket=self.bucket, org=self.org, record=point)
    print(f"Written gesture: {gesture} at {timestamp}")
