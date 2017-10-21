# Udacity_Logs_Project

create view newlog as
select substr(path,10)
as shortpath, status, time, id
from log
where path like '/article/%';

create view daily_errors as
select date(date_trunc('day', time)) as day,
cast(sum(1) as int) as total,
cast(sum(Case when status <>'200 OK' then 1 else 0 end) as int) as errors
from log
group by day;


