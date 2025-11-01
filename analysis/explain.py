# Importing libraries
import shap
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier


class ExplainabilityEngine:

    def explain_model(self, model, X_train):

        print("\n Generating SHAP Explanation ")

        rf_model = None
        preprocessor = None


        print("\n Ensemble Members ")

        for name, estimator in model.estimators_:

            print(f" - {estimator}: {type(estimator)}")

            # Case 1: Pipeline
            if isinstance(estimator, Pipeline):

                steps = estimator.steps

                last_step = steps[-1][1]

                if isinstance(last_step, RandomForestClassifier):

                    rf_model = last_step

                    # Save preprocessor if exists
                    if len(steps) > 1:
                        preprocessor = steps[0][1]

                    break


            # Case 2: Raw RandomForest
            if isinstance(estimator, RandomForestClassifier):

                rf_model = estimator
                break


        # Safety check
        if rf_model is None:

            print("\nRandomForest not found. SHAP skipped.")
            return


        print("\nRandomForest found for SHAP.")


        # Preprocess if needed
        if preprocessor is not None:

            print("Applying preprocessing before SHAP...")

            X_used = preprocessor.transform(X_train)

        else:

            X_used = X_train


        # Creating SHAP explainer
        explainer = shap.TreeExplainer(rf_model)


        # Computing SHAP values
        shap_values = explainer.shap_values(X_used)


        # Plotting
        shap.summary_plot(
            shap_values,
            X_used,
            show=False
        )


        # Saving
        plt.savefig("data/shap_summary.png", dpi=300)

        print("\nSHAP saved: data/shap_summary.png")
