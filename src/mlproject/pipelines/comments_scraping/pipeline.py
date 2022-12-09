"""
This is a boilerplate pipeline 'comments_scraping'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import get_video_info_by_id, request_loop, process_one_list


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
                func=request_loop,
                inputs=["params:video_ids", "params:youtube_data"],
                outputs="iter_num",
                name="request_loop"
            ), 
               
        node(
                func=process_one_list,
                inputs="params:ytb_data",
                outputs="final_data",
                name="process_one_list"
            ),  
    ])
