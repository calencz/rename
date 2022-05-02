#rev. 0.220428
#rev. 0.220430

#coding=utf-8

import os
import re

def VideoRes(sub):
    from pymediainfo import MediaInfo
    t_track = ""  # t_track:视频文件分辨率的初始化
    
    ##print ("--"+sub)
    suff = os.path.splitext(sub) # 将文件名和扩展名拆分成一个列表["文件名“，”.扩展名"]
    if suff[1] in [".mp4",".mkv",".avi",".wmv",".MP4",".MKV",".AVI",".WMV"]:   #rev. 0.220430 增加大写判定
        info = MediaInfo.parse(".\\"+olddirname+"\\"+sub) # 需要将子目录的路径一起写上
        #data = info.to_json()
        #print(data)
        for trackinfo in info.tracks:  # MediaInfo.parse.tracks：一个列表，列表的每个元素为一条轨道（Track）对象，对象包含媒体信息 
            if trackinfo.track_type == "Video": # track_type属性，说明轨道是视频（video）还是音频（Audio）
                if trackinfo.height != "":   #rev. 0.220430
                    # print (trackinfo.height)  
                    if trackinfo.scan_type == "MBAFF": # scan_type属性，说明视频是隔行扫描（MBAFF）还是逐行扫描（Progressive）
                        t_track = str(trackinfo.height)+"i"
                        # print ("--",t_track)  #  .tracks.height：视频的高度，数值变量
                    elif trackinfo.scan_type == "Progressive":
                        t_track = str(trackinfo.height)+"p"
                        # print ("--",t_track) 
                    else:
                        t_track = str(trackinfo.height)+"p"
                        # print ("--",t_track)
                else:
                    print ("分辨率无法识别")  #rev. 0.220430
        info = []
    else:
        pass
        # print ("--\""+sub+"\"","is not the media file or the directory name.") #rev. 0.220428
    return t_track

active = True
while active:
    message = " +----------------------------------------------+\n"
    message += " |                                              |\n"
    message += " |  1. 预览文件名                               |\n"
    message += " |  2. 更改文件名                               |\n"
    message += " |  3. 退出                                     |\n"
    message += " |                                              |\n"
    message += " +----------------------------------------------+\n"
    message += " 选择："
    choice = input (message)
    if choice == "3":
        active = False
        continue
    else:
        if choice not in ["1","2","3"]:
            print ("不是正确的选项序号，请重新选择")
            continue
        rootpath = os.getcwd() # rootpath: 当前目录名
        print ("当前目录名:",rootpath)  # 显示当前目录名
        w_name = os.listdir(rootpath) # w_name: 当前目录下的文件和子目录名列表
        regname = re.compile(r'\[(.*?)\]',re.S) # regname: 提取[]内容的正则表达式
        parname = re.compile(r'[(（](.*?)[）)]',re.S) # regname: 提取全角（）或半角()内容的正则表达式
        for olddirname in w_name:
            if os.path.isdir (olddirname): # 判断是否为目录名
                print ("\n","旧子目录名: ",olddirname)
                # 演员人名有几种形式：
                # 1，单个人名。
                # 2，多个人名，用","分隔。
                # 3，单个人名，但有曾用名，用全角的"（）"或半角"()"标注。
                
                avinfo = re.findall(regname,olddirname) # 将[]内容用正则表达式提取出来，并组成一个列表，avinfo: []内容列表
                avinfo_rname = re.findall(parname,avinfo[0]) #avinfo[0]：默认第一个[]内为人名，人名内可能会有（）或()作为曾用名，本行将提取（）或()内的曾用名
                #print (avinfo_rname)
                if avinfo == []:
                    print ("不是正确的目录名","\n")
                else:
                    
                    #### 目录名去掉末尾人名冗余 ###
                    print ("【姓名】:",avinfo[0]) # 默认avinfo[0]是姓名
                    avname1 = avinfo[0].split(",") # 拆分avinfo[0],如果多姓名并且用","分隔，avname1：多个姓名拆分后的列表
                    ##print (avname1)
                    
                    for indx,avname2 in enumerate(avname1): 
                        if re.findall(parname,avname2) != []:
                            avname1[indx] = re.sub(r"[(（]"+str(avinfo_rname[0])+r"[）)]","",avname2) # 将提取出来的当前人名和曾用名，插入到人名列表
                            avname1.insert(indx+1,avinfo_rname[0])
                    ##print (avname1)
                    
                    newdirname = olddirname
                    for avname3 in avname1:
                        dirname_sp = newdirname.rsplit("-"+avname3,1) #旧文件名从右向左，用"-人名"作为分隔符。
                        newdirname = dirname_sp[0] # 新列表只取第一个元素--->达到将avname3删除(最终完成删除冗余姓名的目的)
                    ##print ("目录名去掉末尾人名冗余: ",newdirname)
                    
                    #### 目录名去掉天，保留年-月 ###
                    if len(avinfo[1].rsplit("-")) >= 3:
                        datename1 = avinfo[1].rsplit("-",1)
                        datename = datename1[0]
                    else:
                        datename = avinfo[1]
                    newdirnamed = re.sub(avinfo[1],datename,newdirname,1) # re.sub用正则表达式做字符串替换
                    ##print ("目录名去掉天，保留年-月: ",newdirnamed)
                
                ### 目录名增加视频分辨率信息和中文字幕信息（中文字幕仅限有-c标志） ###
                s_names = os.listdir(".\\"+olddirname) ## s_names是子目录内的文件和目录列表
                resl = []   #考虑文件夹内可能有多个视频文件，分辨率变量设置为list
                match = 0
                for subname in s_names:
                    res = VideoRes(subname)
                    if res != "":
                        resl.append(res)
                    if re.search("-c",subname,re.I) == None:  ## 判断文件名是否有-C,search()方法用于在整个字符串中搜索第一个匹配的值,如果匹配成功,则返回一个Match对象,否则返回None.
                        match += 0
                    else:
                        match += 1  #文件名有一个带-C，就可认定为带中文字幕 2022/01/08
                resl_str = ",".join(resl)
                if resl_str not in newdirname:  #判断文件是否已经改名 2022/01/08
                    if resl != [] and match != 0:
                        newdirname_hc = newdirnamed+" ["+resl_str+"]"+" [chn]" #join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串
                        if choice == "1":
                            print ("目录名增加视频分辨率信息，有字幕：",newdirname_hc)
                        elif choice == "2":
                            os.rename (olddirname,newdirname_hc)
                            print (newdirname_hc+" -----> 改名完成") if os.path.exists(newdirname_hc) else print (newdirname_hc+" -----> 改名失败")
                    elif resl != [] and match == 0:
                        newdirname_h = newdirnamed+" ["+resl_str+"]"
                        if choice == "1":
                            print ("目录名增加视频分辨率信息，无字幕：",newdirname_h)
                        elif choice == "2":
                            os.rename (olddirname,newdirname_h)
                            print (newdirname_h+" -----> 改名完成") if os.path.exists(newdirname_h) else print (newdirname_h+" -----> 改名失败")
                    else:
                        print ("目录内无视频：",newdirnamed)
                else:
                    print (newdirname)
                    print (" -----> 文件已改名！")
            else:
                print ("\n"+"\""+olddirname+"\"","is the file")
        continue