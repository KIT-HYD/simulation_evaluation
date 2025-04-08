from pathlib import Path
import json
import subprocess
import shutil

from jinja2 import FileSystemLoader, Environment


def create_output_resources(data_names, catchment_plots, catchment_metrics):
    report_src = Path('.') / "report" / "src"
    report_lib = report_src / "lib"

    with open(report_lib / "plot_data.js", "w") as f:
        f.write(f"export const plots = {json.dumps(catchment_plots, indent=4)}")

    with open(report_lib / "report_data.js", "w") as f:
        f.write(f"export const metrics = {json.dumps(catchment_metrics, indent=4)};\n\nexport const names = {json.dumps(data_names)};\n\n")

def build_report():
    report_src = Path('.') / "report"

    subprocess.run(["npm", "install"], cwd=report_src)
    subprocess.run(["npm", "run", "build"], cwd=report_src)

    shutil.copy(report_src / "build" / "index.html", "/out/simulation_report.html")



def create_output(data_names, catchment_plots, catchment_tables, catchment_metrics):
    templateLoader = FileSystemLoader('./templates')
    env = Environment(loader=templateLoader)
    
    json_plots = json.dumps(catchment_plots)
    json_tables = json.dumps(catchment_tables)
    json_metrics = json.dumps(catchment_metrics)
    
    template = env.get_template('default.html')
    html_content = template.render(data_names=data_names, json_plots=json_plots, json_tables=json_tables, json_metrics=json_metrics)
    
    with open("/out/output.html", "w") as f:
        f.write(html_content)
