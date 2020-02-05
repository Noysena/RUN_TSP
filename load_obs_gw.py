#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 18:49:00 2019

@author: kanthanakorn
"""

import os
import time
from datetime import datetime
from tarot.search.pipeline_alert import SMS_direct_alert
from tarot.search.search_gw_alert_grandma import TAROT_Retrieve

# =============================================================================
# Read log and load images, loop data in every 15 minutes
#    print("Serach log on: %s" %datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))
# =============================================================================
#Gw event
def Check_Gws(gwsfile):
    # gwsfile = "Gws.txt"
    with open(gwsfile, 'r') as rgw:
        gwlist = rgw.readlines()
        
    gws = [x.rstrip() for x in gwlist]
    return gws

"""Error log sms report"""
file = "/tmp/read_log_err.txt"

reset_sms_log = input("Do you want to reset sms log (y/n)?: ")
if reset_sms_log == "y":
    if os.path.exists(file):
        os.remove(file)
    else:
        pass
    print("Remove: %s" %file)
else:
    print("Not reset sms alert log: %s" %file)
    with open(file, 'w') as write_log_err:
        write_log_err.write("sent")

for i in ("|", "/", "-", "\\","|", "/", "-", "\\","|", "/", "-", "\\"):
    print("Will start load log shortly...%s" %(i), end='\r') 
    time.sleep(0.25)
    
"""Read grenouille.lgo , log will transfer data every 12:00 (Noon)"""
while True:
    """ Check link TAROT """
    logtt = []
    os.system('clear')
    # gwsfile = "Gws.txt"
    # gws = Check_Gws(gwsfile)
    
    # Load TCA
    print("Read log TCA: %s" %datetime.utcnow().isoformat(' '))
    TCA = TAROT_Retrieve()
    try:
        TCA.Read_Event_Page(TCA.main_link_tca)
    except:
        TCA.gws = []
        
    for link_gw in TCA.gws:
        if len(link_gw) == 13:
            gw = link_gw.replace('.html', '_')
        else:
            gw = link_gw.replace('.html', '')
            
        print("Load event: %s" %gw)
        
        try:
            TCA.Check_Log_link('TCA', link_gw)
            TCA.Read_Log('TCA')
            TCA.Load_Fits(tele='TCA', gwevent = gw)
            
            TCA_err = 1
        except:
            TCA_err = 0
            logtt.append("TCA")
            pass
    
    # Load TCH
    print("Read log TCH %s" %datetime.utcnow().isoformat(' '))
    TCH = TAROT_Retrieve()
    try:
        TCH.Read_Event_Page(TCH.main_link_tch)
    except:
        TCH.gws = []
        
    for link_gw in TCH.gws:
        if len(link_gw) == 13:
            gw = link_gw.replace('.html', '_')
        else:
            gw = link_gw.replace('.html', '')

        print("Load event: %s" %gw)
        
        try:        
            TCH.Check_Log_link('TCH', link_gw)
            TCH.Read_Log('TCH')
            TCH.Load_Fits(tele='TCH', gwevent = gw)
            
            TCH_err = 1
        except:
            TCH_err = 0
            logtt.append("TCH")
            pass
    
    # Load TRE
    print("Read log TRE %s" %datetime.utcnow().isoformat(' '))
    TRE = TAROT_Retrieve()
    try:
        TRE.Read_Event_Page(TRE.main_link_tre)
    except:
        TRE.ges = []
        
    for gw in TRE.gws:
        if len(link_gw) == 13:
            gw = link_gw.replace('.html', '_')
        else:
            gw = link_gw.replace('.html', '')
            
        print("Load event: %s" %gw)
        
        try:
            TRE.Check_Log_link('TRE', link_gw)
            TRE.Read_Log('TRE')
            TRE.Load_Fits(tele='TRE', gwevent = gw)
            
            TRE_err = 1
        except:
            TRE_err = 0
            logtt.append("TRE")
            pass

    """ Check err log and send sms alert to user"""
    try:
        TCA_err
    except(NameError):
        TCA_err = 0
    
    try:
        TCH_err
    except(NameError):
        TCH_err = 0
        
    try:
        TRE_err
    except(NameError):
        TRE_err = 0
        
    errs = TCA_err + TCH_err + TRE_err
    
    if errs < 3:
        """ Check read log if it is err"""
        f = open(file, 'a')
        f.write("err")
        f.close()
        
        if errs == 2:
            text = ("LogErr_%s" %logtt[0])
        elif errs == 1:
            text = ("LogErr_%s_%s" %(logtt[0], logtt[1]))
        elif errs == 0:
            text = ("LogErr_%s_%s_%s" %(logtt[0], logtt[1], logtt[2]))
        else:
            pass
        
        print("Sent sms error log: %s" %text)
        
        with open(file, 'r') as read_log_err:
            log_err = read_log_err.readlines()
#            print(log_err[0])
            print("Will send sms: ", log_err[0]=="err")
            if log_err[0].rstrip() == "err":
                """Alert user and recode sending sms"""
                SMS_direct_alert(text)
                with open(file, 'w') as write_log_err:
                    write_log_err.write("sent")
            else:
                pass
    else:
        pass
    
# =============================================================================
# Wati fo rthe next retriving    
# =============================================================================
    count = 0
    end_count = 60*20 # 60sec * 10mins (Best time between 14 - 20 mins)
    while count <= end_count:
        
        for i in ("|", "/", "-", "\\"):
            print("Waiting for next search...%s" %(i), end='\r')
            count += 1
            try:
                time.sleep(1)
            except(KeyboardInterrupt, SystemExit):
                raise
