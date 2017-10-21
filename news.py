#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Fri Oct 20 19:53:23 2017

@author: simonmcmillan

with thanks to Anon @ Udacity Reviewer for guidance on avoiding code repetition
"""

import sys
import psycopg2

DBNAME = "news"

article_query = """
    select a.title, count(*)
    from articles as a
    join newlog as nl on (a.slug=nl.shortpath)
    where status = '200 OK'
    group by a.title
    order by count(*) desc limit 3;
    """

author_query = """
    select at.name, count(*)
    from authors as at
    join articles as ar on (at.id=ar.author)
    join newlog as nl on (nl.shortpath=ar.slug)
    where nl.status='200 OK' group by at.name
    order by count(*) desc;
    """

error_query = """
    select to_char(day, 'DD-MON-YYYY'),
    round(cast((errors*100.0/total) as decimal),2)
    from daily_errors
    where cast((errors*100.0/total) as decimal)>1;
    """


def connectdb(database_name):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error:
        print "Unable to connect to database"
        sys.exit(1)


def runquery(query):
    db, c = connectdb(DBNAME)
    c.execute(query)
    queryresult = c.fetchall()
    db.close()
    return queryresult


def print_results(query_type, query):
    results = runquery(query)
    print query_type
    for items in results:
        print items[0], items[1]
    print ""


if __name__ == '__main__':
    print_results("Top Articles", article_query)
    print_results("Top Authors", author_query)
    print_results("High Error Days", error_query)
