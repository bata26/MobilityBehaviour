import os
import json
import plotly.graph_objects as go
from jsonschema import validate, ValidationError

class BalancingReportGenerator:

    def __init__(self):
        pass

    def generate_chart(self, dataset):

        items = ['Shopping', 'Sport', 'Cooking', 'Gaming']
        values = [0,0,0,0]

        # prepare data to build the chart
        for prepared_session in dataset:
            activity = prepared_session['calendar']
            index = None
            if activity == 'shopping':
                index = 0
            elif activity == 'sport':
                index = 1
            elif activity == 'cooking':
                index = 2
            elif activity == 'gaming':
                index = 3

            values[index] += 1

        total_activities = sum(values)
        threshold = 50.0

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=items,
                y=values
            ))
        fig.add_hline(y=threshold)

        # save data just calculated in a dict
        info = dict()
        info['shopping_items_number'] = values[0]
        info['sport_items_number'] = values[1]
        info['cooking_items_number'] = values[2]
        info['gaming_items_number'] = values[3]
        info['shopping_average'] = values[0]/total_activities
        info['sport_average'] = values[1]/total_activities
        info['cooking_average'] = values[2]/total_activities
        info['gaming_average'] = values[3]/total_activities
        info['threshold'] = threshold

        # save bar chart in a png image
        chart_path = os.path.join(os.path.abspath('.'), 'data', 'balancing', 'balancing_chart.png')
        try:
            fig.write_image(chart_path)
        except Exception as e:
            print(e)
            print('Failed to save the balance chart')
            return None

        print('Balance chart generated')
        return info

    def generate_report(self, info):

        # Handle human interaction
        print("Analize 'balancing_chart.png'")
        print("Answer only 'balanced' or 'not balanced'")
        evaluation = input('> ')
        if evaluation == 'balanced':
            info['evaluation'] = 'balanced'
        else:
            info['evaluation'] = 'not balanced'

        # Save the report in a json file
        report_path = os.path.join(os.path.abspath('.'), 'data', 'balancing',
                                   'balancing_report.json')
        try:
            with open(report_path, "w") as file:
                json.dump(info, file, indent=4)
        except Exception as e:
            print(e)
            print('Failure to save balancing_report.json')
            return False

        print('Balancing report generated')
        return True

    def evaluate_report(self):

        report_path = os.path.join(os.path.abspath('.'), 'data', 'balancing',
                                   'balancing_report.json')
        schema_path = os.path.join(os.path.abspath('.'), 'schemas', 'balancing_report_schema.json')

        # open chart and validate it
        try:
            with open(report_path) as file:
                report = json.load(file)

            with open(schema_path) as file:
                report_schema = json.load(file)

            validate(report, report_schema)

        except FileNotFoundError:
            print('Failure to open balancing_report.json')
            return -2

        except ValidationError:
            print('Balancing Report has invalid schema')
            return -2

        # Read human evaluation
        evaluation = report['evaluation']

        if evaluation == 'balanced':
            print("Balancing evaluation: Dataset balanced")
            return 0
        elif evaluation == 'not balanced':
            print("Balancing evaluation: Dataset not balanced")
            return -1

        else:
            print("Balancing evaluation not done")
            return -2
        