import wx
import wx.grid
import wx.lib.buttons
import wx.lib.scrolledpanel
from scripts.database.database import Author, Affiliation


class ShowAuthor(wx.Frame):
    def __init__(self, *args, **kwds):
        self.db = args[2]
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 351))
        self.SetTitle("frame")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_4 = wx.Panel(self.panel_1, wx.ID_ANY)
        sizer_1.Add(self.panel_4, 1, wx.ALL | wx.EXPAND, 2)

        grid_sizer_1 = wx.FlexGridSizer(3, 2, 0, 0)

        name_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Name")
        name_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(name_lbl, 0, wx.ALL, 2)

        name_show_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        name_show_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        name_show_lbl.Wrap(400)
        name_show_lbl.SetLabel(self.GetParent().selected_author[1])
        grid_sizer_1.Add(name_show_lbl, 0, wx.ALL, 2)

        affiliation_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Affiliation")
        affiliation_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(affiliation_lbl, 0, wx.ALL, 2)

        affiliation_show_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        affiliation_show_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        a = Author(self.db)
        aff = a.affiliation(self.GetParent().selected_author[0])
        if aff != None:
            affiliation_show_lbl.SetLabel(aff[1])
        grid_sizer_1.Add(affiliation_show_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        papernum_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Number of Papers")
        papernum_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(papernum_lbl, 0, wx.ALL, 2)

        papernum_show_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        papernum_show_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        papernum_show_lbl.Wrap(400)
        papers = a.papers(self.GetParent().selected_author[0])
        papernum_show_lbl.SetLabel(str(len(papers)))
        grid_sizer_1.Add(papernum_show_lbl, 0, wx.ALL, 2)

        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_4, 3, wx.ALL | wx.EXPAND, 2)

        desc_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Description")
        desc_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_4.Add(desc_lbl, 0, wx.ALL, 2)

        self.panel_3 = wx.ScrolledWindow(self.panel_1, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.panel_3.SetScrollRate(10, 10)
        sizer_4.Add(self.panel_3, 1, wx.EXPAND, 0)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        desc_show_lbl = wx.StaticText(self.panel_3, wx.ID_ANY, "")
        desc_show_lbl.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        if self.GetParent().selected_author[2] != None:
            desc_show_lbl.SetLabel(self.GetParent().selected_author[2])
        sizer_2.Add(desc_show_lbl, 1, wx.ALL, 4)

        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_11, 0, wx.ALIGN_RIGHT, 0)

        self.narrowAuthor_btn = wx.Button(self.panel_1, wx.ID_ANY, "Narrow")
        self.narrowAuthor_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(self.narrowAuthor_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        self.editAuthor_btn = wx.Button(self.panel_1, wx.ID_ANY, "Edit")
        self.editAuthor_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(self.editAuthor_btn, 0, wx.ALL, 7)

        self.close_btn = wx.Button(self.panel_1, wx.ID_ANY, "Close")
        self.close_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(self.close_btn, 0, wx.ALL, 7)

        self.panel_3.SetSizer(sizer_2)

        self.panel_4.SetSizer(grid_sizer_1)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.narrowAuthor, self.narrowAuthor_btn)
        self.Bind(wx.EVT_BUTTON, self.editAuthor, self.editAuthor_btn)
        self.Bind(wx.EVT_BUTTON, self.closeWindow, self.close_btn)

    def narrowAuthor(self, event):
        self.GetParent().narAuthor_txtCtrl.SetValue(self.GetParent().selected_author[1])
        self.GetParent().narrowPaper(event)
        self.GetParent().notebook.SetSelection(0)

    def editAuthor(self, event):
        self.Close()
        editAuthor = EditAuthor(self.GetParent(), wx.ID_ANY, self.db)
        editAuthor.Show()

    def closeWindow(self, event):
        self.Close()


class EditAuthor(wx.Frame):
    def __init__(self, *args, **kwds):
        self.db = args[2]
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 396))
        self.SetTitle("rpos : Edit Author")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)

        Name = wx.StaticText(self.panel_1, wx.ID_ANY, "Name")
        Name.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_3.Add(Name, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.name_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.name_txt.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.name_txt.SetFocus()
        self.name_txt.AppendText(self.GetParent().selected_author[1])
        sizer_3.Add(self.name_txt, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(sizer_4, 4, wx.EXPAND, 0)

        desc_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Description")
        desc_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_4.Add(desc_lbl, 0, wx.ALL, 3)

        self.desc_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        self.desc_txt.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.desc_txt.SetFocus()
        if self.GetParent().selected_author[2] != None:
            self.desc_txt.SetValue(self.GetParent().selected_author[2])
        sizer_4.Add(self.desc_txt, 8, wx.ALL | wx.EXPAND, 3)

        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_6, 0, wx.ALL | wx.EXPAND, 2)

        affiliation_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Affiliation")
        affiliation_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_6.Add(affiliation_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.affiliation_cmb = wx.ComboBox(self.panel_1, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.affiliation_cmb.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        af = Affiliation(self.db)
        affs = af.All()
        self.affiliation_cmb.Append("")
        for i, aff in enumerate(affs):
            self.affiliation_cmb.Append(aff[1])
            if self.GetParent().selected_author[3] == aff[0]:
                self.affiliation_cmb.SetSelection(i + 1)
        sizer_6.Add(self.affiliation_cmb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.edit_btn = wx.Button(self.panel_1, wx.ID_ANY, "Update")
        self.edit_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_2.Add(self.edit_btn, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.editAuthor, self.edit_btn)

    def editAuthor(self, event):
        a = Author(self.db)
        af = Affiliation(self.db)

        name = self.name_txt.GetValue()
        desc = self.desc_txt.GetValue()
        if desc == "":
            desc = None
        aff = self.affiliation_cmb.GetValue()
        affs = af.where(name=aff)
        aff_id = affs[0][0]

        author = Author.getDicFormat(name, desc, affs[0][0])
        a.update(self.GetParent().selected_author[0], author)
        aff = a.affiliation(self.GetParent().selected_author[0])
        papers = a.papers(self.GetParent().selected_author[0])
        row_len = self.GetParent().row
        self.GetParent().auth_grid.SetCellValue(row_len, 0, name)
        self.GetParent().auth_grid.SetCellValue(row_len, 1, aff[1])
        self.GetParent().auth_grid.SetCellValue(row_len, 2, str(len(papers)))
        self.GetParent().auth_grid.SetCellValue(row_len, 3, desc if desc != None else "")
        self.Close()
