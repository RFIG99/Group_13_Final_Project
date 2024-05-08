import time
from datetime import datetime
from selenium import webdriver
import collections
import csv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Function to initialize Firebase Admin SDK
def initialize_firebase():
    cred = credentials.Certificate("assignment-3-68e19-firebase-adminsdk-touc4-c05aa26aff.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

# Function to write metrics to Firestore
def write_to_firestore(db, metrics):
    # Add a new document with a generated ID
    db.collection(u'metrics').add(metrics)

# Function to write metrics to CSV
def write_to_csv(filename, metrics):
    with open(filename, mode="w", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=["Timestamp"] + list(metrics.keys()))
        writer.writeheader()

        # Write each row separately
        for i in range(len(metrics["Presence time (Seconds)"])):
            row = {"Timestamp": metrics["Timestamp"][i]}
            for key in metrics.keys():
                row[key] = metrics[key][i]
            writer.writerow(row)

def main():
    # Initialize browser
    driver = webdriver.Chrome()

    # Navigate to your website 
    driver.get("http://localhost:3000/")
    
    metrics = collections.defaultdict(list)
    
    # Track presence time 
    SAMPLE_SIZE = 10
    start_time = time.time()
    
    for _ in range(SAMPLE_SIZE):
        current_time = time.time()
        presence_time = current_time - start_time
        print(f"Presence time: {presence_time} seconds")
        metrics["Presence time (Seconds)"].append(presence_time)
            
        # Track scrolling
        scroll_height = driver.execute_script("return document.body.scrollHeight")  
        current_scroll = driver.execute_script("return window.pageYOffset")
        print(f"Scrolled {current_scroll}/{scroll_height} pixels")
        metrics["Scrolling (Pixels)"].append(current_scroll / scroll_height)
        
        # Add timestamp for each sample
        metrics["Timestamp"].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        time.sleep(2) 

    driver.quit()
    print(metrics)

    # Initialize Firebase and write metrics to Firestore
    db = initialize_firebase()
    write_to_firestore(db, metrics)

    # Write metrics to CSV
    write_to_csv("metrics.csv", metrics)

if __name__ == "__main__":
    main()
