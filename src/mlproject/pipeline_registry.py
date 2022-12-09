"""Project pipelines."""
from typing import Dict

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from .pipelines import data_processing as dp, data_preparing as dpre, models_implementation as mi


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """

    data_processing = dp.create_pipeline()
    data_preparing = dpre.create_pipeline()
    models_implementation = mi.create_pipeline()
    return {
        "__default__": data_processing + data_preparing + models_implementation,
        "dp": data_processing,
        "dpre": data_preparing,
        "mi": models_implementation
    }
