import wx
import wx.lib.mixins.listctrl as listmix
from scripts.database.database import Classification, ClassificationLabelManagement


class ClfListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, panel, style):
        wx.ListCtrl.__init__(self, panel, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER, size=wx.Size(395, 467), pos=wx.Point(10, 20))
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.EnableCheckBoxes(True)
        self.IsChecked = self.IsItemChecked
        self.checkedItem = []


class RegisterClassification(wx.Frame):
    def __init__(self, *args, **kwds):
        self.db = args[2]
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 377))
        self.SetTitle("rpos : Register Classification")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        grid_sizer_1 = wx.FlexGridSizer(3, 2, 5, 5)
        sizer_2.Add(grid_sizer_1, 1, wx.EXPAND, 0)

        name_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Name")
        name_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(name_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.name_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.name_txt.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.name_txt, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)

        sort_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Sort")
        sort_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(sort_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.sort_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.sort_txt.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.sort_txt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)

        parent_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Parent")
        parent_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(parent_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.parent_cmb = wx.ComboBox(self.panel_1, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.parent_cmb.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.parent_cmb.Append("")
        clfs = self.GetParent().getClfWithSubLayer()
        for i, clf in enumerate(clfs):
            self.parent_cmb.Append(str("  ") * clf[0] + clf[1])
            if clf[1] == self.GetParent().selected_clf[1] and self.GetParent().parent is not None:
                self.parent_cmb.SetSelection(i + 1)
        grid_sizer_1.Add(self.parent_cmb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(sizer_4, 4, wx.EXPAND, 0)

        desc_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Description")
        desc_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_4.Add(desc_lbl, 0, wx.ALL, 3)

        self.desc_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        self.desc_txt.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_4.Add(self.desc_txt, 8, wx.ALL | wx.EXPAND, 3)

        self.create_btn = wx.Button(self.panel_1, wx.ID_ANY, "Create")
        self.create_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_2.Add(self.create_btn, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        grid_sizer_1.AddGrowableCol(1)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.createClassification, self.create_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)

    def onKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

    def createClassification(self, event):
        name = self.name_txt.GetValue()
        desc = self.desc_txt.GetValue()
        turn = self.sort_txt.GetValue()
        parent = self.parent_cmb.GetValue().strip()
        if turn == None or turn == "":
            turn = 0
        parent_clf = self.parent_cmb.GetValue()
        c = Classification(self.db)
        clf = c.getDicFormat(name, desc, turn)
        clf = c.create(clf)

        # --- Register Relation ---#
        if parent != "":
            cl_m = ClassificationLabelManagement(self.db)
            parent_clf = c.where(name=parent)
            cl_m.create(parent_clf[0][0], clf[0])
        self.Close()

        # --- Update TreeCtrl ---#
        clfs = c.All(column='turn')
        self.GetParent().indexClassifications(c, clfs)
        self.GetParent().setClfSelection()


class ShowClassification(wx.Frame):
    def __init__(self, *args, **kwds):
        self.db = args[2]
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 300))
        self.SetTitle("rpos : Show Classification")

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
        name_show_lbl.SetLabel(self.GetParent().selected_clf[1])
        grid_sizer_1.Add(name_show_lbl, 0, wx.ALL, 2)

        turn_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "Turn")
        turn_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(turn_lbl, 0, wx.ALL, 2)

        turn_show_lbl = wx.StaticText(self.panel_4, wx.ID_ANY, "")
        turn_show_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        turn_show_lbl.Wrap(400)
        turn_show_lbl.SetLabel(str(self.GetParent().selected_clf[3]))
        grid_sizer_1.Add(turn_show_lbl, 0, wx.ALL, 2)

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
        desc_show_lbl.SetLabel(self.GetParent().selected_clf[2] if self.GetParent().selected_clf[2] != None else "")
        sizer_2.Add(desc_show_lbl, 1, wx.ALL, 4)

        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_11, 0, wx.ALIGN_RIGHT, 0)

        self.narrowClf_btn = wx.Button(self.panel_1, wx.ID_ANY, "Narrow")
        self.narrowClf_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_11.Add(self.narrowClf_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

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

        self.Bind(wx.EVT_BUTTON, self.narrowClf, self.narrowClf_btn)
        self.Bind(wx.EVT_BUTTON, self.editClf, self.editAuthor_btn)
        self.Bind(wx.EVT_BUTTON, self.closeWindow, self.close_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)

    def onKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

    def narrowClf(self, event):
        self.GetParent().narClf_cmb.SetString(self.GetParent().selected_clf[1])
        self.GetParent().narrowPaper(event)
        self.GetParent().notebook.SetSelection(0)

    def editClf(self, event):
        self.Close()
        editClf = EditClassification(self.GetParent(), wx.ID_ANY, self.db)
        editClf.Show()

    def closeWindow(self, event):
        self.Close()


class EditClassification(wx.Frame):
    def __init__(self, *args, **kwds):
        self.db = args[2]
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 426))
        self.SetTitle("rpos : Edit Classification")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)

        grid_sizer_1 = wx.FlexGridSizer(3, 2, 5, 5)
        sizer_2.Add(grid_sizer_1, 1, wx.EXPAND, 0)

        name_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Name")
        name_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(name_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.name_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.name_txt.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.name_txt.SetFocus()
        if self.GetParent().selected_clf[1] != None:
            self.name_txt.SetValue(self.GetParent().selected_clf[1])
        grid_sizer_1.Add(self.name_txt, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)

        sort_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Sort Num")
        sort_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(sort_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.sort_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.sort_txt.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.sort_txt.SetFocus()
        self.sort_txt.SetValue(str(self.GetParent().selected_clf[3]))
        grid_sizer_1.Add(self.sort_txt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)

        parent_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Parent")
        parent_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(parent_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.parent_cmb = wx.ComboBox(self.panel_1, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.parent_cmb.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        c = Classification(self.db)
        parent_clf = c.parentclasses(self.GetParent().selected_clf[0])
        self.parent_cmb.Append("")
        clfs = self.GetParent().getClfWithSubLayer()
        for i, clf in enumerate(clfs):
            self.parent_cmb.Append(str("  ") * clf[0] + clf[1])
            if parent_clf != [] and clf[1] == parent_clf[0][1]:
                self.parent_cmb.SetSelection(i + 1)
        grid_sizer_1.Add(self.parent_cmb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(sizer_3, 2, wx.EXPAND, 0)

        desc_lbl = wx.StaticText(self.panel_1, wx.ID_ANY, "Description")
        desc_lbl.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_3.Add(desc_lbl, 0, wx.ALL, 3)

        self.desc_txt = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        self.desc_txt.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        self.desc_txt.SetFocus()
        if self.GetParent().selected_clf[2] != None:
            self.desc_txt.SetValue(self.GetParent().selected_clf[2])
        sizer_3.Add(self.desc_txt, 8, wx.ALL | wx.EXPAND, 3)

        self.edit_btn = wx.Button(self.panel_1, wx.ID_ANY, "Update")
        self.edit_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_2.Add(self.edit_btn, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        grid_sizer_1.AddGrowableCol(1)

        self.panel_1.SetSizer(sizer_2)

        self.Layout()
        self.Centre()
        self.RegisterHotKey(1234, wx.MOD_CONTROL, ord('z'))

        self.Bind(wx.EVT_BUTTON, self.editClassification, self.edit_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)

    def onKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

    def editClassification(self, event):
        # --- Register New Classification ---#
        name = self.name_txt.GetValue()
        desc = self.desc_txt.GetValue()
        turn = self.sort_txt.GetValue()
        parent = self.parent_cmb.GetValue().strip()
        if turn == None or turn == "":
            turn = 0
        parent_clf = self.parent_cmb.GetValue()
        c = Classification(self.db)
        clf = c.getDicFormat(name, desc, turn)
        c.update(self.GetParent().selected_clf[0], clf)

        # --- Edit Relation ---#
        cl_m = ClassificationLabelManagement(self.db)
        parent_clf_l_man = cl_m.where(sub_classification_id=self.GetParent().selected_clf[0])
        if parent_clf_l_man != []:
            cl_m.deleteByID(parent_clf_l_man[0][0])
        if parent != "":
            parent_clf = c.where(name=parent)
            cl_m.create(parent_clf[0][0], self.GetParent().selected_clf[0])
        self.Close()
        self.GetParent().indexClassifications(c, c.All(column="turn"))

        # --- Update TreeCtrl ---#
        clfs = c.All(column='turn')
        self.GetParent().indexClassifications(c, clfs)
        self.GetParent().setClfSelection()


class AttachClassification(wx.Frame):
    def __init__(self, *args, **kwds):
        self.db = args[2]
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((285, 585))
        self.SetTitle("rpos : Classification List")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./resource/document-2-512.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_1.Add((0, 0), 0, 0, 0)

        self.listctrl = ClfListCtrl(self.panel_1, style=wx.LC_REPORT)
        self.listctrl.InsertColumn(0, " ", wx.LIST_FORMAT_CENTER, 30)
        self.listctrl.InsertColumn(1, "id", wx.LIST_FORMAT_CENTER, 30)
        self.listctrl.InsertColumn(2, "name", wx.LIST_FORMAT_LEFT, 50)
        clfs_layer = self.GetParent().GetParent().getClfWithSubLayer()
        c = Classification(self.db)
        self.clfs = c.All()
        for i, clf_layer in enumerate(clfs_layer):
            clf_buf = c.where(name=clf_layer[1])
            clf = clf_buf[0]
            self.listctrl.Append([" ", clf[0], "   " * clf_layer[0] + clf[1]])
            if clf[0] in self.GetParent().clfs_id:
                self.listctrl.CheckItem(i, True)
        sizer_1.Add(self.listctrl, 1, wx.ALL | wx.EXPAND, 2)

        self.attachClf_btn = wx.Button(self.panel_1, wx.ID_ANY, "Register")
        self.attachClf_btn.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_1.Add(self.attachClf_btn, 0, wx.ALIGN_RIGHT | wx.ALL, 3)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.attachClf, self.attachClf_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)

    def onKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

    def attachClf(self, event):
        self.GetParent().clfs_id = []
        for i in range(self.listctrl.GetItemCount()):
            if self.listctrl.IsChecked(i):
                self.GetParent().clfs_id.append(self.listctrl.GetItemText(i, 1))
        self.Close()
        self.GetParent().indexClassifications()
