import dash
from dash import html, dcc, dash_table, callback_context
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from collections import Counter

# ============================================================
# DATA - All 64 matches
# ============================================================
ALL_MATCHES = [
# Group A
{"id":1,"date":"Nov 20","stage":"Group A","home":"Qatar","away":"Ecuador","hs":0,"as":2,"hg":[],"ag":["Valencia 16'","Valencia 31'"],"venue":"Al Bayt Stadium","pen":None},
{"id":2,"date":"Nov 21","stage":"Group A","home":"Senegal","away":"Netherlands","hs":0,"as":2,"hg":[],"ag":["Gakpo 84'","Klaassen 90+9'"],"venue":"Al Thumama Stadium","pen":None},
{"id":3,"date":"Nov 25","stage":"Group A","home":"Qatar","away":"Senegal","hs":1,"as":3,"hg":["Muntari 78'"],"ag":["Dia 41'","Diedhiou 48'","Dieng 84'"],"venue":"Al Thumama Stadium","pen":None},
{"id":4,"date":"Nov 25","stage":"Group A","home":"Netherlands","away":"Ecuador","hs":1,"as":1,"hg":["Gakpo 6'"],"ag":["Valencia 49'"],"venue":"Khalifa Intl Stadium","pen":None},
{"id":5,"date":"Nov 29","stage":"Group A","home":"Ecuador","away":"Senegal","hs":1,"as":2,"hg":["Caicedo 67'"],"ag":["Sarr 44'","Koulibaly 70'"],"venue":"Khalifa Intl Stadium","pen":None},
{"id":6,"date":"Nov 29","stage":"Group A","home":"Netherlands","away":"Qatar","hs":2,"as":0,"hg":["Gakpo 26'","de Jong 49'"],"ag":[],"venue":"Al Bayt Stadium","pen":None},
# Group B
{"id":7,"date":"Nov 21","stage":"Group B","home":"England","away":"Iran","hs":6,"as":2,"hg":["Bellingham 35'","Saka 43'","Sterling 45+1'","Saka 62'","Rashford 71'","Grealish 90'"],"ag":["Taremi 65'","Taremi 90+13'"],"venue":"Khalifa Intl Stadium","pen":None},
{"id":8,"date":"Nov 21","stage":"Group B","home":"USA","away":"Wales","hs":1,"as":1,"hg":["Weah 36'"],"ag":["Bale 82'"],"venue":"Ahmad bin Ali Stadium","pen":None},
{"id":9,"date":"Nov 25","stage":"Group B","home":"Wales","away":"Iran","hs":0,"as":2,"hg":[],"ag":["Cheshmi 90+8'","Rezaeian 90+11'"],"venue":"Ahmad bin Ali Stadium","pen":None},
{"id":10,"date":"Nov 25","stage":"Group B","home":"England","away":"USA","hs":0,"as":0,"hg":[],"ag":[],"venue":"Al Bayt Stadium","pen":None},
{"id":11,"date":"Nov 29","stage":"Group B","home":"Wales","away":"England","hs":0,"as":3,"hg":[],"ag":["Rashford 50'","Foden 51'","Rashford 68'"],"venue":"Ahmad bin Ali Stadium","pen":None},
{"id":12,"date":"Nov 29","stage":"Group B","home":"Iran","away":"USA","hs":0,"as":1,"hg":[],"ag":["Pulisic 38'"],"venue":"Al Thumama Stadium","pen":None},
# Group C
{"id":13,"date":"Nov 22","stage":"Group C","home":"Argentina","away":"Saudi Arabia","hs":1,"as":2,"hg":["Messi 10'"],"ag":["Al-Shehri 48'","Al-Dawsari 53'"],"venue":"Lusail Stadium","pen":None},
{"id":14,"date":"Nov 22","stage":"Group C","home":"Mexico","away":"Poland","hs":0,"as":0,"hg":[],"ag":[],"venue":"Stadium 974","pen":None},
{"id":15,"date":"Nov 26","stage":"Group C","home":"Poland","away":"Saudi Arabia","hs":2,"as":0,"hg":["Zielinski 39'","Lewandowski 82'"],"ag":[],"venue":"Education City Stadium","pen":None},
{"id":16,"date":"Nov 26","stage":"Group C","home":"Argentina","away":"Mexico","hs":2,"as":0,"hg":["Messi 64'","E. Fernandez 87'"],"ag":[],"venue":"Lusail Stadium","pen":None},
{"id":17,"date":"Nov 30","stage":"Group C","home":"Poland","away":"Argentina","hs":0,"as":2,"hg":[],"ag":["Mac Allister 46'","Alvarez 67'"],"venue":"Stadium 974","pen":None},
{"id":18,"date":"Nov 30","stage":"Group C","home":"Saudi Arabia","away":"Mexico","hs":1,"as":2,"hg":["Al-Dawsari 90+5'"],"ag":["Martin 47'","Chavez 52'"],"venue":"Lusail Stadium","pen":None},
# Group D
{"id":19,"date":"Nov 22","stage":"Group D","home":"Denmark","away":"Tunisia","hs":0,"as":0,"hg":[],"ag":[],"venue":"Education City Stadium","pen":None},
{"id":20,"date":"Nov 22","stage":"Group D","home":"France","away":"Australia","hs":4,"as":1,"hg":["Rabiot 27'","Giroud 32'","Mbappe 68'","Giroud 71'"],"ag":["Goodwin 9'"],"venue":"Al Janoub Stadium","pen":None},
{"id":21,"date":"Nov 26","stage":"Group D","home":"Tunisia","away":"Australia","hs":0,"as":1,"hg":[],"ag":["Duke 23'"],"venue":"Al Janoub Stadium","pen":None},
{"id":22,"date":"Nov 26","stage":"Group D","home":"France","away":"Denmark","hs":2,"as":1,"hg":["Mbappe 61'","Mbappe 86'"],"ag":["Christensen 68'"],"venue":"Stadium 974","pen":None},
{"id":23,"date":"Nov 30","stage":"Group D","home":"Tunisia","away":"France","hs":1,"as":0,"hg":["Khazri 58'"],"ag":[],"venue":"Education City Stadium","pen":None},
{"id":24,"date":"Nov 30","stage":"Group D","home":"Australia","away":"Denmark","hs":1,"as":0,"hg":["Leckie 60'"],"ag":[],"venue":"Al Janoub Stadium","pen":None},
# Group E
{"id":25,"date":"Nov 23","stage":"Group E","home":"Germany","away":"Japan","hs":1,"as":2,"hg":["Gundogan 33'"],"ag":["Doan 75'","Asano 83'"],"venue":"Khalifa Intl Stadium","pen":None},
{"id":26,"date":"Nov 23","stage":"Group E","home":"Spain","away":"Costa Rica","hs":7,"as":0,"hg":["Olmo 11'","Asensio 21'","Torres 31'","Torres 54'","Gavi 74'","Soler 90'","Morata 90+2'"],"ag":[],"venue":"Al Thumama Stadium","pen":None},
{"id":27,"date":"Nov 27","stage":"Group E","home":"Japan","away":"Costa Rica","hs":0,"as":1,"hg":[],"ag":["Fuller 81'"],"venue":"Ahmad bin Ali Stadium","pen":None},
{"id":28,"date":"Nov 27","stage":"Group E","home":"Spain","away":"Germany","hs":1,"as":1,"hg":["Morata 62'"],"ag":["Fullkrug 83'"],"venue":"Al Bayt Stadium","pen":None},
{"id":29,"date":"Dec 1","stage":"Group E","home":"Japan","away":"Spain","hs":2,"as":1,"hg":["Doan 48'","Tanaka 51'"],"ag":["Morata 11'"],"venue":"Khalifa Intl Stadium","pen":None},
{"id":30,"date":"Dec 1","stage":"Group E","home":"Costa Rica","away":"Germany","hs":2,"as":4,"hg":["Tejeda 58'","Vargas 73'"],"ag":["Gnabry 10'","Havertz 73'","Havertz 85'","Fullkrug 89'"],"venue":"Al Bayt Stadium","pen":None},
# Group F
{"id":31,"date":"Nov 23","stage":"Group F","home":"Morocco","away":"Croatia","hs":0,"as":0,"hg":[],"ag":[],"venue":"Al Bayt Stadium","pen":None},
{"id":32,"date":"Nov 23","stage":"Group F","home":"Belgium","away":"Canada","hs":1,"as":0,"hg":["Batshuayi 44'"],"ag":[],"venue":"Ahmad bin Ali Stadium","pen":None},
{"id":33,"date":"Nov 27","stage":"Group F","home":"Belgium","away":"Morocco","hs":0,"as":2,"hg":[],"ag":["Sabiri 73'","Aboukhlal 90+2'"],"venue":"Al Thumama Stadium","pen":None},
{"id":34,"date":"Nov 27","stage":"Group F","home":"Croatia","away":"Canada","hs":4,"as":1,"hg":["Kramaric 36'","Livaja 44'","Kramaric 70'","Majer 94'"],"ag":["Davies 2'"],"venue":"Khalifa Intl Stadium","pen":None},
{"id":35,"date":"Dec 1","stage":"Group F","home":"Croatia","away":"Belgium","hs":0,"as":0,"hg":[],"ag":[],"venue":"Ahmad bin Ali Stadium","pen":None},
{"id":36,"date":"Dec 1","stage":"Group F","home":"Canada","away":"Morocco","hs":1,"as":2,"hg":["Aguerd 40'(OG)"],"ag":["Ziyech 4'","En-Nesyri 23'"],"venue":"Al Thumama Stadium","pen":None},
# Group G
{"id":37,"date":"Nov 24","stage":"Group G","home":"Switzerland","away":"Cameroon","hs":1,"as":0,"hg":["Embolo 48'"],"ag":[],"venue":"Al Janoub Stadium","pen":None},
{"id":38,"date":"Nov 24","stage":"Group G","home":"Brazil","away":"Serbia","hs":2,"as":0,"hg":["Richarlison 62'","Richarlison 73'"],"ag":[],"venue":"Lusail Stadium","pen":None},
{"id":39,"date":"Nov 28","stage":"Group G","home":"Cameroon","away":"Serbia","hs":3,"as":3,"hg":["Castelletto 29'","Choupo-Moting 63'","Aboubakar 66'"],"ag":["Pavlovic 45+1'","Milinkovic-Savic 45+3'","Mitrovic 53'"],"venue":"Al Janoub Stadium","pen":None},
{"id":40,"date":"Nov 28","stage":"Group G","home":"Brazil","away":"Switzerland","hs":1,"as":0,"hg":["Casemiro 83'"],"ag":[],"venue":"Stadium 974","pen":None},
{"id":41,"date":"Dec 2","stage":"Group G","home":"Serbia","away":"Switzerland","hs":2,"as":3,"hg":["Mitrovic 26'","Vlahovic 35'"],"ag":["Shaqiri 20'","Embolo 44'","Freuler 48'"],"venue":"Stadium 974","pen":None},
{"id":42,"date":"Dec 2","stage":"Group G","home":"Cameroon","away":"Brazil","hs":1,"as":0,"hg":["Aboubakar 90+2'"],"ag":[],"venue":"Lusail Stadium","pen":None},
# Group H
{"id":43,"date":"Nov 24","stage":"Group H","home":"Uruguay","away":"South Korea","hs":0,"as":0,"hg":[],"ag":[],"venue":"Education City Stadium","pen":None},
{"id":44,"date":"Nov 24","stage":"Group H","home":"Portugal","away":"Ghana","hs":3,"as":2,"hg":["Ronaldo 65'","Joao Felix 78'","Leao 80'"],"ag":["A. Ayew 73'","Bukari 89'"],"venue":"Stadium 974","pen":None},
{"id":45,"date":"Nov 28","stage":"Group H","home":"South Korea","away":"Ghana","hs":2,"as":3,"hg":["Cho Gue-sung 58'","Cho Gue-sung 61'"],"ag":["Salisu 24'","Kudus 34'","Kudus 68'"],"venue":"Education City Stadium","pen":None},
{"id":46,"date":"Nov 28","stage":"Group H","home":"Portugal","away":"Uruguay","hs":2,"as":0,"hg":["Bruno Fernandes 54'","Bruno Fernandes 90+3'"],"ag":[],"venue":"Lusail Stadium","pen":None},
{"id":47,"date":"Dec 2","stage":"Group H","home":"South Korea","away":"Portugal","hs":2,"as":1,"hg":["Kim Young-gwon 27'","Hwang Hee-chan 90+1'"],"ag":["Horta 5'"],"venue":"Education City Stadium","pen":None},
{"id":48,"date":"Dec 2","stage":"Group H","home":"Ghana","away":"Uruguay","hs":0,"as":2,"hg":[],"ag":["de Arrascaeta 26'","de Arrascaeta 32'"],"venue":"Al Janoub Stadium","pen":None},
# Round of 16
{"id":49,"date":"Dec 3","stage":"Round of 16","home":"Netherlands","away":"USA","hs":3,"as":1,"hg":["Depay 10'","Blind 45+1'","Dumfries 81'"],"ag":["Wright 76'"],"venue":"Khalifa Intl Stadium","pen":None},
{"id":50,"date":"Dec 3","stage":"Round of 16","home":"Argentina","away":"Australia","hs":2,"as":1,"hg":["Messi 35'","Alvarez 57'"],"ag":["Goodwin 77'"],"venue":"Ahmad bin Ali Stadium","pen":None},
{"id":51,"date":"Dec 4","stage":"Round of 16","home":"France","away":"Poland","hs":3,"as":1,"hg":["Giroud 44'","Mbappe 74'","Mbappe 91'"],"ag":["Lewandowski 90+9'"],"venue":"Al Thumama Stadium","pen":None},
{"id":52,"date":"Dec 4","stage":"Round of 16","home":"England","away":"Senegal","hs":3,"as":0,"hg":["Henderson 38'","Kane 45+3'","Saka 57'"],"ag":[],"venue":"Al Bayt Stadium","pen":None},
{"id":53,"date":"Dec 5","stage":"Round of 16","home":"Japan","away":"Croatia","hs":1,"as":1,"hg":["Maeda 43'"],"ag":["Perisic 55'"],"venue":"Al Janoub Stadium","pen":"Croatia 3-1"},
{"id":54,"date":"Dec 5","stage":"Round of 16","home":"Brazil","away":"South Korea","hs":4,"as":1,"hg":["Vinicius 7'","Neymar 13'","Richarlison 29'","Paqueta 36'"],"ag":["Paik 76'"],"venue":"Stadium 974","pen":None},
{"id":55,"date":"Dec 6","stage":"Round of 16","home":"Morocco","away":"Spain","hs":0,"as":0,"hg":[],"ag":[],"venue":"Education City Stadium","pen":"Morocco 3-0"},
{"id":56,"date":"Dec 6","stage":"Round of 16","home":"Portugal","away":"Switzerland","hs":6,"as":1,"hg":["G. Ramos 17'","Pepe 33'","G. Ramos 51'","Guerreiro 55'","G. Ramos 67'","Leao 92'"],"ag":["Akanji 58'"],"venue":"Lusail Stadium","pen":None},
# Quarter-finals
{"id":57,"date":"Dec 9","stage":"Quarter-final","home":"Croatia","away":"Brazil","hs":1,"as":1,"hg":["Petkovic 117'"],"ag":["Neymar 105+1'"],"venue":"Education City Stadium","pen":"Croatia 4-2"},
{"id":58,"date":"Dec 9","stage":"Quarter-final","home":"Netherlands","away":"Argentina","hs":2,"as":2,"hg":["Weghorst 83'","Weghorst 90+11'"],"ag":["Molina 35'","Messi 73'"],"venue":"Lusail Stadium","pen":"Argentina 4-3"},
{"id":59,"date":"Dec 10","stage":"Quarter-final","home":"Morocco","away":"Portugal","hs":1,"as":0,"hg":["En-Nesyri 42'"],"ag":[],"venue":"Al Thumama Stadium","pen":None},
{"id":60,"date":"Dec 10","stage":"Quarter-final","home":"England","away":"France","hs":1,"as":2,"hg":["Kane 54'"],"ag":["Tchouameni 17'","Giroud 78'"],"venue":"Al Bayt Stadium","pen":None},
# Semi-finals
{"id":61,"date":"Dec 13","stage":"Semi-final","home":"Argentina","away":"Croatia","hs":3,"as":0,"hg":["Messi 34'","Alvarez 39'","Alvarez 69'"],"ag":[],"venue":"Lusail Stadium","pen":None},
{"id":62,"date":"Dec 14","stage":"Semi-final","home":"France","away":"Morocco","hs":2,"as":0,"hg":["T. Hernandez 5'","Kolo Muani 79'"],"ag":[],"venue":"Al Bayt Stadium","pen":None},
# 3rd Place & Final
{"id":63,"date":"Dec 17","stage":"3rd Place","home":"Croatia","away":"Morocco","hs":2,"as":1,"hg":["Gvardiol 7'","Orsic 42'"],"ag":["Dari 9'"],"venue":"Khalifa Intl Stadium","pen":None},
{"id":64,"date":"Dec 18","stage":"Final","home":"Argentina","away":"France","hs":3,"as":3,"hg":["Messi 23'","Alvarez 36'","Messi 108'"],"ag":["Mbappe 80'","Mbappe 81'","Mbappe 118'"],"venue":"Lusail Stadium","pen":"Argentina 4-2"},
]

# Match stats: {id: [poss_h,poss_a,shots_h,shots_a,sot_h,sot_a,corners_h,corners_a,fouls_h,fouls_a,yc_h,yc_a]}
MATCH_STATS = {
1:[46,54,5,7,0,3,2,5,10,9,2,3],2:[42,58,9,13,2,3,5,7,14,11,3,2],3:[28,72,6,19,2,5,1,6,13,14,4,5],
4:[47,53,6,5,2,1,4,3,11,10,3,2],5:[44,56,5,10,3,4,5,6,17,13,4,3],6:[24,76,0,12,0,3,2,5,10,8,3,1],
7:[36,64,14,22,4,7,3,10,21,11,4,6],8:[51,49,9,7,2,1,3,2,10,15,2,3],9:[40,60,7,9,1,5,3,7,8,14,3,5],
10:[55,45,9,15,1,6,5,6,7,10,1,2],11:[36,64,3,15,1,6,3,6,13,8,3,2],12:[52,48,11,6,3,2,5,3,16,14,4,3],
13:[64,36,15,3,6,2,5,0,22,8,6,2],14:[52,48,6,5,1,0,3,4,11,16,3,4],15:[30,70,10,7,3,2,4,3,15,12,4,3],
16:[62,38,16,3,6,0,5,0,7,9,2,4],17:[34,66,7,14,3,6,4,6,10,15,3,5],18:[36,64,4,14,2,5,5,7,14,11,5,3],
19:[44,56,6,13,0,4,2,7,14,13,4,2],20:[39,61,5,20,2,8,3,8,11,9,2,3],21:[42,58,4,8,1,4,4,5,15,10,5,2],
22:[34,66,5,12,3,5,4,8,13,7,3,1],23:[49,51,4,4,2,0,2,3,9,8,4,1],24:[40,60,5,9,2,3,3,5,12,13,3,4],
25:[62,38,14,4,5,3,4,2,6,16,2,4],26:[72,28,17,1,9,0,7,0,8,15,0,4],27:[47,53,6,14,2,4,6,7,16,10,4,2],
28:[35,65,4,10,1,5,3,6,12,8,3,1],29:[18,82,11,12,4,5,5,8,16,7,3,0],30:[33,67,6,16,3,6,4,7,11,10,2,4],
31:[44,56,3,7,0,1,4,5,17,11,4,1],32:[34,66,6,9,2,4,4,3,18,14,5,3],33:[35,65,5,13,2,4,3,6,16,12,4,3],
34:[48,52,14,4,5,2,8,1,9,12,2,4],35:[47,53,7,5,1,0,5,2,14,12,3,4],36:[35,65,5,13,1,6,2,8,11,10,2,3],
37:[42,58,7,6,3,1,2,5,13,12,3,1],38:[44,56,5,11,1,4,3,7,18,11,6,2],39:[42,58,16,13,8,5,7,6,10,14,3,4],
40:[60,40,16,5,5,1,6,2,6,15,1,4],41:[43,57,11,14,7,6,4,9,14,10,3,4],42:[61,39,16,4,4,1,6,1,4,9,0,3],
43:[53,47,7,6,0,0,4,2,14,16,2,3],44:[38,62,4,9,3,5,3,6,18,11,6,3],45:[51,49,16,12,5,7,5,4,12,16,3,4],
46:[63,37,15,3,4,0,6,0,5,11,0,3],47:[37,63,9,12,5,3,5,6,16,10,4,2],48:[51,49,12,3,4,0,3,1,14,15,5,3],
49:[46,54,12,18,4,7,3,10,11,13,4,5],50:[65,35,15,5,7,1,5,1,6,12,1,3],51:[34,66,3,12,2,10,2,6,13,6,4,1],
52:[37,63,8,18,3,7,4,8,13,8,3,2],53:[43,57,8,11,4,3,6,5,24,17,5,3],54:[37,63,5,19,2,9,2,8,12,6,4,1],
55:[23,77,2,12,0,3,1,13,14,9,3,2],56:[32,68,4,18,2,12,2,6,13,7,4,1],57:[42,58,7,11,4,3,6,5,24,22,6,4],
58:[52,48,18,15,5,5,5,5,23,21,8,7],59:[24,76,5,14,2,4,2,8,14,7,5,2],60:[37,63,9,16,4,7,4,7,12,9,3,2],
61:[34,66,1,14,0,7,1,5,14,8,4,1],62:[23,77,4,14,1,6,2,6,14,6,5,0],63:[52,48,12,10,3,4,5,4,12,14,4,5],
64:[40,60,10,19,4,8,3,7,19,14,5,4],
}
# ============================================================
# TEAMS DATA
# ============================================================
TEAMS = {
"Qatar":{"grp":"A","flag":"\U0001f1f6\U0001f1e6","gp":3,"w":0,"d":0,"l":3,"gf":1,"ga":7,"pts":0,"finish":"Group Stage"},
"Ecuador":{"grp":"A","flag":"\U0001f1ea\U0001f1e8","gp":3,"w":1,"d":1,"l":1,"gf":4,"ga":3,"pts":4,"finish":"Group Stage"},
"Senegal":{"grp":"A","flag":"\U0001f1f8\U0001f1f3","gp":3,"w":2,"d":0,"l":1,"gf":5,"ga":4,"pts":6,"finish":"Round of 16"},
"Netherlands":{"grp":"A","flag":"\U0001f1f3\U0001f1f1","gp":5,"w":3,"d":1,"l":1,"gf":10,"ga":5,"pts":7,"finish":"Quarter-finals"},
"England":{"grp":"B","flag":"\U0001f3f4","gp":5,"w":3,"d":1,"l":1,"gf":13,"ga":4,"pts":7,"finish":"Quarter-finals"},
"Iran":{"grp":"B","flag":"\U0001f1ee\U0001f1f7","gp":3,"w":1,"d":0,"l":2,"gf":4,"ga":7,"pts":3,"finish":"Group Stage"},
"USA":{"grp":"B","flag":"\U0001f1fa\U0001f1f8","gp":4,"w":1,"d":1,"l":2,"gf":2,"ga":4,"pts":4,"finish":"Round of 16"},
"Wales":{"grp":"B","flag":"\U0001f3f4","gp":3,"w":0,"d":1,"l":2,"gf":1,"ga":6,"pts":1,"finish":"Group Stage"},
"Argentina":{"grp":"C","flag":"\U0001f1e6\U0001f1f7","gp":7,"w":5,"d":1,"l":1,"gf":15,"ga":8,"pts":7,"finish":"Champions"},
"Saudi Arabia":{"grp":"C","flag":"\U0001f1f8\U0001f1e6","gp":3,"w":1,"d":0,"l":2,"gf":3,"ga":5,"pts":3,"finish":"Group Stage"},
"Mexico":{"grp":"C","flag":"\U0001f1f2\U0001f1fd","gp":3,"w":1,"d":1,"l":1,"gf":2,"ga":3,"pts":4,"finish":"Group Stage"},
"Poland":{"grp":"C","flag":"\U0001f1f5\U0001f1f1","gp":4,"w":1,"d":1,"l":2,"gf":2,"ga":5,"pts":4,"finish":"Round of 16"},
"France":{"grp":"D","flag":"\U0001f1eb\U0001f1f7","gp":7,"w":5,"d":0,"l":2,"gf":16,"ga":8,"pts":7,"finish":"Runners-up"},
"Australia":{"grp":"D","flag":"\U0001f1e6\U0001f1fa","gp":4,"w":2,"d":0,"l":2,"gf":3,"ga":7,"pts":6,"finish":"Round of 16"},
"Denmark":{"grp":"D","flag":"\U0001f1e9\U0001f1f0","gp":3,"w":0,"d":1,"l":2,"gf":1,"ga":3,"pts":1,"finish":"Group Stage"},
"Tunisia":{"grp":"D","flag":"\U0001f1f9\U0001f1f3","gp":3,"w":1,"d":1,"l":1,"gf":1,"ga":1,"pts":4,"finish":"Group Stage"},
"Spain":{"grp":"E","flag":"\U0001f1ea\U0001f1f8","gp":4,"w":1,"d":1,"l":2,"gf":9,"ga":3,"pts":4,"finish":"Round of 16"},
"Costa Rica":{"grp":"E","flag":"\U0001f1e8\U0001f1f7","gp":3,"w":1,"d":0,"l":2,"gf":3,"ga":11,"pts":3,"finish":"Group Stage"},
"Germany":{"grp":"E","flag":"\U0001f1e9\U0001f1ea","gp":3,"w":1,"d":1,"l":1,"gf":6,"ga":5,"pts":4,"finish":"Group Stage"},
"Japan":{"grp":"E","flag":"\U0001f1ef\U0001f1f5","gp":4,"w":2,"d":0,"l":2,"gf":4,"ga":4,"pts":6,"finish":"Round of 16"},
"Belgium":{"grp":"F","flag":"\U0001f1e7\U0001f1ea","gp":3,"w":1,"d":1,"l":1,"gf":1,"ga":2,"pts":4,"finish":"Group Stage"},
"Canada":{"grp":"F","flag":"\U0001f1e8\U0001f1e6","gp":3,"w":0,"d":0,"l":3,"gf":2,"ga":7,"pts":0,"finish":"Group Stage"},
"Morocco":{"grp":"F","flag":"\U0001f1f2\U0001f1e6","gp":7,"w":3,"d":3,"l":1,"gf":6,"ga":4,"pts":7,"finish":"4th Place"},
"Croatia":{"grp":"F","flag":"\U0001f1ed\U0001f1f7","gp":7,"w":2,"d":4,"l":1,"gf":8,"ga":6,"pts":7,"finish":"3rd Place"},
"Brazil":{"grp":"G","flag":"\U0001f1e7\U0001f1f7","gp":5,"w":3,"d":0,"l":2,"gf":8,"ga":3,"pts":6,"finish":"Quarter-finals"},
"Switzerland":{"grp":"G","flag":"\U0001f1e8\U0001f1ed","gp":4,"w":2,"d":0,"l":2,"gf":5,"ga":6,"pts":6,"finish":"Round of 16"},
"Cameroon":{"grp":"G","flag":"\U0001f1e8\U0001f1f2","gp":3,"w":1,"d":1,"l":1,"gf":4,"ga":4,"pts":4,"finish":"Group Stage"},
"Serbia":{"grp":"G","flag":"\U0001f1f7\U0001f1f8","gp":3,"w":0,"d":1,"l":2,"gf":5,"ga":8,"pts":1,"finish":"Group Stage"},
"Portugal":{"grp":"H","flag":"\U0001f1f5\U0001f1f9","gp":5,"w":3,"d":0,"l":2,"gf":12,"ga":6,"pts":6,"finish":"Quarter-finals"},
"South Korea":{"grp":"H","flag":"\U0001f1f0\U0001f1f7","gp":4,"w":1,"d":1,"l":2,"gf":4,"ga":5,"pts":4,"finish":"Round of 16"},
"Ghana":{"grp":"H","flag":"\U0001f1ec\U0001f1ed","gp":3,"w":1,"d":0,"l":2,"gf":5,"ga":7,"pts":3,"finish":"Group Stage"},
"Uruguay":{"grp":"H","flag":"\U0001f1fa\U0001f1fe","gp":3,"w":1,"d":1,"l":1,"gf":2,"ga":2,"pts":4,"finish":"Group Stage"},
}

# Players: [name, team, position, matches, goals, assists, yellows, reds]
PLAYERS = [
["Kylian Mbappe","France","FW",7,8,2,1,0],["Lionel Messi","Argentina","FW",7,7,3,1,0],
["Olivier Giroud","France","FW",7,4,0,1,0],["Julian Alvarez","Argentina","FW",7,4,0,0,0],
["Goncalo Ramos","Portugal","FW",3,3,0,0,0],["Richarlison","Brazil","FW",5,3,1,0,0],
["Bukayo Saka","England","FW",5,3,0,0,0],["Marcus Rashford","England","FW",5,3,0,1,0],
["Enner Valencia","Ecuador","FW",3,3,0,1,0],["Alvaro Morata","Spain","FW",4,3,0,0,0],
["Cody Gakpo","Netherlands","FW",5,3,1,0,0],["Antoine Griezmann","France","MF",7,0,3,1,0],
["Bruno Fernandes","Portugal","MF",5,2,2,2,0],["Harry Kane","England","FW",5,2,2,0,0],
["Andrej Kramaric","Croatia","FW",7,2,0,2,0],["Cristiano Ronaldo","Portugal","FW",5,1,0,1,0],
["Neymar","Brazil","FW",5,2,1,1,0],["Luka Modric","Croatia","MF",7,0,1,2,0],
["Jude Bellingham","England","MF",5,1,0,0,0],["Enzo Fernandez","Argentina","MF",7,1,1,2,0],
["Alexis Mac Allister","Argentina","MF",7,1,1,0,0],["Denzel Dumfries","Netherlands","DF",5,1,2,2,0],
["Achraf Hakimi","Morocco","DF",7,0,1,2,0],["Josko Gvardiol","Croatia","DF",7,1,0,2,0],
["Dominik Livakovic","Croatia","GK",7,0,0,1,0],["Emiliano Martinez","Argentina","GK",7,0,0,1,0],
["Hugo Lloris","France","GK",7,0,0,0,0],["Salem Al-Dawsari","Saudi Arabia","MF",3,1,0,1,0],
["Ferran Torres","Spain","FW",4,2,0,0,0],["Dani Olmo","Spain","MF",4,1,1,0,0],
["Memphis Depay","Netherlands","FW",5,1,1,0,0],["Breel Embolo","Switzerland","FW",4,2,0,0,0],
["Pepe","Portugal","DF",5,1,0,2,0],["Theo Hernandez","France","DF",7,1,0,3,0],
["Randal Kolo Muani","France","FW",7,1,0,0,0],["Robert Lewandowski","Poland","FW",4,2,0,1,0],
["Vinicius Junior","Brazil","FW",5,1,1,1,0],["Casemiro","Brazil","MF",5,1,0,2,0],
["Ritsu Doan","Japan","MF",4,2,0,0,0],["Cho Gue-sung","South Korea","FW",4,2,0,0,0],
["Mohammed Kudus","Ghana","MF",3,2,0,0,0],["Youssef En-Nesyri","Morocco","FW",7,2,0,0,0],
["Hakim Ziyech","Morocco","MF",7,1,1,0,0],["Christian Pulisic","USA","MF",4,1,0,0,0],
["Wout Weghorst","Netherlands","FW",5,2,0,0,0],["Vincent Aboubakar","Cameroon","FW",3,2,0,0,1],
["Niklas Fullkrug","Germany","FW",3,2,0,0,0],["Ivan Perisic","Croatia","MF",7,1,2,1,0],
["Nahuel Molina","Argentina","DF",7,1,0,2,0],["Aurelien Tchouameni","France","MF",7,1,0,3,0],
["Kai Havertz","Germany","FW",3,2,0,1,0],["Gavi","Spain","MF",4,1,0,1,0],
["Lucas Paqueta","Brazil","MF",5,1,1,0,0],["Xherdan Shaqiri","Switzerland","MF",4,1,0,0,0],
]

# ============================================================
# ARGENTINA CHAMPIONS THEME CSS
# ============================================================
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
body { font-family: 'Outfit', sans-serif !important; background: #050a15 !important; }
.main-header { background: linear-gradient(135deg, #0f1b38 0%, #050a15 100%);
  border-bottom: 3px solid #43A1D5; padding: 20px 30px; margin-bottom: 20px; border-radius: 0 0 16px 16px; }
.main-header h1 { color: #F6B40E; font-weight: 800; font-size: clamp(1.5rem, 4vw, 2rem); margin: 0; text-shadow: 0 2px 10px rgba(246,180,14,0.3); }
.main-header p { color: #43A1D5; margin: 0; font-size: 0.95rem; }
.kpi-card { background: linear-gradient(145deg, #0f1b38, #050a15); border: 1px solid rgba(67,161,213,0.4);
  border-radius: 16px; padding: 20px; text-align: center; transition: all 0.3s ease; }
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 8px 25px rgba(67,161,213,0.3); border-color: #F6B40E; }
.kpi-value { font-size: clamp(1.5rem, 5vw, 2.5rem); font-weight: 800; color: #FFFFFF; }
.kpi-label { font-size: 0.85rem; color: #43A1D5; text-transform: uppercase; letter-spacing: 1px; }
.match-card { background: linear-gradient(145deg, #0f1b38, #050a15); border: 1px solid rgba(67,161,213,0.2);
  border-radius: 14px; padding: 16px; margin-bottom: 12px; cursor: pointer; transition: all 0.3s ease; }
.match-card:hover { border-color: #F6B40E; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(246,180,14,0.15); }
.match-score { font-size: 1.8rem; font-weight: 800; color: #FFFFFF; }
.match-team { font-size: 1rem; color: #dde; font-weight: 500; }
.match-info { font-size: 0.8rem; color: #75AADB; }
.stage-badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem;
  font-weight: 600; background: rgba(67,161,213,0.2); color: #F6B40E; border: 1px solid rgba(246,180,14,0.3); }
.stat-row { display: flex; align-items: center; margin: 6px 0; }
.stat-bar-container { flex: 1; height: 8px; background: #050a15; border-radius: 4px; margin: 0 10px; position: relative; }
.stat-bar-left { position: absolute; right: 50%; height: 100%; background: linear-gradient(90deg, #FFFFFF, #43A1D5); border-radius: 4px 0 0 4px; }
.stat-bar-right { position: absolute; left: 50%; height: 100%; background: linear-gradient(90deg, #F6B40E, #D49A0B); border-radius: 0 4px 4px 0; }
.stat-val { width: 35px; text-align: center; font-weight: 600; color: #ccd; font-size: 0.9rem; }
.stat-name { width: 100px; text-align: center; font-size: 0.8rem; color: #889; }
.detail-panel { background: linear-gradient(145deg, #050a15, #0f1b38); border: 1px solid rgba(67,161,213,0.3);
  border-radius: 16px; padding: 15px; }
.scorer-item { padding: 4px 8px; margin: 2px 0; border-radius: 6px; background: rgba(67,161,213,0.1);
  font-size: 0.9rem; color: #FFFFFF; }
.team-card { background: linear-gradient(145deg, #0f1b38, #050a15); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px; padding: 16px; text-align: center; transition: all 0.3s ease; cursor: pointer; }
.team-card:hover { border-color: #F6B40E; transform: translateY(-3px); box-shadow: 0 6px 20px rgba(246,180,14,0.15); }
.team-flag { font-size: 2.5rem; }
.tab-custom .nav-link { color: #75AADB !important; border: none !important; font-weight: 500; white-space: nowrap; }
.tab-custom .nav-link.active { color: #F6B40E !important; border-bottom: 3px solid #F6B40E !important;
  background: transparent !important; font-weight: 700; }
.nav-pills .nav-link.active { background: linear-gradient(135deg, #43A1D5, #0f1b38) !important; color: #FFFFFF !important; }
.dash-table-container .dash-spreadsheet { background: #050a15 !important; }
.penalty-badge { background: rgba(246,180,14,0.15); color: #F6B40E; padding: 2px 8px; border-radius: 10px;
  font-size: 0.75rem; font-weight: 600; }
"""

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def make_kpi(value, label, icon=""):
    return dbc.Col(html.Div([
        html.Div(icon, style={"fontSize":"1.5rem","marginBottom":"4px"}),
        html.Div(str(value), className="kpi-value"),
        html.Div(label, className="kpi-label"),
    ], className="kpi-card"), xs=6, sm=6, md=3, className="mb-3")

def make_match_card(m):
    pen_text = ""
    if m["pen"]:
        pen_text = html.Span(f" (pen: {m['pen']})", className="penalty-badge")
    score_display = f"{m['hs']} - {m['as']}"
    return dbc.Col(html.Div([
        html.Div([html.Span(m["stage"], className="stage-badge"),
                  html.Span(f"   {m['date']}", style={"color":"#667","fontSize":"0.8rem"})]),
        html.Div([
            dbc.Row([
                dbc.Col(html.Div(m["home"], className="match-team text-end"), xs=4, md=4),
                dbc.Col(html.Div([html.Span(score_display, className="match-score"), html.Br(), pen_text],
                        style={"textAlign":"center"}), xs=4, md=4),
                dbc.Col(html.Div(m["away"], className="match-team"), xs=4, md=4),
            ], align="center", className="mt-2"),
        ]),
        html.Div(m["venue"], className="match-info text-center mt-1"),
    ], className="match-card", id={"type":"match-card","index":m["id"]}),
    xs=12, sm=6, md=6, lg=4, className="mb-2")

def make_stat_bar(label, val_h, val_a):
    total = val_h + val_a if (val_h + val_a) > 0 else 1
    pct_h = (val_h / total) * 50
    pct_a = (val_a / total) * 50
    return html.Div([
        html.Span(str(val_h), className="stat-val"),
        html.Div([
            html.Div(style={"width":f"{pct_h}%"}, className="stat-bar-left"),
            html.Div(style={"width":f"{pct_a}%"}, className="stat-bar-right"),
        ], className="stat-bar-container"),
        html.Span(str(val_a), className="stat-val"),
    ], className="stat-row", style={"display":"flex","alignItems":"center","marginBottom":"8px"})

def get_match_detail(match_id):
    m = next((x for x in ALL_MATCHES if x["id"] == match_id), None)
    if not m:
        return html.Div("Match not found")
    stats = MATCH_STATS.get(match_id, [50,50,0,0,0,0,0,0,0,0,0,0])
    stat_labels = ["Possession %","Shots","Shots on Target","Corners","Fouls","Yellow Cards"]
    pen_info = ""
    if m["pen"]:
        pen_info = html.Div(html.Span(f"Penalties: {m['pen']}", className="penalty-badge"),
                           style={"textAlign":"center","marginTop":"8px"})
    h_scorers = html.Div([html.Div(s, className="scorer-item") for s in m["hg"]]) if m["hg"] else html.Div("\u2014", style={"color":"#556"})
    a_scorers = html.Div([html.Div(s, className="scorer-item") for s in m["ag"]]) if m["ag"] else html.Div("\u2014", style={"color":"#556"})

    return html.Div([
        html.Div([
            html.Span(m["stage"], className="stage-badge"),
            html.Span(f"   {m['date']} 2022  \u2022  {m['venue']}", style={"color":"#778","fontSize":"0.85rem"}),
        ], style={"textAlign":"center","marginBottom":"16px"}),
        dbc.Row([
            dbc.Col(html.H4(m["home"], style={"color":"#dde","textAlign":"right","fontWeight":"700"}), xs=4),
            dbc.Col(html.H3(f"{m['hs']} \u2014 {m['as']}", style={"color":"#F6B40E","textAlign":"center","fontWeight":"800"}), xs=4),
            dbc.Col(html.H4(m["away"], style={"color":"#dde","fontWeight":"700"}), xs=4),
        ], align="center"),
        pen_info if pen_info else html.Div(),
        html.Hr(style={"borderColor":"rgba(255,255,255,0.1)","margin":"16px 0"}),
        html.H6("Goal Scorers", style={"color":"#F6B40E","fontWeight":"600","textAlign":"center","marginBottom":"12px"}),
        dbc.Row([
            dbc.Col(h_scorers, xs=6, style={"textAlign":"right"}),
            dbc.Col(a_scorers, xs=6),
        ]),
        html.Hr(style={"borderColor":"rgba(255,255,255,0.1)","margin":"16px 0"}),
        html.H6("Match Statistics", style={"color":"#F6B40E","fontWeight":"600","textAlign":"center","marginBottom":"12px"}),
    ] + [
        html.Div([
            html.Div(stat_labels[i], style={"textAlign":"center","color":"#889","fontSize":"0.8rem","marginBottom":"2px"}),
            make_stat_bar(stat_labels[i], stats[i*2], stats[i*2+1]),
        ]) for i in range(6)
    ], className="detail-panel")

# ============================================================
# BUILD APP
# ============================================================
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.CYBORG, dbc.icons.FONT_AWESOME],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1, maximum-scale=1'}]
)

load_figure_template("cyborg")

# Inject custom CSS
app.index_string = '''<!DOCTYPE html><html><head>{%metas%}<title>FIFA World Cup 2022 Dashboard</title>{%favicon%}{%css%}
<style>''' + CUSTOM_CSS + '''</style></head><body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body></html>'''

# ============================================================
# LAYOUT
# ============================================================
stages_list = sorted(set(m["stage"] for m in ALL_MATCHES))
teams_list = sorted(TEAMS.keys())

players_df = pd.DataFrame(PLAYERS, columns=["Name","Team","Position","Matches","Goals","Assists","Yellows","Reds"])
players_df["G+A"] = players_df["Goals"] + players_df["Assists"]

app.layout = dbc.Container([
    # Header
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H1([html.I(className="fas fa-futbol me-2"), "FIFA World Cup Qatar 2022"]),
                html.P("Complete Tournament Dashboard \u2022 64 Matches \u2022 32 Teams \u2022 172 Goals"),
            ], xs=12),
        ]),
    ], className="main-header"),

    # Tabs (Scrollable on mobile)
    html.Div([
        dbc.Tabs([
            # ========== TAB 1: OVERVIEW ==========
            dbc.Tab(label="Overview", tab_id="tab-overview", children=[
                html.Div([
                    # Download Button Section
                    dcc.Download(id="download-schedule-csv"),
                    dbc.Row([
                        dbc.Col(
                            dbc.Button([html.I(className="fas fa-download me-2"), "Download Match Schedule"], 
                                       id="btn-download-schedule", 
                                       style={"backgroundColor": "#F6B40E", "color": "#050a15", "fontWeight": "bold", "border": "none", "borderRadius": "8px", "padding": "10px 20px", "width": "100%"}),
                            xs=12, md=4, className="ms-auto mt-2 mb-3"
                        )
                    ]),
                    
                    dbc.Row([
                        make_kpi("64", "Total Matches", "⚽"),
                        make_kpi("172", "Total Goals", "🎯"),
                        make_kpi("32", "Teams", "🌍"),
                        make_kpi("Argentina", "Champions", "🏆"),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="top-scorers-chart", config={'displayModeBar': False}), xs=12, md=6),
                        dbc.Col(dcc.Graph(id="goals-by-stage-chart", config={'displayModeBar': False}), xs=12, md=6),
                    ], className="mt-3"),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="team-goals-chart", config={'displayModeBar': False}), xs=12),
                    ], className="mt-3"),
                ], style={"padding":"10px"})
            ]),

            # ========== TAB 2: MATCHES ==========
            dbc.Tab(label="All Matches", tab_id="tab-matches", children=[
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Filter by Stage", style={"color":"#889","fontWeight":"500"}),
                            dcc.Dropdown(id="stage-filter", options=[{"label":"All Matches","value":"all"}]+
                                [{"label":s,"value":s} for s in stages_list],
                                value="all", clearable=False,
                                style={"backgroundColor":"#0f1b38","color":"#000"}),
                        ], xs=12, md=6, className="mb-2"),
                        dbc.Col([
                            html.Label("Search Team", style={"color":"#889","fontWeight":"500"}),
                            dbc.Input(id="team-search", placeholder="Type team name...",
                                     style={"backgroundColor":"#0f1b38","color":"#dde","border":"1px solid #333"}),
                        ], xs=12, md=6, className="mb-2"),
                    ], className="mt-3 mb-3"),
                    html.Div(id="matches-grid"),
                    dbc.Modal([
                        dbc.ModalHeader(dbc.ModalTitle("Match Details", style={"color":"#F6B40E"}),
                                       style={"background":"#050a15","borderBottom":"1px solid #222"}),
                        dbc.ModalBody(id="match-detail-body", style={"background":"#050a15", "padding": "10px"}),
                    ], id="match-modal", size="lg", is_open=False, centered=True),
                ], style={"padding":"10px"})
            ]),

            # ========== TAB 3: TEAMS ==========
            dbc.Tab(label="Teams", tab_id="tab-teams", children=[
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Select Team", style={"color":"#889","fontWeight":"500"}),
                            dcc.Dropdown(id="team-selector",
                                options=[{"label":f"{TEAMS[t].get('flag','')} {t}","value":t} for t in teams_list],
                                value="Argentina", clearable=False,
                                style={"backgroundColor":"#0f1b38","color":"#000"}),
                        ], xs=12, md=6),
                    ], className="mt-3"),
                    html.Div(id="team-detail-content", className="mt-3"),
                ], style={"padding":"10px"})
            ]),

            # ========== TAB 4: PLAYERS ==========
            dbc.Tab(label="Players", tab_id="tab-players", children=[
                html.Div([
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="player-goals-chart", config={'displayModeBar': False}), xs=12, md=6),
                        dbc.Col(dcc.Graph(id="player-assists-chart", config={'displayModeBar': False}), xs=12, md=6),
                    ], className="mt-3"),
                    dbc.Row([
                        dbc.Col([
                            html.H5("All Player Statistics", style={"color":"#F6B40E","fontWeight":"600","marginTop":"16px"}),
                            dash_table.DataTable(
                                id="players-table",
                                columns=[{"name":c,"id":c} for c in ["Name","Team","Position","Matches","Goals","Assists","G+A","Yellows","Reds"]],
                                data=players_df.sort_values("Goals",ascending=False).to_dict("records"),
                                sort_action="native", filter_action="native",
                                page_size=15,
                                style_table={'overflowX': 'auto'},
                                style_header={"backgroundColor":"#0f1b38","color":"#F6B40E","fontWeight":"700","border":"1px solid #333"},
                                style_cell={"backgroundColor":"#050a15","color":"#ccd","border":"1px solid #222",
                                           "fontFamily":"Outfit","fontSize":"0.9rem","padding":"8px", "minWidth": "100px"},
                                style_data_conditional=[
                                    {"if":{"row_index":"odd"},"backgroundColor":"#0a1329"},
                                    {"if":{"filter_query":"{Goals} >= 3"},"color":"#F6B40E","fontWeight":"600"},
                                ],
                                style_filter={"backgroundColor":"#0f1b38","color":"#ccd"},
                            ),
                        ], xs=12),
                    ], className="mt-2"),
                ], style={"padding":"10px"})
            ]),

        ], id="main-tabs", active_tab="tab-overview", className="tab-custom")
    ], style={'overflowX': 'auto'}), # Ensures tabs scroll horizontally on very small screens if needed
    
    # ---------------------------------------------------------
    # DASHBOARD FOOTER
    # ---------------------------------------------------------
    html.Div([
        html.P([
            "A Project by ", 
            html.Span("M.Sameer", style={"color": "#F6B40E", "fontWeight": "800", "letterSpacing": "1px"})
        ], style={"margin": "0", "fontSize": "1.1rem"}),
        html.P("© 2026 | Data Visualization Dashboard", style={"color": "#75AADB", "fontSize": "0.85rem", "margin": "5px 0 0 0"})
    ], style={"textAlign": "center", "padding": "25px 0", "marginTop": "30px", "borderTop": "1px solid rgba(67,161,213,0.3)"})

], fluid=True, style={"maxWidth":"1400px", "padding": "10px"})

# ============================================================
# CALLBACKS
# ============================================================

# Overview Charts
@app.callback(
    [Output("top-scorers-chart","figure"),
     Output("goals-by-stage-chart","figure"),
     Output("team-goals-chart","figure")],
    Input("main-tabs","active_tab"))
def update_overview(_):
    # Top Scorers
    top = players_df.nlargest(10, "Goals")
    fig1 = px.bar(top, x="Goals", y="Name", orientation="h", color="Goals",
                  color_continuous_scale=["#0f1b38", "#43A1D5", "#FFFFFF"], template="cyborg",
                  title="Top 10 Goal Scorers")
    fig1.update_layout(yaxis=dict(autorange="reversed"), showlegend=False,
                       plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(family="Outfit"), title_font_color="#F6B40E",
                       coloraxis_showscale=False, margin=dict(l=10,r=10,t=40,b=10))

    # Goals by stage
    stage_goals = {}
    for m in ALL_MATCHES:
        s = m["stage"] if "Group" not in m["stage"] else "Group Stage"
        stage_goals[s] = stage_goals.get(s, 0) + m["hs"] + m["as"]
    fig2 = px.pie(names=list(stage_goals.keys()), values=list(stage_goals.values()),
                  title="Goals by Tournament Stage", template="cyborg",
                  color_discrete_sequence=["#43A1D5", "#FFFFFF", "#F6B40E", "#0f1b38", "#75AADB", "#D49A0B"])
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(family="Outfit"), title_font_color="#F6B40E",
                       margin=dict(l=10,r=10,t=40,b=10))

    # Team goals
    team_gf = {}
    for m in ALL_MATCHES:
        team_gf[m["home"]] = team_gf.get(m["home"],0) + m["hs"]
        team_gf[m["away"]] = team_gf.get(m["away"],0) + m["as"]
    tg = sorted(team_gf.items(), key=lambda x: x[1], reverse=True)[:16]
    fig3 = px.bar(x=[t[0] for t in tg], y=[t[1] for t in tg], title="Goals Scored by Team (Top 16)",
                  template="cyborg", color=[t[1] for t in tg],
                  color_continuous_scale=["#0f1b38", "#43A1D5", "#FFFFFF"])
    fig3.update_layout(xaxis_title="", yaxis_title="Goals", showlegend=False,
                       plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(family="Outfit"), title_font_color="#F6B40E",
                       coloraxis_showscale=False, margin=dict(l=10,r=10,t=40,b=10))
    return fig1, fig2, fig3

# Matches Grid
@app.callback(Output("matches-grid","children"),
              [Input("stage-filter","value"), Input("team-search","value")])
def update_matches(stage, search):
    filtered = ALL_MATCHES
    if stage and stage != "all":
        filtered = [m for m in filtered if m["stage"] == stage]
    if search:
        s = search.lower()
        filtered = [m for m in filtered if s in m["home"].lower() or s in m["away"].lower()]
    if not filtered:
        return html.Div("No matches found.", style={"color":"#889","textAlign":"center","padding":"40px"})
    return dbc.Row([make_match_card(m) for m in filtered])

# Match Detail Modal
@app.callback(
    [Output("match-modal","is_open"), Output("match-detail-body","children")],
    Input({"type":"match-card","index":dash.ALL},"n_clicks"),
    prevent_initial_call=True)
def show_match_detail(clicks):
    if not callback_context.triggered or all(c is None for c in clicks):
        return False, ""
    triggered = callback_context.triggered[0]
    import json
    prop_id = triggered["prop_id"].rsplit(".",1)[0]
    match_id = json.loads(prop_id)["index"]
    return True, get_match_detail(match_id)

# Team Detail
@app.callback(Output("team-detail-content","children"), Input("team-selector","value"))
def update_team(team_name):
    if not team_name:
        return html.Div()
    t = TEAMS[team_name]
    team_matches = [m for m in ALL_MATCHES if m["home"] == team_name or m["away"] == team_name]

    # Team KPIs
    gf = sum(m["hs"] if m["home"]==team_name else m["as"] for m in team_matches)
    ga = sum(m["as"] if m["home"]==team_name else m["hs"] for m in team_matches)
    wins = sum(1 for m in team_matches if (m["home"]==team_name and m["hs"]>m["as"]) or (m["away"]==team_name and m["as"]>m["hs"]))
    draws = sum(1 for m in team_matches if m["hs"]==m["as"])
    cs = sum(1 for m in team_matches if (m["home"]==team_name and m["as"]==0) or (m["away"]==team_name and m["hs"]==0))

    # Team players
    tp = players_df[players_df["Team"]==team_name].sort_values("Goals",ascending=False)

    # Avg possession
    possessions = []
    for m in team_matches:
        st = MATCH_STATS.get(m["id"])
        if st:
            possessions.append(st[0] if m["home"]==team_name else st[1])
    avg_poss = round(sum(possessions)/len(possessions),1) if possessions else 0

    return html.Div([
        dbc.Row([
            dbc.Col(html.Div([
                html.Div(t.get("flag",""), style={"fontSize":"3rem"}),
                html.H2(team_name, style={"color":"#F6B40E","fontWeight":"800"}),
                html.Span(t["finish"], className="stage-badge", style={"fontSize":"1rem"}),
            ], style={"textAlign":"center"}), xs=12, className="mb-3"),
        ]),
        dbc.Row([
            make_kpi(len(team_matches), "Matches", ""),
            make_kpi(f"{wins}W {draws}D {len(team_matches)-wins-draws}L", "Record", ""),
            make_kpi(f"{gf}-{ga}", "GF-GA", ""),
            make_kpi(f"{avg_poss}%", "Avg Possession", ""),
        ]),
        html.H5("Tournament Matches", style={"color":"#F6B40E","fontWeight":"600","marginTop":"20px"}),
        dbc.Row([make_match_card(m) for m in team_matches]),
        html.H5("Squad Players in Database", style={"color":"#F6B40E","fontWeight":"600","marginTop":"20px"}),
        dash_table.DataTable(
            columns=[{"name":c,"id":c} for c in ["Name","Position","Matches","Goals","Assists","Yellows","Reds"]],
            data=tp.to_dict("records") if len(tp) > 0 else [],
            style_table={'overflowX': 'auto'},
            style_header={"backgroundColor":"#0f1b38","color":"#F6B40E","fontWeight":"700","border":"1px solid #333"},
            style_cell={"backgroundColor":"#050a15","color":"#ccd","border":"1px solid #222",
                        "fontFamily":"Outfit","fontSize":"0.9rem","padding":"8px", "minWidth": "100px"},
            style_data_conditional=[{"if":{"row_index":"odd"},"backgroundColor":"#0a1329"}],
        ) if len(tp) > 0 else html.P("No player data available for this team.", style={"color":"#667"}),
    ])

# Player Charts
@app.callback(
    [Output("player-goals-chart","figure"), Output("player-assists-chart","figure")],
    Input("main-tabs","active_tab"))
def update_player_charts(_):
    top_g = players_df.nlargest(12, "Goals")
    fig1 = px.bar(top_g, x="Name", y="Goals", color="Team", template="cyborg",
                  title="Top Goal Scorers",
                  color_discrete_sequence=["#43A1D5", "#FFFFFF", "#F6B40E", "#0f1b38", "#75AADB", "#D49A0B", "#1c2541", "#A1C4DF"])
    fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(family="Outfit"), title_font_color="#F6B40E",
                       margin=dict(l=10,r=10,t=40,b=10), xaxis_tickangle=-45)

    top_a = players_df[players_df["Assists"]>0].nlargest(12, "Assists")
    fig2 = px.bar(top_a, x="Name", y="Assists", color="Team", template="cyborg",
                  title="Top Assist Providers",
                  color_discrete_sequence=["#FFFFFF", "#F6B40E", "#43A1D5", "#75AADB", "#D49A0B", "#0f1b38"])
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(family="Outfit"), title_font_color="#F6B40E",
                       margin=dict(l=10,r=10,t=40,b=10), xaxis_tickangle=-45)
    return fig1, fig2

# Download Schedule Callback
@app.callback(
    Output("download-schedule-csv", "data"),
    Input("btn-download-schedule", "n_clicks"),
    prevent_initial_call=True,
)
def download_match_schedule(n_clicks):
    schedule_df = pd.DataFrame(ALL_MATCHES)
    clean_schedule = schedule_df[['date', 'stage', 'home', 'away', 'venue']]
    clean_schedule.columns = ['Date', 'Stage', 'Home Team', 'Away Team', 'Venue']
    return dcc.send_data_frame(clean_schedule.to_csv, "FIFA_2022_Schedule.csv", index=False)


# ============================================================
# RUN APP LOCALLY (Open to Network for Mobile viewing)
# ============================================================
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)