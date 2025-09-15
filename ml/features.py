# Importing libraries
import pandas as pd
import numpy as np


# Defining feature extractor
class FeatureExtractor:

    def extract_features(self, file_path):

        # Loading raw logs
        df = pd.read_csv(file_path)

        # Creating time windows (3-second windows)
        df["Window"] = (df["Timestamp"] // 3).astype(int)

        # Entropy of packet sizes
        def calculate_entropy(series):

            probs = series.value_counts(normalize=True)

            return -np.sum(probs * np.log2(probs + 1e-9))

        # Entropy of packet sizes
        entropy_series = df.groupby(
            ["Source", "Window"]
        )["Packet_Size"].apply(calculate_entropy)


        # Rolling mean (temporal trend)
        rolling = (
            df.groupby("Source")["Packet_Size"]
              .rolling(window=5, min_periods=1)
              .mean()
              .reset_index(level=0, drop=True)
        )

        df["Rolling_Mean"] = rolling.values

        # Rolling mean (temporal trend)
        rolling_series = df.groupby(
            ["Source", "Window"]
        )["Rolling_Mean"].mean()

        # Direction ratio 
        if "Direction" in df.columns:

            dir_ratio = df.groupby(
                ["Source", "Window"]
            )["Direction"].apply(
                lambda x: (x == "OUT").mean()
            )

        else:
            # Fallback
            dir_ratio = None
        
        # Aggregated flow features
        features = df.groupby(
            ["Source", "Window"]
        ).agg({

            "Packet_Size": ["mean", "std", "max", "min"],

            "Timestamp": ["count", "max", "min"],

            "Attack_Type": lambda x: x.value_counts().idxmax()
        })

        # Flattening columns
        features.columns = [
            "_".join(col).strip()
            for col in features.columns
        ]

        # Renaming label
        features = features.rename(
            columns={"Attack_Type_<lambda>": "Label"}
        )

        # Resetting index
        features = features.reset_index()

        # Flow duration
        features["Duration"] = (
            features["Timestamp_max"] -
            features["Timestamp_min"]
        )


        # Packet rate
        features["Packet_Rate"] = (
            features["Timestamp_count"] /
            (features["Duration"] + 1e-6)
        )


        # Size variance ratio
        features["Size_Variance_Ratio"] = (
            features["Packet_Size_std"] /
            (features["Packet_Size_mean"] + 1e-6)
        )


        # Burstiness
        features["Burstiness"] = (
            features["Packet_Size_max"] /
            (features["Packet_Size_mean"] + 1e-6)
        )

        # Adding entropy
        features["Size_Entropy"] = entropy_series.values


        # Adding rolling mean
        features["Rolling_Mean"] = rolling_series.values


        # Adding direction ratio
        if dir_ratio is not None:
            features["Out_Ratio"] = dir_ratio.values
        else:
            features["Out_Ratio"] = 0.5


        # Debug output
        print("\nFeature Columns ")
        print(features.columns)

        # Handling remaining NaN safely
        features = features.fillna(0)

        return features
