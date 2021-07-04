![GooglePlay](https://user-images.githubusercontent.com/50144690/124400709-28b86b00-dd57-11eb-930e-5c537919c10e.jpeg)
# Google Play Crawler

A crawler that crawls all applications' data from the Google Play and save it to MySQL.

## Requirements
- Python 3
- MySQL

## Usage

```shell
# Clone this repo
git clone https://github.com/simple1017/google_play_crawler.git

# Switch the directory
cd google_play_crawler

# Install all the package required in this project
pip3 install -r requirements.txt

# Run SQL initial script (There is many way to run this script)
mysql -uroot < init.sql

# Run crawler
scrapy crawl google -s JOBDIR=crawls/google_play
```
