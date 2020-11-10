from pybtex.plugin import find_plugin
from pybtex.database import*
from . import*


def readBibtex(pap, file, doi=None, description=None, isread=0):
    """[summary]

    Args:
        pap (string): Bibtex

    Returns:
        paperInfo (list) : Information about Paper [paper, authors]
    """
    bib_data = parse_string(pap, "bibtex")
    data_lower = bib_data.lower()
    for e in data_lower.entries.values():
        pass
    authors = []
    for author in e.persons['author']:
        name = ""
        if(author.first_names != [] and author.first_names != None):
            name += str(author.first_names[0]) + " "
        if(author.middle_names != [] and author.middle_names != None):
            name += str(author.middle_names[0]) + " "
        if(author.last_names != [] and author.last_names != None):
            name += str(author.last_names[0])
        authors.append(Author.getDicFormat(name))
    if('year' in e.fields):
        year = int(e.fields['year'])
    else:
        year = None

    paperInfo = Paper.getDicFormat(str(e.fields['title']), year=year, filepath=file, bibtex=pap, doi=doi, description=description, isread=isread), authors
    return paperInfo
