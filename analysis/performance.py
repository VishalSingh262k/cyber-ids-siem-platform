# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt

# Defining performance analyzer
class PerformanceAnalyzer:

    def analyze(self, file_path):

        # Loading logs
        df = pd.read_csv(file_path)

        # Plotting traffic volume
        df.groupby("Timestamp").size().plot()

        plt.title("Network Traffic Over Time")
        plt.xlabel("Time")
        plt.ylabel("Packets")

        plt.show()
