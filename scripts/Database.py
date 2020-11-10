import sqlite3
import datetime


class Paper():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()

    def All(self):
        """[summary]

        Returns:
            flag : Success Papers, Failed 0
        """
        try:
            self.c.execute("select * from Papers")
            return self.c.fetchall()
        except:
            return 0

    def find(self, id):
        """[summary]

        Args:
            id (int): [description]

        Returns:
            flag: Success Authors, Failed 0
        """
        try:
            self.c.execute("SELECT * FROM Papers WHERE id=" + str(id))
            return self.c.fetchone()
        except:
            return 0

    def where(self, title=None, year=None, isread=None):
        """[summary]

        Args:
            title (string): [description]. Defaults to None.
            year (string): [description]. Defaults to None.

        Returns:
            flag: Success Papers, Failed 0
        """
        try:
            self.c.execute("SELECT * FROM Papers")
            papers = self.c.fetchall()
            if(title != None and title != ""):
                self.c.execute("SELECT * FROM Papers WHERE title like ?", ('%' + str(title) + '%',))
                papers = set(papers) & set(self.c.fetchall())
            if(year != None and year != ""):
                papers = set(papers) & set(self.c.execute("SELECT * FROM Papers WHERE year=?", (year,)))
            if(isread != None and isread != ""):
                self.c.execute("SELECT * FROM Papers WHERE isread=?", (isread,))
                papers = set(papers) & set(self.c.fetchall())
            return list(papers)
        except:
            return 0

    def create(self, request):
        """[summary]

        Args:
            request (dic): [description]

        Returns:
            flag: Success Paper, Failed 0
        """
        title = request['title']
        year = request['year']
        filepath = request['filepath']
        bibtex = request['bibtex']
        doi = request['doi']
        description = request['description']
        isread = request['isread']
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        if(title != "" and title != None):
            self.c.execute(
                "INSERT INTO Papers(title, year, filepath, bibtex, doi, description, isread, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (title, year, filepath, bibtex, doi, description, isread, date, date)
            )
            self.conn.commit()
            self.c.execute("SELECT * from Papers where id=last_insert_rowid()")
            return self.c.fetchone()
        else:
            return 0

    def update(self, id, request):
        """[summary]

        Args:
            id (int): [description]
            request (dic): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            title = request['title']
            year = request['year']
            filepath = request['filepath']
            bibtex = request['bibtex']
            doi = request['doi']
            description = request['description']
            isread = request['isread']
            now = datetime.datetime.now()
            updated_at = now.strftime("%Y-%m-%d %H:%M:%S")
            self.c.execute(
                "update Papers set title=?, year=?, filepath=?, bibtex=?, doi=?, description=?, isread=?, updated_at=? where id=" + str(id),
                (title, year, filepath, bibtex, doi, description, isread, updated_at)
            )
            self.conn.commit()
            return self.where(title=title)
        except:
            return 0

    def delete(self, id):
        """[summary]

        Args:
            id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            self.c.execute("delete from Papers where id = " + str(id))
            self.conn.commit()
            return 1
        except:
            return 0

    def authors(self, id):
        """
        Return Authors Information related to specified Paper

        Args:
            id (int): [description]

        Returns:
            DB : Authors related to Paper
        """
        paper = self.find(id)
        paper_id = paper[0]
        author_management = AuthorManagement(self.db_name)
        authors_man = author_management.where(paper_id=paper_id)
        authors = []
        for author_man in authors_man:
            a = Author(self.db_name)
            authors.append(a.find(author_man[2]))
        return authors

    def classifications(self, id):
        """
        Return Classifications Information related to specified Paper

        Args:
            id (int): [description]

        Returns:
            DB : Classifications related to Paper
        """
        paper = self.find(id)
        paper_id = paper[0]
        classification_management = ClassificationManagement(self.db_name)
        clfs_man = classification_management.where(paper_id=paper_id)
        clfs = []
        for clf_man in clfs_man:
            clf = Classification(self.db_name)
            clfs.append(clf.find(clf_man[2]))
        return clfs

    def affiliations(self, id):
        """
        Return Authors Information related to specified Paper

        Args:
            id (int): [description]

        Returns:
            DB : Authors related to Paper
        """
        paper = self.find(id)
        paper_id = paper[0]
        affiliation_management = AffiliationManagement(self.db_name)
        affiliations_man = affiliation_management.where(paper_id=paper_id)
        affiliations = []
        for affiliation_man in affiliations_man:
            a = Affiliation(self.db_name)
            affiliations.append(a.find(affiliation_man[2]))
        return affiliations

    @ classmethod
    def getDicFormat(cls, title, year=None, filepath=None, bibtex=None, doi=None, description=None, isread=0):
        """[summary]

        Args:
            title (string): [description]
            year (string): [description]. Defaults to None.
            filepath (string): [description]. Defaults to None.
            bibtex (string): [description]. Defaults to None.
            doi (string): [description]. Defaults to None.
            description (string): [description]. Defaults to None.
            isread (int): [description]. Defaults to 0.

        Returns:
            Dicstionary: [description]
        """
        return {'title': title, 'year': year, 'filepath': filepath, 'bibtex': bibtex, 'doi': doi, 'description': description, 'isread': isread}

    def __del__(self):
        self.conn.close()


class Author():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()

    def All(self):
        """[summary]

        Returns:
            flag : Success Authors, Failed 0
        """
        try:
            self.c.execute("select * from Authors")
            return self.c.fetchall()
        except:
            return 0

    def find(self, id):
        """[summary]

        Args:
            id (int): [description]

        Returns:
            flag: Success author, Failed 0
        """
        try:
            self.c.execute("select * from Authors where id=" + str(id))
            return self.c.fetchone()
        except:
            return 0

    def where(self, name=None, affiliation_id=None):
        """[summary]

        Args:
            name (string): [description]. Defaults to None.
            affiliation_id (int): [description]. Defaults to None.

        Returns:
            flag : Success authors, Failed 0
        """
        try:
            if(name != None and name != ""):
                if(affiliation_id != None and affiliation_id != ""):
                    self.c.execute("select * from Authors where name like ? and affiliation_id=" + str(affiliation_id), ('%' + name + '%',))
                else:
                    self.c.execute("select * from Authors where name like ?", ('%' + name + '%',))
            else:
                if(affiliation_id != None and affiliation_id != ""):
                    self.c.execute("select * from Authors where affiliation_id = " + str(affiliation_id))
                else:
                    self.c.execute("select * from Authors")
            return self.c.fetchall()
        except:
            return 0

    def create(self, request):
        """[summary]

        Args:
            request ([dic]): [description]

        Returns:
            flag : Success created paper, Failed 0
        """
        name = request['name']
        description = request['description']
        affiliation_id = request['affiliation_id']
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        if(name != "" and name != None):
            self.c.execute("SELECT * from Authors WHERE name=?", (name,))
            author = self.c.fetchone()
            if(author == None):
                self.c.execute(
                    "INSERT INTO Authors(name, description, affiliation_id, created_at, updated_at) SELECT ?, ?, ?, ?, ?",
                    (name, description, affiliation_id, date, date)
                )
                self.conn.commit()
                self.c.execute("SELECT * from Authors WHERE name=?", (name,))
                return 0, self.c.fetchone()
            else:
                return 1, author
        else:
            return 0, 0

    def update(self, id, request):
        """[summary]

        Args:
            id (int): [description]
            request (dic): [description]

        Returns:
            flag : Success 1, Failed 0
        """
        try:
            name = request['name']
            description = request['description']
            affiliation_id = request['affiliation_id']
            now = datetime.datetime.now()
            updated_at = now.strftime("%Y-%m-%d %H:%M:%S")
            self.c.execute(
                "update Authors set name=?, description=?, affiliation_id=?, updated_at=? where id=" + str(id),
                (name, description, affiliation_id, updated_at)
            )
            self.conn.commit()
            return 1
        except:
            return 0

    def delete(self, id):
        """[summary]

        Args:
            id (int): id of Author

        Returns:
            flag (int): Success 1, Failed 0
        """
        try:
            self.c.execute("delete from Authors where id = " + str(id))
            self.conn.commit()
            return 1
        except:
            return 0

    def papers(self, id):
        """
        Return Paper Information related to specified Author

        Args:
            id (int): id of Author

        Returns:
            DB : Papers related to Author
        """
        author = self.find(id)
        author_id = author[0]
        author_management = AuthorManagement(self.db_name)
        authors_man = author_management.where(author_id=author_id)
        papers = []
        for author_man in authors_man:
            p = Paper(self.db_name)
            papers.append(p.find(author_man[1]))
        return papers

    def affiliation(self, id):
        author = self.find(id)
        af = Affiliation(self.db_name)
        if(author[3] == None):
            affiliation = None
        else:
            affiliation = af.find(author[3])
        return affiliation

    @ classmethod
    def getDicFormat(cls, name, description=None, affiliation_id=None):
        """[summary]

        Args:
            name (string): [description]
            description (string): [description]. Defaults to None.
            affiliation_id (string): [description]. Defaults to None.

        Returns:
            Dicstionary: [description]
        """
        return {'name': name, 'description': description, 'affiliation_id': affiliation_id}

    def __del__(self):
        self.conn.close()


class Classification():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()

    def All(self, column='id', order='ASC'):
        """[summary]

        Returns:
            flag: Success Classifications, Failed 0
        """
        try:
            self.c.execute("SELECT * FROM Classifications ORDER BY " + column + " " + order)
            return self.c.fetchall()
        except:
            return 0

    def find(self, id):
        """[summary]

        Args:
            id (int): [description]

        Returns:
            flag: Success Classification
        """
        try:
            self.c.execute("SELECT * FROM Classifications WHERE id=" + str(id))
            return self.c.fetchone()
        except:
            return 0

    def where(self, name=None, column='id', order='ASC'):
        """[summary]

        Args:
            name (string): [description]. Defaults to None.

        Returns:
            flag: Success Classifications, Failed 0
        """
        try:
            if(name != None and name != ""):
                self.c.execute("SELECT * FROM Classifications WHERE name like ? ORDER BY " + column + " " + order, ('%' + name + '%',))
            else:
                self.c.execute("select * from Classifications ORDER BY " + column + " " + order)
            return self.c.fetchall()
        except:
            return 0

    def create(self, request):
        """[summary]

        Args:
            request (dic): [description]

        Returns:
            flag: Success Classification, Failed 0
        """
        name = request['name']
        description = request['description']
        turn = request['turn']
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        if(name != "" and name != None):
            self.c.execute(
                "INSERT INTO Classifications(name, description, turn, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (name, description, turn, date, date)
            )
            self.conn.commit()
            self.c.execute("SELECT * from Classifications where id=last_insert_rowid()")
            return self.c.fetchone()
        else:
            return 0

    def update(self, id, request):
        """[summary]

        Args:
            id (int): [description]
            request (dic): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            name = request['name']
            description = request['description']
            turn = request['turn']
            now = datetime.datetime.now()
            updated_at = now.strftime("%Y-%m-%d %H:%M:%S")
            self.c.execute(
                "update Classifications set name=?, description=?, turn=?, updated_at=? where id=" + str(id),
                (name, description, turn, updated_at)
            )
            self.conn.commit()
            return 1
        except:
            return 0

    def delete(self, id):
        """[summary]

        Args:
            id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            self.c.execute("delete from Classifications where id = " + str(id))
            self.conn.commit()
            return 1
        except:
            return 0

    def papers(self, id):
        clf = self.find(id)
        clf_id = clf[0]
        clf_management = ClassificationManagement(self.db_name)
        clfs_man = clf_management.where(classification_id=clf_id)
        papers = []
        for clf_man in clfs_man:
            p = Paper(self.db_name)
            papers.append(p.find(clf_man[1]))
        return papers

    def subclasses(self, id):
        clf = self.find(id)
        clf_id = clf[0]
        clf_label_management = ClassificationLabelManagement(self.db_name)
        clfs_label_man = clf_label_management.where(classification_id=clf_id)
        sub_clfs = []
        for clf_label_man in clfs_label_man:
            sub_clfs.append(self.find(clf_label_man[2]))
        return sub_clfs

    def parentclasses(self, id):
        clf = self.find(id)
        clf_id = clf[0]
        clf_label_management = ClassificationLabelManagement(self.db_name)
        clfs_label_man = clf_label_management.where(sub_classification_id=clf_id)
        clfs = []
        for clf_label_man in clfs_label_man:
            clfs.append(self.find(clf_label_man[1]))
        return clfs

    @ classmethod
    def getDicFormat(cls, name, description=None, turn=0):
        """[summary]

        Args:
            name (string): [description]
            description (string): [description]. Defaults to None.
            turn (int): [description]. Defaults to None.

        Returns:
            (dic) : [description]
        """
        return {'name': name, 'description': description, 'turn': turn}

    def __del__(self):
        self.conn.close()


class Affiliation():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()

    def All(self):
        """[summary]

        Returns:
            flag: Success Affiliations, Failed 0
        """
        try:
            self.c.execute("select * from Affiliations")
            return self.c.fetchall()
        except:
            return 0

    def find(self, id):
        """[summary]

        Args:
            id (int): [description]

        Returns:
            flag: Success Affiliation
        """
        try:
            self.c.execute("SELECT * FROM Affiliations WHERE id=" + str(id))
            return self.c.fetchone()
        except:
            return 0

    def where(self, name=None, attribute=None):
        """[summary]

        Args:
            name (string): [description]. Defaults to None.
            attribute (string): [description]. Defaults to None.

        Returns:
            flag: Success Affiliations, Failed 0
        """
        try:
            if(name != None and name != ""):
                if(attribute != None and attribute != ""):
                    self.c.execute(
                        "SELECT * FROM Affiliations WHERE name like ? and attribute like ?",
                        ('%' + name + '%', '%' + attribute + '%')
                    )
                else:
                    self.c.execute("SELECT * FROM Affiliations WHERE name like ?", ('%' + name + '%',))
            else:
                if(attribute != None and attribute != ""):
                    self.c.execute("SELECT * FROM Affiliations WHERE attribute like ?", ('%' + attribute + '%',))
                else:
                    self.c.execute("select * from Affiliations")
            return self.c.fetchall()
        except:
            return 0

    def create(self, request):
        """[summary]

        Args:
            request (dic): [description]

        Returns:
            flag: Success Affiliation, Failed 0
        """
        name = request['name']
        description = request['description']
        attribute = request['attribute']
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        if(name != "" and name != None):
            self.c.execute(
                "INSERT INTO Affiliations(name, description, attribute, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (name, description, attribute, date, date)
            )
            self.conn.commit()
            self.c.execute("SELECT * from Affiliations where id=last_insert_rowid()")
            return self.c.fetchone()
        else:
            return 0

    def update(self, id, request):
        """[summary]

        Args:
            id (int): [description]
            request (dic): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            name = request['name']
            description = request['description']
            attribute = request['attribute']
            now = datetime.datetime.now()
            updated_at = now.strftime("%Y-%m-%d %H:%M:%S")
            self.c.execute(
                "update Affiliations set name=?, description=?, attribute=?, updated_at=? where id=" + str(id),
                (name, description, attribute, updated_at)
            )
            self.conn.commit()
            return 1
        except:
            return 0

    def delete(self, id):
        """[summary]

        Args:
            id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            self.c.execute("DELETE FROM Affiliations WHERE id=" + str(id))
            self.conn.commit()
            return 1
        except:
            return 0

    def papers(self, id):
        aff = self.find(id)
        aff_id = aff[0]
        aff_management = AffiliationManagement(self.db_name)
        affs_man = aff_management.where(affiliation_id=aff_id)
        papers = []
        for aff_man in affs_man:
            p = Paper(self.db_name)
            papers.append(p.find(aff_man[1]))
        return papers

    @ classmethod
    def getDicFormat(cls, name, description=None, attribute=None):
        """[summary]

        Args:
            name (string): [description]
            description (string): [description]. Defaults to None.
            attribute (string): [description]. Defaults to None.

        Returns:
            (dic) : [description]
        """
        return {'name': name, 'description': description, 'attribute': attribute}

    def __del__(self):
        self.conn.close()


class AuthorManagement():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()

    def All(self):
        """[summary]

        Returns:
            flag: Success AuthorManagements, Failed 0
        """
        try:
            self.c.execute("select * from AuthorManagements")
            return self.c.fetchall()
        except:
            return 0

    def find(self, id):
        """[summary]

        Args:
            id (int): [description]

        Returns:
            flag: Success AuthorManagement, Failed 0
        """
        try:
            self.c.execute("select * from AuthorManagements where id = " + str(id))
            return self.c.fetchone()
        except:
            return 0

    def where(self, paper_id=None, author_id=None):
        """[summary]

        Args:
            paper_id (int): [description]. Defaults to None.
            author_id (int): [description]. Defaults to None.

        Returns:
            flag: Success Papers, Failed 0
        """
        try:
            if(paper_id != None and paper_id != ""):
                if(author_id != None and author_id != ""):
                    self.c.execute("SELECT * FROM AuthorManagements WHERE paper_id like ? and author_id=" + str(author_id), ('%' + paper_id + '%',))
                else:
                    self.c.execute("SELECT * FROM AuthorManagements WHERE paper_id=?", (paper_id,))
            else:
                if(author_id != None and author_id != ""):
                    self.c.execute("SELECT * FROM AuthorManagements WHERE author_id = " + str(author_id))
                else:
                    self.c.execute("select * from AuthorManagements")
            return self.c.fetchall()
        except:
            return 0

    def create(self, paper_id, author_id):
        """[summary]

        Args:
            paper_id (int): [description]
            author_id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        if(paper_id != "" and paper_id != None):
            self.c.execute(
                "INSERT INTO AuthorManagements(paper_id, author_id) VALUES (?, ?)",
                (paper_id, author_id)
            )
            self.conn.commit()
            return 1
        else:
            return 0

    def update(self, id, paper_id, author_id):
        """[summary]

        Args:
            id (int): [description]
            paper_id (int): [description]
            author_id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            self.c.execute(
                "UPDATE AuthorManagements SET paper_id=?, author_id=? WHERE id=" + str(id),
                (paper_id, author_id)
            )
            self.conn.commit()
            return 1
        except:
            return 0

    def deleteByID(self, id):
        """
        Delete Relation specified by ID

        Args:
            id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            self.c.execute("delete from AuthorManagements where id = " + str(id))
            self.conn.commit()
            return 1
        except:
            return 0

    def delete(self, paper_id, author_id):
        """[summary]

        Args:
            paper_id (int): [description]
            author_id (int): [description]
        """
        self.c.execute(
            "delete from AuthorManagements where paper_id=? and author_id=?",
            (paper_id, author_id)
        )
        self.conn.commit()

    @ classmethod
    def getDicFormat(cls, paper_id, author_id=None):
        """[summary]

        Args:
            paper_id (int): [description]
            author_id (int, optional): [description]. Defaults to None.

        Returns:
            dic: [description]
        """
        return {'paper_id': paper_id, 'author_id': author_id}

    def __del__(self):
        self.conn.close()


class ClassificationManagement():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()

    def All(self):
        """[summary]

        Returns:
            flag: Success ClassificationManagements, Failed 0
        """
        try:
            self.c.execute("select * from ClassificationManagements")
            return self.c.fetchall()
        except:
            return 0

    def find(self, id):
        """[summary]

        Args:
            id (int): [description]

        Returns:
            flag: Success ClassificationManagement, Failed 0
        """
        try:
            self.c.execute("select * from ClassificationManagements where id = " + str(id))
            return self.c.fetchone()
        except:
            return 0

    def where(self, paper_id=None, classification_id=None):
        """[summary]

        Args:
            paper_id (int): [description]. Defaults to None.
            classification_id (int): [description]. Defaults to None.

        Returns:
            flag: Success Papers, Failed 0
        """
        try:
            if(paper_id != None and paper_id != ""):
                if(classification_id != None and classification_id != ""):
                    self.c.execute("SELECT * FROM ClassificationManagements WHERE paper_id like ? and classification_id=" + str(classification_id), ('%' + paper_id + '%',))
                else:
                    self.c.execute("SELECT * FROM ClassificationManagements WHERE paper_id=" + str(paper_id))
            else:
                if(classification_id != None and classification_id != ""):
                    self.c.execute("SELECT * FROM ClassificationManagements WHERE classification_id = " + str(classification_id))
                else:
                    self.c.execute("select * from ClassificationManagements")
            return self.c.fetchall()
        except:
            return 0

    def create(self, paper_id, classification_id):
        """[summary]

        Args:
            paper_id (int): [description]
            classification_id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        if(paper_id != "" and paper_id != None):
            self.c.execute(
                "INSERT INTO ClassificationManagements(paper_id, classification_id) VALUES (?, ?)",
                (paper_id, classification_id)
            )
            self.conn.commit()
            return 1
        else:
            return 0

    def update(self, id, paper_id, classification_id):
        """[summary]

        Args:
            id (int): [description]
            paper_id (int): [description]
            classification_id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            self.c.execute(
                "update ClassificationManagements set paper_id=?, classification_id=? where id=" + str(id),
                (paper_id, classification_id)
            )
            self.conn.commit()
            return 1
        except:
            return 0

    def deleteByID(self, id):
        """
        Delete Relation specified by ID

        Args:
            id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            self.c.execute("delete from ClassificationManagements where id = " + str(id))
            self.conn.commit()
            return 1
        except:
            return 0

    def delete(self, paper_id, classification_id):
        """[summary]

        Args:
            paper_id (int): [description]
            classification_id (int): [description]
        """
        self.c.execute(
            "delete from ClassificationManagements where paper_id=? and classification_id=?",
            (paper_id, classification_id)
        )
        self.conn.commit()

    @ classmethod
    def getDicFormat(cls, paper_id, classification_id=None):
        """[summary]

        Args:
            paper_id (int): [description]
            classification_id (int, optional): [description]. Defaults to None.

        Returns:
            dic: [description]
        """
        return {'paper_id': paper_id, 'classification_id': classification_id}

    def __del__(self):
        self.conn.close()


class ClassificationLabelManagement():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()

    def All(self):
        """[summary]

        Returns:
            flag: Success ClassificationLabelManagements, Failed 0
        """
        try:
            self.c.execute("select * from ClassificationLabelManagements")
            return self.c.fetchall()
        except:
            return 0

    def find(self, id):
        """[summary]

        Args:
            id (int): [description]

        Returns:
            flag: Success ClassificationLabelManagement, Failed 0
        """
        try:
            self.c.execute("select * from ClassificationLabelManagements where id=" + str(id))
            return self.c.fetchone()
        except:
            return 0

    def where(self, classification_id=None, sub_classification_id=None):
        """[summary]

        Args:
            classification_id (int): [description]. Defaults to None.
            sub_classification_id (int): [description]. Defaults to None.

        Returns:
            flag: Success Papers, Failed 0
        """
        try:
            if(classification_id != None and classification_id != ""):
                if(sub_classification_id != None and sub_classification_id != ""):
                    self.c.execute("SELECT * FROM ClassificationLabelManagements WHERE classification_id like ? and sub_classification_id=" +
                                   str(sub_classification_id), ('%' + classification_id + '%',))
                else:
                    self.c.execute("SELECT * FROM ClassificationLabelManagements WHERE classification_id=" + str(classification_id))
            else:
                if(sub_classification_id != None and sub_classification_id != ""):
                    self.c.execute("SELECT * FROM ClassificationLabelManagements WHERE sub_classification_id = " + str(sub_classification_id))
                else:
                    self.c.execute("select * from ClassificationLabelManagements")
            return self.c.fetchall()
        except:
            return 0

    def create(self, classification_id, sub_classification_id):
        """[summary]

        Args:
            classification_id (int): [description]
            sub_classification_id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        if(classification_id != "" and classification_id != None):
            self.c.execute(
                "INSERT INTO ClassificationLabelManagements(classification_id, sub_classification_id) VALUES (?, ?)",
                (classification_id, sub_classification_id)
            )
            self.conn.commit()
            return 1
        else:
            return 0

    def update(self, id, classification_id, sub_classification_id):
        """[summary]

        Args:
            id (int): [description]
            classification_id (int): [description]
            sub_classification_id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            self.c.execute(
                "update ClassificationLabelManagements set classification_id=?, sub_classification_id=? where id=" + str(id),
                (classification_id, sub_classification_id)
            )
            self.conn.commit()
            return 1
        except:
            return 0

    def deleteByID(self, id):
        """
        Delete Relation specified by ID

        Args:
            id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            self.c.execute("delete from ClassificationLabelManagements where id = " + str(id))
            self.conn.commit()
            return 1
        except:
            return 0

    def delete(self, classification_id, sub_classification_id):
        """[summary]

        Args:
            classification_id (int): [description]
            sub_classification_id (int): [description]
        """
        self.c.execute(
            "delete from ClassificationLabelManagements where classification_id=? and sub_classification_id=?",
            (classification_id, sub_classification_id)
        )
        self.conn.commit()

    @ classmethod
    def getDicFormat(cls, classification_id, sub_classification_id=None):
        """[summary]

        Args:
            classification_id (int): [description]
            sub_classification_id (int, optional): [description]. Defaults to None.

        Returns:
            dic: [description]
        """
        return {'classification_id': classification_id, 'sub_classification_id': sub_classification_id}

    def __del__(self):
        self.conn.close()


class AffiliationManagement():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()

    def All(self):
        """[summary]

        Returns:
            flag: Success AffiliationManagements, Failed 0
        """
        try:
            self.c.execute("select * from AffiliationManagements")
            return self.c.fetchall()
        except:
            return 0

    def find(self, id):
        """[summary]

        Args:
            id (int): [description]

        Returns:
            flag: Success AffiliationManagement, Failed 0
        """
        try:
            self.c.execute("select * from AffiliationManagements where id = " + str(id))
            return self.c.fetchone()
        except:
            return 0

    def where(self, paper_id=None, affiliation_id=None):
        """[summary]

        Args:
            paper_id (int): [description]. Defaults to None.
            affiliation_id (int): [description]. Defaults to None.

        Returns:
            flag: Success Papers, Failed 0
        """
        try:
            if(paper_id != None and paper_id != ""):
                if(affiliation_id != None and affiliation_id != ""):
                    self.c.execute("SELECT * FROM AffiliationManagements WHERE paper_id like ? and affiliation_id=" + str(affiliation_id), ('%' + paper_id + '%',))
                else:
                    self.c.execute("SELECT * FROM AffiliationManagements WHERE paper_id=" + str(paper_id))
            else:
                if(affiliation_id != None and affiliation_id != ""):
                    self.c.execute("SELECT * FROM AffiliationManagements WHERE affiliation_id = " + str(affiliation_id))
                else:
                    self.c.execute("select * from AffiliationManagements")
            return self.c.fetchall()
        except:
            return 0

    def create(self, paper_id, affiliation_id):
        """[summary]

        Args:
            paper_id (int): [description]
            affiliation_id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        if(paper_id != "" and paper_id != None):
            self.c.execute(
                "INSERT INTO AffiliationManagements(paper_id, affiliation_id) VALUES (?, ?)",
                (paper_id, affiliation_id)
            )
            self.conn.commit()
            return 1
        else:
            return 0

    def update(self, id, paper_id, affiliation_id):
        """[summary]

        Args:
            id (int): [description]
            paper_id (int): [description]
            affiliation_id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            self.c.execute(
                "update AffiliationManagements set paper_id=?, affiliation_id=? where id=" + str(id),
                (paper_id, affiliation_id)
            )
            self.conn.commit()
            return 1
        except:
            return 0

    def deleteByID(self, id):
        """
        Delete Relation specified by ID

        Args:
            id (int): [description]

        Returns:
            flag: Success 1, Failed 0
        """
        try:
            self.c.execute("delete from AffiliationManagements where id = " + str(id))
            self.conn.commit()
            return 1
        except:
            return 0

    def delete(self, paper_id, affiliation_id):
        """[summary]

        Args:
            paper_id (int): [description]
            affiliation_id (int): [description]
        """
        self.c.execute(
            "delete from AffiliationManagements where paper_id=? and affiliation_id=?",
            (paper_id, affiliation_id)
        )
        self.conn.commit()

    @ classmethod
    def getDicFormat(cls, paper_id, affiliation_id=None):
        """[summary]

        Args:
            paper_id (int): [description]
            affiliation_id (int, optional): [description]. Defaults to None.

        Returns:
            dic: [description]
        """
        return {'paper_id': paper_id, 'affiliation_id': affiliation_id}

    def __del__(self):
        self.conn.close()
