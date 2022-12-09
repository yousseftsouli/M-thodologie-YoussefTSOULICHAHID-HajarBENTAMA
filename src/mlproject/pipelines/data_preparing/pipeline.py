"""
This is a boilerplate pipeline 'data_preparing'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import data_preparing_1


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([

        node(
            func=data_preparing_1,
            inputs=["youtube_dataset_final"],
            outputs="youtube_dataset_prepared",
            name="data_preparing_1"
        ),


    ])
