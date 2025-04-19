#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NSQL - Lightweight MySQL Wrapper for Python

Project: MySQL-Wrapper
Author: WYT
Created: 2025/4/20
Version: 0.1.497
GitHub: https://github.com/GVSADS/NSQL/

Copyright (c) 2023 [WYT/GVSDS]. All rights reserved.

License: MIT License

Description:
A thread-safe Python wrapper for PyMySQL with enhanced features
including SQL injection protection, automatic type conversion
and debug mode support.

Dependencies:
- PyMySQL >= 1.0.0
- Python >= 3.6
"""

import threading
import pymysql
import binascii
import traceback
import json
import re

class Light():
    def __init__(self):
        self.conn = pymysql.Connection
class Disposes():
    def __init__(self):
        pass
    def _PK(self, a=(None), k={None}):
        _ = ""
        for i in a:
            _ += "%s," % self._PS(i)
        _ = _[:-1]
        return _
    def _PS(self, s):
        if isinstance(s, _Func):
            return str(s)
        elif type(s) == str:
            return "'%s'" % pymysql.converters.escape_string(s)
        elif type(s) == bytes:
            return Func.insertbytes(s)
        else:
            return "%s" % s
    def _PR(self, _, head):
        if _ == None:
            return {}
        return _ if head[1] == "text" else int(_) if head[1] == "int" else float(_) if head[1] == "float" else json.loads(_) if head[1] == "json" else _
Disposes = Disposes()
class MySQL():
    def __init__(self, host, port, charset="utf8", debug=False):
        self.host, self.port, self.charset, self.debug = host, port, charset, debug
        self.Lock = threading.Lock()
    def __login__(self, user, passwd):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=user, passwd=passwd, charset=self.charset)
        self.conn.connect_timeout = 1000000000000
    class NewCursor():
        def __init__(self, parent: Light) -> None:
            self.parent = parent
            self.conn = self.parent.conn
            self.cursor = self.parent.conn.cursor()
            self.debug = self.parent.debug
            self.Table = None
            self.db = None
        def to_connect(self):
            print("Server DisConnect")
        def __run_sql__(self, sql, args=()):
            try:
                if self.debug:
                    print("SQL [%s] [%s]: %s" % (self.db, self.Table, sql))
                    print("Params:", args)
                self.parent.Lock.acquire()
                if self.db: self.cursor.execute("USE `%s`" % self.db)
                self.cursor.execute(sql, args)
                self.conn.commit()
                return self.cursor.fetchall()
            except Exception as e:
                if isinstance(e, pymysql.err.InterfaceError):
                    self.conn = self.to_connect()
                    print(traceback.format_exc())
                    return False
                if self.conn and self.debug:
                    print(traceback.format_exc())
                return False
            finally:
                self.parent.Lock.release()
        def is_valid_identifier(self, identifier):
            return re.match(r"^[a-zA-Z0-9_]+$", identifier) is not None
        def use(self, db, Table=None):
            if not self.is_valid_identifier(db):
                raise ValueError("Invalid database name")
            self.Table = Table
            self.db = db
            return self.__run_sql__("USE `%s`" % db)
        def __ChanceFrom__(self, FROM):
            return FROM if FROM else self.Table
        def __add_fin__(self, FROM=None, WHERE=None, _limit=None):
            FROM = self.__ChanceFrom__(FROM)
            from_clause = f"FROM `{FROM}`" if FROM else ""
            where_clause = ""
            where_params = ()
            if WHERE is not None:
                if isinstance(WHERE, tuple):
                    if len(WHERE) != 2:
                        raise ValueError("WHERE IS DICT: (condition_template, params)")
                    where_cond, where_params = WHERE[0], WHERE[1]
                    where_clause = f"WHERE {where_cond}"
                elif isinstance(WHERE, str):
                    where_clause = f"WHERE {WHERE}"
                else:
                    raise TypeError("WHERE BE MUST DICT OR VALUE")
            limit_clause = f"LIMIT {_limit}" if _limit else ""
            if not isinstance(where_params, tuple):
                where_params=(where_params,)
            return (
                f"{from_clause} {where_clause} {limit_clause}".strip(),
                where_params
            )
        def __load_sql__(self, run, _table, FROM=None, WHERE=None, _limit=None):
            clauses, where_params = self.__add_fin__(FROM, WHERE, _limit)
            full_sql = f"{run} {_table} {clauses}"
            return self.__run_sql__(full_sql, where_params)
        def delete(self, FROM=None, WHERE=None):
            return self.__load_sql__("DELETE", "", FROM, WHERE)
        def insert(self, _Table, values=None, WHERE=None, **k):
            if values is None:
                values = k
            elif k:
                raise ValueError("CAN'T SET VALUE AND KEY AT SAME TIME")
            columns = []
            params = []
            for key, value in values.items():
                if not self.is_valid_identifier(key):
                    raise ValueError(f"EKEY: {key}")
                columns.append(key)
                params.append(value)
            columns_str = ", ".join([f"`{col}`" for col in columns])
            placeholders = ", ".join(["%s" if not isinstance(v, _Func) else str(v) for v in params])
            clauses, clause_params = self.__add_fin__(WHERE=WHERE)
            sql = f"INSERT INTO `{_Table}` ({columns_str}) VALUES ({placeholders}) {clauses}"
            return self.__run_sql__(sql, tuple(v for v in params if not isinstance(v, _Func)) + clause_params)
        def show(self, _Table, FROM=None, WHERE=None):
            return self.__load_sql__("SHOW", _Table, FROM, WHERE)
        def select(self, _Table, FROM=None, WHERE=None, _limit=None):
            if (res := self.__load_sql__("SELECT", _Table, FROM, WHERE, _limit)):
                head=self.show(MOD.COLUMNS,FROM=FROM)
                tables=[]
                heads=[]
                for _ in head:
                    heads.append(_[0])
                if _Table not in heads:
                    for i in res:
                        mr=[]
                        for s, _ in enumerate(i):
                            mr.append(Disposes._PR(_,head[s]))
                        tables.append(mr)
                    return tables
                else:
                    for i in head:
                        if i[0] == _Table:
                            return Disposes._PR(res[0][0],i)
                    return False
            return res
        def selectashead(self, _Table, FROM=None, WHERE=None, _limit=None):
            if (res := self.__load_sql__("select", _Table, FROM, WHERE, _limit)):
                head = self.show(MOD.COLUMNS, FROM=FROM)
                tables = []
                for i in res:
                    mr = {}
                    for s, _ in enumerate(i):
                        mr[head[s][0]] = Disposes._PR(_, head[s])
                    tables.append(mr)
                return tables
            return res
        def update(self, WHERE, FROM=None, **k):
            set_fields = []
            set_params = []
            for key, value in k.items():
                set_fields.append(f"{key}=%s")
                set_params.append(value)
            where_clause, where_params = self.__add_fin__(WHERE=WHERE)
            all_params = tuple(set_params) + where_params
            sql = f"UPDATE `{FROM}` SET {', '.join(set_fields)} {where_clause}"
            return self.__run_sql__(sql, all_params)
        def insertasdict(self, _dict, TableName, WHERE=None):
            self.insert(TableName, values=_dict, WHERE=WHERE)
        def istrue(self, FROM=None, WHERE=None):
            return bool(self.select(1, FROM=FROM, WHERE=WHERE, _limit=1))
class MOD():
    ALL = "*"
    FROM = "FROM"
    WHERE = "WHERE"
    CREATE = "CREATE"
    TABLE = "TABLE"
    COLUMNS = "COLUMNS"
class _Func(str):
    def __init__(self, s):
        str.__init__(self)
class Func():
    @staticmethod
    def NOW():
        return _Func("NOW()")
    @staticmethod
    def JSON_ARRAY(*a):
        return _Func("JSON_ARRAY(%s)" % Disposes._PK(a))
    @staticmethod
    def LOAD_FILE(path):
        return _Func("LOAD_FILE('%s')" % path)
    @staticmethod
    def UNHEX(s):
        return _Func("UNHEX('%s')" % s)
    @staticmethod
    def insertbytes(s, charset: str = ""):
        return _Func("0x%s" % binascii.hexlify(s).decode() if type(s) == bytes else binascii.hexlify(str(s).encode(charset)).decode())
    @staticmethod
    def insert16(s):
        return _Func("0x%s" % s)