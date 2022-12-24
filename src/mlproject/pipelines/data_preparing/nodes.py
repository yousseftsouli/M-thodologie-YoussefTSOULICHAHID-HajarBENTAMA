import texthero as hero
from texthero import preprocessing
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer


def data_preparing_1(df_new : pd.DataFrame):
    custom_pipeline = [preprocessing.fillna, preprocessing.remove_whitespace, preprocessing.remove_urls]
    df_new['description'] = df_new['description'].pipe(hero.clean, custom_pipeline)
    df_new['comments'] = df_new['comments'].pipe(hero.clean, custom_pipeline)
    df_new['tags'] = df_new['tags'].pipe(hero.clean, custom_pipeline)
    analyzer = SentimentIntensityAnalyzer()
    description_analysis = df_new['description'].apply(analyzer.polarity_scores).apply(pd.Series)
    tags_analysis = df_new['tags'].apply(analyzer.polarity_scores).apply(pd.Series)
    comments_analysis = df_new['comments'].apply(analyzer.polarity_scores).apply(pd.Series)
    description_analysis.rename(
        columns={"neg": "des_neg", "neu": "des_neu", "pos": "des_pos", "compound": "des_compound"}, inplace=True)
    comments_analysis.rename(columns={"neg": "com_neg", "neu": "com_neu", "pos": "com_pos", "compound": "com_compound"},
                             inplace=True)
    tags_analysis.rename(columns={"neg": "tag_neg", "neu": "tag_neu", "pos": "tag_pos", "compound": "tag_compound"},
                         inplace=True)

    sentiment_df = pd.concat([description_analysis, comments_analysis, tags_analysis], axis=1)
    cleaned_df = pd.concat([df_new, sentiment_df], axis=1)
    cleaned_df = cleaned_df.drop(["comments", "description", "tags", "title"], axis=1)
    return cleaned_df

def data_preparing_2(df_new : pd.DataFrame):
    df_new['title'] = df_new['title'].pipe(hero.clean, [preprocessing.remove_urls, preprocessing.clean])
    df_new['tags'] = df_new['tags'].pipe(hero.clean, [preprocessing.remove_urls, preprocessing.clean])
    bag_of_words_df = pd.DataFrame()
    TOP_N_WORDS = 10
    for text_column in ['title', 'tags']:
        vec = CountVectorizer(max_features=TOP_N_WORDS)
        txt_to_fts = vec.fit_transform(df_new[text_column]).toarray()
        txt_to_fts.shape

        names = vec.get_feature_names_out()
        #print("Top repeated words for {}:".format(text_column), names)
        txt_fts_names = [text_column + f'_word_{i}_count' for i in range(TOP_N_WORDS)]
        bag_of_words_df[txt_fts_names] = txt_to_fts
        merged_df = pd.concat([df_new, bag_of_words_df], axis=1).drop(["tags", "title"], axis=1)
        return merged_df
