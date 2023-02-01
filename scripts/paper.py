import os
import wx
import shutil
import pyperclip
from scripts.database.register import updateByBibtex, registerByBibtex
from scripts.database.database import Paper, Author, Classification, Affiliation, ClassificationManagement, AffiliationManagement, AuthorManagement
from scripts.classification import AttachClassification
from scripts.affiliation import AttachAffiliation


class RegisterPaper(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((606, 549))
        self.SetTitle("rpos : Register Paper")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(sizer_10, 5, wx.EXPAND, 0)

        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, "BibTex")
        label_1.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_10.Add(label_1, 0, wx.ALL, 3)

        self.bibtex_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_MULTILINE)
        self.bibtex_txt.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_10.Add(self.bibtex_txt, 12, wx.ALL | wx.EXPAND, 2)

        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(sizer_4, 1, wx.EXPAND, 0)

        description_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Description")
        description_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_4.Add(description_lbl, 3, wx.ALL, 2)

        self.description_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_MULTILINE)
        self.description_txt.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_4.Add(self.description_txt, 12, wx.ALL | wx.EXPAND, 2)

        grid_sizer_1 = wx.FlexGridSizer(5, 2, 5, 5)
        sizer_2.Add(grid_sizer_1, 1, wx.EXPAND, 0)

        fileBibtex_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "File", style=wx.ALIGN_CENTER_HORIZONTAL)
        fileBibtex_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(fileBibtex_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

        self.fileBibtex_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.fileBibtex_txt.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_3.Add(self.fileBibtex_txt, 15, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.fileselect_btn = wx.Button(self.panel_1, wx.ID_ANY, "Select")
        self.fileselect_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_3.Add(self.fileselect_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)

        doi_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "DOI", style=wx.ALIGN_CENTER_HORIZONTAL)
        doi_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(doi_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.doi_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.doi_txt.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.doi_txt, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)

        self.isread_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "IsRead")
        self.isread_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.isread_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.isread_cmb = wx.ComboBox(self.panel_1, wx.ID_ANY, choices=["Not Yet", "Done"], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.isread_cmb.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.isread_cmb.SetSelection(0)
        grid_sizer_1.Add(self.isread_cmb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.clf_btn = wx.Button(self.panel_1, wx.ID_ANY, "Classification")
        self.clf_btn.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.clf_btn, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 2)

        self.clf_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "")
        self.clf_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.clf_lbl, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 6)

        self.aff_btn = wx.Button(self.panel_1, wx.ID_ANY, "Affiliation")
        self.aff_btn.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.aff_btn, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 2)

        self.aff_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "")
        self.aff_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.aff_lbl, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 6)

        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_6, 1, wx.ALIGN_RIGHT, 0)

        self.registerPaper_btn = wx.Button(self.panel_1, wx.ID_ANY, "Register")
        self.registerPaper_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_6.Add(self.registerPaper_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        grid_sizer_1.AddGrowableCol(1)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()
        self.db = args[2]
        self.filedialog = wx.FileDialog(self, u'選択')
        self.clfs_id = []
        self.affs_id = []

        self.Bind(wx.EVT_BUTTON, self.selectFile, self.fileselect_btn)
        self.Bind(wx.EVT_BUTTON, self.attachClf, self.clf_btn)
        self.Bind(wx.EVT_BUTTON, self.attachAff, self.aff_btn)
        self.Bind(wx.EVT_BUTTON, self.registerPaper, self.registerPaper_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)

    def onKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

    def registerPaper(self, event):
        bibtex = self.bibtex_txt.GetValue()
        selected_file = self.fileBibtex_txt.GetValue()
        isread = self.isread_cmb.GetSelection()
        description = self.description_txt.GetValue() if self.description_txt.GetValue() != "" else None
        doi = self.doi_txt.GetValue() if self.doi_txt.GetValue() != "" else None
        if selected_file == "" or selected_file == None:
            filepath = None
        else:
            filepath = './resource/doc/' + os.path.splitext(os.path.basename(self.db))[0] + '/' + os.path.basename(selected_file)

        # --- Register Paper---#
        [paper, registered_authors] = registerByBibtex(
            self.db,
            bibtex,
            filepath,
            description=description,
            doi=doi,
            isread=isread
        )
        if paper == 0:
            wx.MessageBox(u'処理に失敗しました\n登録を中断しました', u'Paper Register Failed', wx.ICON_ERROR)
            return

        # --- Copy File ---#
        if os.path.isfile(selected_file):
            shutil.copyfile(
                selected_file,
                './resource/doc/' + os.path.splitext(os.path.basename(self.db))[0] + '/' + os.path.basename(selected_file)
            )
        self.Close()

        # --- Attach Classification to Paper ---#
        c_m = ClassificationManagement(self.db)
        for clf_id in self.clfs_id:
            c_m.create(paper[0], clf_id)

        # --- Attach Affiliation to Paper ---#
        af_m = AffiliationManagement(self.db)
        for aff_id in self.affs_id:
            af_m.create(paper[0], aff_id)

        # --- Update Paper Grid ---#
        p = Paper(self.db)
        a = Author(self.db)
        row_len = self.GetParent().paper_grid.GetNumberRows()
        self.GetParent().paper_grid.AppendRows()
        self.GetParent().paper_grid.SetCellValue(row_len, 0, paper[1])
        if paper[2] != None:
            self.GetParent().paper_grid.SetCellValue(row_len, 1, str(paper[2]))  # Year
        authors = ""
        clfs = ""
        affs = ""
        if p.authors(paper[0]) != None or p.authors(paper[0]) != []:
            for author in p.authors(paper[0]):
                authors += author[1] + "; "
            self.GetParent().paper_grid.SetCellValue(row_len, 2, authors)  # Author
        if p.classifications(paper[0]) != None or p.classifications(paper[0]) != []:
            for clf in p.classifications(paper[0]):
                clfs += clf[1] + "; "
        self.GetParent().paper_grid.SetCellValue(row_len, 3, clfs)  # Classification
        if p.affiliations(paper[0]) != None or p.affiliations(paper[0]) != []:
            for aff in p.affiliations(paper[0]):
                affs += aff[1] + "; "
        self.GetParent().paper_grid.SetCellValue(row_len, 4, affs)  # Affiliationn
        self.GetParent().paper_grid.SetCellValue(row_len, 5, paper[8])
        self.GetParent().paper_grid.SetCellValue(row_len, 6, paper[9])
        if paper[7] == 0:
            for col in range(self.GetParent().paper_grid.GetNumberCols()):
                self.GetParent().paper_grid.SetCellBackgroundColour(row_len, col, wx.Colour('#ffffd0'))
        self.GetParent().paper_grid.ForceRefresh()

        # --- Update Author Grid ---#
        for registered_author in registered_authors:
            row_len = self.GetParent().auth_grid.GetNumberRows()
            self.GetParent().auth_grid.AppendRows()
            self.GetParent().auth_grid.SetCellValue(row_len, 0, registered_author[1])
            aff = a.affiliation(author[0])
            if aff != None:
                self.GetParent().auth_grid.SetCellValue(row_len, 1, aff[1])
            papers = a.papers(author[0])
            self.GetParent().auth_grid.SetCellValue(row_len, 2, str(len(papers)))

    def selectFile(self, event):  # wxGlade: RegisterPaper.<event_handler>
        self.filedialog.ShowModal()
        self.fileBibtex_txt.SetValue(self.filedialog.GetPath())

    def attachClf(self, event):  # wxGlade: RegisterPaper.<event_handler>
        self.AttachClf = AttachClassification(self, wx.ID_ANY, self.db)
        self.AttachClf.Show()

    def attachAff(self, event):  # wxGlade: RegisterPaper.<event_handler>
        self.AttachAff = AttachAffiliation(self, wx.ID_ANY, self.db)
        self.AttachAff.Show()

    def indexClassifications(self):
        clf_lbl = ""
        for clf_id in self.clfs_id:
            c = Classification(self.db)
            clf = c.find(clf_id)
            clf_lbl += str(clf[1]) + "; "
        self.clf_lbl.SetLabel(clf_lbl)

    def showAffiliations(self):
        aff_lbl = ""
        for aff_id in self.affs_id:
            af = Affiliation(self.db)
            aff = af.find(aff_id)
            aff_lbl += str(aff[1]) + "; "
        self.aff_lbl.SetLabel(aff_lbl)


class ShowPaper(wx.Frame):
    def __init__(self, *args, **kwds):
        self.db = args[2]
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((679, 559))
        self.SetTitle("rpos : Show Paper")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_4 = wx.ScrolledWindow(self.panel_1, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.panel_4.SetScrollRate(10, 10)
        sizer_1.Add(self.panel_4, 1, wx.EXPAND, 0)

        grid_sizer_1 = wx.FlexGridSizer(7, 2, 0, 0)

        title_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Title")
        title_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(title_lbl, 0, wx.ALL, 2)

        title_show_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        title_show_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        title_show_lbl.Wrap(400)
        if self.GetParent().selected_paper[1] != None:
            title_show_lbl.SetLabel(self.GetParent().selected_paper[1])
        grid_sizer_1.Add(title_show_lbl, 0, wx.ALL, 2)

        year_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Year")
        year_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(year_lbl, 0, wx.ALL, 2)

        year_show_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        year_show_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        if self.GetParent().selected_paper[2] != None:
            year_show_lbl.SetLabel(str(self.GetParent().selected_paper[2]))
        grid_sizer_1.Add(year_show_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        author_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Author")
        author_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(author_lbl, 0, wx.ALL, 2)

        author_show_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        author_show_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        author_show_lbl.Wrap(400)
        p = Paper(self.db)
        authors = p.authors(self.GetParent().selected_paper[0])
        names = ""
        for i, author in enumerate(authors):
            names += author[1] + "; "
        author_show_lbl.SetLabel(names)
        grid_sizer_1.Add(author_show_lbl, 0, wx.ALL, 2)

        doi_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "DOI", style=wx.ALIGN_CENTER_HORIZONTAL)
        doi_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(doi_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.doi_show_link = wx.adv.HyperlinkCtrl(self.panel_4, wx.ID_ANY, "", "")
        self.doi_show_link.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        if self.GetParent().selected_paper[5] != None:
            self.doi_show_link.SetLabel(self.GetParent().selected_paper[5])
            self.doi_show_link.SetURL(self.GetParent().selected_paper[5])
        grid_sizer_1.Add(self.doi_show_link, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.isread_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Is Read")
        self.isread_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.isread_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        isread_show_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        isread_show_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        if self.GetParent().selected_paper[7] == 0:
            isread_show_lbl.SetLabel("Not Yet")
        else:
            isread_show_lbl.SetLabel("Done")
        grid_sizer_1.Add(isread_show_lbl, 0, wx.ALL, 2)

        self.clf_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Classification")
        self.clf_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.clf_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        clf_show_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        clf_show_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        clfs = p.classifications(self.GetParent().selected_paper[0])
        clf_name = ""
        for clf in clfs:
            clf_name += str(clf[1]) + "; "
        clf_show_lbl.SetLabel(clf_name)

        grid_sizer_1.Add(clf_show_lbl, 0, wx.ALL, 2)

        self.aff_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Affiliation")
        self.aff_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.aff_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        aff_show_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        aff_show_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        affs = p.affiliations(self.GetParent().selected_paper[0])
        aff_name = ""
        for aff in affs:
            aff_name += str(aff[1]) + "; "
        aff_show_lbl.SetLabel(aff_name)
        grid_sizer_1.Add(aff_show_lbl, 0, wx.ALL, 2)

        grid_sizer_2 = wx.GridSizer(1, 2, 0, 0)
        sizer_1.Add(grid_sizer_2, 1, wx.ALL | wx.EXPAND, 4)

        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_2.Add(sizer_4, 1, wx.EXPAND, 0)

        desc_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Description")
        desc_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_4.Add(desc_lbl, 0, wx.ALL, 2)

        self.panel_3 = wx.ScrolledWindow(self.panel_1, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.panel_3.SetScrollRate(10, 10)
        sizer_4.Add(self.panel_3, 1, wx.EXPAND, 0)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        desc_show_lbl = wx.StaticText(self.panel_3, wx.ID_ANY, "")
        desc_show_lbl.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        if self.GetParent().selected_paper[6] != None:
            desc_show_lbl.SetLabel(self.GetParent().selected_paper[6])
        sizer_2.Add(desc_show_lbl, 2, wx.ALL, 2)

        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_2.Add(sizer_10, 1, wx.EXPAND, 0)

        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10.Add(sizer_6, 0, 0, 0)

        bibtex_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "BibTex")
        bibtex_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_6.Add(bibtex_lbl, 0, wx.ALL, 2)

        self.copyBibtex_btn = wx.Button(self.panel_1, wx.ID_ANY, "Copy Bibtex")
        sizer_6.Add(self.copyBibtex_btn, 0, wx.ALL | wx.EXPAND, 2)

        self.copiedFlag_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "")
        self.copiedFlag_lbl.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_6.Add(self.copiedFlag_lbl, 0, wx.ALIGN_BOTTOM | wx.ALL, 4)

        self.panel_2 = wx.ScrolledWindow(self.panel_1, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.panel_2.SetScrollRate(10, 10)
        sizer_10.Add(self.panel_2, 1, wx.EXPAND, 0)

        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)

        bibtex_show_lbl = wx.StaticText(self.panel_2, wx.ID_ANY, "")
        bibtex_show_lbl.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        bibtex_show_lbl.SetLabel(self.GetParent().selected_paper[4])
        sizer_12.Add(bibtex_show_lbl, 2, wx.ALL | wx.EXPAND, 2)

        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_11, 0, wx.ALIGN_RIGHT, 0)

        self.openFile_btn = wx.Button(self.panel_1, wx.ID_ANY, "Open File")
        self.openFile_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(self.openFile_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        self.editPaper_btn = wx.Button(self.panel_1, wx.ID_ANY, "Edit")
        self.editPaper_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(self.editPaper_btn, 0, wx.ALL, 7)

        self.close_btn = wx.Button(self.panel_1, wx.ID_ANY, "Close")
        self.close_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(self.close_btn, 0, wx.ALL, 7)

        self.panel_2.SetSizer(sizer_12)

        self.panel_3.SetSizer(sizer_2)

        self.panel_4.SetSizer(grid_sizer_1)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.paperCopyBibtex, self.copyBibtex_btn)
        self.Bind(wx.EVT_BUTTON, self.openFile, self.openFile_btn)
        self.Bind(wx.EVT_BUTTON, self.editPaper, self.editPaper_btn)
        self.Bind(wx.EVT_BUTTON, self.closeWindow, self.close_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)

    def onKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

    def editPaper(self, event):
        self.Close()
        editPaper = EditPaper(self.GetParent(), wx.ID_ANY, self.db)
        editPaper.Show()

    def openFile(self, event):
        self.GetParent().paperFileOpen(event)

    def closeWindow(self, event):
        self.Close()

    def paperCopyBibtex(self, event):
        pyperclip.copy(self.GetParent().selected_paper[4])
        self.copiedFlag_lbl.SetLabel("Copied")


class EditPaper(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: EditPaper.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((623, 607))
        self.SetTitle("rpos : Edit Paper")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.ScrolledWindow(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.panel_1.SetScrollRate(10, 10)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_2 = wx.Panel(self.panel_1, wx.ID_ANY)
        sizer_1.Add(self.panel_2, 1, wx.EXPAND, 0)

        sizer_10 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self.panel_2, wx.ID_ANY, "BibTex")
        label_1.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_10.Add(label_1, 0, wx.ALL, 3)

        self.bibtex_txt = wx.TextCtrl(self.panel_2, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_MULTILINE)
        self.bibtex_txt.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        if self.GetParent().selected_paper[4] != None:
            self.bibtex_txt.SetValue(self.GetParent().selected_paper[4])
        sizer_10.Add(self.bibtex_txt, 1, wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 2)

        self.panel_3 = wx.Panel(self.panel_1, wx.ID_ANY)
        sizer_1.Add(self.panel_3, 1, wx.ALL | wx.EXPAND, 0)

        sizer_4 = wx.BoxSizer(wx.VERTICAL)

        description_lbl = wx.StaticText(self.panel_3, wx.ID_ANY, "Description")
        description_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_4.Add(description_lbl, 0, wx.ALL, 3)

        self.description_txt = wx.TextCtrl(self.panel_3, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_MULTILINE)
        self.description_txt.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        if self.GetParent().selected_paper[6] != None:
            self.description_txt.SetValue(self.GetParent().selected_paper[6])
        sizer_4.Add(self.description_txt, 1, wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 2)

        self.panel_4 = wx.Panel(self.panel_1, wx.ID_ANY)
        sizer_1.Add(self.panel_4, 0, wx.EXPAND, 0)

        grid_sizer_1 = wx.FlexGridSizer(5, 2, 2, 0)

        fileBibtex_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "File", style=wx.ALIGN_CENTER_HORIZONTAL)
        fileBibtex_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(fileBibtex_lbl, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1.Add(sizer_11, 0, wx.EXPAND, 0)

        self.fileBibtex_txt = wx.TextCtrl(self.panel_4, wx.ID_ANY, "")
        self.fileBibtex_txt.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        if self.GetParent().selected_paper[3] != None:
            self.fileBibtex_txt.SetValue(self.GetParent().selected_paper[3])
        sizer_11.Add(self.fileBibtex_txt, 13, wx.ALL | wx.EXPAND, 3)

        self.fileselect_btn = wx.Button(self.panel_4, wx.ID_ANY, "Edit")
        self.fileselect_btn.SetMinSize((68, 25))
        self.fileselect_btn.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(self.fileselect_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND | wx.SHAPED, 1)

        doi_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "DOI", style=wx.ALIGN_CENTER_HORIZONTAL)
        doi_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(doi_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.doi_txt = wx.TextCtrl(self.panel_4, wx.ID_ANY, "")
        self.doi_txt.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        if self.GetParent().selected_paper[5] != None:
            self.doi_txt.SetValue(self.GetParent().selected_paper[5])
        grid_sizer_1.Add(self.doi_txt, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 2)

        self.isread_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "IsRead")
        self.isread_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.isread_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.isread_cmb = wx.ComboBox(self.panel_4, wx.ID_ANY, choices=["NotYet", "Done"], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.isread_cmb.SetMinSize((80, 27))
        self.isread_cmb.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.isread_cmb.SetSelection(self.GetParent().selected_paper[7])
        grid_sizer_1.Add(self.isread_cmb, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.clf_btn = wx.Button(self.panel_4, wx.ID_ANY, "Classification")
        self.clf_btn.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.clf_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 2)

        self.clf_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        self.clf_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.clf_lbl, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.aff_btn = wx.Button(self.panel_4, wx.ID_ANY, "Affiliation")
        self.aff_btn.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.aff_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 2)

        self.aff_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        self.aff_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.aff_lbl, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.editPaper_btn = wx.Button(self.panel_1, wx.ID_ANY, "Update")
        self.editPaper_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_1.Add(self.editPaper_btn, 0, wx.ALIGN_RIGHT | wx.ALL, 7)

        grid_sizer_1.AddGrowableCol(1)
        self.panel_4.SetSizer(grid_sizer_1)

        self.panel_3.SetSizer(sizer_4)

        self.panel_2.SetSizer(sizer_10)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()
        self.db = args[2]
        self.filedialog = wx.FileDialog(self, u'選択')

        p = Paper(self.db)

        # --- Show Classification ---#
        clfs = p.classifications(self.GetParent().selected_paper[0])
        self.clfs_id = []
        for clf in clfs:
            self.clfs_id.append(clf[0])
        self.indexClassifications()

        # --- Show Affiliations ---#
        affs = p.affiliations(self.GetParent().selected_paper[0])
        self.affs_id = []
        for aff in affs:
            self.affs_id.append(aff[0])
        self.showAffiliations()

        self.Bind(wx.EVT_BUTTON, self.selectFile, self.fileselect_btn)
        self.Bind(wx.EVT_BUTTON, self.attachClf, self.clf_btn)
        self.Bind(wx.EVT_BUTTON, self.attachAff, self.aff_btn)
        self.Bind(wx.EVT_BUTTON, self.editPaper, self.editPaper_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)

    def onKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

    def editPaper(self, event):
        bibtex = self.bibtex_txt.GetValue()
        selected_file = self.fileBibtex_txt.GetValue()
        isread = self.isread_cmb.GetSelection()
        description = self.description_txt.GetValue() if self.description_txt.GetValue() != "" else None
        doi = self.doi_txt.GetValue() if self.doi_txt.GetValue() != "" else None

        # --- Set New File Path ---#
        if selected_file == "" or selected_file == None:
            new_filepath = None
        else:
            new_filepath = './resource/doc/' + os.path.splitext(os.path.basename(self.db))[0] + '/' + os.path.basename(selected_file)

        # --- Delete Old File ---#
        if (
            self.GetParent().selected_paper[3] != None and  # 変更前のファイルがNULLではない
            self.GetParent().selected_paper[3] != new_filepath and  # 変更前のファイルと新しいファイルが同じではない
            os.path.isfile(self.GetParent().selected_paper[3])  # 変更前のファイルが存在する
        ):
            try:
                msg = wx.MessageBox(
                    u'以下のファイルが削除されます\n' + self.GetParent().selected_paper[3] + '\n削除しますか',
                    u'Paper Delete',
                    wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING
                )
                if msg == wx.YES:
                    os.remove(self.GetParent().selected_paper[3])
                else:
                    wx.MessageBox(u'ファイルを削除できません\n更新処理を中断しました', u'Could not Delete', wx.ICON_ERROR)
                    return
            except PermissionError:
                wx.MessageBox(u'ファイルを削除できません\n更新処理を中断しました', u'Could not Delete', wx.ICON_ERROR)
                return

        # --- Copy File ---#
        if new_filepath != "" and new_filepath != None and not (os.path.isfile(new_filepath)):
            shutil.copyfile(
                selected_file,
                './resource/doc/' + os.path.splitext(os.path.basename(self.db))[0] + '/' + os.path.basename(selected_file)
            )

        # --- Update Paper Information ---#
        paper = updateByBibtex(
            self.db,
            self.GetParent().selected_paper[0],
            bibtex,
            new_filepath,
            description=description,
            doi=doi,
            isread=isread
        )
        if paper == 0:
            wx.MessageBox(u'処理に失敗しました\n変更を中断しました', u'Paper Update Failed', wx.ICON_ERROR)
            return

        # --- Attach Classification to Paper ---#
        c_m = ClassificationManagement(self.db)
        clfs_old = c_m.where(paper_id=self.GetParent().selected_paper[0])
        for clf in clfs_old:
            c_m.deleteByID(clf[0])
        for clf_id in self.clfs_id:
            c_m.create(self.GetParent().selected_paper[0], clf_id)

        # --- Attach Affiliation to Paper ---#
        af_m = AffiliationManagement(self.db)
        affs_old = af_m.where(paper_id=self.GetParent().selected_paper[0])
        for aff in affs_old:
            af_m.deleteByID(aff[0])
        for aff_id in self.affs_id:
            af_m.create(self.GetParent().selected_paper[0], aff_id)

        self.Close()

        # --- Update Paper Grid ---#
        p = Paper(self.db)
        a = Author(self.db)
        authors = a.All()
        self.GetParent().indexAuthor(authors)

        row_len = self.GetParent().row
        self.GetParent().paper_grid.SetCellValue(row_len, 0, paper[1])
        if paper[2] != None:
            self.GetParent().paper_grid.SetCellValue(row_len, 1, str(paper[2]))  # Year
        authors = ""
        clfs = ""
        affs = ""
        if p.authors(paper[0]) != None or p.authors(paper[0]) != []:
            for author in p.authors(paper[0]):
                authors += author[1] + "; "
            self.GetParent().paper_grid.SetCellValue(row_len, 2, authors)  # Author
        if p.classifications(paper[0]) != None or p.classifications(paper[0]) != []:
            for clf in p.classifications(paper[0]):
                clfs += clf[1] + "; "
        self.GetParent().paper_grid.SetCellValue(row_len, 3, clfs)  # Classification
        if p.affiliations(paper[0]) != None or p.affiliations(paper[0]) != []:
            for aff in p.affiliations(paper[0]):
                affs += aff[1] + "; "
        self.GetParent().paper_grid.SetCellValue(row_len, 4, affs)  # Affiliationn

        if paper[7] == 0:
            for col in range(self.GetParent().paper_grid.GetNumberCols()):
                self.GetParent().paper_grid.SetCellBackgroundColour(row_len, col, wx.Colour('#ffffd0'))
        else:
            for col in range(self.GetParent().paper_grid.GetNumberCols()):
                self.GetParent().paper_grid.SetCellBackgroundColour(row_len, col, wx.Colour('#ffffff'))
        self.GetParent().paper_grid.ForceRefresh()

    def selectFile(self, event):
        self.filedialog.ShowModal()
        self.fileBibtex_txt.SetValue(self.filedialog.GetPath())

    def attachClf(self, event):
        self.AttachClf = AttachClassification(self, wx.ID_ANY, self.db)
        self.AttachClf.Show()

    def attachAff(self, event):
        self.AttachAff = AttachAffiliation(self, wx.ID_ANY, self.db)
        self.AttachAff.Show()

    def indexClassifications(self):
        clf_lbl = ""
        c = Classification(self.db)
        for clf_id in self.clfs_id:
            clf = c.find(clf_id)
            clf_lbl += str(clf[1]) + "; "
        self.clf_lbl.SetLabel(clf_lbl)

    def showAffiliations(self):
        aff_lbl = ""
        for aff_id in self.affs_id:
            af = Affiliation(self.db)
            aff = af.find(aff_id)
            aff_lbl += str(aff[1]) + "; "
        self.aff_lbl.SetLabel(aff_lbl)
