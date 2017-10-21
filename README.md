# Udacity_Logs_Project

news.py analyses the news database and returns details about the most popular
articles, ranks the authors and identifies days wehre the http error rate 
exceeded 1%

## Pre-requisites

Please ensure the following views are added to the database before running

```
create view newlog as
select substr(path,10)
as shortpath, status, time, id
from log
where path like '/article/%';
```

```
create view daily_errors as
select date(date_trunc('day', time)) as day,
cast(sum(1) as int) as total,
cast(sum(Case when status <>'200 OK' then 1 else 0 end) as int) as errors
from log
group by day;
```

## Usage

python news.py

## Output

news.py will output a file _loganalysis.txt_

###  Code Explanation 

news.py uses the psycopg2 library. It uses 3 functions, each of which makes a 
select query on the news database. The content from each is of these is stored
in a list and then output to _loganalysis.txt_
