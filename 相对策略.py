import warnings,itertools,re,copy,numpy as np,pandas as pd,matplotlib.pyplot as plt,matplotlib.font_manager as f;from datetime import datetime;from matplotlib.cm import RdYlGn as c 
f.fontManager.addfont("s.ttf"); plt.rcParams['axes.unicode_minus']=0; plt.rcParams['font.sans-serif']=[f.FontProperties(fname="s.ttf").get_name()]; from tqdm import tqdm; r=range
左=lambda 价:np.insert(价[:-1],0,价[0]); 掩点=lambda 掩:np.where(掩)[0]; 画线=lambda 线:plt.plot(r(1,len(线)+1),线,'o-',lw=1.5,ms=4); 画竖=lambda 点:plt.axvline(点,c='gray',lw=10)
pp=lambda a:np.array(a); 抠数=lambda l,位:pp([int(str(日).split('-')[位]) for 日 in l]); 变幅=lambda 次,首:(次-首)/首*100; 集=['d201.csv','d223.csv','d245.csv']
def 周点买卖(买日=1,查询码=[0,]): # 买日>0仅在特定日期买入,买日=0表示任点皆可买故查询码应非空,均次日卖出||查询码=0表将买点前溯长长度内的二元序列和次日收益编入码典,查询码=[**]则进入查询模式 
    起=3; f=pp(l:=pd.read_csv(名,encoding=['utf-8','gbk'][0],header=0).replace(0,np.nan)); 掩=pp([False]*(f.shape[1]-起)); 掩[-2400:]=True; df=f[:,起:][:,掩] 
    时间=pp([日.split(".")[0] for 日 in l.columns[起:]])[掩]; 长=len(时间); 内集=pp([i%4+1 for i in r(长)]); 周集=pp([datetime.strptime(日,'%Y-%m-%d').weekday()+1 for 日 in 时间])
    print(周集[:5],时间[:5],长); 溯长=4; 目集=[周集,内集]['.'in str(l.columns[3])]; 断集=掩点(目集<左(目集)); 宽=len(set(目集[目集>0])); 星否=宽<6 # 也可尝试: 目集=(周集-1)*4+内集
    总益集=[]; 累典={tuple(k):np.zeros(长) for k in [pp(模).tolist() for 深 in r(溯长+1) for 模 in itertools.product([0,1],repeat=深)]}; 长典=copy.deepcopy(累典) 
    for 股号 in tqdm(r(min(len(df),10000)),position=0,leave=True): # l.columns
        价线=df[股号]; 收盘线=价线[3::4]; 益集=[]; 邻变=lambda a,点,长:a[点-长+1:点+1]>a[点-长:点]; 基变=lambda a,点,长:a[点-长+1:点+1]>a[点-4] 
        for 点 in [掩点(目集*买日==买日*买日),掩点(目集<4)][买日==-1]: # ↓ 日线过滤买不进的涨停票+各线均抠除前后不足的端点+去除前两日等价的停牌票+次日不属于买日周点的次点 
            if 变幅(价线[点],价线[点-1])>(限速:=[100,4][星否]) or 点<溯长+27 or 点>长-10 or 价线[点-2]==价线[点-1]==价线[点] or 目集[点+1]*买日!=(买日%宽+1)*买日: continue 
            if 宽==4: # and 价线[点]<价线[点-4] and 价线[点-4]<价线[点-8] and 价线[点-8]<价线[点-12] and 价线[点-12]<价线[点-16] and 价线[点-16]<价线[点-20]
                偏量=[4,8-目集[点]][买日==-1]; 幅=变幅(价线[点+偏量],价线[点]) 
                if 变幅(价线[点+偏量],价线[点])>-1000: # set(邻变(收盘线,(点+1)//4-1,前零天数).astype(int))=={0}
                    for i in r(1,目集[点]+1): 累典[q:=tuple(基变(价线,点,i).astype(int)[::[1,-1][买日==4]])][点]+=[幅,int(幅>0)][出率]; 长典[q][点]+=[1,int(幅!=0)][出率] 
                continue 
            if 查询码==0: # ↑ 小时线先行处理,买日=-1是个特殊功能,日点前态推收盘涨跌,代表晚期点的下层编码的头部正好对应代表早期点的上层编码因此不可后置,其掩点为123小时线,另买日=4才4小时线 
                for i in r(溯长+1): 幅=变幅(价线[点+1],价线[点]); 累典[q:=tuple(邻变(价线,点,i).astype(int)[::-1])][点]+=[幅,int(幅>0)][出率]; 长典[q][点]+=[1,int(幅!=0)][出率] 
                continue # 古日后置 
            if (邻变(价线,点,len(查询码)).astype(int)[::-1]!=pp(查询码)).any(): continue # 筛掉前面的二元序列不等于查询码的买点 
            if 价线[点]*价线[点+1]>0: 益=变幅(价线[点+1],价线[点]); 益集.append(益); 总益集.append(益) 
            if len(益集)==1: plt.figure(figsize=(长/5,长/30)); 画线(价线); plt.xlim(0,长-1); plt.xticks(r(0,长,8)); 星否 and [画竖(断集[i]-0.5) for i in r(len(断集))] 
            plt.axvline(点+1,color='red'); plt.text(点,plt.ylim()[0],f'{益:.1f}',fontsize=8,bbox=dict(facecolor=["y","w"][益>0])) # 有则准备画布
        if len(益集)>0: plt.show(); print(股号+1,f[:,2][股号],f"盈{(pp(益集)>0).mean()*100:.2f}%,均益{pp(益集).mean():.2f}%") # 出图后顺势打印出当的图盈率和收益,次项是股名 
    return pp(总益集).mean().round(3) if 查询码!=0 else {k:np.nanmean(累典[k]/长典[k]).round(2) for k in 累典} # {k:np.sum((长典[k]>0).astype(int)) for k in 长典} 
# def 解构(益矩,长矩): return (np.nanmean(np.where(益矩!=0,益矩/长矩,np.nan),axis=2)), (np.sum(np.where(长矩>0,1,0),axis=2)) 
# a=周点买卖(0,[0,0,0,0]); print(a) # 查特况k线 ||下面对齐是通过末尾填零以对齐混淆矩最长行,否则报错 ↓ 目集[点+1]!=买日%宽+1  
# 益矢=[周点买卖(买日,[]) for 买日 in tqdm(r(1,宽+1))]; 益矢=pp([益矢[-1]]+益矢[:-1]); plt.figure(figsize=(宽*0.3,2)); 画线(益矢); plt.axhline(y=0,linestyle='--') 
# plt.grid(True); plt.xlim(1,宽); plt.xticks(r(1,宽+1)); 宽==20 and [画竖(4*i+4.5) for i in r(4)] # 每个星期的四个小时线共5*4=20条可视化时每四点画一竖线 
def 画树(点,x,y,横,纵,ax,标,色):ax.text(x,y,标,ha='center',va='center',bbox=dict(facecolor=色),fontsize=12);点['l'] and 定(点,x,y,横,纵,ax,-1);点['r'] and 定(点,x,y,横,纵,ax,1)
def 定(点,x,y,横,纵,ax,向):ax.plot([x,x+横*向],[y,y-纵],'k-');下=[点['l'],点['r']][向>0];画树(下,x+横*向,y-纵,横/2,纵,ax,f"{''.join(map(str,下['p']))}\n{round(下['b'],2)}",c(下['b'])) 
def 画建树(买日): # 宽==4即考察小时线时无论前推后还是后推明都以末值为基准而用-1,异于一般周点用的次值即列码的0||定函中右向为正 ↑
    横=(溯长/2)**2; 纵=0.7; 数码字典=周点买卖(买日,0); 树根=结点={'p':[],'l':None,'r':None,'b':None}; # print(数码字典) 
    for 深度 in r(1,溯长+1): # 每个模式都先搬来前面的树根以构建自顶到底的旁路,顺次标记路径 怎么把r(1,宽+1)或是r(0,长,8)里面的r均用r代替以缩短长度
        for 模式 in itertools.product([1,0],repeat=深度): # 1即涨时用左子树表示,反之0即跌时用右子树 
            for 新底当元 in 模式[:-1]: 结点=[结点['r'],结点['l']][新底当元==1] # 未突破底部瓶颈直接套用前面建立的即可 
            if 模式[-1] == 1: 结点['l']=结点['l'] or {'p':结点['p']+[1],'l':None,'r':None,'b':None}; 结点=结点['l'] # 到底新建 
            else: 结点['r']=结点['r'] or {'p':结点['p']+[0],'l':None,'r':None,'b':None}; 结点=结点['r'] # 为当前出现的新路线填充路标
            结点['b']=数码字典.get(tuple(模式),None); 结点=树根 # 遍历完内层即当前模式的所有数码则对应填充字典的值,随后归零初始坐标供下轮模式使用  
    x=plt.subplots(figsize=(横*4,纵*4-0.5))[1]; 画树(结点,0,0,横,纵,x,f"周{买日}先验收益:{数码字典[tuple(())]}",'w'); x.axis('off'); plt.show() # 两子图  
出率=1 
# 买日=4 # 日内推理(买日=-1)/隔日推理(买日=4) 
名='d205.csv' 
前零天数=0 
画建树(0) 
_=[画建树(买日) for 买日 in r(1,5+1)] # 先无定点回测(买日=0),再逐点回测(买日=1~宽),但日份和月份常与持续多日的牛熊市重合,因此只能测试普适性,星份可额测特异性 
# for 星号 in r(1): 溯长=[3,4][买日==4]; 画建树(买日) # 目集=内集*(周集*星号==星号*星号); 
# for 集名 in 集: 名=集名; 溯长=[3,4][买日==4]; 画建树(买日) 