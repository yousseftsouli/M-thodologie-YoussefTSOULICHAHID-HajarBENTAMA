This project aims to predict the dislikes of a youtube video, based on an analysis of the comments, tags and description.

The dataset we used is public on Kaggle : https://www.kaggle.com/datasets/dmitrynikolaev/youtube-dislikes-dataset

These are the criterias that we want to match in our dataset : 
 -We are only interested in the videos published during the year 2021
 -We are only interested in videos that have more than 5000 likes
 -We are only interested in videos that gathered a total of more than 250 000 views during the year 2021
 -We are only interested in videos that have more than 150 dislikes
This way, this scenario is more realistic and close to a real world problem and will help us filter out small and negligible videos.

We are testing different ways to perform the scraping in order to create our own dataset similar to the one on Kaggle used.

Once the dataset is ready, we have used two algorithms to predict the dislikes, first we used Catboost and Sentiment Analysis then bag of words model, at the moment
of writing this text, we have successfuly completed our purpose with the first model and still trying to do it with the second model.
We ultimately aim to compare the accucary of both models and chose the more optimal one.

Finally, we will implement all of this in our own pipeline using kedro.
