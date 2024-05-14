import ast
import csv

def calculate_presence_time(file_path):
    total_presence_time = 0
    total_users = 0

    # Read the metrics.csv file
    with open(file_path, mode="r") as fp:
        reader = csv.DictReader(fp)

        # Iterate over each row in the CSV file
        for row in reader:
            try:
                # Extracting the presence time as a list
                presence_time_list = ast.literal_eval(row["Presence time (Seconds)"])
                
                # Converting the list to a float
                presence_time = float(presence_time_list[0])
                
                total_presence_time += presence_time
                total_users += 1
            except (ValueError, SyntaxError) as e:
                print(f"Error: Presence time value is not a valid number. Skipping this row. Error details: {e}")

    # Calculate the average presence time
    if total_users > 0:
        average_presence_time = total_presence_time / total_users
    else:
        average_presence_time = 0

    return total_presence_time, average_presence_time

def main():
    file_path = "metrics.csv"
    total_presence_time, average_presence_time = calculate_presence_time(file_path)

    print("Total Presence Time:", total_presence_time, "seconds")
    print("Average Presence Time per User:", average_presence_time, "seconds")

if __name__ == "__main__":
    main()

