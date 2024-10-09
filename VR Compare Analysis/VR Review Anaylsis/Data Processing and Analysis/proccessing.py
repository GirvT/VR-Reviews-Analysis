
import string
import re
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime

import nltk as nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Data Cleaning and Tranformations

def fix_columns(df):
    '''
    Use helper functions to fix the naming scheme of columns, values, and add sentiment
    '''
    df = (
        df.pipe(convert_stars)
        .pipe(convert_date)
    )
    return df

def convert_stars(df):
    df['Stars Given'] = [int(item[6]) for item in df['Stars Given']]
    return df

def relative_time(ago):
    try:
        value, unit = re.search(r'(\d+) (\w+) ago', ago).groups()
        if not unit.endswith('s'):
            unit += 's'
        delta = relativedelta(**{unit: int(value)})
        result = (datetime(2024, 7, 24) - delta)
    except:
        if ago == 'a day ago':
            result = datetime(2024, 7, 23)
        elif ago == 'a week ago':
            result = datetime(2024, 7, 17)
        elif ago == 'a month ago':
            result = datetime(2024, 6, 24)
        else:
            result = datetime(2023, 7, 24)
    return result

def convert_date(df):
    df['Relative Date (from 7/24/2024)'] = [relative_time(date) for date in df['Relative Date']]
    df.rename(columns={'Relative Date (from 7/24/2024)':'Date'}, inplace=True)
    return df


# Data Processing (sentiment and n-grams)

def apply_sentiment(df):
    '''
    Mutate df to include sentiment scores
    We'll use compound scores which are documented here
    https://github.com/cjhutto/vaderSentiment?tab=readme-ov-file#about-the-scoring
    normalized between -1 (negative) to 1 (positive)
    we want to intentionally not perform data cleaning 
    as VADER can glean sentiment from punctuation
    '''
    sid = SentimentIntensityAnalyzer()
    sid_col = df['Review'].apply(lambda x: sid.polarity_scores(x) if x != 'nan' else {'compound':'nan'})
    df['Sentiment'] = [score['compound'] for score in sid_col]
    return df

def apply_preprocessing(df):
    '''
    Perform
        Tokenization
        Stopword Removal
        Non-alphanumeric Removal
    '''
    df['Tokens'] = df['Review'].apply(lambda x: nltk.word_tokenize(x.lower()))
    stop_words = set(stopwords.words('english'))
    df['Filtered_Tokens'] = df['Tokens'].apply(lambda x: [word for word in x if word.isalpha() and word not in stop_words])
    df.head()
    return df

def display_common(df, n = 20):
    '''
    Requires apply_preprocessing
    '''
    all_words = [word for tokens in df['Filtered_Tokens'] for word in tokens]
    word_counts = nltk.Counter(all_words)
    most_common_words = word_counts.most_common(n)
    plt.figure(figsize=(10, 6))
    sns.barplot(x = [count for word, count in most_common_words], 
                y = [word for word, count in most_common_words])
    plt.title('Top '+str(n)+' Most Common Words in Reviews')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.show()

def generate_ngrams(tokens_list, n):
    '''
    helper function for display_ngrams
    '''
    ngrams_list = nltk.ngrams(tokens_list, n)
    ngrams_counts = nltk.Counter(ngrams_list)
    return ngrams_counts

def display_ngrams(df0, n = 2, top = 10):
    '''
    Requires apply_preprocessing
    '''
    df = df0.copy()
    ngrams_count = nltk.Counter()
    df[str(n) + '-grams'] = df['Filtered_Tokens'].apply(lambda x: generate_ngrams(x, n))
    for ngrams_counter in df[str(n) + '-grams']:
        ngrams_count.update(ngrams_counter)
        
    # Most common
    most_common_ngrams = ngrams_count.most_common(top)

    plt.figure(figsize=(10, 6))

    sns.barplot(x = [count for ngram, count in most_common_ngrams],
                y = [' '.join(ngram) for ngram, count in most_common_ngrams])
    plt.title('Top '+str(top)+' Most Common '+str(n)+'-grams in Reviews')
    plt.xlabel('Frequency')
    plt.ylabel(str(n) + '-grams')
    plt.tight_layout()
    plt.show()

def display_wordcloud(df0, n = 2):
    df = df0.copy()
    ngrams_count = nltk.Counter()
    df[str(n) + '-grams'] = df['Filtered_Tokens'].apply(lambda x: generate_ngrams(x, n))
    for ngrams_counter in df[str(n) + '-grams']:
        ngrams_count.update(ngrams_counter)
    word_freq = {' '.join(k): v for k, v in ngrams_count.items()}
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Wordcloud', fontsize=18)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    with open("./CTRLV_reviews.csv", encoding='utf8') as df_CTRLV, open("./levelup_reviews.csv", encoding='utf8') as df_levelup, open("./sandbox_reviews.csv", encoding='utf8') as df_sandbox, open("./VRNOBLE_reviews.csv", encoding='utf8') as df_VRNOBLE, open("./zerolatency_reviews.csv", encoding='utf8') as df_zerolatency:
        def import_helper(fp):
            df = fix_columns(pd.read_csv(fp).astype(str))
            df = df[df['Review'] != 'nan']
            df = (
                df.pipe(apply_sentiment)
                .pipe(apply_preprocessing)
            )
            return df
        #nltk.download('vader_lexicon')
        #nltk.download('punkt')
        #nltk.download('stopwords')
        df_CTRLV = import_helper(df_CTRLV)
        df_levelup = import_helper(df_levelup)
        df_sandbox = import_helper(df_sandbox)
        df_VRNOBLE = import_helper(df_VRNOBLE)
        df_zerolatency = import_helper(df_zerolatency)

        #Average Sentiment
        #print(df.describe())

        #Highest and Lowest Sentiment Reviews
        '''
        sort_df = df.sort_values(by=['Sentiment', 'Stars Given'], ascending=False)
        head_df = sort_df.head(1)
        tail_df = sort_df.tail(1)
        print((list(head_df['Stars Given'])[0], list(head_df['Review'])[0], list(head_df['Date'])[0]))
        print((list(tail_df['Stars Given'])[0], list(tail_df['Review'])[0], list(tail_df['Date'])[0]))
            # By 2024
        sort_df = sort_df[sort_df['Date'] >= datetime(2024, 1, 1)]
        head_df = sort_df.head(1)
        tail_df = sort_df.tail(1)
        print((list(head_df['Stars Given'])[0], list(head_df['Review'])[0], list(head_df['Date'])[0]))
        print((list(tail_df['Stars Given'])[0], list(tail_df['Review'])[0], list(tail_df['Date'])[0]))

        # N-grams
        for df in (df_CTRLV, df_levelup, df_sandbox, df_VRNOBLE, df_zerolatency):
            df_low_stars = df[df['Stars Given'].isin([1, 2])]
            df_high_stars = df[df['Stars Given'].isin([4, 5])]
            display_ngrams(df_low_stars, 1)
            display_ngrams(df_high_stars, 2)
            display_ngrams(df_high_stars, 3)
        '''
        # N-grams
        display_ngrams(df_VRNOBLE, n=3, top=5)

        # Token Comparison
        '''
        def token_helper(df_list):
            return nltk.Counter(x for xs in df_list for x in set(xs))
        
        tokens_CTRLV = token_helper(df_CTRLV['Filtered_Tokens'])
        tokens_levelup = token_helper(df_levelup['Filtered_Tokens'])
        tokens_sandbox = token_helper(df_sandbox['Filtered_Tokens'])
        tokens_VRNOBLE = token_helper(df_VRNOBLE['Filtered_Tokens'])
        tokens_zerolatency = token_helper(df_zerolatency['Filtered_Tokens'])

        def value_by_ten(counterObj):
            for k in counterObj.keys():
                counterObj[k] = counterObj[k] * 10
            return counterObj
        exclude_CTRLV = value_by_ten(tokens_levelup | tokens_sandbox | tokens_VRNOBLE | tokens_zerolatency)
        
        exclude_levelup = value_by_ten(tokens_CTRLV | tokens_sandbox | tokens_VRNOBLE | tokens_zerolatency)
        exclude_sandbox = value_by_ten(tokens_CTRLV | tokens_levelup | tokens_VRNOBLE | tokens_zerolatency)
        exclude_VRNOBLE = value_by_ten(tokens_CTRLV | tokens_levelup | tokens_sandbox | tokens_zerolatency)
        exclude_zerolatency = value_by_ten(tokens_CTRLV | tokens_levelup | tokens_sandbox | tokens_VRNOBLE)

        full_union = tokens_CTRLV | tokens_levelup | tokens_sandbox | tokens_VRNOBLE | tokens_zerolatency

        print((tokens_CTRLV - exclude_CTRLV))
        print((tokens_levelup - exclude_levelup))
        print((tokens_sandbox - exclude_sandbox))
        print((tokens_VRNOBLE - exclude_VRNOBLE))
        print((tokens_zerolatency - exclude_zerolatency))
        print(df_zerolatency[df_zerolatency.Filtered_Tokens.apply(lambda x: 'gloomy' in x)])
        '''
        