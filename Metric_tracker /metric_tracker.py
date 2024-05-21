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

# Function to write metrics to Firestore with a specific document ID
def write_to_firestore(db, metrics, document_id):
    # Set the document reference with the specified document ID
    doc_ref = db.collection(u'metrics').document(document_id)
    # Set the document data
    doc_ref.set(metrics)
    print(f"Metrics added to document with ID: {document_id}")

# Function to write metrics to CSV
def write_to_csv(filename, metrics):
    # Writing the metrics as rows in the CSV file
    with open(filename, mode="w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(["User", "Group", "Iteration", "Presence time (Seconds)"])
        for i in range(len(metrics["User"])):
            writer.writerow([
                metrics["User"][i],
                metrics["Group"][i],
                metrics["Iteration"][i],
                metrics["Presence time (Seconds)"][i]
            ])

# Function to get user scripts based on group
def get_user_scripts(group):
    if group == 'control':
        group_dir = 'Control_Group'
    elif group == 'test':
        group_dir = 'Test_Group'
    else:
        raise ValueError("Invalid group specified. Use 'control' or 'test'.")

    return [script for script in os.listdir(group_dir) if script.endswith('.py')]

def main(db, user_scripts, group, document_id):
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
            driver.get("http://localhost:3000/")
            
            # Set iteration directly to 0
            iteration = 4

            presence_time = time.time() - start_time

            metrics["Iteration"].append(iteration)
            metrics["Group"].append(group)
            metrics["User"].append(user_script)
            metrics["Presence time (Seconds)"].append(presence_time)

            print("Iteration:", iteration)  # Print only the current iteration number
            print("Group:", ", ".join(map(str, metrics["Group"])))
            print("User:", ", ".join(map(str, metrics["User"])))
            print("Presence time (Seconds):", ", ".join(map(str, metrics["Presence time (Seconds)"])))


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
            all_metrics[key].extend(value)  # Append to all_metrics, not metrics
        print(f"Metrics collected for user script: {user_script}")

    # Calculate average presence time
    total_presence_time = sum(all_metrics["Presence time (Seconds)"])
    average_presence_time = total_presence_time / len(all_metrics["Presence time (Seconds)"])

  
  


    # Write average presence time to Firestore
    db.collection(u'metrics').document(document_id).update({u"Average_Presence_Time": average_presence_time})
    print("Average Presence Time written to Firestore.")

    # Write all metrics to Firestore with the specified document ID
    write_to_firestore(db, all_metrics, document_id)

    # Write all metrics to a single CSV file named "metrics.csv"
    write_to_csv("metrics.csv", all_metrics)
    print("All metrics recorded and stored successfully in metrics.csv")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Perform A/B testing with dynamic importing')
    parser.add_argument('--group', type=str, required=True, choices=['control', 'test'], help='Specify the group for A/B testing')
    args = parser.parse_args()

    group = args.group

    # Get a list of all user scripts under the specified group directory
    user_scripts = get_user_scripts(group)

    # Initialize Firebase
    db = initialize_firebase()

    # Specify the document ID to write to
    document_id = "finaliteration"

    # Now, pass the user scripts, group, Firebase database, and document ID to the main function
    main(db, user_scripts, group, document_id)
