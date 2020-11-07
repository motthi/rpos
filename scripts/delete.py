import sqlite3


def deleteTable(db, table):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql = "drop table " + str(table) + ";"
    c.execute(sql)


def deleteAllTable(db):
    tables = [
        'Papers',
        'Authors',
        'Affiliations',
        'Classifications',
        'ClassificationManagements',
        'ClassificationLabelManagements',
        'AffiliationManagements',
        'AuthorManagements'
    ]

    for table in tables:
        deleteTable(db, table)
