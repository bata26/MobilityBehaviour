import os
import json
import plotly.graph_objects as go
from jsonschema import validate, ValidationError

class CoverageReportGenerator:

    def __init__(self):
        pass

    def generate_chart(self, dataset):

        # Get data from the prepared sessions
        maximum_pressure_ts = []
        minimum_pressure_ts = []
        median_pressure_ts = []
        mean_absolute_deviation_pressure_ts = []
        activity_and_small_scatter = []
        environment_and_small_scatter = []

        # prepare data to build the chart
        for prepared_session in dataset:
            maximum_pressure_ts.append(prepared_session['features']['maximum_pressure_ts'])
            minimum_pressure_ts.append(prepared_session['features']['minimum_pressure_ts'])
            median_pressure_ts.append(prepared_session['features']['median_pressure_ts'])
            mean_absolute_deviation_pressure_ts.append(
                prepared_session['features']['mean_absolute_deviation_pressure_ts'])
            activity_and_small_scatter.append(
                prepared_session['features']['activity_and_small_scatter'])
            environment_and_small_scatter.append(
                prepared_session['features']['environment_and_small_scatter'])

        # Generate radar chart
        categories = ['maximum_pressure_ts','minimum_pressure_ts','median_pressure_ts',
                    'mean_absolute_deviation_pressure_ts', 'activity_and_small_scatter',
                    'environment_and_small_scatter']

        fig = go.Figure()

        # maximum_pressure_ts is used because every list has the same numbers
        # of elements
        for i in range(len(maximum_pressure_ts)):
            fig.add_trace(go.Scatterpolar(
            r=[maximum_pressure_ts[i], minimum_pressure_ts[i], median_pressure_ts[i],
               mean_absolute_deviation_pressure_ts[i], activity_and_small_scatter[i],
               environment_and_small_scatter[i]],
            theta=categories,
            fill='toself',
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                visible=True,
                range=[0, 6]
                )),
            showlegend=False
            )

        chart_path = os.path.join(os.path.abspath('.'), 'data', 'coverage', 'coverage_chart.png')
        # save bar chart in a png image
        try:
            fig.write_image(chart_path)
        except Exception as e:
            print(e)
            print('Failed to save the coverage chart')
            return None

        print('Coverage chart generated')

        # Get the info for the report
        info = dict()
        info['maximum_pressure_ts'] = maximum_pressure_ts
        info['minimum_pressure_ts'] = minimum_pressure_ts
        info['median_pressure_ts'] = median_pressure_ts
        info['mean_absolute_deviation_pressure_ts'] = mean_absolute_deviation_pressure_ts
        info['activity_and_small_scatter'] = activity_and_small_scatter
        info['environment_and_small_scatter'] = environment_and_small_scatter

        return info

    def generate_report(self, info):

        # Handle human interaction
        print("Analize 'coverage_chart.png'")
        print("Answer only 'ok' or 'not ok")
        evaluation = input('> ')
        if evaluation == 'ok':
            info['evaluation'] = 'ok'
        else:
            info['evaluation'] = 'not ok'


        # save a report with the evaluation that a human will make
        report_path = os.path.join(os.path.abspath('.'), 'data', 'coverage',
                                   'coverage_report.json')
        try:
            with open(report_path, "w") as file:
                json.dump(info, file, indent=4)
        except Exception as e:
            print(e)
            print("Failure to save coverage_report.json")
            return False
        return True

    def evaluate_report(self):

        report_path = os.path.join(os.path.abspath('.'), 'data', 'coverage',
                                   'coverage_report.json')
        schema_path = os.path.join(os.path.abspath('.'), 'schemas', 'coverage_report_schema.json')

        # open the report file and validate it
        try:
            with open(report_path) as file:
                report = json.load(file)

            with open(schema_path) as file:
                report_schema = json.load(file)

            validate(report, report_schema)

        except FileNotFoundError:
            print('Failure to open coverage_report.json')
            return -2

        except ValidationError:
            print('Coverage Report has invalid schema')
            return -2

        # Read human evaluation
        evaluation = report['evaluation']

        if evaluation == 'ok':
            print("Coverage evaluation: ok")
            return 0
        elif evaluation == 'not ok':
            print("Coverage evaluation: not ok")
            return -1
        else:
            print("[!] Coverage evaluation non done")
            return -2
        