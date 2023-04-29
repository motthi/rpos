import os
import wx
import wx.xrc
import wx.grid
import wx.adv
import wx.html
import wx.xml
import shutil
import pyperclip
import subprocess
from scripts.paper import *
from scripts.classification import *
from scripts.author import *
from scripts.affiliation import *
from scripts.database.create import createAllTables


class CreateDB(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((515, 221))
        self.SetTitle("rpos : Creat Database")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.panel_1.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        newDBname_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Database Name")
        newDBname_lbl.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_2.Add(newDBname_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.newDBname_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.newDBname_txt.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_2.Add(self.newDBname_txt, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 9)

        self.createDB_btn = wx.Button(self.panel_1, wx.ID_ANY, "Create")
        sizer_2.Add(self.createDB_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_3, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.return_btn = wx.Button(self.panel_1, wx.ID_ANY, "Return")
        sizer_3.Add(self.return_btn, 0, wx.ALIGN_BOTTOM | wx.ALL, 10)

        self.close_btn = wx.Button(self.panel_1, wx.ID_ANY, "Close")
        sizer_3.Add(self.close_btn, 0, wx.ALIGN_BOTTOM | wx.ALL, 10)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.createDB, self.createDB_btn)
        self.Bind(wx.EVT_BUTTON, self.returnToWelcomePage, self.return_btn)
        self.Bind(wx.EVT_BUTTON, self.closeWindow, self.close_btn)
        self.Bind(wx.EVT_CLOSE, self.exitProgram, self)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)

    def onKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.returnToWelcomePage()
        else:
            event.Skip()

    def createDB(self, event):
        db_name = self.newDBname_txt.GetValue()
        if db_name == "" or db_name == None:
            wx.MessageBox("ファイル名を入力してください")
        elif os.path.splitext(db_name)[1] == "":
            wx.MessageBox("拡張子を入力してください")
        elif os.path.exists("./resource/db/" + db_name):
            wx.MessageBox("すでに存在するデータベースです")
        else:
            createAllTables("./resource/db/" + db_name)
            if not os.path.exists('./resource/doc/' + os.path.splitext(os.path.basename(db_name))[0]):
                os.mkdir('./resource/doc/' + os.path.splitext(os.path.basename(db_name))[0])
            self.Close()
            self.RposMain = RposMain(None, wx.ID_ANY, "./resource/db/" + db_name)
            self.RposMain.Show()

    def exitProgram(self, event):
        self.Destroy()

    def closeWindow(self, event):
        self.Close()

    def returnToWelcomePage(self, event):
        self.Close()
        self.welcomepage = WelcomePage(None, wx.ID_ANY, "")
        self.welcomepage.Show()


class WelcomePage(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: WelcomePage.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((600, 400))
        self.SetTitle("rpos : Welcome Page")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_5, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)

        welcome = wx.StaticText(self.panel_1, wx.ID_ANY, "Welcome to RPOS!")
        welcome.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_5.Add(welcome, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_3, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)

        selectDB_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Select Database", style=wx.ALIGN_CENTER_HORIZONTAL)
        selectDB_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_3.Add(selectDB_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 13)

        self.selectDB_dbx = wx.ComboBox(self.panel_1, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.selectDB_dbx.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        if not os.path.exists('./resource'):
            os.mkdir('./resource')
        if not os.path.exists('./resource/db'):
            os.mkdir('./resource/db')
        self.dbs = os.listdir('./resource/db')
        for db in self.dbs:
            self.selectDB_dbx.Append(db)
        if len(self.dbs) >= 1:
            self.selectDB_dbx.SetSelection(0)
        sizer_3.Add(self.selectDB_dbx, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        self.selectDB_btn = wx.Button(self.panel_1, wx.ID_ANY, "Open")
        self.selectDB_btn.SetMinSize((100, 40))
        self.selectDB_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_3.Add(self.selectDB_btn, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 13)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_4, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.createDB_btn = wx.Button(self.panel_1, wx.ID_ANY, "Create New")
        self.createDB_btn.SetMinSize((120, 50))
        self.createDB_btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_4.Add(self.createDB_btn, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 30)

        self.rposGitHub_hl = wx.adv.HyperlinkCtrl(self.panel_1, wx.ID_ANY, "https://github.com/motthi/rpos", "https://github.com/motthi/rpos")
        self.rposGitHub_hl.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_2.Add(self.rposGitHub_hl, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.selectedDB, self.selectDB_btn)
        self.Bind(wx.EVT_BUTTON, self.createNewDB, self.createDB_btn)
        self.Bind(wx.EVT_CLOSE, self.exitProgram, self)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)

    def onKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

    def selectedDB(self, event):  # wxGlade: WelcomePage.<event_handler>
        if self.selectDB_dbx.GetSelection() == -1:
            wx.MessageBox("データベースを選択してください")
            return
        db_name = './resource/db/' + str(self.dbs[self.selectDB_dbx.GetSelection()])
        self.Close()
        self.RposMain = RposMain(None, wx.ID_ANY, db_name)
        self.RposMain.Show()

    def createNewDB(self, event):  # wxGlade: WelcomePage.<event_handler>
        self.Close()
        self.CreateDB = CreateDB(None, wx.ID_ANY, "")
        self.CreateDB.Show()

    def exitProgram(self, event):  # wxGlade: WelcomePage.<event_handler>
        self.Destroy()


class RposMain(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE
        self.db = args[2]
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1296, 696))
        self.SetTitle("rpos")

        # Icon
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.SetBackgroundColour(wx.Colour(239, 247, 255))

        self.createMenuBar()

        self.panel = wx.Panel(self, wx.ID_ANY)
        grid_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=1, hgap=0)

        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_16 = wx.BoxSizer(wx.VERTICAL)

        show_label_idx_lbl = wx.StaticText(self.panel, wx.ID_ANY, u"ラベル一覧")
        show_label_idx_lbl.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))

        idx_paper_lbl = wx.StaticText(self.panel, wx.ID_ANY, u"論文一覧　　")
        idx_paper_lbl.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))

        title_lbl = wx.StaticText(self.panel, wx.ID_ANY, "Title")
        title_lbl.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))

        self.title_txt_ctrl = wx.SearchCtrl(self.panel, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.title_txt_ctrl.SetMinSize((110, 23))
        self.title_txt_ctrl.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.title_txt_ctrl.ShowCancelButton(True)

        author_lbl = wx.StaticText(self.panel, wx.ID_ANY, "Author")
        author_lbl.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))

        self.author_txt_ctrl = wx.SearchCtrl(self.panel, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.author_txt_ctrl.SetMinSize((130, 23))
        self.author_txt_ctrl.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.author_txt_ctrl.ShowCancelButton(True)

        clf_lbl = wx.StaticText(self.panel, wx.ID_ANY, "Classification")
        clf_lbl.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))

        self.clf_cmb = wx.ComboBox(self.panel, wx.ID_ANY, choices=[""], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.clf_cmb.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        for clf in self.getClfWithSubLayer():
            self.clf_cmb.Append(str("  ") * clf[0] + clf[1])

        aff_lbl = wx.StaticText(self.panel, wx.ID_ANY, "Affiliation")
        aff_lbl.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))

        self.aff_cmb = wx.ComboBox(self.panel, wx.ID_ANY, choices=[""], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.aff_cmb.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        for aff in Affiliation(self.db).All():
            self.aff_cmb.Append(aff[1])

        has_red_label = wx.StaticText(self.panel, wx.ID_ANY, "IsRead")
        has_red_label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))

        self.has_read_cmb = wx.ComboBox(self.panel, wx.ID_ANY, choices=["", "Not Yet", "Done"], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.has_read_cmb.SetMinSize((50, 23))
        self.has_read_cmb.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))

        self.reset_btn = wx.Button(self.panel, wx.ID_ANY, "Reset")
        self.reset_btn.SetMinSize((55, 30))
        self.reset_btn.SetBackgroundColour(wx.Colour(217, 250, 255))
        self.reset_btn.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))

        sizer_10.Add(sizer_8, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        sizer_8.Add(idx_paper_lbl, 0, 0, 0)
        sizer_10.Add(sizer_11, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        sizer_11.Add(sizer_12, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        sizer_12.Add(title_lbl, 0, 0, 0)
        sizer_12.Add(self.title_txt_ctrl, 0, wx.LEFT, 20)
        sizer_11.Add(sizer_13, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        sizer_16.Add(has_red_label, 0, 0, 0)
        sizer_13.Add(author_lbl, 0, 0, 0)
        sizer_11.Add(sizer_14, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        sizer_14.Add(clf_lbl, 0, 0, 0)
        sizer_13.Add(self.author_txt_ctrl, 0, wx.LEFT, 20)
        sizer_14.Add(self.clf_cmb, 0, wx.EXPAND | wx.LEFT, 20)
        sizer_11.Add(sizer_15, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        sizer_15.Add(aff_lbl, 0, 0, 0)
        sizer_15.Add(self.aff_cmb, 0, wx.EXPAND | wx.LEFT, 20)
        sizer_11.Add(sizer_16, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        sizer_16.Add(self.has_read_cmb, 0, wx.LEFT, 20)
        sizer_11.Add(self.reset_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        self.clf_tree_ctrl = wx.TreeCtrl(self.panel, wx.ID_ANY)
        self.clf_tree_ctrl.SetBackgroundColour(wx.Colour(255, 250, 239))
        self.clf_tree_ctrl.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.indexClassifications(Classification(self.db), Classification(self.db).All('turn', 'ASC'))

        self.notebook = wx.Notebook(self.panel, wx.ID_ANY)
        self.notebook.SetBackgroundColour(wx.Colour(239, 247, 255))

        self.paper_ntbk_pnl, self.paper_grid = self.initializePaperGrid()
        self.auth_ntbk_tbl, self.auth_grid = self.initializeAuthorGrid()
        self.aff_ntbk_pnl, self.aff_grid = self.initializeAffiliationGrid()
        self.indexPaper(Paper(self.db).All())
        self.indexAuthor(Author(self.db).All())
        self.indexAffiliation(Affiliation(self.db).All())

        self.notebook.AddPage(self.paper_ntbk_pnl, "Papers")
        self.notebook.AddPage(self.auth_ntbk_tbl, "Authors")
        self.notebook.AddPage(self.aff_ntbk_pnl, "Affiliations")

        grid_sizer.Add(show_label_idx_lbl, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        grid_sizer.Add(sizer_10, 1, wx.EXPAND, 0)
        grid_sizer.Add(self.clf_tree_ctrl, 1, wx.ALL | wx.EXPAND, 3)
        grid_sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 2)
        grid_sizer.AddGrowableRow(1)
        grid_sizer.AddGrowableCol(0, 1)
        grid_sizer.AddGrowableCol(1, 1)
        self.panel.SetSizer(grid_sizer)

        self.Layout()

        self.Bind(wx.EVT_SEARCH, self.searchPaper, self.title_txt_ctrl)
        self.Bind(wx.EVT_SEARCH, self.searchPaper, self.author_txt_ctrl)
        self.Bind(wx.EVT_SEARCH_CANCEL, self.searchPaper, self.author_txt_ctrl)
        self.Bind(wx.EVT_SEARCH_CANCEL, self.searchPaper, self.title_txt_ctrl)
        self.Bind(wx.EVT_COMBOBOX, self.searchPaper, self.clf_cmb)
        self.Bind(wx.EVT_COMBOBOX, self.searchPaper, self.aff_cmb)
        self.Bind(wx.EVT_COMBOBOX, self.searchPaper, self.has_read_cmb)
        self.Bind(wx.EVT_BUTTON, self.resetSearching, self.reset_btn)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.treeCtrlActivated, self.clf_tree_ctrl)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.treeCtrlRightClicked, self.clf_tree_ctrl)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_LEFT_DCLICK, self.paperGridDoubleLeftClick, self.paper_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_RIGHT_CLICK, self.paperGridRightClick, self.paper_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_LABEL_LEFT_CLICK, self.pgridLabelLeftClicked, self.paper_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.paperGridLeftClick, self.paper_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_RIGHT_CLICK, self.authGridRightClick, self.auth_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.authGridLeftClick, self.auth_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_RIGHT_CLICK, self.affGridRightClick, self.aff_grid)
        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.affGridLeftClick, self.aff_grid)
        self.Bind(wx.EVT_CLOSE, self.exitProgram, self)

    def createMenuBar(self):
        self.rposmain_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.openDatabase, wxglade_tmp_menu.Append(wx.ID_ANY, "Open", ""))
        self.Bind(wx.EVT_MENU, self.openRposLocation, wxglade_tmp_menu.Append(wx.ID_ANY, "Open RPOS location", ""))
        self.Bind(wx.EVT_MENU, self.closeDatabase, wxglade_tmp_menu.Append(wx.ID_ANY, "Close", ""))
        self.Bind(wx.EVT_MENU, self.exitProgram, wxglade_tmp_menu.Append(wx.ID_ANY, "Exit", ""))
        self.rposmain_menubar.Append(wxglade_tmp_menu, "File")
        wxglade_tmp_menu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.registerPaper, wxglade_tmp_menu.Append(wx.ID_ANY, "Paper", ""))
        self.Bind(wx.EVT_MENU, self.registerAuthor, wxglade_tmp_menu.Append(wx.ID_ANY, "Author", ""))
        self.Bind(wx.EVT_MENU, self.registerClassification, wxglade_tmp_menu.Append(wx.ID_ANY, "Classification", ""))
        self.Bind(wx.EVT_MENU, self.registerAffiliation, wxglade_tmp_menu.Append(wx.ID_ANY, "Affiliation", ""))
        self.rposmain_menubar.Append(wxglade_tmp_menu, "Register")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_ANY, "Backup", "")
        wxglade_tmp_menu.Append(wx.ID_ANY, "Delete All Data", "")
        wxglade_tmp_menu.Append(wx.ID_ANY, "Reset Database", "")
        self.rposmain_menubar.Append(wxglade_tmp_menu, "Database")
        self.SetMenuBar(self.rposmain_menubar)

    def initializePaperGrid(self):
        ntbk_pnl = wx.Panel(self.notebook, wx.ID_ANY)
        ntbk_pnl.SetBackgroundColour(wx.Colour(239, 247, 255))
        grid = wx.grid.Grid(ntbk_pnl, wx.ID_ANY, size=(1, 1))
        grid.CreateGrid(1, 7)
        grid.SetRowLabelSize(31)
        grid.SetColLabelSize(25)
        grid.EnableEditing(0)
        grid.SetLabelBackgroundColour(wx.Colour(245, 255, 244))
        grid.SetColLabelValue(0, "Title")
        grid.SetColSize(0, 488)
        grid.SetColLabelValue(1, "Year")
        grid.SetColSize(1, 48)
        grid.SetColLabelValue(2, "Author")
        grid.SetColSize(2, 403)
        grid.SetColLabelValue(3, "Classification")
        grid.SetColSize(3, 252)
        grid.SetColLabelValue(4, "Affiliation")
        grid.SetColSize(4, 106)
        grid.SetColLabelValue(5, "Registered At")
        grid.SetColSize(5, 160)
        grid.SetColLabelValue(6, "Updated At")
        grid.SetColSize(6, 160)
        grid.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.pgrid_title_state = 0
        self.pgrid_year_state = 0
        self.pgrid_register_state = 0
        self.pgrid_update_state = 0
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 20, wx.ALL | wx.EXPAND, 1)
        ntbk_pnl.SetSizer(sizer)
        return ntbk_pnl, grid

    def initializeAuthorGrid(self):
        ntbk_pnl = wx.Panel(self.notebook, wx.ID_ANY)
        ntbk_pnl.SetBackgroundColour(wx.Colour(239, 247, 255))
        grid = wx.grid.Grid(ntbk_pnl, wx.ID_ANY, size=(1, 1))
        grid.CreateGrid(1, 4)
        grid.SetRowLabelSize(31)
        grid.SetColLabelSize(25)
        grid.EnableEditing(0)
        grid.SetLabelBackgroundColour(wx.Colour(245, 255, 244))
        grid.SetColLabelValue(0, "name")
        grid.SetColSize(0, 208)
        grid.SetColLabelValue(1, "affiliation")
        grid.SetColSize(1, 127)
        grid.SetColLabelValue(2, "papers")
        grid.SetColSize(2, 75)
        grid.SetColLabelValue(3, "description")
        grid.SetColSize(3, 431)
        grid.SetBackgroundColour(wx.Colour(234, 255, 233))
        grid.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 20, wx.ALL | wx.EXPAND, 1)
        ntbk_pnl.SetSizer(sizer)
        return ntbk_pnl, grid

    def initializeAffiliationGrid(self):
        ntbk_pnl = wx.Panel(self.notebook, wx.ID_ANY)
        ntbk_pnl.SetBackgroundColour(wx.Colour(239, 247, 255))
        grid = wx.grid.Grid(ntbk_pnl, wx.ID_ANY, size=(1, 1))
        grid.CreateGrid(1, 2)
        grid.SetRowLabelSize(31)
        grid.SetColLabelSize(25)
        grid.EnableEditing(0)
        grid.SetLabelBackgroundColour(wx.Colour(245, 255, 244))
        grid.SetColLabelValue(0, "name")
        grid.SetColSize(0, 162)
        grid.SetColLabelValue(1, "attribute")
        grid.SetColSize(1, 211)
        grid.SetBackgroundColour(wx.Colour(234, 255, 233))
        grid.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 30, wx.ALL | wx.EXPAND, 1)
        ntbk_pnl.SetSizer(sizer)
        return ntbk_pnl, grid

    ### --- Paper ---###
    def indexPaper(self, papers):
        if self.paper_grid.GetNumberRows() != 0:
            self.paper_grid.DeleteRows(0, self.paper_grid.GetNumberRows(), True)
        if papers == []:
            return

        # --- Show Each Paper ---#
        for i, paper in enumerate(papers):
            p = Paper(self.db)
            self.paper_grid.AppendRows()
            self.paper_grid.SetCellValue(i, 0, paper[1])  # Title
            if paper[2] != None:
                self.paper_grid.SetCellValue(i, 1, str(paper[2]))  # Year

            authors = ""
            clfs = ""
            affs = ""
            if p.authors(paper[0]) != None or p.authors(paper[0]) != []:
                for author in p.authors(paper[0]):
                    authors += author[1] + "; "
                self.paper_grid.SetCellValue(i, 2, authors)  # Author
            if p.classifications(paper[0]) != None or p.classifications(paper[0]) != []:
                for clf in p.classifications(paper[0]):
                    clfs += clf[1] + "; "
            self.paper_grid.SetCellValue(i, 3, clfs)  # Classification
            if p.affiliations(paper[0]) != None or p.affiliations(paper[0]) != []:
                for aff in p.affiliations(paper[0]):
                    affs += aff[1] + "; "
            self.paper_grid.SetCellValue(i, 4, affs)  # Affiliationn
            self.paper_grid.SetCellValue(i, 5, paper[8])
            self.paper_grid.SetCellValue(i, 6, paper[9])
            if paper[7] == 0:
                for col in range(self.paper_grid.GetNumberCols()):
                    self.paper_grid.SetCellBackgroundColour(i, col, wx.Colour('#ffffd0'))
        self.paper_grid.ForceRefresh()

    def registerPaper(self, event):
        self.RegisterPaper = RegisterPaper(self, wx.ID_ANY, self.db)
        self.RegisterPaper.Show()

    def showPaper(self, event):
        self.ShowPaper = ShowPaper(self, wx.ID_ANY, self.db)
        self.ShowPaper.Show()

    def editPaper(self, event):
        self.EditPaper = EditPaper(self, wx.ID_ANY, self.db)  # params : database name
        self.EditPaper.Show()

    def deletePaper(self, event):
        msg = wx.MessageBox(u'削除しますか', u'Paper Delete', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
        if msg == wx.NO:
            return

        # --- Delete File ---#
        if self.selected_paper[3] != None:
            if os.path.isfile(self.selected_paper[3]):
                try:
                    os.remove(self.selected_paper[3])
                except PermissionError:
                    wx.MessageBox(u'ファイルを削除できません\n削除処理を中断しました', u'Could not Delete', wx.ICON_ERROR)
                    return

        Paper(self.db).delete(self.selected_paper[0])

        # --- Delete Relation to Author ---$
        a_m = AuthorManagement(self.db)
        authors_man = a_m.where(paper_id=self.selected_paper[0])
        for author_man in authors_man:
            a_m.deleteByID(author_man[0])

        # --- Delete Relation to Classification ---#
        c_m = ClassificationManagement(self.db)
        clfs_man = c_m.where(paper_id=self.selected_paper[0])
        for clf_man in clfs_man:
            c_m.deleteByID(clf_man[0])

        # --- Delete Relation to Affiliation ---#
        af_m = AffiliationManagement(self.db)
        affs_man = af_m.where(paper_id=self.selected_paper[0])
        for aff_man in affs_man:
            af_m.deleteByID(aff_man[0])

        # --- Update Paper Grid ---#
        self.paper_grid.DeleteRows(self.row, 1)

    def openPaper(self, event):
        file_path = self.selected_paper[3]
        if file_path != None and os.path.isfile(file_path):
            if " " in file_path:
                subprocess.Popen(r'"{}"'.format(file_path), shell=True)
            else:
                subprocess.Popen(['start', file_path], shell=True)
        else:
            msg = wx.MessageBox(u'ファイルが存在しません', u'File Not Found', wx.ICON_ERROR)

    def copyPaperBibtex(self, event):
        pyperclip.copy(self.selected_paper[4])

    def copyPaperFile(self, event):
        file_path = self.selected_paper[3]
        if file_path != None and os.path.isfile(file_path):
            shutil.copy2(file_path, "./")
        else:
            msg = wx.MessageBox(u'File not found', u'File Not Found', wx.ICON_ERROR)

    def searchPaper(self, event):
        title = self.title_txt_ctrl.GetValue()
        auth = self.author_txt_ctrl.GetValue()
        clf = self.clf_cmb.GetValue().strip()
        aff = self.aff_cmb.GetValue()
        has_read = self.has_read_cmb.GetValue()

        papers = Paper(self.db).All()
        if title != "" or auth != "" or clf != "" or aff != "" or has_read != "":
            if title != "" or has_read != "":
                papers = set(papers) & set(self.searchByTitleAndIsRead(title, has_read))
            if auth != "":
                papers = set(papers) & set(self.searchByAuthor(auth))
            if clf != "":
                papers = set(papers) & set(self.searchByClf(clf))
            if aff != "":
                papers = set(papers) & set(self.searchByAff(aff))
            papers = list(papers)
        elif auth == "":
            self.indexAuthor(Author(self.db).All())

        # --- sort ---#
        if self.pgrid_title_state == 1:
            papers = sorted(papers, key=lambda x: x[1], reverse=True)
        elif self.pgrid_title_state == 2:
            papers = sorted(papers, key=lambda x: x[1], reverse=False)
        elif self.pgrid_year_state == 1:
            papers = sorted(papers, key=lambda x: x[2], reverse=True)
        elif self.pgrid_year_state == 2:
            papers = sorted(papers, key=lambda x: x[2], reverse=False)
        elif self.pgrid_register_state == 1:
            papers = sorted(papers, key=lambda x: x[8], reverse=True)
        elif self.pgrid_register_state == 2:
            papers = sorted(papers, key=lambda x: x[8], reverse=False)
        elif self.pgrid_update_state == 1:
            papers = sorted(papers, key=lambda x: x[9], reverse=True)
        elif self.pgrid_update_state == 2:
            papers = sorted(papers, key=lambda x: x[9], reverse=False)
        self.indexPaper(papers)

    ### --- Author --- ###
    def indexAuthor(self, auths):
        if self.auth_grid.GetNumberRows() != 0:
            self.auth_grid.DeleteRows(0, self.auth_grid.GetNumberRows(), True)
        if auths == []:
            return
        for i, author in enumerate(auths):
            papers = Author(self.db).papers(author[0])
            aff = Affiliation(self.db).find(author[3]) if author[3] != None else ["", ""]
            self.auth_grid.AppendRows()
            self.auth_grid.SetCellValue(i, 0, author[1])
            self.auth_grid.SetCellValue(i, 1, aff[1])
            self.auth_grid.SetCellValue(i, 2, str(len(papers)))
            self.auth_grid.SetCellValue(i, 3, author[2] if author[2] != None else "")

    def registerAuthor(self, event):
        event.Skip()

    def showAuthor(self, event):
        self.ShowAuthor = ShowAuthor(self, wx.ID_ANY, self.db)
        self.ShowAuthor.Show()

    def editAuthor(self, event):
        self.EditAuthor = EditAuthor(self, wx.ID_ANY, self.db)
        self.EditAuthor.Show()

    def deleteAuthor(self, event):
        msg = wx.MessageBox(u'削除しますか', u'Paper Delete', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_ERROR)
        if msg == wx.NO:
            return

        # --- Delete Author ---#
        a = Author(self.db)
        a.delete(self.selected_author[0])

        # --- Delete Relation to Paper ---$
        a_m = AuthorManagement(self.db)
        authors_man = a_m.where(author_id=self.selected_author[0])
        for author_man in authors_man:
            a_m.deleteByID(author_man[0])

        # --- Update Grids ---#
        p = Paper(self.db)
        self.indexPaper(p.All())
        self.auth_grid.DeleteRows(self.row, 1)

    ### --- Classification ---###
    def indexClassifications(self, c, clfs):
        c = Classification(self.db)
        if clfs == []:
            return
        clfs = sorted(clfs, key=lambda x: x[3], reverse=False)
        self.clf_tree_ctrl.DeleteAllItems()
        root = self.clf_tree_ctrl.AddRoot("Classifications")
        for clf in clfs:
            parentclfs = c.parentclasses(clf[0])
            if parentclfs == []:  # Show Only Top Classification
                self.getAndShowSubClf(c, root, clf)  # Recursive Function
        self.clf_tree_ctrl.Expand(root)

    def registerClassification(self, event):
        self.parent = None
        self.createClf = RegisterClassification(self, wx.ID_ANY, self.db)
        self.createClf.Show()

    def registerSubClassification(self, event):
        self.parent = self.selected_clf
        self.createClf = RegisterClassification(self, wx.ID_ANY, self.db)
        self.createClf.Show()

    def showClassification(self, event):
        self.showClf = ShowClassification(self, wx.ID_ANY, self.db)
        self.showClf.Show()

    def editClassification(self, event):
        self.editClf = EditClassification(self, wx.ID_ANY, self.db)
        self.editClf.Show()

    def deleteClassification(self, event):
        msg = wx.MessageBox(u'削除しますか', u'Classification Delete', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_ERROR)
        if msg == wx.NO:
            return
        c = Classification(self.db)
        Classification(self.db).delete(self.selected_clf[0])

        # --- Delete Relation to Paper ---#
        c_m = ClassificationManagement(self.db)
        clfs_man = c_m.where(classification_id=self.selected_clf[0])
        for clf_man in clfs_man:
            c_m.deleteByID(clf_man[0])

        # --- Delete Relation to Classification Label ---#
        cl_m = ClassificationLabelManagement(self.db)
        clfs_l_man = cl_m.where(sub_classification_id=self.selected_clf[0])
        for clf_l_man in clfs_l_man:
            cl_m.deleteByID(clf_l_man[0])

        # --- Update TreeCtrl and Combox ---#
        self.indexClassifications(c, c.All())
        self.setClfSelection()

    def narrowClassification(self, event):
        if self.selected_clf == 'All':
            papers = Paper(self.db).All()
            self.clf_cmb.SetSelection(-1)
        else:
            papers = Classification(self.db).papers(self.selected_clf[0])
            self.clf_cmb.SetStringSelection("  " * (self.selected_clf_layer - 1) + self.selected_clf[1])
        self.indexPaper(papers)

    def getAndShowSubClf(self, c, parent, clf):
        """Get sub classification and show

        Args:
            c : Classification Class
            parent : parent class
            clf : classification
        """
        sub_clfs = c.subclasses(clf[0])
        sub_clfs = sorted(sub_clfs, key=lambda x: x[3], reverse=False)
        item = self.clf_tree_ctrl.AppendItem(parent, clf[1])
        for subclf in sub_clfs:
            self.getAndShowSubClf(c, item, subclf)
        self.clf_tree_ctrl.Expand(item)

    def setClfSelection(self):
        self.clf_cmb.Clear()
        clfs = self.getClfWithSubLayer()
        for clf in clfs:
            self.clf_cmb.Append(str("  ") * clf[0] + clf[1])

    def getClfWithSubLayer(self):
        c = Classification(self.db)
        clfs = c.All(column='turn')
        clfs_name_layer = []
        for clf in clfs:
            if c.parentclasses(clf[0]) == []:
                clfs_name_layer.append([0, clf[1]])
                self.getSubClf(c, clf[0], 0, clfs_name_layer)
        return clfs_name_layer

    def getSubClf(self, c, clf_id, layer, clfs_name_layer):
        clfs = sorted(c.subclasses(clf_id), key=lambda x: x[3], reverse=False)
        layer += 1
        for clf in clfs:
            clfs_name_layer.append([layer, clf[1]])
            self.getSubClf(c, clf[0], layer, clfs_name_layer)

    def getLayer(self, layer, clf_item):
        if self.clf_tree_ctrl.GetItemText(clf_item) == 'Classifications':
            return layer
        else:
            parent_clf = self.clf_tree_ctrl.GetItemParent(clf_item)
            return self.getLayer(layer + 1, parent_clf)

    ### --- Affiliation ---###
    def indexAffiliation(self, affs):
        if affs == []:
            return
        self.aff_grid.DeleteRows(0, self.aff_grid.GetNumberRows(), True)
        for i, aff in enumerate(affs):
            self.aff_grid.AppendRows()
            self.aff_grid.SetCellValue(i, 0, aff[1])
            self.aff_grid.SetCellValue(i, 1, aff[3])

    def registerAffiliation(self, event):
        registeraffiliation = RegisterAffiliation(self, wx.ID_ANY, self.db)
        registeraffiliation.Show()

    def showAffiliation(self, event):
        self.showAff = ShowAffiliation(self, wx.ID_ANY, self.db)
        self.showAff.Show()

    def editAffiliation(self, event):
        self.editAff = EditAffiliation(self, wx.ID_ANY, self.db)
        self.editAff.Show()

    def deleteAffiliation(self, event):
        msg = wx.MessageBox(u'削除しますか', u'Paper Delete', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_ERROR)
        if msg == wx.NO:
            return
        af = Affiliation(self.db)
        af.delete(self.selected_aff[0])
        self.indexAffiliation(af.All())

        # --- Delete Relation to Paper ---#
        af_m = AffiliationManagement(self.db)
        affs_man = af_m.where(affiliation_id=self.selected_aff[0])
        for aff_man in affs_man:
            af_m.deleteByID(aff_man[0])

    ### --- Event ---###
    def paperGridLeftClick(self, event):
        self.selectedPaper = self.paper_grid.GetSelectedCells()

    def paperGridDoubleLeftClick(self, event):
        row = event.GetRow()
        selected_paper_title = self.paper_grid.GetCellValue(row, 0)
        selected_papers = Paper(self.db).where(title=selected_paper_title)
        self.selected_paper = selected_papers[0]
        self.openPaper(event)

    def paperGridRightClick(self, event):
        # --- Extract selected Paper ---#
        self.row = event.GetRow()
        selected_paper_title = self.paper_grid.GetCellValue(self.row, 0)
        selected_papers = Paper(self.db).where(title=selected_paper_title)
        self.selected_paper = selected_papers[0]

        # --- Configure Menu ---#
        menu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.registerPaper, menu.Append(-1, 'Register New Paper'))
        self.Bind(wx.EVT_MENU, self.openPaper, menu.Append(-1, 'Open PDF File'))
        self.Bind(wx.EVT_MENU, self.copyPaperBibtex, menu.Append(-1, 'Copy Bibtex'))
        self.Bind(wx.EVT_MENU, self.copyPaperFile, menu.Append(-1, 'Copy File'))
        self.Bind(wx.EVT_MENU, self.showPaper, menu.Append(-1, 'Show'))
        self.Bind(wx.EVT_MENU, self.editPaper, menu.Append(-1, 'Edit'))
        self.Bind(wx.EVT_MENU, self.deletePaper, menu.Append(-1, 'Delete'))
        self.paper_grid.PopupMenu(menu)
        menu.Destroy()

    def pgridLabelLeftClicked(self, event):
        """Sort Grid

        Args:
            event
        """
        if event.GetCol() == 1:
            self.pgrid_title_state = 0
            self.pgrid_register_state = 0
            self.pgrid_update_state = 0
            self.paper_grid.SetColLabelValue(0, "Title")
            self.paper_grid.SetColLabelValue(5, "Registered At")
            self.paper_grid.SetColLabelValue(6, "Updated At")
            if self.pgrid_year_state == 0:
                self.paper_grid.SetColLabelValue(1, "Year↓")
                self.pgrid_year_state = 1
            elif self.pgrid_year_state == 1:
                self.paper_grid.SetColLabelValue(1, "Year↑")
                self.pgrid_year_state = 2
            elif self.pgrid_year_state == 2:
                self.paper_grid.SetColLabelValue(1, "Year")
                self.pgrid_year_state = 0
        elif event.GetCol() == 0:
            self.pgrid_year_state = 0
            self.pgrid_register_state = 0
            self.paper_grid.SetColLabelValue(1, "Year")
            self.paper_grid.SetColLabelValue(5, "Registered At")
            if self.pgrid_title_state == 0:
                self.paper_grid.SetColLabelValue(0, "Title↓")
                self.pgrid_title_state = 1
            elif self.pgrid_title_state == 1:
                self.paper_grid.SetColLabelValue(0, "Title↑")
                self.pgrid_title_state = 2
            elif self.pgrid_title_state == 2:
                self.paper_grid.SetColLabelValue(0, "Title")
                self.pgrid_title_state = 0
        elif event.GetCol() == 5:
            self.pgrid_title_state = 0
            self.pgrid_year_state = 0
            self.pgrid_update_state = 0
            self.paper_grid.SetColLabelValue(0, "Title")
            self.paper_grid.SetColLabelValue(1, "Year")
            self.paper_grid.SetColLabelValue(6, "Updated At")
            if self.pgrid_register_state == 0:
                self.paper_grid.SetColLabelValue(5, "Registered At↓")
                self.pgrid_register_state = 1
            elif self.pgrid_register_state == 1:
                self.paper_grid.SetColLabelValue(5, "Registered At↑")
                self.pgrid_register_state = 2
            elif self.pgrid_register_state == 2:
                self.paper_grid.SetColLabelValue(5, "Registered At")
                self.pgrid_register_state = 0
        elif event.GetCol() == 6:
            self.pgrid_title_state = 0
            self.pgrid_year_state = 0
            self.pgrid_register_state = 0
            self.paper_grid.SetColLabelValue(0, "Title")
            self.paper_grid.SetColLabelValue(1, "Year")
            self.paper_grid.SetColLabelValue(5, "Registered At")
            if self.pgrid_update_state == 0:
                self.paper_grid.SetColLabelValue(6, "Updated At↓")
                self.pgrid_update_state = 1
            elif self.pgrid_update_state == 1:
                self.paper_grid.SetColLabelValue(6, "Updated At↑")
                self.pgrid_update_state = 2
            elif self.pgrid_update_state == 2:
                self.paper_grid.SetColLabelValue(6, "Updated At")
                self.pgrid_update_state = 0
        else:
            return

        self.searchPaper(event)

    def authGridLeftClick(self, event):
        event.Skip()

    def authGridRightClick(self, event):
        self.row = event.GetRow()
        selected_author_name = self.auth_grid.GetCellValue(self.row, 0)
        selected_authors = Author(self.db).where(name=selected_author_name)
        self.selected_author = selected_authors[0]

        # --- Configure Menu ---#
        menu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.registerAuthor, menu.Append(-1, 'Register New Author'))
        self.Bind(wx.EVT_MENU, self.showAuthor, menu.Append(-1, 'Show'))
        self.Bind(wx.EVT_MENU, self.editAuthor, menu.Append(-1, 'Edit'))
        self.Bind(wx.EVT_MENU, self.deleteAuthor, menu.Append(-1, 'Delete'))
        self.auth_grid.PopupMenu(menu)
        menu.Destroy()

    def affGridLeftClick(self, event):
        event.Skip()

    def affGridRightClick(self, event):
        self.row = event.GetRow()
        selected_aff_name = self.aff_grid.GetCellValue(self.row, 0)
        selected_affs = Affiliation(self.db).where(name=selected_aff_name)
        self.selected_aff = selected_affs[0]

        # --- Configure Menu ---#
        menu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.registerAffiliation, menu.Append(-1, 'Register New Affiliation'))
        self.Bind(wx.EVT_MENU, self.showAffiliation, menu.Append(-1, 'Show'))
        self.Bind(wx.EVT_MENU, self.editAffiliation, menu.Append(-1, 'Edit'))
        self.Bind(wx.EVT_MENU, self.deleteAffiliation, menu.Append(-1, 'Delete'))
        self.aff_grid.PopupMenu(menu)
        menu.Destroy()

    def treeCtrlActivated(self, event):
        selected_classification = Classification(self.db).where(name=self.clf_tree_ctrl.GetItemText(event.GetItem()))
        self.selected_clf_layer = self.getLayer(0, event.GetItem())
        if selected_classification == []:
            self.selected_clf = 'All'
        else:
            self.selected_clf = selected_classification[0]
        self.narrowClassification(event)

    def treeCtrlRightClicked(self, event):
        c = Classification(self.db)
        selected_classification = Classification(self.db).where(name=self.clf_tree_ctrl.GetItemText(event.GetItem()))
        if selected_classification == []:
            menu = wx.Menu()
            self.selected_clf = "All"
            self.Bind(wx.EVT_MENU, self.registerClassification, menu.Append(-1, 'Register New Classification'))
            self.Bind(wx.EVT_MENU, self.narrowClassification, menu.Append(-1, 'Clear Narrowing'))
        else:
            self.selected_clf = selected_classification[0]
            self.selected_clf_layer = self.getLayer(0, event.GetItem())
            menu = wx.Menu()
            self.Bind(wx.EVT_MENU, self.registerClassification, menu.Append(-1, 'Register New Classification'))
            self.Bind(wx.EVT_MENU, self.registerSubClassification, menu.Append(-1, 'Register Sub Classification in ' + str(self.selected_clf[1])))
            self.Bind(wx.EVT_MENU, self.showClassification, menu.Append(-1, 'Show Detail'))
            self.Bind(wx.EVT_MENU, self.editClassification, menu.Append(-1, 'Edit'))
            self.Bind(wx.EVT_MENU, self.deleteClassification, menu.Append(-1, 'Delete'))
            self.Bind(wx.EVT_MENU, self.narrowClassification, menu.Append(-1, 'Narrow Down by this Classification'))
        self.paper_grid.PopupMenu(menu)
        menu.Destroy()

    def searchByTitleAndIsRead(self, title, is_read):
        p = Paper(self.db)
        if is_read == "Done":
            isread = 1
        elif is_read == "Not Yet":
            isread = 0
        else:
            isread = None
        return p.where(title=title, isread=isread)

    def searchByAuthor(self, narAuthor):
        a = Author(self.db)
        authors = a.where(name=narAuthor)
        papers = []
        for author in authors:
            for paper in a.papers(author[0]):
                if paper == None:
                    continue
                papers.append(paper)
        self.indexAuthor(authors)
        return list(dict.fromkeys(papers))

    def searchByClf(self, clf):
        c = Classification(self.db)
        narClf = c.where(name=clf)
        return c.papers(narClf[0][0])

    def searchByAff(self, aff):
        af = Affiliation(self.db)
        narAff = af.where(name=aff)
        return af.papers(narAff[0][0])

    def resetSearching(self, event):
        self.title_txt_ctrl.SetValue("")
        self.author_txt_ctrl.SetValue("")
        self.clf_cmb.SetSelection(-1)
        self.aff_cmb.SetSelection(-1)
        self.has_read_cmb.SetSelection(-1)
        p = Paper(self.db)
        a = Author(self.db)
        self.indexPaper(p.All())
        self.indexAuthor(a.All())

    def exitProgram(self, event):
        self.Destroy()

    def openDatabase(self, event):
        welcomepage = WelcomePage(None, wx.ID_ANY, "")
        welcomepage.Show()

    def openRposLocation(self, event):
        os.startfile(os.path.abspath(os.path.dirname(__file__)))

    def closeDatabase(self, event):
        self.Close()
        welcomepage = WelcomePage(None, wx.ID_ANY, "")
        welcomepage.Show()
