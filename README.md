# stockly (DS Backend)

### Prerequisites 

```
cd /some/directory/on/your/computer
git clone (giturlhere)
cd (path/to/stockly)
pip install requirements.txt
```

### Known Issues 

##### Please feel free to open pull requests if you have **any** ideas or solutions to the issues I will present below:

1. Issue with concurrency and assigning tasks / jobs to workers in a Redis queue. 

2. Problem with migrating databases with Postgres RDS (Not sure if this is an actual problem since tweets are only added if the ticker does not exist in the database)


### TODO:

1. Redis Queue for jobs

2. Faster JSON responses

3. Create Dockerfile for development purposes (probably not)

4. Write more documentation

### Historical/Future Usage

```python
from preprocess import Magic

# insert stock ticker to instantiate Historical object.

tesla = Magic('TSLA')

# two endpoint methods that return a dictionary of softmax scores in format:
# {'Sell': 0.25, 'Hold': 0.5, 'Buy': 0.25}

# first method :output_historical:

historical = tesla.output_historical()
print(historical)

# second method :output_future:

future = tesla.output_future()
print(future)
```
### TwitterSentiment Usage

```python
from sentiment import TwitterSentiment

# same as above

tesla = TwitterSentiment('TSLA')

twitter_sentiment = tesla.output_twitter()
print(twitter_sentiment)

# should display :
# {'Sell': 0.1, 'Hold': 0.3, 'Buy': 0.6}
```
