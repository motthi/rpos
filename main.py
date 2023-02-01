#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import wx
from scripts.rposmain import WelcomePage


class MyApp(wx.App):
    def OnInit(self):
        self.welcomepage = WelcomePage(None, wx.ID_ANY, "")
        self.SetTopWindow(self.welcomepage)
        self.welcomepage.Show()
        return True


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
