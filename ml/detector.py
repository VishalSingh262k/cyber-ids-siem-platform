# Importing libraries
import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from analysis.alerts import AlertManager
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


# Defining detector class
class AttackDetector:

    def train_model(self, data):

        # Initialising alert manager
        alert_manager = AlertManager()

        # Printing raw label distribution
        print("\n Raw Label Counts ")
        print(data["Label"].value_counts())

        # Balancing data
        min_samples = data["Label"].value_counts().min()

        data_balanced = (
            data
            .groupby("Label")
            .sample(min_samples, random_state=42)
            .reset_index(drop=True)
        )


        print("\n Balanced Class Distribution ")
        print(data_balanced["Label"].value_counts())

        # Feature selection
        X = data_balanced[
            [
                "Packet_Size_mean",
                "Packet_Size_std",
                "Packet_Size_max",
                "Packet_Size_min",
                "Timestamp_count",
                "Duration",
                "Packet_Rate",
                "Size_Variance_Ratio",
                "Burstiness",
                "Size_Entropy",
                "Rolling_Mean",
                "Out_Ratio"
            ]
        ]


        # Encoding labels
        y = data_balanced["Label"].astype("category").cat.codes

        # Train / Test split
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.25,
            random_state=42,
            stratify=y
        )

        # Ensemble model
        print("\n Using Ensemble IDS Model ")

        # Creating preprocessing pipeline
        preprocess = Pipeline([
            ("imputer", SimpleImputer(strategy="median"))
        ])


        # Base learners with preprocessing
        rf = Pipeline([
            ("prep", preprocess),
            ("clf", RandomForestClassifier(
                n_estimators=400,
                max_depth=25,
                min_samples_leaf=5,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1
            ))
        ])


        gb = Pipeline([
            ("prep", preprocess),
            ("clf", GradientBoostingClassifier(
                n_estimators=200,
                learning_rate=0.05,
                max_depth=5,
                random_state=42
            ))
        ])

        lr = Pipeline([
            ("prep", preprocess),
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(
                max_iter=5000,
                solver="lbfgs"
            ))
        ])


        # Voting ensemble
        model = VotingClassifier(
            estimators=[
                ("rf", rf),
                ("gb", gb),
                ("lr", lr)
            ],
            voting="soft"
        )

        # Training
        model.fit(X_train, y_train)

        # Prediction
        y_pred = model.predict(X_test)

        # Alert generation
        results = pd.DataFrame({
            "Actual": y_test,
            "Predicted": y_pred
        })

        # Reverse label mapping
        label_map = dict(
            enumerate(
                data_balanced["Label"]
                .astype("category")
                .cat.categories
            )
        )

        attack_counts = results["Predicted"].value_counts()

        for attack, count in attack_counts.items():

            attack_name = label_map.get(attack, "Unknown")

            # Do not alert on Benign
            if count > 50 and attack_name != "Benign":

                alert_manager.raise_alert(
                    "Multiple",
                    attack_name,
                    count
                )

        alert_manager.save_alerts()
        
        # Evaluation
        print("\n Multi-Class IDS Report \n")
        report = classification_report(
            y_test,
            y_pred,
            zero_division=0,
            output_dict=True
        )
        print(classification_report(y_test, y_pred, zero_division=0))

        # Save metrics
        metrics = {
            "accuracy": report["accuracy"],
            "macro_f1": report["macro avg"]["f1-score"],
            "precision": report["macro avg"]["precision"],
            "recall": report["macro avg"]["recall"]
        }
        
        with open("data/performance.json", "w") as f:
            json.dump(metrics, f, indent=4)

        return model, X_train