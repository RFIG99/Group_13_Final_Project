import argparse
import os
import time
from selenium import webdriver
import collections
import csv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import importlib

# Function to initialize Firebase Admin SDK
def initialize_firebase():
    if not firebase_admin._apps:  # Check if Firebase app is already initialized
        cred = credentials.Certificate("assignment-3-68e19-firebase-adminsdk-touc4-c05aa26aff.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()

# Function to write metrics to Firestore
def write_to_firestore(db, metrics):
    # Add a new document with a generated ID
    doc_ref = db.collection(u'metrics').add(metrics)
    print(f"Document added with ID: {doc_ref.id}")

# Function to write metrics to CSV
def write_to_csv(filename, metrics):
    # Extracting the first value from each metric
    iterations = [metric["Iteration"][0] for metric in metrics]
    groups = [metric["Group"][0] for metric in metrics]
    users = [metric["User"][0] for metric in metrics]
    presence_times = [metric["Presence time (Seconds)"][0] for metric in metrics]

    # Writing the metrics as columns
    with open(filename, mode="w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(["Iteration"] + iterations)
        writer.writerow(["Group"] + groups)
        writer.writerow(["User"] + users)
        writer.writerow(["Presence time (Seconds)"] + presence_times)

# Function to get user scripts based on group
def get_user_scripts(group):
    if group == 'control':
        group_dir = 'Control_Group'
    elif group == 'test':
        group_dir = 'Test_Group'
    else:
        raise ValueError("Invalid group specified. Use 'control' or 'test'.")

    return [script for script in os.listdir(group_dir) if script.endswith('.py')]

def main(user_scripts, group):
    # Define the group directory based on the value of the group argument
    if group == 'control':
        group_dir = 'Control_Group'
    elif group == 'test':
        group_dir = 'Test_Group'
    else:
        print("Invalid group specified.")
        return

    # Initialize a list to store metrics from all users
    all_metrics = collections.defaultdict(list)

    for user_script in user_scripts:
        print(f"Processing user script: {user_script}")
        start_time = time.time()  # Define and initialize start_time
        driver = webdriver.Chrome()
        driver.get("http://localhost:3000/")
        metrics = collections.defaultdict(list)
        db = initialize_firebase()

        try:
            # Set iteration directly to 1
            iteration = 1
            presence_time = time.time() - start_time

            metrics["Iteration"].append(iteration)
            metrics["Group"].append(group)
            metrics["User"].append(user_script)
            metrics["Presence time (Seconds)"].append(presence_time)

            print("Iteration:", metrics["Iteration"][0])
            print("Group:", metrics["Group"][0])
            print("User:", metrics["User"][0])
            print("Presence time (Seconds):", metrics["Presence time (Seconds)"][0])

            # Dynamically import the user script based on the file name
            module_name = os.path.splitext(user_script)[0]  # Remove the file extension
            user_module = importlib.import_module(f"{group_dir}.{module_name}")
            print(f"User script imported: {user_script}")
            user_module.userAction(driver)  # Pass the driver instance to userAction
            print(f"User action performed: {user_script}")

            time.sleep(2)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            try:
                driver.quit()
                print("WebDriver instance quit.")
            except Exception as e:
                print(f"An error occurred while quitting the WebDriver: {e}")

        # Append metrics for the current user script to all_metrics
        for key, value in metrics.items():
            all_metrics[key].extend(value)
        print(f"Metrics collected for user script: {user_script}")

    # Write all metrics to Firestore
    db = initialize_firebase()
    doc_ref = db.collection(u'metrics').add(dict(all_metrics))
    print(f"Document added with ID: {doc_ref[1].id}")

    # Write all metrics to a single CSV file named "metrics.csv"
    write_to_csv("metrics.csv", [dict(all_metrics)])
    print("All metrics recorded and stored successfully in metrics.csv")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Perform A/B testing with dynamic importing')
    parser.add_argument('--group', type=str, required=True, choices=['control', 'test'], help='Specify the group for A/B testing')
    args = parser.parse_args()

    group = args.group

    # Get a list of all user scripts under the specified group directory
    user_scripts = get_user_scripts(group)

    # Now, pass the user scripts and the group to the main function
    main(user_scripts, group)

