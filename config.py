#!/bin/env python
import pymongo
connection = pymogo.MongoClient('10.24.46.56',27017)
db = connection['movie']
col_rate = db.rate
col_base = db.base
