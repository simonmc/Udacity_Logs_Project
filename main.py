#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Fri Oct 20 19:53:23 2017

@author: simonmcmillan
"""

import psycopg2

DBNAME = "news"

def popular_titles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = """
    select a.title, count(*) 
    from articles as a 
    join newlog as nl on (a.slug=nl.shortpath) 
    where status = '200 OK' 
    group by a.title 
    order by count(*) desc limit 3;
    """
    c.execute(query)
    titles = c.fetchall()
    db.close()
    return titles

def author_count():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = """
    select at.name, count(*) 
    from authors as at 
    join articles as ar on (at.id=ar.author) 
    join newlog as nl on (nl.shortpath=ar.slug) 
    where nl.status='200 OK' group by at.name 
    order by count(*) desc;
    """
    c.execute(query)
    authors = c.fetchall()
    db.close()
    return authors

def high_error_days():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = """
    select to_char(day, 'Month DD, YYYY') 
    from daily_errors 
    where cast((errors*100.0/total) as decimal)>1;
    """
    c.execute(query)
    errordays = c.fetchall()
    db.close()
    return errordays

titles = popular_titles()
authors = author_count()
error_days = high_error_days()

print("Most Popular Titles")
for items in titles:
    print items[0], items[1]

print ""

print("Authors, ranked")
for items in authors:
    print items[0], items[1]

print""

print("Days with high error rate")
for items in error_days:
    print items[0]