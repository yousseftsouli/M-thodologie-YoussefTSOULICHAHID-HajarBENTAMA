"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import preprocessing_date, preprocessing_final


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=preprocessing_date,
            inputs=["youtube_dataset"],
            outputs="youtube_dataset_processed",
            name="preprocessing_date"
        ),
        node(
            func=preprocessing_final,
            inputs=["youtube_dataset_processed"],
            outputs="youtube_dataset_final",
            name="preprocessing_final"
        ),

    ])
