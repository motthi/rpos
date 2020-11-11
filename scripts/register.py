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
        paper, authors = readBibtex(bibtex, file, doi=doi, description=description, isread=isread)
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
        paper, authors = readBibtex(bibtex, file, doi=doi, description=description, isread=isread)
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
