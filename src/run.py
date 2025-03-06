import os
from datetime import datetime as dt
from time import time
from pathlib import Path

from json2args import get_parameter
from json2args.data import get_data_paths
from json2args.logger import logger

from evaluation import process_all, load_data, create_output

# parse parameters with correct section
kwargs = get_parameter(section="simulation_evaluation", typed=True)
datapaths = get_data_paths(section="simulation_evaluation")

# check if a toolname was set in env
toolname = os.environ.get('TOOL_RUN', 'simulation_evaluation').lower()

# switch the tool
if toolname == 'simulation_evaluation':
    logger.info("#TOOL START - simulation evaluation")
    logger.debug(f"Passed parameters: {kwargs}")
    start = time()

    # Handle simulation and observation data paths
    sim_data_dir = Path(datapaths.get("simulation_data", ""))  # Ensures it returns a valid Path
    obs_data_dir = Path(datapaths.get("observation_data", "")) if "observation_data" in datapaths else None

    # Load data explicitly using provided parameters
    data = load_data(
        simulation_path=sim_data_dir,
        observation_path=obs_data_dir,
        index_column=kwargs.index_column,
        observation_column=kwargs.observation_column,
        simulation_column=kwargs.simulation_column
    )
    
    data_names = list(data.keys())
    logger.debug(f"Found {len(data)} datasets in the {sim_data_dir} folder: [{', '.join(data_names)}]")

    # Process data
    catchment_plots, catchment_tables, catchment_metrics = process_all(data)

    # Create output
    create_output(data_names, catchment_plots, catchment_tables, catchment_metrics)
    
    logger.info("#TOOL FINISHED")
    logger.info(f"total runtime: {time() - start:.2f} seconds.")

else:
    raise AttributeError(f"[{dt.now().isocalendar()}] Either no TOOL_RUN environment variable available, or '{toolname}' is not valid.\n")
