import sqlite3
import datetime


def insertPaper(db_name, title, year, filepath, bibtex, doi, description):
    if(title != '' and title != None):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        value = "('" + str(title) + "', " + str(year) + ", '" + str(filepath) + "', '" + str(bibtex) + "', '" + str(doi) + "', '" + \
            str(description) + "', 0, '" + str(datetime.datetime.now()) + \
            "', '" + str(datetime.datetime.now()) + "')"
        c.execute(
            "INSERT INTO Papers(title, year, filepath, bibtex, doi, description, isread, created_at, updated_at) VALUES " + value)
        conn.commit()
        return 1
    else:
        return 0


def insertAuthor(db_name, name, description, affiliation_id):
    if(name != '' and name != None):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        value = "('" + str(name) + "', '" + str(description) + "', " + str(affiliation_id) + \
            ", '" + str(datetime.datetime.now()) + "', '" + \
            str(datetime.datetime.now()) + "')"
        c.execute(
            "INSERT INTO Authors(name, description, affiliation_id, created_at, updated_at) VALUES " + value)
        conn.commit()
        return 1
    else:
        return 0


def insertClassification(db_name, name, description):
    if(name != '' and name != None):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        value = "('" + str(name) + "', '" + str(description) + "', '" + str(datetime.datetime.now()) + "', '" + \
            str(datetime.datetime.now()) + "')"
        c.execute(
            "INSERT INTO Classifications(name, description, created_at, updated_at) VALUES " + value)
        conn.commit()
        return 1
    else:
        return 0


def insertAffiliation(db_name, name, description, attribute):
    if(name != '' and name != None):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        value = "('" + str(name) + "', '" + str(description) + "', '" + str(attribute) + \
            "', '" + str(datetime.datetime.now()) + "', '" + \
            str(datetime.datetime.now()) + "')"
        c.execute(
            "INSERT INTO Affiliations(name, description, attribute, created_at, updated_at) VALUES " + value)
        conn.commit()
        return 1
    else:
        return 0


def insertClassificationManagement(db_name, paper_id, classificatoin_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    value = "('" + str(paper_id) + "', '" + str(classificatoin_id) + "')"
    c.execute(
        "INSERT INTO ClassificationManagements(paper_id, classification_id) VALUES " + value)
    conn.commit()
    return 1


def insertClassificationLabelManagement(db_name, classification_id, sub_classification_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    value = "('" + str(classification_id) + "', '" + \
        str(sub_classification_id) + "')"
    c.execute(
        "INSERT INTO ClassificationLabelManangements(classification_id, sub_classification_id) VALUES " + value)
    conn.commit()
    return 1


def insertAuthorManagement(db_name, paper_id, author_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    value = "('" + str(paper_id) + "', '" + \
        str(author_id) + "')"
    c.execute(
        "INSERT INTO AuthorManagements(paper_id, author_id) VALUES " + value)
    conn.commit()
    return 1


def insertAffiliationManagement(db_name, paper_id, affiliation_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    value = "('" + str(paper_id) + "', '" + \
        str(affiliation_id) + "')"
    c.execute(
        "INSERT INTO AffiliationManagements(paper_id, affiliation_id) VALUES " + value)
    conn.commit()
    return 1
