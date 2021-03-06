# -*- coding: utf-8 -*-
"""PORTFOLIO OPTIMIZE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jD7ygLqApU9j4pNCepPknjbjvitEg5zH
"""

!pip install yfinance
!pip install catboost
!pip install PyPortfolioOpt
!pip install keras-ordered-neurons
!pip install seq2seq-lstm

#!/usr/bin/env python
# coding: utf-8

# In[1]:

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns


from pandas_datareader import data as pdr
import yfinance as yf
#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

#import the necessary modelling algos.

#classifiaction.
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC,SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

#regression
from sklearn.linear_model import LinearRegression,Ridge,Lasso,RidgeCV
from sklearn.ensemble import RandomForestRegressor,BaggingRegressor,GradientBoostingRegressor,AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

#model selection
from sklearn.model_selection import train_test_split,cross_validate
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV

#evaluation metrics
from sklearn.metrics import mean_squared_log_error,mean_squared_error, r2_score,mean_absolute_error # for regression
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score  # for classification

from sklearn.model_selection import train_test_split
from sklearn import model_selection, tree, preprocessing, metrics, linear_model
from sklearn.svm import LinearSVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression, LogisticRegression, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier, Pool, cv
from sklearn.model_selection import cross_val_predict

import datetime
import catboost
from catboost import CatBoostRegressor, Pool, cv
import matplotlib.pyplot as plt
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import seaborn as sns

from sklearn import model_selection, tree, preprocessing, metrics, linear_model
from sklearn.svm import LinearSVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression, LogisticRegression, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import r2_score
import xgboost as xg
from sklearn.model_selection import GridSearchCV

hatali

# In[2]:


data = pdr.get_data_yahoo('AVOD.IS', start="2017-01-01", end="2040-04-30")


# In[3]:


data.head()


# In[4]:


l=['AVOD ', 'A1CAP, ACP ', 'ACSEL ', 'ADEL ', 'ADESE ', 'AFYON ',
       'AGHOL ', 'AKSFA ', 'AKM, AKMEN ', 'AKBNK ', 'AKCNS ', 'AKDFA ',
       'AKYHO ', 'AKENR ', 'AKFGY ', 'AKFEN ', 'ATEKS ', 'AKSGY ',
       'AKMGY ', 'AKSA ', 'AKSEN ', 'AKGRT ', 'AKSUE ', 'AKTVK ',
       'AFB, AKTIF ', 'ALCAR ', 'ALGYO ', 'ALARK ', 'ALBRK, ALK ',
       'ALCTL ', 'ALKIM ', 'ALKA ', 'ALNTF, ANF ', 'AYCES ', 'ALMAD ',
       'ANSGR ', 'AEFES ', 'ANHYT ', 'ASUZU ', 'ANELE ', 'ARCLK ',
       'ARDYZ ', 'ARENA ', 'ARNFK ', 'ARMDA ', 'ARSAN ', 'ARTI ',
       'ASELS ', 'ATAGY ', 'AGYO ', 'ATLFA ', 'ATSYH ', 'ATLAS ',
       'AVISA ', 'AVGYO ', 'AVTUR ', 'AVHOL ', 'AYEN ', 'AYES ', 'AYGAZ ',
      'BAGFS ', 'BAKAB ', 'BALAT ', 'BNTAS ', 'BANVT ', 'BSRFK ',
       'BASCM ', 'BTCIM ', 'BSOKE ', 'BAYRK ', 'BERA ', 'BRKT ', 'BRKSN ',
       'BJKAS ', 'BEYAZ ', 'BLCYT ', 'BIMAS ', 'BRKVY ', 'BRKO ',
       'BRMEN ', 'BIZIM ', 'BOGVY ', 'BRSAN ', 'BRYAT ', 'BFREN ',
       'BOSSA ', 'BRISA ', 'BURCE ', 'BURVA ', 'BUCIM ',  'CRFSA ',
       'CASA ', 'CEOEM ', 'CCOLA ', 'COSMO ', 'CRDFA ',  'CLEBI ',
       'CELHA ', 'CEMAS ', 'CEMTS ', 'CMBTN ', 'CMENT ', 'CIMSA ',
       'CUSAN ', 'DAGI ', 'DAGHL ', 'DARDL ', 'DGATE ', 'DMSAS ',
       'DENVA ', 'DENGE ', 'DENFA ', 'DNFIN ', 'DZGYO ', 'DZY, DZYMK ',
       'DENIZ, DNZ ', 'DERIM ', 'DERAS ', 'DESA ', 'DESPC ', 'DSTKF ',
       'DEVA ', 'DEVIR ', 'DNISI ', 'DIRIT ', 'DITAS ', 'DOCO ', 'DOBUR ',
       'DOHOL ', 'DGKLB ', 'DOGUB ', 'DGGYO ', 'DGHOL ', 'DOAS ',
       'DFKTR ', 'DOKTA ', 'DURDO ', 'DNYVA ', 'DYOBY ',  'ECZYT ',
       'EDIP ', 'EGEEN ', 'EGGUB ', 'EGPRO ', 'EGSER ', 'EPLAS ',
       'ECILC ', 'EKIZ ', 'EKOFA ', 'EMKEL ', 'EMNIS ', 'EKTVK ',
       'EKGYO ', 'ENJSA ', 'ENKAI ', 'ERBOS ', 'EREGL ', 'ERGLI ',
       'EROGL ', 'ERSU ', 'ESCOM ', 'ESEN ', 'ETILR ', 'EUKYO ', 'EUYO ',
       'ETYAT ', 'EUHOL ', 'FADE ', 'FMIZP ', 'FENER ',
       'FBB, FBBNK ', 'FLAP ', 'FONET ', 'FROTO ', 'FORMT ', 'FRIGO ',
        'GSRAY ', 'GARFA ', 'GRFIN ', 'GRNYO ', 'GEDIK ', 'GEDZA ',
       'GENTS ', 'GEREL ', 'GLB, GLBMD ', 'GLYHO ', 'GOODY ', 'GOLTS ',
       'GOZDE ', 'GSDDE ', 'GSDHO ', 'GUBRF ', 'GLRYH ', 'H', 'SAHOL ',
       'HALKF ', 'HLGYO ', 'HLVKS ', 'HATEK ', 'HDFGS ', 'HEKTS ',
       'HSB, HSBCB ', 'HUBVC ', 'HUZFA ', 'HURGZ ',  'ICB, ICBCT ',
       'INVEO ', 'IEYHO ',  'IDEAS ', 'IDGYO ', 'IHEVA ', 'IHLGM ',
       'IHGZT ', 'IHLAS ', 'IHYAY ', 'INDES ', 'INFO, IYF ', 'INTEM ',
       'IPEKE ', 'ISDMR ', 'ISFAK ', 'ISFIN ', 'ISGYO ', 'ISGSY ',
       'ISMEN, IYM ', 'ISYAT ', 'ISBIR ', 'ITTFH ', 'IZTAR ', 'IZMDC ',
       'IZFAS ',  'JANTS ', 'KFEIN ', 'KALES ',
       'KAPTESTAS001, TRAKAPTEST01 ', 'KAPLM ', 'KRDMA, KRDMB, KRDMD ',
       'KAREL ', 'KARSN ', 'KRTEK ', 'KARTN ', 'KATMR ', 'KNTFA ',
       'KENT ', 'KERVT ', 'KRVGD ', 'KERVN ', 'KLGYO ', 'KLMSN ',
       'KFKTF ', 'KOCFN ', 'KCHOL ', 'KNFRT ', 'KONTR ', 'KONYA ',
       'KORDS ', 'KORTS ', 'KOZAL ', 'KOZAA ', 'KRGYO ', 'KRSTL ',
       'KRONT ', 'KTKVK ', 'KSTUR ', 'KUYAS ', 'KUTPO ',  'LIDFA ',
       'LINK ', 'LOGO ', 'LKMNH ', 'LUKSK ',  'MAKTK ', 'MARKA ',
       'MAALT ', 'MRSHL ', 'MRGYO ', 'MARTI ', 'MAVI ', 'MZHLD ',
       'MEGAP ', 'MNDRS ', 'MEPET ', 'MBFTR ', 'MERIT ', 'MERKO ',
       'METUR ', 'METRO ', 'MTRYO ', 'MGROS ', 'MIPAZ ', 'MSGYO ',
       'MPARK ', 'MMCAS ', 'TIRE ', 'NATEN ', 'NTHOL ', 'NETAS ',
       'NIBAS ', 'NUHCM ', 'NUGYO ', 'NRHOL ', 'NURVK ', 'NRBNK, NYB ',
        'ODAS ', 'ODB, ODEA ', 'OLMIP ', 'OPET ', 'ORFIN ', 'ORGE ',
       'ORMA ', 'OMD, OSMEN ', 'OSTIM ', 'OTKAR ', 'OTOKC ', 'OYAKC ',
       'OYA, OYYAT ', 'OYAYO ', 'OYLUM ', '?????', 'OZKGY ', 'OZBAL ',
       'OZGYO ', 'OZRDN ', 'PAMEL ', 'PAGYO ', 'PAPIL ', 'PRKME ',
       'PARSN ', 'PBT, PBTR ', 'PGSUS ', 'PEKGY ', 'PENGD ', 'PEGYO ',
       'PSDTC ', 'PETKM ', 'PKENT ', 'PHC, PHLLP ', 'PETUN ', 'PINSU ',
       'PNSUT ', 'PKART ', 'POLHO ', 'POLTK ', 'PRZMA ',  'QNBFF ',
       'QNBFL ', 'QNBVK ', 'FNY, QNBFI ', 'FIN, QNBFB ', 'RALYH ',
       'RAYSG ', 'RYGYO ', 'RYSAS ', 'RHEAG ', 'RODRG ', 'ROYAL ',
       'RTALB ', 'SAFKR ', 'SANEL ', 'SANFM ', 'SANKO ', 'SAMAT ',
       'SARKY ', 'SARTN ', 'SASA ', 'SAYAS ', 'SEKUR ', 'SELEC ',
       'SELGD ', 'SNKRN ', 'SERVE ', 'SRVGY ', 'SEYKM ', 'SILVR ',
       'SNGYO ', 'SMART ', 'SODSN ', 'SKTAS ', 'SONME ', 'SNPAM ',
       'SUMAS ', 'SMRFA ', 'SMRVA ', 'SEKFA ', 'SEKFK ',
       'SKY, SKYMD ', 'SEK, SKBNK ', 'SOKM ', 'TOKI ', 'TCZ, TCZB ',
       'TAC, TCRYT ', 'TACTR ', 'TAMFA ', 'TATGD ', 'TAVHL ', 'TKURU ',
       'TEBCE ', 'TEKTU ', 'TKFEN ', 'TKNSA ', 'TMPOL ', 'STK, TRMNK ',
       'TFNVK ', 'TGSAS ', 'TOASO ', 'TRGYO ', 'TLMAN ', 'TSPOR ',
       'TDGYO ', 'TSGYO ', 'TUCLK ', 'TUKAS ', 'TRCAS ', 'TCELL ',
       'TBA, TRKSH ', 'TMSN ', 'TUPRS ', 'TEB, TEBNK ', 'THYAO ',
       'PRKAB ', 'TTKOM ', 'TTRAK ', 'TBORG ', 'TURGG ', 'GARAN, TGB ',
       'HALKB, THL ', 'EXIMB, THR ', 'ISATR, ISBTR, ISCTR, ISKUR, TIB ',
       'KLN, KLNMA ', 'TSK, TSKB ', 'TURSG ', 'SISE ', 'TVB, VAKBN ',
       'UFUK ', 'ULAS ', 'ULSFA ', 'ULUSE ', 'ULUUN ', 'UMPAS ', 'USAK ',
       'UTPYA ', 'UZERB ', 'ULKER ', 'UNLUS, UNS ', 'VAKFA ',
       'VAKFN ', 'VKGYO ', 'VKFYO ', 'VAKVK ', 'VAKKO ', 'VANGD ',
       'VERUS ', 'VERTU ', 'VESBE ', 'VESTL ', 'VKING ', 'YKFKT ',
       'YKGYO ', 'YKR, YKYAT ', 'YKB, YKBNK ', 'YAPRK ', 'YATAS ',
       'YAT, YFMEN ', 'YATVK ', 'YAYLA ', 'YDATH ', 'YGGYO ', 'YGYO ',
       'YYAPI ', 'YESIL ', 'YBTAS ', 'YONGA ', 'YKSLN ', 'YUNSA ',
       'ZKBVK ', 'ZOREN ', 'ZORLF ']


# In[5]:



'''tay = pd.Series(l)

tay = tay.apply(lambda x: x.split(',')[0])

lan = [i for i in l if 7 <=  len(i)]

lan = pd.Series(lan).apply(lambda x: x.split(',')[1])

type(tay)

type(len)

lan = np.array(lan)

aq = pd.Series(tay.values).append(pd.Series(lan))'''



aq = aq.reset_index()

aq = aq.drop(['index'],axis=1)


bq = []
for i in range(0,len(aq[0])):
  bq.append(aq[0][i].strip())
  #bq.append(bq)


cq = [suit + '.IS' for suit in bq]

dq = cq + bq

dq = pd.Series(dq)

dq = dq.reset_index()

dq = dq.drop(['index'],axis=1)

net = ['AVOD.IS',
 'ACSEL.IS',
 'ADEL.IS',
 'ADESE.IS',
 'AFYON.IS',
 'AGHOL.IS',
 'AKBNK.IS',
 'AKCNS.IS',
 'AKYHO.IS',
 'AKENR.IS',
 'AKFGY.IS',
 'ATEKS.IS',
 'AKSGY.IS',
 'AKMGY.IS',
 'AKSA.IS',
 'AKSEN.IS',
 'AKGRT.IS',
 'AKSUE.IS',
 'ALCAR.IS',
 'ALGYO.IS',
 'ALARK.IS',
 'ALBRK.IS',
 'ALCTL.IS',
 'ALKIM.IS',
 'ALKA.IS',
 'AYCES.IS',
 'ALMAD.IS',
 'ANSGR.IS',
 'AEFES.IS',
 'ANHYT.IS',
 'ASUZU.IS',
 'ANELE.IS',
 'ARCLK.IS',
 'ARDYZ.IS',
 'ARENA.IS',
 'ARMDA.IS',
 'ARSAN.IS',
 'ARTI.IS',
 'ASELS.IS',
 'ATAGY.IS',
 'AGYO.IS',
 'ATSYH.IS',
 'ATLAS.IS',
 'AVISA.IS',
 'AVGYO.IS',
 'AVTUR.IS',
 'AVHOL.IS',
 'AYEN.IS',
 'AYES.IS',
 'AYGAZ.IS',
 'BAGFS.IS',
 'BAKAB.IS',
 'BALAT.IS',
 'BNTAS.IS',
 'BANVT.IS',
 'BASCM.IS',
 'BTCIM.IS',
 'BSOKE.IS',
 'BAYRK.IS',
 'BERA.IS',
 'BRKSN.IS',
 'BJKAS.IS',
 'BEYAZ.IS',
 'BLCYT.IS',
 'BIMAS.IS',
 'BRKO.IS',
 'BRMEN.IS',
 'BIZIM.IS',
 'BRSAN.IS',
 'BRYAT.IS',
 'BFREN.IS',
 'BOSSA.IS',
 'BRISA.IS',
 'BURCE.IS',
 'BURVA.IS',
 'BUCIM.IS',
 'CRFSA.IS',
 'CASA.IS',
 'CEOEM.IS',
 'CCOLA.IS',
 'COSMO.IS',
 'CRDFA.IS',
 'CLEBI.IS',
 'CELHA.IS',
 'CEMAS.IS',
 'CEMTS.IS',
 'CMBTN.IS',
 'CMENT.IS',
 'CIMSA.IS',
 'CUSAN.IS',
 'DAGI.IS',
 'DAGHL.IS',
 'DARDL.IS',
 'DGATE.IS',
 'DMSAS.IS',
 'DENGE.IS',
 'DZGYO.IS',
 'DERIM.IS',
 'DERAS.IS',
 'DESA.IS',
 'DESPC.IS',
 'DEVA.IS',
 'DNISI.IS',
 'DIRIT.IS',
 'DITAS.IS',
 'DOCO.IS',
 'DOBUR.IS',
 'DOHOL.IS',
 'DGKLB.IS',
 'DOGUB.IS',
 'DGGYO.IS',
 'DOAS.IS',
 'DOKTA.IS',
 'DURDO.IS',
 'DYOBY.IS',
 'ECZYT.IS',
 'EDIP.IS',
 'EGEEN.IS',
 'EGGUB.IS',
 'EGPRO.IS',
 'EGSER.IS',
 'EPLAS.IS',
 'ECILC.IS',
 'EKIZ.IS',
 'EMKEL.IS',
 'EMNIS.IS',
 'EKGYO.IS',
 'ENJSA.IS',
 'ENKAI.IS',
 'ERBOS.IS',
 'EREGL.IS',
 'ERSU.IS',
 'ESCOM.IS',
 'ESEN.IS',
 'ETILR.IS',
 'EUKYO.IS',
 'EUYO.IS',
 'ETYAT.IS',
 'EUHOL.IS',
 'FADE.IS',
 'FMIZP.IS',
 'FENER.IS',
 'FLAP.IS',
 'FONET.IS',
 'FROTO.IS',
 'FORMT.IS',
 'FRIGO.IS',
 'GSRAY.IS',
 'GARFA.IS',
 'GRNYO.IS',
 'GEDIK.IS',
 'GEDZA.IS',
 'GENTS.IS',
 'GEREL.IS',
 'GLYHO.IS',
 'GOODY.IS',
 'GOLTS.IS',
 'GOZDE.IS',
 'GSDDE.IS',
 'GSDHO.IS',
 'GUBRF.IS',
 'GLRYH.IS',
 'SAHOL.IS',
 'HLGYO.IS',
 'HATEK.IS',
 'HDFGS.IS',
 'HEKTS.IS',
 'HUBVC.IS',
 'HURGZ.IS',
 'INVEO.IS',
 'IEYHO.IS',
 'IDEAS.IS',
 'IDGYO.IS',
 'IHEVA.IS',
 'IHLGM.IS',
 'IHGZT.IS',
 'IHLAS.IS',
 'IHYAY.IS',
 'INDES.IS',
 'INFO.IS',
 'INTEM.IS',
 'IPEKE.IS',
 'ISDMR.IS',
 'ISFIN.IS',
 'ISGYO.IS',
 'ISGSY.IS',
 'ISMEN.IS',
 'ISYAT.IS',
 'ISBIR.IS',
 'ITTFH.IS',
 'IZTAR.IS',
 'IZMDC.IS',
 'IZFAS.IS',
 'JANTS.IS',
 'KFEIN.IS',
 'KAPLM.IS',
 'KRDMA.IS',
 'KAREL.IS',
 'KARSN.IS',
 'KRTEK.IS',
 'KARTN.IS',
 'KATMR.IS',
 'KENT.IS',
 'KERVT.IS',
 'KRVGD.IS',
 'KERVN.IS',
 'KLGYO.IS',
 'KLMSN.IS',
 'KCHOL.IS',
 'KNFRT.IS',
 'KONTR.IS',
 'KONYA.IS',
 'KORDS.IS',
 'KOZAL.IS',
 'KOZAA.IS',
 'KRGYO.IS',
 'KRSTL.IS',
 'KRONT.IS',
 'KSTUR.IS',
 'KUYAS.IS',
 'KUTPO.IS',
 'LIDFA.IS',
 'LINK.IS',
 'LOGO.IS',
 'LKMNH.IS',
 'LUKSK.IS',
 'MAKTK.IS',
 'MARKA.IS',
 'MAALT.IS',
 'MRSHL.IS',
 'MRGYO.IS',
 'MARTI.IS',
 'MAVI.IS',
 'MZHLD.IS',
 'MEGAP.IS',
 'MNDRS.IS',
 'MEPET.IS',
 'MERIT.IS',
 'MERKO.IS',
 'METUR.IS',
 'METRO.IS',
 'MTRYO.IS',
 'MGROS.IS',
 'MIPAZ.IS',
 'MSGYO.IS',
 'MPARK.IS',
 'MMCAS.IS',
 'TIRE.IS',
 'NATEN.IS',
 'NTHOL.IS',
 'NETAS.IS',
 'NIBAS.IS',
 'NUHCM.IS',
 'NUGYO.IS',
 'ODAS.IS',
 'OLMIP.IS',
 'ORGE.IS',
 'ORMA.IS',
 'OSTIM.IS',
 'OTKAR.IS',
 'OYAKC.IS',
 'OYAYO.IS',
 'OYLUM.IS',
 'OZKGY.IS',
 'OZBAL.IS',
 'OZGYO.IS',
 'OZRDN.IS',
 'PAMEL.IS',
 'PAGYO.IS',
 'PAPIL.IS',
 'PRKME.IS',
 'PARSN.IS',
 'PGSUS.IS',
 'PEKGY.IS',
 'PENGD.IS',
 'PEGYO.IS',
 'PSDTC.IS',
 'PETKM.IS',
 'PKENT.IS',
 'PETUN.IS',
 'PINSU.IS',
 'PNSUT.IS',
 'PKART.IS',
 'POLHO.IS',
 'POLTK.IS',
 'PRZMA.IS',
 'QNBFL.IS',
 'RALYH.IS',
 'RAYSG.IS',
 'RYGYO.IS',
 'RYSAS.IS',
 'RHEAG.IS',
 'RODRG.IS',
 'ROYAL.IS',
 'RTALB.IS',
 'SAFKR.IS',
 'SANEL.IS',
 'SANFM.IS',
 'SANKO.IS',
 'SAMAT.IS',
 'SARKY.IS',
 'SASA.IS',
 'SAYAS.IS',
 'SEKUR.IS',
 'SELEC.IS',
 'SELGD.IS',
 'SNKRN.IS',
 'SERVE.IS',
 'SRVGY.IS',
 'SEYKM.IS',
 'SILVR.IS',
 'SNGYO.IS',
 'SMART.IS',
 'SODSN.IS',
 'SKTAS.IS',
 'SONME.IS',
 'SNPAM.IS',
 'SUMAS.IS',
 'SEKFK.IS',
 'SOKM.IS',
 'TACTR.IS',
 'TATGD.IS',
 'TAVHL.IS',
 'TKURU.IS',
 'TEKTU.IS',
 'TKFEN.IS',
 'TKNSA.IS',
 'TMPOL.IS',
 'TGSAS.IS',
 'TOASO.IS',
 'TRGYO.IS',
 'TLMAN.IS',
 'TSPOR.IS',
 'TDGYO.IS',
 'TSGYO.IS',
 'TUCLK.IS',
 'TUKAS.IS',
 'TRCAS.IS',
 'TCELL.IS',
 'TMSN.IS',
 'TUPRS.IS',
 'THYAO.IS',
 'PRKAB.IS',
 'TTKOM.IS',
 'TTRAK.IS',
 'TBORG.IS',
 'TURGG.IS',
 'GARAN.IS',
 'HALKB.IS',
 'ISATR.IS',
 'TURSG.IS',
 'SISE.IS',
 'UFUK.IS',
 'ULAS.IS',
 'ULUSE.IS',
 'ULUUN.IS',
 'UMPAS.IS',
 'USAK.IS',
 'UTPYA.IS',
 'UZERB.IS',
 'ULKER.IS',
 'VAKFN.IS',
 'VKGYO.IS',
 'VKFYO.IS',
 'VAKKO.IS',
 'VANGD.IS',
 'VERUS.IS',
 'VERTU.IS',
 'VESBE.IS',
 'VESTL.IS',
 'VKING.IS',
 'YKGYO.IS',
 'YAPRK.IS',
 'YATAS.IS',
 'YAYLA.IS',
 'YGGYO.IS',
 'YGYO.IS',
 'YYAPI.IS',
 'YESIL.IS',
 'YBTAS.IS',
 'YONGA.IS',
 'YKSLN.IS',
 'YUNSA.IS',
 'ZOREN.IS',
 'GLBMD.IS',
 'ICBCT.IS',
 'KRDMB.IS',
 'OSMEN.IS',
 'QNBFB.IS',
 'SKBNK.IS',
 'TEBNK.IS',
 'ISBTR.IS',
 'KLNMA.IS',
 'TSKB.IS',
 'VAKBN.IS',
 'YKBNK.IS',
 'AFB',
 'ALNTF',
 'ARTI',
 'BRKO',
 'CASA',
 'DAGI',
 'GLB',
 'H',
 'HSB',
 'ICB',
 'INFO',
 'KENT',
 'LINK',
 'PBT',
 'PHC',
 'FNY',
 'FIN',
 'SASA',
 'SKY',
 'TAC',
 'STK',
 'TBA',
 'TSK',
 'USAK',
 'ACP',
 'ALK',
 'ANF',
 'IYF',
 'IYM',
 'TGB',
 'THR']

net = pd.Series(net)

net = net.reset_index()

net = net.drop(['index'],axis=1)


hatali = []
print('SA')
data = pdr.get_data_yahoo('AVOD.IS', start="2017-01-01", end="2040-04-30")
data = data.rename(columns={"Adj Close": 'AVOD.IS'.strip()})
data = data.reset_index()
data = data[['Date','AVOD.IS'.strip()]]
data_merge = data

for symbol in range(1,len(net)): #len(dq)):
    try:
        print(net[0][symbol].strip())
        data_new = pdr.get_data_yahoo(net[0][symbol].strip(), start="2015-01-01", end="2042-01-1")
        data_new = data_new.rename(columns={"Adj Close": net[0][symbol].strip()})
        data_new = data_new.reset_index()
        data_new = data_new[['Date',net[0][symbol].strip()]]
        data_merge = pd.merge(data_merge,data_new,on='Date',how='outer')
    except:
        print("hatal??",net[0][symbol].strip())
        hatali.append(net[0][symbol].strip())
        pass



# In[21]:

#data_merge = data_merge.drop(['AAPL'],axis=1)
#data_merge = data_merge.set_index('Date')


# In[22]:


data_merge

data_merge = data_merge.drop(['H'],axis=1)

data_merge.shape

port = data_merge.iloc[:,0:215]

port = port.set_index('Date')
port

'''START FROM READ FILE'''

df = pd.read_csv('stock_predict_future')
df = df.drop(df.columns[0],axis=1)
port = df.set_index('ds')
port=port.iloc[:,0:150]

"""PORTFOLIO OPTIMIZE"""

returns = port.pct_change()
weights = np.array([1/(port.shape[1]) for i in range(0,port.shape[1])])
weights


cov_matrix_annual=returns.cov()*252
port_variance = np.dot(weights.T,np.dot(cov_matrix_annual,weights))
port_volatility = np.sqrt(port_variance)
port_simple_annual_return = np.sum(returns.mean()*weights)*252


print('Annual Variance='+str(round(port_variance,2)),
        'Annual Volatility='+str(round(port_volatility,2)),
'Expected annual return='+str(round(port_simple_annual_return,2)))

mu = expected_returns.mean_historical_return(port)
S = risk_models.sample_cov(port)
ef = EfficientFrontier(mu,S)
#weights = ef.min_volatility()
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
print(cleaned_weights)
ef.portfolio_performance(verbose=True)

from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
latest_prices = get_latest_prices(port)
weights = cleaned_weights
da = DiscreteAllocation(weights,latest_prices,total_portfolio_value=100000)
allocation, leftover = da.lp_portfolio()
print('allocation='+str(allocation),'leftover='+str(leftover))

"""** MONEY FLOW INDEX**"""

df = pdr.get_data_yahoo('MIGROS.IS', start="2017-01-01", end="2040-04-30")

typical_price = (df['Close'] + df['High'] + df['Low'])/3

period = 14
money_flow = typical_price*df['Volume']

positive_flow=[]
negative_flow=[]
for i in range(1,len(typical_price)):
  if typical_price[i]>typical_price[i-1]:
    positive_flow.append(money_flow[i-1])
    negative_flow.append(0)
  elif typical_price[i]<typical_price[i-1]:
    positive_flow.append(0)
    negative_flow.append(money_flow[i-1])
  else:
    positive_flow.append(0)
    negative_flow.append(0)

positive_mf = []
negative_mf = []
for i in range(period-1,len(positive_flow)):
  positive_mf.append(sum(positive_flow[i+1-period:i+1]))
for i in range(period-1,len(negative_flow)):
  negative_mf.append(sum(negative_flow[i+1-period:i+1]))

mfi = 100*(np.array(positive_mf)/(np.array(positive_mf) + np.array(negative_mf)))
mfi_df = pd.DataFrame()
mfi_df['MFI'] = mfi
plt.figure(figsize=[13,5])
plt.plot(mfi_df['MFI'],label='MFI')
plt.axhline(10,linestyle='--', color='orange')
plt.axhline(20,linestyle='--', color='blue')
plt.axhline(80,linestyle='--', color='blue')
plt.axhline(90,linestyle='--', color='orange')
plt.title('MFI')
plt.ylabel('MFI VALUES')
plt.show()

new_df = pd.DataFrame()
new_df = df[period:]
new_df['MFI'] = mfi

def get_signal(data,high,low):
  buy = []
  sell = []

  for i in range(len(data['MFI'])):
    if data['MFI'][i]>high:
      buy.append(np.nan)
      sell.append(data['Close'][i])
    elif data['MFI'][i]<low:
      buy.append(data['Close'][i])
      sell.append(np.nan)
    else:
      buy.append(np.nan)
      sell.append(np.nan)

  return (buy,sell)

new_df['Buy'] = get_signal(new_df,80,20)[0]
new_df['Sell'] = get_signal(new_df,80,20)[1]

new_df = new_df.reset_index()
new_df = new_df.set_index(pd.DatetimeIndex(new_df['Date'].values))

plt.figure(figsize=[20,10])
plt.plot(new_df['Close'],label='Close Price', alpha = 0.5)
plt.scatter(new_df.index, new_df['Buy'],color='green',label='Buy',marker='^',alpha=1)
plt.scatter(new_df.index, new_df['Sell'],color='red',label='Sell',marker='v',alpha=1)

plt.title('BUY SELL')

plt.xlabel('Date')
plt.ylabel('Close')
plt.legend(loc='upper left')
plt.show()

df.head()

AAPL = pd.DataFrame()
stock = 'GARAN.IS'
AAPL["Adj Close Price"] = df[stock]
#plt.figure(figsize=(20,10))
plt.plot(AAPL["Adj Close Price"], label = stock)
plt.title("Title")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc="upper left")
plt.show()

SMA30 = pd.DataFrame()
SMA30["Adj Close Price"] = AAPL["Adj Close Price"].rolling(window = 30).mean()

SMA100 = pd.DataFrame()
SMA100["Adj Close Price"] = AAPL["Adj Close Price"].rolling(window = 100).mean()

plt.figure(figsize=(12.5,4.5))
plt.plot(AAPL["Adj Close Price"], label = stock)
plt.plot(SMA30["Adj Close Price"], label = "SMA30")
plt.plot(SMA100["Adj Close Price"], label = "SMA100")
plt.title("Title")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc="upper left")
plt.show()

data = pd.DataFrame()
data["AAPL"] = AAPL["Adj Close Price"]
data["SMA30"] = SMA30["Adj Close Price"]
data["SMA100"] = SMA100["Adj Close Price"]

def buy_sell(data):
  sigPriceBuy = []
  sigPriceSell = []
  flag = -1

  for i in range(len(data)):
    if data['SMA30'][i] > data['SMA100'][i]:
      if flag != 1:
        sigPriceBuy.append(data['AAPL'][i])
        sigPriceSell.append(np.nan)
        flag = 1

      else:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(np.nan)
    elif data['SMA30'][i] < data['SMA100'][i]:
      if flag != 0:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(data['AAPL'][i])
        flag = 0
      else:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(np.nan)
    else:
      sigPriceBuy.append(np.nan)
      sigPriceSell.append(np.nan)

  return (sigPriceBuy, sigPriceSell)

buy_sell = buy_sell(data)
data['Buy_Signal_Price'] = buy_sell[0]
data['Sell_Signal_Price'] = buy_sell[1]

plt.figure(figsize=(12.6,4.6))
plt.plot(data["AAPL"],label = stock,alpha = 0.35)
plt.plot(data["SMA30"],label = "SMA30",alpha = 0.35)
plt.plot(data["SMA100"],label = "SMA100",alpha = 0.35)
plt.scatter(data.index, data["Buy_Signal_Price"],label = "Buy", marker = "^",color = "green")
plt.scatter(data.index, data["Sell_Signal_Price"],label = "Sell", marker = "v",color = "red")
plt.title("title")
plt.xlabel("time")
plt.ylabel("$")
plt.legend(loc = "upper left")
plt.show()

"""PREDICTION"""

def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white',figsize=(20,10))
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    print ('yo')
    #Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
    plt.show()

def load_data(filename, seq_len, normalise_window):
    f = open(filename, 'r').read()
    data = f.split('\n')

    sequence_length = seq_len + 1
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])
    
    if normalise_window:
        result = normalise_windows(result)

    result = np.array(result)

    row = round(0.9 * result.shape[0])
    train = result[:int(row), :]
    np.random.shuffle(train)
    x_train = train[:, :-1]
    y_train = train[:, -1]
    x_test = result[int(row):, :-1]
    y_test = result[int(row):, -1]

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))  

    return [x_train, y_train, x_test, y_test]

def normalise_windows(window_data):
    normalised_data = []
    for window in window_data:
        normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
        normalised_data.append(normalised_window)
    return normalised_data

def build_model(layers):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1],1)))
    model.add(LSTM(50,return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    
    '''model = Sequential()

    model.add(LSTM(
        input_dim=layers[0],
        output_dim=layers[1],
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        layers[2],
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=layers[3]))
    model.add(Activation("linear"))
'''
    start = time.time()
    model.compile(loss="mse", optimizer="rmsprop")
    print("Compilation Time : ", time.time() - start)
    return model

def predict_point_by_point(model, data):
    #Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
    predicted = model.predict(data)
    predicted = np.reshape(predicted, (predicted.size,))
    return predicted

def predict_sequence_full(model, data, window_size):
    #Shift the window by 1 new prediction each time, re-run predictions on new window
    curr_frame = data[0]
    predicted = []
    for i in range(len(data)):
        predicted.append(model.predict(curr_frame[np.newaxis,:,:])[0,0])
        curr_frame = curr_frame[1:]
        curr_frame = np.insert(curr_frame, [window_size-1], predicted[-1], axis=0)
    return predicted

def predict_sequences_multiple(model, data, window_size, prediction_len):
    #Predict sequence of 50 steps before shifting prediction run forward by 50 steps
    prediction_seqs = []
    for i in range(int(len(data)/prediction_len)):
        curr_frame = data[i*prediction_len]
        predicted = []
        for j in range(prediction_len):
            predicted.append(model.predict(curr_frame[np.newaxis,:,:])[0,0])
            curr_frame = curr_frame[1:]
            curr_frame = np.insert(curr_frame, [window_size-1], predicted[-1], axis=0)
        prediction_seqs.append(predicted)
    return prediction_seqs
