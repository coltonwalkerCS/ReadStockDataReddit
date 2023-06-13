from import_stock_data import tickerDS

import nltk
import praw
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


def getKeys():
    with open('/Users/colewalker/Desktop/Random_Code_Projects/Reddit_Stock_Keys/import_items.txt', 'r') as file:
        CLIENT_ID = file.readline()
        SECRET_KEY = file.readline()
        USER_NAME = file.readline()
        PASSWORD = file.readline()
    return CLIENT_ID[:-1], SECRET_KEY[:-1], USER_NAME[:-1], PASSWORD[:-1]


CLIENT_ID, SECRET_KEY, USER_NAME, PASSWORD = getKeys()

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=SECRET_KEY,
    user_agent="StockAPI/0.0.3",
    username=USER_NAME,
    password=PASSWORD
    )


def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    compound_score = sentiment['compound']
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'


def reviewSentiment(post):

    post.comments.replace_more(limit=0)
    comments = post.comments.list()

    sentiment_score = 0
    for comment in comments:
        sentiment = analyze_sentiment(comment.body)
        if sentiment == 'Positive':
            sentiment_score += 1
        elif sentiment == 'Negative':
            sentiment_score -= 1

    return sentiment_score


def getStockInTitle(post, tickerHash):
    words = post.title.split()
    words += post.selftext.split()
    tickerList = []
    for word in words:
        if word[0] == '$':
            if word[-1].isalpha():
                word = word[1:]
            else:
                word = word[1:len(word)-1]
            if tickerHash.hasKey(word):
                tickerList.append(word)
        else:
            if tickerHash.hasKey(word):
                tickerList.append(word)
    return tickerList


def main():
    # Get tickers found on NASDAQ
    tickers = tickerDS('nasdaq_screener_data.csv')

    # Set-up Reddit praw API
    reddit_api = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=SECRET_KEY,
        user_agent="StockAPI/0.0.2",
        username=USER_NAME,
        password=PASSWORD)

    # Give list of usable subreddits to get sentiment from
    subredditList = ["StockMarket", "investing", "wallstreetbets", "SecurityAnalysis", "Daytrading", "options",
                     "InvestmentClub", "Dividends", "finance", "ValueInvesting", "FinancialPlanning",
                     "InvestmentEducation", "StockMarketNoobs", "DividendInvesting"]

    # Go through subreddits to find which stocks are being discussed and their sentiment
    tick_loc = 0
    added_tickers = {}
    tickers_and_sentiment = []

    for subreddit in subredditList:
        print(f"Subreddit : {subreddit}")

        sub = reddit_api.subreddit(subreddit)

        sub_top_posts = sub.top(limit=20, time_filter="day")
        sub_hot_posts = sub.hot(limit=20)
        sub_new_post = sub.new(limit=30)

        allPost = [sub_top_posts, sub_hot_posts, sub_new_post]

        for ind_post in allPost:
            # Go through top post in subreddit
            for post in ind_post:

                # Find the ticker residing in the post
                post_tickers = getStockInTitle(post, tickers)

                sent_score = 0

                # If there exist a ticker, find the sentiment among the post
                if len(post_tickers) > 0:
                    sent_score = reviewSentiment(post)

                # If it is already in the added tickers add its sent_score
                for post_ticker in post_tickers:
                    if post_ticker in added_tickers:
                        tickers_and_sentiment[added_tickers[post_ticker]][1] += sent_score
                    else:
                        added_tickers[post_ticker] = tick_loc
                        tickers_and_sentiment.append([post_ticker, sent_score])
                        tick_loc += 1

    print("Sentiment score of tickers: ")
    for item in tickers_and_sentiment:
        print(f"Ticker {item[0]} w/ score {item[1]}")


if __name__ == '__main__':
    main()
