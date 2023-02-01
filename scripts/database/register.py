import sys
sys.path.append("./scripts")
import re
from scripts.database.database import Paper, Author, AuthorManagement


def registerByBibtex(db_name, bibtex, file, description=None, doi=None, isread=0):
    """[summary]

    Args:
        db_name (string): [description]
        bibtex (string): [description]

    Returns:
        flag: Success 1, Failed 0
    """
    try:
        p = Paper(db_name)
        a = Author(db_name)
        a_management = AuthorManagement(db_name)
        paper, authors = getPaperInfoFromBibtex(bibtex, file, doi=doi, description=description, isread=isread)
        if paper == 0 or authors == 0:
            return 0, 0
        inserted_paper = p.create(paper)
        paper_id = inserted_paper[0]
        authors_id = []
        inserted_authors = []
        for author in authors:
            [flag, inserted_author] = a.create(author)
            authors_id.append(inserted_author[0])
            if flag == 0:
                inserted_authors.append(inserted_author)
            else:
                # If return value is None, Author data already exist
                pass

        # -- Register Relation --#
        for author_id in authors_id:
            a_management.create(paper_id, author_id)
        return inserted_paper, inserted_authors
    except:
        return 0, 0


def updateByBibtex(db_name, id, bibtex, file, description=None, doi=None, isread=0):
    """[summary]

    Args:
        db_name (string): [description]
        bibtex (string): [description]

    Returns:
        flag: Success 1, Failed 0
    """
    try:
        p = Paper(db_name)
        a = Author(db_name)
        a_management = AuthorManagement(db_name)
        paper, authors = getPaperInfoFromBibtex(bibtex, file, doi=doi, description=description, isread=isread)
        if paper == 0 or authors == 0:
            return 0
        inserted_paper = p.update(id, paper)
        paper_id = inserted_paper[0][0]

        # --- Delete Old Relation ---#
        inserted_authors = []
        authors_man = a_management.where(paper_id=paper_id)
        for author_man in authors_man:
            a_management.deleteByID(author_man[0])
        authors_id = []
        for author in authors:
            [flag, inserted_author] = a.create(author)
            authors_id.append(inserted_author[0])
            if flag == 0:
                inserted_authors.append(inserted_author)
            else:
                # If return value is None, Author data already exist
                pass

        # -- Register Relation --#
        for author_id in authors_id:
            a_management.create(paper_id, author_id)
        return inserted_paper[0]
    except:
        return 0


def getPaperInfoFromBibtex(pap: str, file=None, doi=None, description=None, isread=0):
    if pap.count("{") != pap.count("}") or pap.count('"') != pap.count('"'):
        return 0, 0
    bib = pap
    rows = re.findall(r'.*?=\s*{.*?}[,|\n]', bib)
    title = ""
    authorsBibtex = ""
    authors = []
    year = ""
    journal = ""

    match_title = '[^a-zA-Z*]title'
    match_year = 'year.*?=.*?'

    if rows == [] or rows == None:
        m = re.search(match_title, bib)
        num = m.start()
        numberCurly = 0
        for i in range(num, len(bib)):
            if bib[i] == '"':
                if numberCurly == 1:
                    break
                numberCurly = numberCurly + 1
                continue
            if numberCurly >= 1:
                title += bib[i]

        m = re.search(match_year, bib)
        if m is not None:
            num = m.start()
            numberCurly = 0
            for i in range(num, len(bib)):
                if bib[i] == '"':
                    if numberCurly == 1:
                        break
                    numberCurly = numberCurly + 1
                    continue
                if numberCurly >= 1:
                    year += bib[i]
            year = int(year)
        else:
            year = None

        num = bib.find('journal')
        numberCurly = 0
        for i in range(num, len(bib)):
            if bib[i] == '"':
                if numberCurly == 1:
                    break
                numberCurly = numberCurly + 1
                continue
            if numberCurly >= 1:
                journal += bib[i]

        num = bib.find('author')
        numberCurly = 0
        for i in range(num, len(bib)):
            if bib[i] == '"':
                if numberCurly == 1:
                    break
                numberCurly = numberCurly + 1
                continue
            if numberCurly >= 1:
                authorsBibtex += bib[i]
        authorList = authorsBibtex.lstrip("{").rstrip("}").replace('"', "").replace('"', "").split(' and ')
        for author in authorList:
            author = author.strip()
            authorName = ""
            if "," in author:
                nameList = author.split(",")
                for name in nameList:
                    authorName = name.strip() + " " + authorName
            else:
                authorName = author
            if authorName == "":
                continue
            authorName = authorName.strip()
            authors.append(Author.getDicFormat(authorName))
    else:
        m = re.search(match_title, bib)
        num = m.start()
        numberCurly = 0
        for i in range(num, len(bib)):
            if bib[i] == "{":
                numberCurly = numberCurly + 1
                continue
            if bib[i] == "}":
                numberCurly = numberCurly - 1
                if numberCurly == 0:
                    break
            if numberCurly >= 1:
                title += bib[i]

        m = re.search(match_year, bib)
        if m is not None:
            num = m.start()
            numberCurly = 0
            for i in range(num, len(bib)):
                if bib[i] == "{":
                    numberCurly = numberCurly + 1
                    continue
                if bib[i] == "}":
                    numberCurly = numberCurly - 1
                    if numberCurly == 0:
                        break
                    continue
                if numberCurly >= 1:
                    year += bib[i]
            year = int(year)
        else:
            year = None

        num = bib.find('journal')
        if num != -1:
            numberCurly = 0
            for i in range(num, len(bib)):
                if bib[i] == "{":
                    numberCurly = numberCurly + 1
                    continue
                if bib[i] == "}":
                    numberCurly = numberCurly - 1
                    if numberCurly == 0:
                        break
                    continue
                if numberCurly >= 1:
                    journal += bib[i]

        num = bib.find('author')
        numberCurly = 0
        for i in range(num, len(bib)):
            if bib[i] == "{":
                numberCurly = numberCurly + 1
                if numberCurly == 1:
                    continue
            if bib[i] == "}":
                numberCurly = numberCurly - 1
                if numberCurly == 0:
                    break
            if numberCurly >= 1:
                authorsBibtex += bib[i]
        authorList = authorsBibtex.lstrip("{").rstrip("}").replace('"', "").replace('"', "").split(' and ')
        for author in authorList:
            author = author.strip()
            authorName = ""
            if "," in author:
                nameList = author.split(",")
                for name in nameList:
                    authorName = name.strip() + " " + authorName
            else:
                authorName = author
            if authorName == "":
                continue
            authorName = authorName.strip()
            authors.append(Author.getDicFormat(authorName))

    paper = Paper.getDicFormat(title, year=year, filepath=file, bibtex=pap, doi=doi, description=description, isread=isread)
    return paper, authors
