#!/usr/bin/env python3

from string import ascii_letters, digits
from itertools import chain
from random import choice
import os
import sqlite3


def save(uid=None, code=None, language=None):
    if uid is None:
        code = '# Write your code here...'
        with sqlite3.connect('code.sqlite3') as c:
            curs = c.cursor()
            curs.execute('INSERT INTO code(code,language) VALUES(?,?)',
                        (code, language))
            c.commit()
    else:
        with sqlite3.connect('code.sqlite3') as c:
            curs = c.cursor()
            curs.execute('UPDATE code SET code = ?, language = ? WHERE id = ?',
                        (code, language, uid))
            c.commit()
    return curs.lastrowid


def read(id):
    with sqlite3.connect('code.sqlite3') as c:
        curs = c.cursor()
        curs.execute('SELECT code, language FROM code WHERE id = ? LIMIT 1',
                    id)
        record = curs.fetchone()
        return {'code': record[0], 'language': record[1]}


def getAll():
    d = []
    with sqlite3.connect('code.sqlite3') as c:
        curs = c.cursor()
        curs.execute('SELECT id, code FROM code ORDER BY id DESC LIMIT 10')
        for data in curs.fetchall():
            d.append({'uid': data[0], 'code': data[1]})
        return d