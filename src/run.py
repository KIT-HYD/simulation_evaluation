import os
from datetime import datetime as dt
from time import time
from pathlib import Path

from json2args import get_parameter
from json2args.data import get_data_paths
from json2args.logger import logger


from evaluation import process_all, load_data, create_output

# parse parameters
kwargs = get_parameter(typed=True)
datapaths = get_data_paths()

# check if a toolname was set in env
toolname = os.environ.get('TOOL_RUN', 'simulation_evaluation').lower()

# switch the tool
if toolname == 'simulation_evaluation':
    logger.info("#TOOL START - simulation evaluation")
    logger.debug(f"Passed parameters: {kwargs}")
    start = time()

    data_dir = Path(datapaths["simulation_data"])
    data = load_data(data_dir, kwargs.index_column) 
    data_names = list(data.keys())
    logger.debug(f"Found {len(data)} datasets in the {data_dir} folder: [{','.join(data_names)}]")

    catchment_plots, catchment_tables, catchment_metrics = process_all(data)  # Capture return values

    create_output(data_names, catchment_plots, catchment_tables, catchment_metrics)
    
    logger.info(f"#TOOL FINISHED")
    logger.info(f"total runtime: {time() - start:.2f} seconds.")
    

# In any other case, it was not clear which tool to run
else:
    raise AttributeError(f"[{dt.now().isocalendar()}] Either no TOOL_RUN environment variable available, or '{toolname}' is not valid.\n")
