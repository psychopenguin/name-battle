#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import itertools
import random
from config import db


def dbconn():
    return pymysql.connect(host=db['host'],
                           port=db['port'],
                           user=db['user'],
                           password=db['password'],
                           db=db['db'])


def ranking():
    conn = dbconn()
    query = ('select name, points, battles, wins, loses from names '
             'order by points desc, wins desc, loses, battles')
    c = conn.cursor()
    c.execute(query)
    conn.close()
    return c.fetchall()


def getbattle(user):
    conn = dbconn()
    nquery = ('select name from names')
    c = conn.cursor()
    c.execute(nquery)
    names = [n[0] for n in c.fetchall()]
    allbattles = [b for b in itertools.permutations(names, 2)]
    bquery = ('select home, visitor from battles where player = "%s"' % user)
    c.execute(bquery)
    playedbattles = [n for n in c.fetchall()]
    conn.close()
    avaliablebattles = [n for n in allbattles if n not in playedbattles]
    if len(avaliablebattles) > 0:
        return random.choice(avaliablebattles)
    else:
        return False


def setwinner(name):
    conn = dbconn()
    query = ('update names set battles = battles + 1,'
             ' wins = wins + 1, points = points + 1'
             ' where name = "%s"' % name)
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()


def setloser(name):
    conn = dbconn()
    query = ('update names set battles = battles + 1,'
             ' loses = loses + 1, points = points - 1'
             ' where name = "%s"' % name)
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()


def dobattle(battle, player, winner):
    home = battle[0]
    visitor = battle[1]
    if winner == 0:
        loser = visitor
    else:
        loser = home
    conn = dbconn()
    query = ('insert into battles (home, visitor, player, winner)'
             ' values (%s, %s, %s, %s)')
    c = conn.cursor()
    c.execute(query, (home, visitor, player, battle[winner]))
    conn.commit()
    conn.close()
    setwinner(battle[winner])
    setloser(loser)


def isparent(email):
    conn = dbconn()
    query = ('select email from parents where email = "%s"' % email)
    c = conn.cursor()
    c.execute(query)
    conn.close()
    if len(c.fetchall()) > 0:
        return True
    else:
        return False
