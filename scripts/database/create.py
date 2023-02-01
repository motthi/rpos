import sqlite3
import os


def createAllTables(db_name) -> bool:
    if os.path.splitext(db_name)[1] == '.db':
        createPaper(db_name)
        createAffiliations(db_name)
        createAuthor(db_name)
        createClassification(db_name)
        createClassificationManagement(db_name)
        createAffiliationManagement(db_name)
        createAuthorManagement(db_name)
        createClassificationLabelManagement(db_name)
        return True
    else:
        return False


def createPaper(db_name):
    c = sqlite3.connect(db_name).cursor()
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


def createClassification(db_name):
    c = sqlite3.connect(db_name).cursor()
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


def createAffiliations(db_name):
    c = sqlite3.connect(db_name).cursor()
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


def createAuthor(db_name):
    c = sqlite3.connect(db_name).cursor()
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


def createClassificationManagement(db_name):
    c = sqlite3.connect(db_name).cursor()
    c.execute(
        '''CREATE TABLE ClassificationManagements(
            id integer primary key not null,
            paper_id integer not null,
            classification_id integer not null
        )'''
    )


def createAuthorManagement(db_name):
    c = sqlite3.connect(db_name).cursor()
    c.execute(
        '''CREATE TABLE AuthorManagements(
            id integer primary key not null,
            paper_id integer not null,
            author_id integer not null
        )'''
    )


def createAffiliationManagement(db_name):
    c = sqlite3.connect(db_name).cursor()
    c.execute(
        '''CREATE TABLE AffiliationManagements(
            id integer primary key not null,
            paper_id integer not null,
            affiliation_id integer not null
        )'''
    )


def createClassificationLabelManagement(db_name):
    c = sqlite3.connect(db_name).cursor()
    c.execute(
        '''CREATE TABLE ClassificationLabelManagements(
            id integer primary key not null,
            classification_id integer not null,
            sub_classification_id integer not null
        )'''
    )
