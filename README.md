# News-fetching-api

This program is made for screening task of dendrite ai by Neeraj Pratap Hazarika

# Steps to install

- clone repo
- create virtual enviroment with python3
- install dependencies from requirements.txt

# Steps to run

- open a new terminal 
- install redis server using command `sudo apt install redis-server`
- start redis server using command `redis-server`
- open another terminal
- change working directory to news-fetching-api
- activate your virtual enviroment that you created using `source {your_enviroment_name}/bin/activate` command
- start worker process with `rq worker` command
- open a new terminal and activate virtual enviroment by changing working directory to new-fetching-api
- start the python program with `flask run`
- server should be running at port 5000

# steps to fetch news

- open browser or postman
- in browser write "http://localhost:5000/fetchNews?tickerInput=msft" along with ticker input query (eg : msft = microsoft)
- open a new terminal and enter command `redis-cli` to access redis database
- enter command `KEYS '*'` to get a list of all the keys in the database
- enter `smembers "msft"` (example) to get list of 8 news article of that particular stock from NASDAQ RSS news feed

# TASK GIVEN ( AS INTERPRETTED BY ME)

- given a company symbol (ticker input) fetch its new feed
- store list of articles in cache (REDDIS) (Running as docker)
- data stored format, key : company symbol, value : list of articles with time stamps
- this program needs to run via api and must be a background process (non blocking api call)
- use queue to put the task on, and then a call back triggered when job is completed

# TASK LEFT TO DO

- run REDDIS in docker (I was getting error as containerized reddis wasnt able to communicate with python api)
- add time stamps along with news article (will try this now and update the code once i do complete it)
- task added to queue are in the same reddis cache as key-value of pair ticker input and it's news article (should I seperate it?)
- query made through api can be made more dynamic by allowing users to query number of articles along with ticker input

# SCREENSHOTS

![Screenshot 2022-06-16 222225](https://user-images.githubusercontent.com/72177954/174124992-329f779e-d41c-4852-b5b3-fb0a636fc447.jpg)

![Screenshot 2022-06-16 222131](https://user-images.githubusercontent.com/72177954/174124819-b415f7b3-a5a1-4aca-ab21-0ff033684d60.jpg)
