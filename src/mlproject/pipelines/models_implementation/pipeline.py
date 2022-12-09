"""
This is a boilerplate pipeline 'models_implementation'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import catboost


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([

        node(
            func=catboost,
            inputs=["youtube_dataset_prepared"],
            outputs="catboostregressormodel",
            name="catboost"
        ),

    ])
