import wx
import wx.grid
import wx.lib.mixins.listctrl as listmix
from database.database import Affiliation


class AffListCtrl(wx.ListCtrl, listmix.CheckListCtrlMixin, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, panel, style):
        wx.ListCtrl.__init__(self, panel, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER, size=wx.Size(395, 467), pos=wx.Point(10, 20))
        listmix.CheckListCtrlMixin.__init__(self)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.checkedItem = []

    def OnCheckItem(self, index, flag):
        af = Affiliation(self.GetParent().GetParent().db)
        aff = af.find(int(self.GetItemText(index, 1)))
        if flag == True:
            self.checkedItem.append(aff[0])
        elif (flag == False):
            self.checkedItem.remove(aff[0])


class RegisterAffiliation(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: RegisterAffiliation.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 330))
        self.SetTitle("rpos : Register Affiliation")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.FlexGridSizer(2, 2, 5, 5)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        name_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Name")
        name_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_2.Add(name_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.name_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.name_txt.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_2.Add(self.name_txt, 1, wx.ALL | wx.EXPAND, 2)

        self.attribute_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Attribute")
        self.attribute_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_2.Add(self.attribute_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.attribute_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.attribute_txt.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_2.Add(self.attribute_txt, 1, wx.ALL | wx.EXPAND, 2)

        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_11, 5, wx.EXPAND, 0)

        description_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Description")
        description_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(description_lbl, 0, wx.ALL, 3)

        self.description_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        sizer_11.Add(self.description_txt, 12, wx.ALL | wx.EXPAND, 2)

        self.registerAff_btn = wx.Button(self.panel_1, wx.ID_ANY, "Create")
        self.registerAff_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_1.Add(self.registerAff_btn, 0, wx.ALIGN_RIGHT | wx.ALL, 7)

        sizer_2.AddGrowableCol(1)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()
        self.db = args[2]
        self.affs_id = []

        self.Bind(wx.EVT_BUTTON, self.registerAffiliation, self.registerAff_btn)
        # end wxGlade

    def registerAffiliation(self, event):
        name = self.name_txt.GetValue()
        description = self.description_txt.GetValue() if self.description_txt.GetValue() != None else None
        attribute = self.attribute_txt.GetValue() if self.attribute_txt.GetValue() != None else None

        af = Affiliation(self.db)
        affiliation = af.getDicFormat(name, description, attribute)
        af.create(affiliation)
        self.Close()
        row_len = self.GetParent().aff_grid.GetNumberRows()
        self.GetParent().aff_grid.AppendRows()
        self.GetParent().aff_grid.SetCellValue(row_len, 0, name)
        self.GetParent().aff_grid.SetCellValue(row_len, 1, attribute if attribute != None else "")
# end of class RegisterAffiliation


class ShowAffiliation(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ShowAffiliation.__init__
        self.db = args[2]
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 300))
        self.SetTitle("rpos : Show Affiliation")

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_4 = wx.Panel(self.panel_1, wx.ID_ANY)
        sizer_1.Add(self.panel_4, 1, wx.ALL | wx.EXPAND, 2)

        grid_sizer_1 = wx.FlexGridSizer(2, 2, 0, 0)

        name_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Name")
        name_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(name_lbl, 0, wx.ALL, 2)

        name_show_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        name_show_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        name_show_lbl.Wrap(400)
        name_show_lbl.SetLabel(self.GetParent().selected_aff[1])
        grid_sizer_1.Add(name_show_lbl, 0, wx.ALL, 2)

        attribute_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Attribute")
        attribute_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(attribute_lbl, 0, wx.ALL, 2)

        attribute_show_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        attribute_show_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        attribute_show_lbl.Wrap(400)
        attribute_show_lbl.SetLabel(str(self.GetParent().selected_aff[3]) if self.GetParent().selected_aff[3] != None else "")
        grid_sizer_1.Add(attribute_show_lbl, 0, wx.ALL, 2)

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
        desc_show_lbl.SetLabel(self.GetParent().selected_aff[2] if self.GetParent().selected_aff[2] != None else "")
        sizer_2.Add(desc_show_lbl, 1, wx.ALL, 4)

        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_11, 0, wx.ALIGN_RIGHT, 0)

        self.narrowAff_btn = wx.Button(self.panel_1, wx.ID_ANY, "Narrow")
        self.narrowAff_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(self.narrowAff_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        self.editAff_btn = wx.Button(self.panel_1, wx.ID_ANY, "Edit")
        self.editAff_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(self.editAff_btn, 0, wx.ALL, 7)

        self.close_btn = wx.Button(self.panel_1, wx.ID_ANY, "Close")
        self.close_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(self.close_btn, 0, wx.ALL, 7)

        self.panel_3.SetSizer(sizer_2)

        self.panel_4.SetSizer(grid_sizer_1)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.narrowAff, self.narrowAff_btn)
        self.Bind(wx.EVT_BUTTON, self.editAff, self.editAff_btn)
        self.Bind(wx.EVT_BUTTON, self.closeWindow, self.close_btn)
        # end wxGlade

    def narrowAff(self, event):  # wxGlade: ShowAffiliation.<event_handler>
        print("Event handler 'narrowAff' not implemented!")
        event.Skip()

    def editAff(self, event):  # wxGlade: ShowAffiliation.<event_handler>
        self.Close()
        editAff = EditAffiliation(self.GetParent(), wx.ID_ANY, self.db)
        editAff.Show()

    def closeWindow(self, event):  # wxGlade: ShowAffiliation.<event_handler>
        self.Close()
# end of class ShowAffiliation


class EditAffiliation(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: EditAffiliation.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 335))
        self.SetTitle("rpos : Edit Affiliation")

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_4 = wx.Panel(self.panel_1, wx.ID_ANY)
        sizer_1.Add(self.panel_4, 1, wx.ALL | wx.EXPAND, 2)

        grid_sizer_1 = wx.FlexGridSizer(2, 2, 5, 5)

        name_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Name")
        name_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(name_lbl, 0, wx.ALL, 2)

        self.name_txt = wx.TextCtrl(self.panel_4, wx.ID_ANY, "")
        self.name_txt.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.name_txt.SetFocus()
        self.name_txt.SetValue(self.GetParent().selected_aff[1] if self.GetParent().selected_aff[1] else "")
        grid_sizer_1.Add(self.name_txt, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)

        attribute_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Attribute")
        attribute_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(attribute_lbl, 0, wx.ALL, 2)

        self.attribute_txt = wx.TextCtrl(self.panel_4, wx.ID_ANY, "")
        self.attribute_txt.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.attribute_txt.SetFocus()
        self.attribute_txt.SetValue(self.GetParent().selected_aff[3] if self.GetParent().selected_aff[3] else "")
        grid_sizer_1.Add(self.attribute_txt, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)

        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_4, 2, wx.ALL | wx.EXPAND, 3)

        desc_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Description")
        desc_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_4.Add(desc_lbl, 0, wx.ALL, 2)

        self.panel_3 = wx.ScrolledWindow(self.panel_1, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.panel_3.SetScrollRate(10, 10)
        sizer_4.Add(self.panel_3, 1, wx.EXPAND, 0)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        self.desc_txt = wx.TextCtrl(self.panel_3, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        self.desc_txt.SetFocus()
        self.desc_txt.SetValue(self.GetParent().selected_aff[2] if self.GetParent().selected_aff[2] else "")
        sizer_2.Add(self.desc_txt, 1, wx.EXPAND, 0)

        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_11, 0, wx.ALIGN_RIGHT, 0)

        self.edit_btn = wx.Button(self.panel_1, wx.ID_ANY, "Close")
        self.edit_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(self.edit_btn, 0, wx.ALL, 7)

        self.panel_3.SetSizer(sizer_2)

        grid_sizer_1.AddGrowableRow(0)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableCol(1)
        self.panel_4.SetSizer(grid_sizer_1)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()
        self.db = args[2]

        self.Bind(wx.EVT_BUTTON, self.closeWindow, self.edit_btn)
        # end wxGlade

    def closeWindow(self, event):
        name = self.name_txt.GetValue()
        desc = self.desc_txt.GetValue() if self.desc_txt.GetValue() != None else None
        attribute = self.attribute_txt.GetValue() if self.attribute_txt.GetValue() != None else None
        af = Affiliation(self.db)
        aff = af.getDicFormat(name, desc, attribute)
        af.update(self.GetParent().selected_aff[0], aff)

        self.Close()
        row_len = self.GetParent().row
        self.GetParent().aff_grid.SetCellValue(row_len, 0, name)
        self.GetParent().aff_grid.SetCellValue(row_len, 1, attribute if attribute != None else "")
# end of class EditAffiliation


class AttachAffiliation(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: AttachAffiliation.__init__
        self.db = args[2]
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 300))
        self.SetTitle("rpos : Affiliation List")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_1.Add((0, 0), 0, 0, 0)

        self.listctrl = AffListCtrl(self.panel_1, style=wx.LC_REPORT)
        self.listctrl.InsertColumn(0, " ", wx.LIST_FORMAT_CENTER, 30)
        self.listctrl.InsertColumn(1, "id", wx.LIST_FORMAT_CENTER, 30)
        self.listctrl.InsertColumn(2, "name", wx.LIST_FORMAT_LEFT, 50)
        af = Affiliation(self.db)
        self.affs = af.All()
        for i, aff in enumerate(self.affs):
            self.listctrl.Append([" ", aff[0], aff[1]])
            if aff[0] in self.GetParent().affs_id:
                self.listctrl.CheckItem(i, True)
        sizer_1.Add(self.listctrl, 1, wx.ALL | wx.EXPAND, 2)

        self.attachClf_btn = wx.Button(self.panel_1, wx.ID_ANY, "Register")
        self.attachClf_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_1.Add(self.attachClf_btn, 0, wx.ALIGN_RIGHT | wx.ALL, 3)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.attachClf, self.attachClf_btn)

    def attachClf(self, event):
        self.GetParent().affs_id = self.listctrl.checkedItem
        self.Close()
        self.GetParent().showAffiliations()
