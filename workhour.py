#-*- coding: utf-8 -*-
'''Record the work hours'''

import wx
import wx.dataview as dv
from wx.lib.buttons import GenButton
from datetime import datetime
import sqlite3
import re
import time
import traceback
import logging

g_dbname  = 'workhour.db'
g_logname = 'workhour.log'
g_logger = None
g_sql_create ="create table if not exists workhour(date TEXT primary key, begin TEXT, end TEXT, verify TEXT, modify TEXT)"
g_sql_insert = "insert into workhour values('%s','%s','%s','%s','%s')"
g_sql_update = "update workhour set begin='%s', end='%s', verify='%s', modify='%s' where date = '%s'"
g_sql_select = "select * from  workhour where date = '%s'"
g_sql_search = "select * from  workhour"
        
class InputDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            ):

        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        self.PostCreate(pre)

        sizer = wx.BoxSizer(wx.VERTICAL)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "begin")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.text1 = wx.TextCtrl(self, -1, "", size=(80,-1))
        box.Add(self.text1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "end")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.text2 = wx.TextCtrl(self, -1, "", size=(80,-1))
        box.Add(self.text2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        #line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        #sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, 10, "insert", (20,20))
        self.Bind(wx.EVT_BUTTON, self.OnInsert, btn)
        btn.SetDefault()

        sizer.Add(btn, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        
        #True:insert    False:update
        self.IUflag = True
        
        conn = None
        day = datetime.now().strftime('%Y-%m-%d')
        try:
            conn = sqlite3.connect(g_dbname)
            curs = conn.cursor()
            curs.execute(g_sql_select % day)
            row = curs.fetchone()
            if row:
                self.IUflag = False
                self.text1.SetValue(row[1])
                self.text2.SetValue(row[2])
            g_logger.info('select')
        except:
            g_logger.error(traceback.format_exc())
            dlg = wx.MessageDialog(self, traceback.format_exc(), 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()            
        finally:
            if conn:
                conn.close()        
        
    def OnInsert(self, event):
        begin_t = self.text1.GetValue()
        end_t   = self.text2.GetValue()
        #check begin_t and end_t
        if begin_t == '' and end_t == '':
            err = 'warning:Input one at least!'
            g_logger.warning(err)
            dlg = wx.MessageDialog(self, err, 'Warn', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()             
            return
        pattern  = re.compile('^\d{2}:\d{2}$')
        if (begin_t != '' and not re.match(pattern, begin_t)) or (end_t != '' and not re.match(pattern, end_t)):
            err = 'The format is wrong!(xx:xx)'
            g_logger.warning(err)
            dlg = wx.MessageDialog(self, err, 'Warn', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()            
            return
        
        now     = datetime.now()
        day     = now.strftime('%Y-%m-%d') 
        verify  = ''
        modify  = now.strftime('%Y-%m-%d %H:%M:%S') 
        #verify the work hours
        if '' != begin_t and '' != end_t:
            s = time.strptime(day + begin_t, '%Y-%m-%d%H:%M')    
            e = time.strptime(day + end_t, '%Y-%m-%d%H:%M')    
            
            seconds = time.mktime(e) - time.mktime(s)
            stand1 = time.strptime(day + '18:00', '%Y-%m-%d%H:%M')
            if e <= stand1:
                mins = (seconds - 1.5*3600)/60 
            elif e > stand1:
                mins = (seconds - 2*3600)/60 
            verify = str(mins- 8*60).split('.')[0]
            
        conn = None
        try:
            conn = sqlite3.connect(g_dbname)
            curs = conn.cursor()
            curs.execute(g_sql_create)
            if True == self.IUflag:
                curs.execute(g_sql_insert % (day, begin_t, end_t, verify, modify))
                g_logger.info('insert: %s   %s  %s' % (day, begin_t, end_t))
            else:
                curs.execute(g_sql_update % (begin_t, end_t, verify, modify, day))
                g_logger.info('update: %s   %s  %s' % (day, begin_t, end_t))
            conn.commit()
            
            dlg = wx.MessageDialog(self, 'Successful!', 'Success', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()            
        except:
            g_logger.error(traceback.format_exc())
            dlg = wx.MessageDialog(self, traceback.format_exc(), 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()            
        finally:
            if conn:
                conn.close()
                
        self.Destroy()

class WorkHour(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "WorkHour", size=(480,500)) 
        
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        btnS = wx.Button(self, 10, "search", (20,20))
        btnS.Bind(wx.EVT_BUTTON, self.OnSearch)
        btnS.SetDefault()
        btnS.SetSize(btnS.GetBestSize())
        
        btnSizer.Add(btnS, 0, wx.ALL, 4)
        
        btnI = wx.Button(self, 10, "insert", (20,20))
        btnI.Bind(wx.EVT_BUTTON, self.OnInsert)
        btnI.SetDefault()
        btnI.SetSize(btnI.GetBestSize())
        
        btnSizer.Add(btnI, 0, wx.ALL, 4)
        
        self.label = wx.StaticText(self, -1, "Total:");
        
        btnSizer.Add(self.label, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        ''' 
        btnM = wx.Button(self, 10, "modify", (20,20))
        self.Bind(wx.EVT_BUTTON, self.OnModify, btnM)
        btnM.SetDefault()
        btnM.SetSize(btnS.GetBestSize())
        '''
        
        self.dvlc = dvlc = dv.DataViewListCtrl(self)
        dvlc.AppendTextColumn('date', width = 80) 
        dvlc.AppendTextColumn('begin', width = 80) 
        dvlc.AppendTextColumn('end', width = 80) 
        dvlc.AppendTextColumn('verify/min', width = 80) 
        dvlc.AppendTextColumn('modify', width = 160) 
        
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(btnSizer, 0, wx.ALL, 4)
        self.Sizer.Add(dvlc, 1, wx.EXPAND)
        
        
        #call the Onsearch
        #wx.PostEvent(self, wx.CommandEvent(wx.EVT_BUTTON.typeId, btnS.GetId()))
        self.OnSearch(0)
        
    def OnSearch(self, event):
        conn = None
        date = datetime.now().strftime('%Y-%m-%d')
        try:
            conn = sqlite3.connect(g_dbname)
            curs = conn.cursor()
            curs.execute(g_sql_search)
            rows = curs.fetchall()
            self.dvlc.DeleteAllItems()
            Total = 0.0
            for row in rows:
                if '' != row[3]:
                    Total += int(row[3])
                self.dvlc.InsertItem(0, row)
            self.label.SetLabelText('Total:' + str(Total))
            g_logger.info('search')
        except:
            g_logger.error(traceback.format_exc())
            dlg = wx.MessageDialog(self, traceback.format_exc(), 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        finally:
            if conn:
                conn.close()
        
    def OnInsert(self, event):
        dlg = InputDialog(self, -1, "Insert", size=(550, 200),
                         style=wx.DEFAULT_DIALOG_STYLE, )
        val = dlg.ShowModal()
        dlg.Destroy()        
        self.OnSearch(0)
        
    def OnModify(self, event):
        pass
    
if __name__ == '__main__':
    #log
    g_logger = logging.getLogger()
    log_file = logging.FileHandler(g_logname)
    g_logger.addHandler(log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    log_file.setFormatter(formatter)
    g_logger.setLevel(logging.DEBUG)
           
    #start up
    g_logger.info('**********************************Start**********************************')
    app = wx.PySimpleApp()
    dlg = WorkHour()
    dlg.ShowModal()
    #app.MainLoop()
    g_logger.info('**********************************Stop**********************************')
