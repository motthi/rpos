import sqlite3
import os


def createAllTables(db_name):
    if(os.path.splitext(db_name)[1] == '.db'):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        createPaper(c, db_name)
        createAffiliations(c, db_name)
        createAuthor(c, db_name)
        createClassification(c, db_name)
        createClassificationManagement(c, db_name)
        createAffiliationManagement(c, db_name)
        createAuthorManagement(c, db_name)
        createClassificationLabelManagement(c, db_name)
        return 1
    else:
        return 0


def createPaper(c, db_name):
    c.execute(
        '''CREATE TABLE Papers(
            id integer primary key not null,
            title text not null,
            year intger,
            filepath text,
            bibtex text,
            doi text,
            description text,
            isread integer not null,
            created_at text not null,
            updated_at text not null
        )'''
    )


def createClassification(c, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE Classifications(
            id integer primary key not null,
            name text not null,
            description text,
            turn integer not null default 0,
            created_at text not null,
            updated_at text not null
        )'''
    )


def createAffiliations(c, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE Affiliations(
            id integer primary key not null,
            name text not null,
            description text,
            attribute text,
            created_at text not null,
            updated_at text not null
        )'''
    )


def createAuthor(c, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE Authors(
            id integer primary key not null,
            name text not null,
            description text,
            affiliation_id integer,
            created_at text not null,
            updated_at text not null
        )'''
    )


def createClassificationManagement(c, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE ClassificationManagements(
            id integer primary key not null,
            paper_id integer not null,
            classification_id integer not null
        )'''
    )


def createAuthorManagement(c, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE AuthorManagements(
            id integer primary key not null,
            paper_id integer not null,
            author_id integer not null
        )'''
    )


def createAffiliationManagement(c, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE AffiliationManagements(
            id integer primary key not null,
            paper_id integer not null,
            affiliation_id integer not null
        )'''
    )


def createClassificationLabelManagement(c, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE ClassificationLabelManagements(
            id integer primary key not null,
            classification_id integer not null,
            sub_classification_id integer not null
        )'''
    )
