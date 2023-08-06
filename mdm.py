import flet as ft
import pandas as pd
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
import matplotlib
import os
import datetime
global viewlist
viewlist=[]
data=pd.read_excel('data.xlsx')
data.fillna('',inplace=True)
oldd=data.copy(deep=True)

print(data)

wfl=pd.read_excel('data/boyswfl.xlsx',index_col='Length')
wfl2=pd.read_excel('data/girlwfl.xlsx',index_col='Length')
wfa=pd.read_excel('data/boyswfa.xlsx',index_col='Day')
wfa2=pd.read_excel('data/girlwfa.xlsx',index_col='Day')
lfa=pd.read_excel('data/boyslfa.xlsx',index_col='Day')
lfa2=pd.read_excel('data/girllfa.xlsx',index_col='Day')

lidata=[[wfl,wfa,lfa],[wfl2,wfa2,lfa2],['Height/Length for Age','Weight for Age','Weight for length'],[['length','weight'],['Age (months)','weight'],['Age (months)','length']]]
madata={'M':[wfl,wfa,lfa],'F':[wfl2,wfa2,lfa2]}
matplotlib.use("svg")

def colorstatus(status):
    val=['Height/Length for Age','Weight for Age','Weight for length']
    y=['background-color: #ffffff','background-color: #ffffff','background-color: #ffffff']
    for i in range(len(val)):
     if status[val[i]]=='0SD to +2SD':#normal
          y[i]='background-color: #99ff99'
     if status[val[i]]=='-2SD to 0SD':#normal
          y[i]='background-color: #99ff99'
     if status[val[i]]=='-2SD to -3SD':#mild
          y[i]='background-color: #ff6666'
     if status[val[i]]=='Less than -3SD':#mild
          y[i]='background-color: #ff0000'

     if status[val[i]]=='Greater than +3SD':#Very fat 
          y[i]='background-color: #3366ff'
     if status[val[i]]=='+2SD to +3SD':#some fat 
          y[i]='background-color: #6699ff'
    return y



def zscore(df,ind):
       cnt=0
       cal={}
       for i in lidata[2]:
          cal[i]=''
       age=df.iloc[ind]['Age (months)']*30
       weight=df.iloc[ind]['weight']
       leng=df.iloc[ind]['length']
       gender=df.iloc[ind]['Gender']
       if gender in madata:
        for i in madata[gender]:
            if cnt==0:#wfl
                if leng in i.index.values:
                    va=i.loc[leng]
                    if weight>va['SD2neg'] and weight<va['M']:
                        cal[lidata[2][cnt]]='-2SD to 0SD'
                    if weight>va['M'] and weight<va['SD2']:
                        cal[lidata[2][cnt]]='0SD to +2SD'
                    if weight<va['SD2neg'] and weight>va['SD3neg']:
                        cal[lidata[2][cnt]]='-2SD to -3SD'
                    if weight<va['SD3'] and weight>va['SD2']:
                        cal[lidata[2][cnt]]='+2SD to +3SD'
                    if weight<va['SD3neg']:
                        cal[lidata[2][cnt]]='Less than -3SD'
                    if weight>va['SD3']:
                        cal[lidata[2][cnt]]='Greater than +3SD'
            if cnt==1:#wfa
                if age in i.index.values:
                    va=i.loc[age]
                    if weight>va['SD2neg'] and weight<va['M']:
                        cal[lidata[2][cnt]]='-2SD to 0SD'
                    if weight>va['M'] and weight<va['SD2']:
                        cal[lidata[2][cnt]]='0SD to +2SD'
                    if weight<va['SD2neg'] and weight>va['SD3neg']:
                        cal[lidata[2][cnt]]='-2SD to -3SD'
                    if weight<va['SD3'] and weight>va['SD2']:
                        cal[lidata[2][cnt]]='+2SD to +3SD'
                    if weight<va['SD3neg']:
                        cal[lidata[2][cnt]]='Less than -3SD'
                    if weight>va['SD3']:
                        cal[lidata[2][cnt]]='Greater than +3SD'
            if cnt==2:#lfa
                if age in i.index.values:
                    va=i.loc[age]
                    if leng>va['SD2neg'] and leng<va['M']:
                        cal[lidata[2][cnt]]='-2SD to 0SD'
                    if leng>va['M'] and leng<va['SD2']:
                        cal[lidata[2][cnt]]='0SD to +2SD'
                    if leng<va['SD2neg'] and leng>va['SD3neg']:
                        cal[lidata[2][cnt]]='-2SD to -3SD'
                    if leng<va['SD3'] and leng>va['SD2']:
                        cal[lidata[2][cnt]]='+2SD to +3SD'
                    if leng<va['SD3neg']:
                        cal[lidata[2][cnt]]='Less than -3SD'
                    if leng>va['SD3']:
                        cal[lidata[2][cnt]]='Greater than +3SD'
            cnt+=1
        for i in cal:
            df.at[df.index[ind],i]=cal[i]
        return(cal)
       

class topbarmdm(ft.UserControl):
    def __init__(self,page):
        super().__init__()
        self.page=page
        self.ids=ft.TextField(label='MDM ID',text_style=ft.TextStyle(color='black'),on_submit=self.mdmaction,color='black',bgcolor=ft.colors.WHITE)
        self.name=ft.TextField(label='Name',on_submit=self.nameaction,text_style=ft.TextStyle(color='white'),color='black',bgcolor=ft.colors.WHITE)
        self.save=ft.IconButton(icon=ft.icons.SAVE,on_click=self.savefile,icon_color='white')
        self.add=ft.IconButton(icon=ft.icons.ADD,on_click=self.adddata,icon_color='white')
    def savefile(self,e):
        global data
        xl=data.style.apply(colorstatus, axis=1,subset=['Height/Length for Age','Weight for Age','Weight for length'])
        xl.to_excel('data.xlsx',index=False)
        e.page.snack_bar=ft.SnackBar(content=ft.Text('File saved'))
        e.page.snack_bar.open = True
        e.page.update()
    def adddata(self,e):
        global data
        ind=[data.index.values.max()+1]
        emp={}
        nemdm=oldd['SN'].max()+1
        for i in data.columns:
            emp[i]=''
            if i =='SN':
                emp['SN']=nemdm
            if i=='Gender':
                emp[i]='M'
            

                
        data=oldd.copy(deep=True)
        frame=pd.DataFrame(data=emp,index=ind)
        data=pd.concat([data,frame],axis=0)
        print(data)
        print(ind[0])
        le=len(e.page.controls)
        for i in range(1,le):
            e.page.remove(e.page.controls[le-i])
            e.page.update()
        e.page.add(ft.Container(height=100))
        e.page.add(profile(mdmid=nemdm))
        

        e.page.snack_bar=ft.SnackBar(content=ft.Text('Added'))
        e.page.snack_bar.open = True
        e.page.update()
    def nameaction(self,e):
        print('sub')
        name=e.control.value.upper()
        print(name)
        uppernames=data.copy(deep=True)
        uppernames['Name']=uppernames['Name'].str.upper()
        localdata=data.loc[uppernames['Name'].str.contains(name)]
        print(localdata)
        cnt=0
        print(len(self.page.controls),cnt)
        old=len(self.page.controls)
        for i in range(1,old):
            print('xx',i,len(self.page.controls),cnt)
            cnt+=1
            self.page.remove_at(old-i)
            self.page.update()
        print(localdata['SN'].unique())
        self.page.add(ft.Container(height=100))
        for i in localdata['SN'].unique():
            print(i)
            self.page.add(profile(mdmid=i))
            self.page.update()
        self.page.update()
    def mdmaction(self,e):
        print('sub')
        name=int(e.control.value)
        localdata=data.loc[data['SN']==name]
        old=len(self.page.controls)
        for i in range(1,old):
            self.page.remove_at(old-i)
            self.page.update()
        print(localdata['SN'].unique())
        self.page.add(ft.Container(height=100))
        for i in localdata['SN'].unique():
            print(i)
            self.page.add(profile(mdmid=i))
            self.page.update()
        self.page.update()
    def build(self):
        self.view=ft.Container(content=ft.Row([self.ids,self.name,self.save,self.add]),bgcolor=ft.colors.BLACK,height=100)
        return self.view
    
class zscore_display(ft.UserControl):
    def __init__(self,zscore):
        super().__init__()
        self.zscore=zscore
    def build(self):
        red=['Less than -3SD','Greater than +3SD']
        black=['0SD to +2SD','-2SD to 0SD']
        pink=['-2SD to -3SD','+2SD to +3SD']
        if self.zscore in red:
            return ft.Text(self.zscore,bgcolor=ft.colors.RED)
        if self.zscore in black:
            return ft.Text(self.zscore,bgcolor=ft.colors.GREEN_300,weight=4)
        if self.zscore in pink:
            return ft.Text(self.zscore,bgcolor=ft.colors.RED_300,weight=30)
        return ft.Text(self.zscore)
    
class graph(ft.UserControl):
    def __init__(self,type,dataz,gender):
        self.type=type
        self.dataz=dataz.copy(deep=True)
        self.gender=gender
        self.dataz['Age (months)']=self.dataz['Age (months)']*30
        print(dataz)
        super().__init__()

    def build(self): 
        fig, ax = plt.subplots()  
        g=['M','F']
        gen=g.index(self.gender)
        wfl=lidata[gen][self.type]
        x=lidata[3][self.type][0]
        y=lidata[3][self.type][1]
        print('xxxxxxx',self.data)
        self.dataz=self.dataz.filter([x,y])
        self.dataz.set_index(x,inplace=True)
        self.dataz.rename(columns={y:'data'},inplace=True)
        self.dataz = self.dataz[~self.dataz.index.duplicated(keep='last')]
        wfl=pd.concat([wfl,self.dataz],axis=1)
        print(wfl)
        ax.set_title(lidata[2][self.type])
        ax.plot(wfl.index.values,wfl['M'],color='green')
        ax.plot(wfl.index.values,wfl['SD3neg'],color='red')
        ax.plot(wfl.index.values,wfl['SD3'],color='red')
        ax.plot(wfl.index.values,wfl['SD2'],color='blue')
        ax.plot(wfl.index.values,wfl['SD2neg'],color='blue')
        ax.scatter(wfl.index.values,wfl['data'])
        ax.grid()
        return MatplotlibChart(fig)
    
class profile(ft.UserControl):
    def __init__(self,mdmid):
        self.mdmid=mdmid
        super().__init__()
    def close_dialog(self,e):
         self.diag.open=False

    def show_graph(self,e):
        try:
            t=e.control.data
            x=data.loc[data['SN']==self.mdmid]
            print(x)
            x=x.iloc[0]['Gender']
            print(x)
            self.diag=ft.AlertDialog(content=graph(type=t,dataz=self.biodata,gender=x),actions=[ft.IconButton(icon=ft.icons.CLOSE,on_click=self.close_dialog)])
            e.page.show_dialog(self.diag)
        except:
            pass
    def build(self): 
        global data
        unique=data["SN"].unique()
        if self.mdmid in data["SN"].values:
            self.sn=ft.TextField(value=data.loc[data["SN"]==self.mdmid].iloc[0]['SN'],width=80,height=30,label='MDM ID',disabled=True)
            self.name=ft.TextField(value=data.loc[data["SN"]==self.mdmid].iloc[0]['Name'],width=200,height=30,label='Name',on_change=self.save)
            self.address=ft.TextField(value=data.loc[data["SN"]==self.mdmid].iloc[0]['Address'],width=200,height=30,label='Address',on_change= self.save)
            self.phone=ft.TextField(value=data.loc[data["SN"]==self.mdmid].iloc[0]['phone number'],width=200,height=30,label='Phone',on_change=self.save)
            self.gender=ft.Dropdown(value=data.loc[data["SN"]==self.mdmid].iloc[0]['Gender'],options=[ft.dropdown.Option(text='M',),ft.dropdown.Option(text='F')],width=80,height=50,text_size=15,label='Gender',on_change=self.save)
            self.biodata=data.loc[data["SN"]==self.mdmid].filter(['Date','weight','length','Age (months)','Height/Length for Age','Weight for Age','Weight for length'])
            self.biodatacol=measuementable(df=self.biodata,mdmid=self.mdmid)
            self.buttons=[]
            for i in range(len(lidata[2])):
                 last=self.biodata.iloc[-1][lidata[2][i]]
                 self.buttons+=[ft.Row([ft.TextButton(lidata[2][i],on_click=self.show_graph,data=i),ft.Text('Last Read:'),zscore_display(zscore=last)])]
            self.buttons=ft.Row(self.buttons)
            return(ft.Container(ft.Column([ft.Row([self.sn,self.name,self.gender,self.address,self.phone]),self.biodatacol,self.buttons
                              ],),border=ft.Border(bottom=ft.BorderSide(color='black',width=4))))
    def save(self,e):
        global data
        print(self.mdmid)
        oldd=data.copy(deep=True)
        data['Name'].where((data['SN']!=self.mdmid),self.name.value,inplace=True)
        data['Address'].where((data['SN']!=self.mdmid),self.address.value,inplace=True)
        data['phone number'].where((data['SN']!=self.mdmid),self.phone.value,inplace=True)
        data['Gender'].where((data['SN']!=self.mdmid),self.gender.value,inplace=True)
        print(data)


class measuementable(ft.UserControl):
        def __init__(self,df,mdmid):
            super().__init__()
            self.df=df
            self.mdmid=mdmid

        def addfunc(self,e):
            global data
            
            x=data.loc[data['SN']==self.mdmid].copy(deep=True)
            x=x[0:1]
            print(x)
            if self.adddate.value in data.loc[data['SN']==self.mdmid]['Date'].tolist():
                try:
                    data['Age (months)'].where((data['SN']!=self.mdmid)&(data['Date']!=self.adddate.value),int(self.addage.value),inplace=True)
                    data['length'].where((data['SN']!=self.mdmid)&(data['Date']!=self.adddate.value),int(self.addlength.value),inplace=True)
                    data['weight'].where((data['SN']!=self.mdmid)&(data['Date']!=self.adddate.value),int(self.addweight.value),inplace=True)
                except:
                    return ''
            elif '' in data.loc[data['SN']==self.mdmid]['Date'].tolist():
                try:
                    data['Age (months)'].where((data['SN']!=self.mdmid)&(data['Date']!=''),int(self.addage.value),inplace=True)
                    data['length'].where((data['SN']!=self.mdmid)&(data['Date']!=''),int(self.addlength.value),inplace=True)
                    data['weight'].where((data['SN']!=self.mdmid)&(data['Date']!=''),int(self.addweight.value),inplace=True)
                    data['Date'].where((data['SN']!=self.mdmid)&(data['Date']!=''),self.adddate.value,inplace=True)
                except:
                    return ""
            else:
                try:
                    x['weight']=int(self.addweight.value)
                    x['length']=int(self.addlength.value)
                    x['Age (months)']=int(self.addage.value)
                    x['Date']=self.adddate.value
                    data=pd.concat([data,x],axis=0)
                    data.reset_index(drop=True, inplace=True)
                except:
                    return ''
            print(data)
            self.update()
            zscore(data,data.index[len(data.index.values)-1])
            if True:
                for i in e.page.controls:
                    if isinstance(i,profile):
                        if i.mdmid==self.mdmid:
                            ind=e.page.controls.index(i)
                            e.page.remove(i)
                            e.page.insert(ind,profile(mdmid=self.mdmid))
                            break

             
        def build(self):
            col=[]
            for i in self.df.columns:
                col+=[ft.DataColumn(ft.Text(i))]
            row=[]
            for i in range(len(self.df)):
                cell=[]
                for j in self.df.columns:
                        cell+=[ft.DataCell(zscore_display(zscore=str(self.df.iloc[i][j])))]
                row+=[ft.DataRow(cells=cell)]
            self.adddate=ft.TextField(value=datetime.datetime.now().strftime('%Y-%m-%d'),label='Date',width=200,height=30)
            self.addweight=ft.TextField(label='weight',width=100,height=30)
            self.addlength=ft.TextField(label='lenghth',width=100,height=30)
            self.addage=ft.TextField(label='Age (months)',width=100,height=30)
            self.addbutton=ft.IconButton(icon=ft.icons.ADD,on_click=self.addfunc)

            self.adddata=ft.Row([self.adddate,self.addweight,self.addlength,self.addage,self.addbutton])
            self.table=ft.DataTable(columns=col,rows=row)
            return ft.Column([self.table,self.adddata])

def main(page: ft.Page):
    page.add(ft.Text('a'))
    page.banner=topbarmdm(page=page)
    page.scroll='AUTO'
    print()
    page.add(ft.Container(height=100))
    

    #for i in data["SN"].unique():
    #    page.add(profile(mdmid=i))
    

    
    page.update()

ft.app(target=main)


    
    page.update()

ft.app(target=main)
