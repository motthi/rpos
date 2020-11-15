from . import*


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
        if(paper == 0 or authors == 0):
            return 0, 0
        inserted_paper = p.create(paper)
        paper_id = inserted_paper[0]
        authors_id = []
        inserted_authors = []
        for author in authors:
            [flag, inserted_author] = a.create(author)
            authors_id.append(inserted_author[0])
            if(flag == 0):
                inserted_authors.append(inserted_author)
            else:
                # If return value is None, Author data already exist
                pass

        #-- Register Relation --#
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
        if(paper == 0 or authors == 0):
            return 0
        inserted_paper = p.update(id, paper)
        paper_id = inserted_paper[0][0]

        #--- Delete Old Relation ---#
        authors_man = a_management.where(paper_id=paper_id)
        for author_man in authors_man:
            a_management.deleteByID(author_man[0])
        authors_id = []
        for author in authors:
            [flag, inserted_author] = a.create(author)
            authors_id.append(inserted_author[0])
            if(flag == 0):
                inserted_authors.append(inserted_author)
            else:
                # If return value is None, Author data already exist
                pass

        #-- Register Relation --#
        for author_id in authors_id:
            a_management.create(paper_id, author_id)
        return inserted_paper[0]
    except:
        return 0


def getPaperInfoFromBibtex(pap, file=None, doi=None, description=None, isread=0):
    if(pap.count("{") != pap.count("}") or pap.count('"') != pap.count('"')):
        return 0, 0
    rows = re.findall(r'.*?=\s*{.*?}[,|\n]', pap)
    title = None
    authors = []
    year = None
    journal = None
    paperInfo = {}
    if(rows == [] or rows == None):
        rows = re.findall(r'.*?=\s*".*?"', pap)
    for row in rows:
        row = row.rstrip(",")
        info = row.strip().split("=")
        if(info[0].strip() == 'title'):
            title = info[1]
            title = title.strip().lstrip("{").rstrip("}").lstrip('"').rstrip('"')
        elif(info[0].strip() == 'author'):
            authorList = info[1].lstrip("{").rstrip("}").replace('"', "").replace('"', "").split(' and ')
            for author in authorList:
                author = author.strip()
                authorName = ""
                if("," in author):
                    nameList = author.split(",")
                    for name in nameList:
                        authorName = name.strip() + " " + authorName
                else:
                    authorName = author
                if(authorName == ""):
                    continue
                authorName = authorName.strip()
                authors.append(Author.getDicFormat(authorName))
        elif(info[0].strip() == 'year'):
            year = int(info[1].replace('"', "").replace('"', "").replace("{", "").replace("}", ""))
        elif(info[0].strip() == 'journal'):
            journal = info[1]
            journal = journal.replace("{", "").replace("}", "").replace('"', "").replace('"', "").strip()
    paper = Paper.getDicFormat(title, year=year, filepath=file, bibtex=pap, doi=doi, description=description, isread=isread)
    return paper, authors
