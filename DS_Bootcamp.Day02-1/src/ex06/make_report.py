import os
import sys

from analytics import *
from config import NUM_OF_STEPS, REPORT_FILENAME, REPORT_TEMPLATE


def make_report(
    total,
    tails,
    heads,
    tails_percent,
    heads_percent,
    steps,
    predicted_tails,
    predicted_heads,
):
    report_data = REPORT_TEMPLATE.format(
        total=total,
        tails=tails,
        heads=heads,
        tails_percent=tails_percent,
        heads_percent=heads_percent,
        steps=steps,
        predicted_tails=predicted_tails,
        predicted_heads=predicted_heads,
    )
    analytics = Research.Analytics(report_data)
    analytics.save_file(REPORT_FILENAME, "txt")


def main():
    try:
        if len(sys.argv) == 2:
            researcher = Research(sys.argv[1])
            file = researcher.file_reader()

            calculator = Research.Calculations(file)
            counts = calculator.counts()
            fractions = calculator.Fractions()
            total = sum(counts)
            tails = counts[0]
            heads = counts[1]
            tails_percent = fractions[0]
            heads_percent = fractions[1]
            steps = NUM_OF_STEPS

            analytics = Research.Analytics(file)
            prediction_data = analytics.predict_random(steps)
            predictor_calculator = Research.Calculations(prediction_data)
            prediction_counts = predictor_calculator.counts()
            predicted_tails = prediction_counts[0]
            predicted_heads = prediction_counts[1]
            make_report(
                total,
                tails,
                heads,
                tails_percent,
                heads_percent,
                steps,
                predicted_tails,
                predicted_heads,
            )

        else:
            raise ValueError("Incorrect input. Check exmaple: first_child.py data.csv")
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except ValueError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
