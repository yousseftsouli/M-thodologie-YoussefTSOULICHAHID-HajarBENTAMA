"""
This is a boilerplate pipeline 'models_implementation'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import catboost, bag_of_words


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([

        node(
            func=catboost,
            inputs=["youtube_dataset_prepared"],
            outputs="catboostregressormodel",
            name="catboost"
        ),

        node(
            func=bag_of_words,
            inputs=["youtube_dataset_prepared"],
            outputs="bag_of_words_model",
            name="bag_of_words"
        ),

    ])
