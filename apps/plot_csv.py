import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser(description="Read and analyze SNR-BLER data from multiple CSV files.")
    parser.add_argument("csv_files", nargs='+', type=str, help="Paths to CSV files containing SNR-BLER data")
    parser.add_argument("--labels", nargs='+', type=str, help="Labels for each CSV file", default=None)
    return parser.parse_args()

def calculate_95_confidence_interval(data):
    n = len(data)
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)  # ddof=1 for sample standard deviation
    t_value = 1.984  # t-score for 95% confidence interval (for a two-tailed test with n-1 degrees of freedom)
    margin_of_error = t_value * (std_dev / np.sqrt(n))
    return margin_of_error

def main():
    args = parse_args()

    if args.labels and len(args.labels) != len(args.csv_files):
        print("Number of labels should match the number of CSV files.")
        return

    # Define a custom color cycle with red and blue
    colors = ['r', 'b']

    # Initialize dictionaries to store SNR and BLER data
    snr_data = {}
    labels = args.labels or [f"File {i+1}" for i in range(len(args.csv_files))]

    # Read data from the CSV files
    for csv_file, label, color in zip(args.csv_files, labels, colors):
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                snr, bler = float(row[0]), float(row[1])
                if snr not in snr_data:
                    snr_data[snr] = {label: [bler]}
                else:
                    if label not in snr_data[snr]:
                        snr_data[snr][label] = [bler]
                    else:
                        snr_data[snr][label].append(bler)

    # Calculate average and 95% confidence interval for each BLER point
    snr_values = sorted(snr_data.keys())
    plt.figure(figsize=(10, 6))

    for label, color in zip(labels, colors):
        average_bler = []
        confidence_intervals = []

        for snr in snr_values:
            bler_values = snr_data[snr].get(label, [])
            avg = np.mean(bler_values)
            margin_of_error = calculate_95_confidence_interval(bler_values)
            average_bler.append(avg)
            confidence_intervals.append(margin_of_error)

        # Plot the average BLER versus SNR graph with error bars, matching line and marker colors
        plt.errorbar(snr_values, average_bler, yerr=confidence_intervals, fmt='o', capsize=5, label=label, color=color, markeredgecolor=color)
        
        # Draw lines between the points with the same color
        plt.plot(snr_values, average_bler, linestyle='-', color=color, marker='o')

    plt.xlabel('SNR')
    plt.ylabel('Average BLER')
    plt.title('Average BLER vs. SNR with 95% Confidence Intervals')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()

