#!/usr/local/bin/python3



# data
syncs_ratio_001_threshold_05=[0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 1, 2, 1, 0, 0, 1, 2, 1, 0, 1]
syncs_ratio_001_threshold_06=[0, 0, 0, 0, 1, 1, 2, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 3]
syncs_ratio_002_threshold_05=[0, 2, 2, 2, 0, 4, 0, 2, 2, 2, 0, 4, 0, 2, 2, 2, 0, 4, 0, 2]
syncs_ratio_002_threshold_06=[0, 1, 2, 2, 0, 3, 0, 2, 2, 1, 0, 3, 1, 0, 2, 2, 1, 1, 2, 1]
syncs_ratio_003_threshold_05=[1, 3, 2, 3, 2, 3, 3, 2, 2, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 1]
syncs_ratio_003_threshold_06=[0, 4, 0, 3, 2, 2, 2, 2, 2, 3, 1, 3, 1, 3, 1, 2, 2, 3, 1, 3]
syncs_ratio_004_threshold_05=[3, 3, 3, 3, 3, 4, 2, 4, 3, 3, 3, 3, 3, 4, 2, 4, 2, 4, 2, 4]
syncs_ratio_004_threshold_06=[2, 3, 3, 2, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 2, 3, 1, 3, 2]


utils_ratio_001_threshold_05=[[0.1625914971116528, 0.17867116680155656, 0.14461726393218366, 0.10348097928122546], [0.28841214001660403, 0.34459223147269, 0.31211957674444935, 0.20999701115242453], [0.3847745527898782, 0.4895328839544929, 0.49636429414704497, 0.3307917835694737], [0.41545473942061406, 0.4895328839544929, 0.034331606150961855, 0.42065572849311816], [0.14979436005502222, 0.4895328839544929, 0.18190632313177507, 0.48723437174841283], [0.30091920734161326, 0.3945667310748847, 0.3536781881625136, 0.32426757373520776], [0.4555628996930389, 0.1057315172389839, 0.4421720820957011, 0.10756032797404239], [0.4521875750579987, 0.23215952092773773, 0.04257308690523786, 0.21406228359009077], [0.15095400239664267, 0.3546319479048791, 0.19604026138049785, 0.32115938545478023], [0.2955089804328031, 0.4554635717020329, 0.40353967487306436, 0.46148666802929833], [0.4515777464673051, 0.48937798891886675, 0.48141477210259914, 0.43570843356215194], [0.49448503316153597, 0.24141363104556157, 0.04336066089417545, 0.10348647427891938], [0.47410646237146703, 0.11673181424254407, 0.20892009931741307, 0.2025358555486072], [0.1295473408799517, 0.2271245108643421, 0.34517000394088243, 0.3177803644445647], [0.2642864676078932, 0.3439637532658018, 0.4647310947322637, 0.42016070822209484], [0.38688004712823787, 0.43803330315093586, 0.364745070155822, 0.4987920957963322], [0.3444630652809275, 0.4656982551945019, 0.1692594443782925, 0.4511193707101775], [0.13166512786582926, 0.2207248658891181, 0.35569738450414573, 0.12239227772495559], [0.26644667092873153, 0.13305416227822794, 0.44945591234298377, 0.23314499498829716], [0.40645282959072926, 0.256506312372307, 0.3188596351346304, 0.3351290743357874]]
utils_ratio_001_threshold_06=[[0.16437376663032083, 0.16780862850755235, 0.1473583327359139, 0.12053246218593497], [0.24752583990124408, 0.3592650122189328, 0.30271938809079724, 0.22265000716163205], [0.3630419494116072, 0.516107058376455, 0.4955480333259573, 0.328120518600539], [0.5260550635444785, 0.516107058376455, 0.5317478317962525, 0.4346013212145444], [0.5894240163218587, 0.5392387974173771, 0.4134837110017031, 0.5525278565377867], [0.2543496425022714, 0.5770492007044351, 0.16217162128252127, 0.5934541598621973], [0.15160272652412068, 0.3691588762246559, 0.34165784014301465, 0.2517905153375808], [0.3043100706417211, 0.11732238414647347, 0.5354366100214865, 0.1319677544747842], [0.4301324432020484, 0.2364046476218371, 0.5769730465023726, 0.22894680507318643], [0.5790277490226636, 0.3427166671990121, 0.41445645592777525, 0.3397606926548105], [0.372074571802648, 0.4608174880511964, 0.15332644834716944, 0.4552068694578384], [0.13669912686672625, 0.5661181064794562, 0.30555998295172887, 0.562723760583896], [0.2830225165685757, 0.5688648497961006, 0.48835219161303706, 0.4123794864942384], [0.4267642568650992, 0.4990376206760211, 0.5970718715909376, 0.12012927977736781], [0.5642777335838071, 0.12390280654761403, 0.21845613259213476, 0.2182343246945763], [0.2798544036385864, 0.2481431757891647, 0.21581940285090198, 0.3194109735735622], [0.15253681614441006, 0.36863921937650557, 0.42076569166274685, 0.4429912939992629], [0.2778440869277261, 0.47132037592196513, 0.5781998567796685, 0.5426703220141657], [0.4149866475725888, 0.5828118275454434, 0.5870633715948229, 0.5963840637724895], [0.5550906574850369, 0.38373435996146843, 0.051887032190090415, 0.38756739506372373]]
utils_ratio_002_threshold_05=[[0.3072197027526929, 0.3421877079143965, 0.24976859347633684, 0.21423586177459272], [0.3082827780871301, 0.47920287538105855, 0.07802902957598172, 0.44185499071322865], [0.2905426566739452, 0.3642297222623931, 0.38538999070712066, 0.26625928781600905], [0.47728876075529836, 0.27440066776706173, 0.008404439405282783, 0.2236257617061619], [0.29419372095951946, 0.49627941653911184, 0.3426566443126678, 0.4394642423777591], [0.3992896038079716, 0.3286506856360718, 0.2430704323337623, 0.40874422176994146], [0.3142913412688823, 0.1888947819251453, 0.35873495876894657, 0.21839199793722683], [0.3531398062893554, 0.434707302090796, 0.01726817291689759, 0.47504054398871115], [0.27334873320065867, 0.3739932112739084, 0.36618239899429217, 0.47993527185963497], [0.354826542433592, 0.2152384487341168, 0.11743948303236687, 0.2142330571346514], [0.33246844854345975, 0.42922461199569667, 0.3776327832710589, 0.41137769523939], [0.28307888956064525, 0.2586430032711723, 0.24522788365278214, 0.43297569105462885], [0.32533574810857063, 0.22756332293370793, 0.3326257085608282, 0.24973709984973383], [0.4187388293024506, 0.440557522854256, 0.10445194602259647, 0.4693093175007685], [0.2760118723768146, 0.38828087954636437, 0.38237586659888284, 0.2604255966655647], [0.2339691970825019, 0.23246188546192537, 0.009425687476130743, 0.23076510526362384], [0.2887410018309779, 0.4687992720866204, 0.37949039555218067, 0.4831057283213302], [0.2178408619421213, 0.27929502703391346, 0.4145698006380367, 0.23396492616728057], [0.28345194924864014, 0.20516363180375757, 0.351728343947687, 0.23688590243417035], [0.3518501225530237, 0.42000637076030906, 0.08051638395998907, 0.4577463839609101]]
utils_ratio_002_threshold_06=[[0.2712222290822351, 0.3213435470593091, 0.3207544689861091, 0.23065652247924906], [0.4359803138269371, 0.47513145673233403, 0.3284543362894614, 0.42207584867712283], [0.24312617254468524, 0.5922108548069347, 0.385020920258431, 0.26691516602755033], [0.2915116960951696, 0.3704694262436615, 0.08724466786658958, 0.2475643353546796], [0.5804276113249645, 0.24474635243070259, 0.3655234864799089, 0.45676757131404067], [0.31907442934235886, 0.4550512539254967, 0.13566641685291397, 0.3610007508792805], [0.2911066240020623, 0.5812113842886102, 0.42435941759140283, 0.24294559816578562], [0.5209944686891523, 0.24263231652907047, 0.08821154178920342, 0.4370577847348224], [0.2588678992009681, 0.24735477181724555, 0.40153102823120546, 0.3634689224482585], [0.27002902674550416, 0.4655498582172077, 0.27432799468623015, 0.23001979814595938], [0.5832591845285625, 0.5949874039915486, 0.35609376033229573, 0.4313073879994342], [0.4026333689736452, 0.21454516411390498, 0.21808955060617277, 0.578024906968368], [0.2756099740240673, 0.2492236687644619, 0.33538549903555326, 0.3954352869575094], [0.5526579154769559, 0.49618188095266136, 0.5994321008191236, 0.2571568609983153], [0.39624445584537904, 0.5682654310631168, 0.11328076594085967, 0.47235614964062395], [0.2803592723772366, 0.37181746132985016, 0.3835047493284942, 0.3519429298611697], [0.5948781767630119, 0.2036844846323507, 0.3662791491282705, 0.22622324638952343], [0.2016977934192985, 0.3924156973652707, 0.3278301484693281, 0.45233240085956267], [0.2965257125813543, 0.566377629983883, 0.42141631225567766, 0.3854427742589343], [0.5613359011218926, 0.24644397576457636, 0.3812083343255394, 0.22694809483041908]]
utils_ratio_003_threshold_05=[[0.43132721997896084, 0.22536556253502815, 0.42981705293101624, 0.32830978231501967], [0.2019211288467477, 0.41671869172981413, 0.14367088566984512, 0.4509872722609938], [0.4761789821121267, 0.2644265249088177, 0.16150194167415885, 0.38573444812435365], [0.4811107906619363, 0.31689379224159847, 0.09820716028325141, 0.2612767029377281], [0.46695565061826744, 0.3948650114833486, 0.1878994255923568, 0.3426394747381681], [0.20316456960481208, 0.30795373967921974, 0.1406180663152279, 0.3567200883625047], [0.37268981398145107, 0.4348002780668221, 0.23638674122826642, 0.3622780371524602], [0.41455346244151864, 0.38480082481664873, 0.478936642065564, 0.4164026665144738], [0.43895606585713876, 0.37671506350982586, 0.4848760138553084, 0.34323675258745573], [0.4709454335297865, 0.37736847189746814, 0.34815990680430153, 0.31849621808322665], [0.2152154888059868, 0.45378772343280566, 0.3511486790203854, 0.3156304774081698], [0.49690707119783367, 0.369021879138418, 0.3090816623524021, 0.29574965551097127], [0.44905335848343025, 0.4925309610671298, 0.3748918057233295, 0.3255733552385672], [0.41002867970146295, 0.382668928606927, 0.23847535099118403, 0.2610438448617591], [0.2518338593083905, 0.3424462957623236, 0.3548762321162693, 0.34393640312586315], [0.42080052242671034, 0.39793229083320525, 0.20569708909827256, 0.3940390405284576], [0.4698996025232761, 0.2564865823698899, 0.4397080790318231, 0.37624152906277464], [0.43304943847874894, 0.32744229363255867, 0.45028433340963675, 0.4169261957809742], [0.29559414993107413, 0.39686807679664826, 0.27117713252879994, 0.3475264927701001], [0.46500125886674365, 0.3922244602541826, 0.4930516541779134, 0.3647117012657119]]
utils_ratio_003_threshold_06=[[0.4664990516650571, 0.5565795347632986, 0.4739978861972722, 0.2855633347149273], [0.20531541598359457, 0.3904279642892021, 0.2960903974588466, 0.32357256303490545], [0.4378826485586484, 0.3287856642918391, 0.48863208575006967, 0.35540747219505125], [0.3125215443923274, 0.5595367236502526, 0.1783153046255961, 0.4038162665538223], [0.4591303104511219, 0.2031704232877228, 0.17730995152882337, 0.3835352219843345], [0.4007651929785069, 0.36680258238103997, 0.5890559986168393, 0.3619290593311604], [0.47335668948556847, 0.3193647170559393, 0.10283291376862391, 0.3279294383361578], [0.36215860844942505, 0.36283408613777374, 0.5633635478406931, 0.20471815261674228], [0.44033522745544945, 0.2396990301075228, 0.16778934137685134, 0.4094959198620262], [0.41298439064468484, 0.38634177516815854, 0.14404563478973187, 0.22784184970248073], [0.48698201771615873, 0.2323161166526781, 0.5676195973284963, 0.30314340468255885], [0.2747967475758604, 0.34641144332372725, 0.1521364136655097, 0.44075227220721275], [0.381065688315448, 0.5800808411094929, 0.43349291967676445, 0.3195805074712508], [0.4671045353562257, 0.38499748121463667, 0.5241795308160717, 0.48835817213300403], [0.4532669251218166, 0.3042206709868993, 0.2733795177612897, 0.3624428209479654], [0.2030768499117168, 0.583592333050923, 0.5678328643832075, 0.3646834381474921], [0.4455017408575769, 0.3875643519500792, 0.16421332476466957, 0.4251021958460898], [0.4218977296774423, 0.3523262263769913, 0.24207673485896483, 0.3299751332720213], [0.40910431623695054, 0.5984385822711441, 0.397904737837916, 0.37977969471183237], [0.4239518135110997, 0.38283926586379, 0.5082847093560888, 0.3711885856091526]]
utils_ratio_004_threshold_05=[[0.3995007266659386, 0.33007191834378824, 0.23813052171516497, 0.4833100441496658], [0.4901953430516814, 0.4717557516955246, 0.1799368197985816, 0.36915901204344526], [0.3267770144994868, 0.38368042690868276, 0.45105835811174655, 0.4550968086678499], [0.4136603007752946, 0.43801789297598515, 0.16902167050533407, 0.37583771023630785], [0.38704224939796716, 0.21893622951402555, 0.2891066970416391, 0.454595049587723], [0.24365871815951315, 0.35186572270908956, 0.2915451160964135, 0.362270581075661], [0.3440349966369596, 0.4592106863273689, 0.12999493100494058, 0.49927066943258586], [0.33720784239311685, 0.3148428081517962, 0.4173388345762955, 0.23812418684654368], [0.46071510507978963, 0.20842886835134206, 0.37480516717013984, 0.4999264096554854], [0.3282344752708444, 0.44755165499473637, 0.2194210572786087, 0.23082125867189232], [0.44530348139792286, 0.473179995866482, 0.2850019129657201, 0.45745990088118854], [0.3972685801387036, 0.4886649168211108, 0.15162411422344235, 0.35152619395471674], [0.4983826154893282, 0.3055325452629062, 0.2789463812495803, 0.4503338611362082], [0.24549378144373146, 0.2938761038779417, 0.47742609417296084, 0.35759981992609774], [0.29449174208636797, 0.452922036847125, 0.2883804401453506, 0.46231559450852217], [0.3356127290327727, 0.24455689705587633, 0.2540182099734531, 0.4951253692534391], [0.2866251122442095, 0.4562609237733577, 0.13586561875906786, 0.478671866501204], [0.2775032616449805, 0.38551331168521774, 0.3139102042212447, 0.34578202748820686], [0.48365749105434436, 0.4772188792857978, 0.20886270237971183, 0.46772546557974554], [0.3423533181750346, 0.24384448147269602, 0.2916762248133314, 0.3541822021083265]]
utils_ratio_004_threshold_06=[[0.5995452490735786, 0.4206822496595437, 0.001111528557880783, 0.48214436978592945], [0.22857613709678776, 0.4879957622261251, 0.20502605156850306, 0.34449261264887376], [0.2116557083082087, 0.4366061250649046, 0.21482833625277994, 0.4506288977555932], [0.5843207270172639, 0.411373334546205, 0.39844015205825845, 0.22701094870317745], [0.23409264026339596, 0.3199421905096706, 0.2043501733135305, 0.4610801626755123], [0.5433931579999569, 0.41285598300882576, 0.4830608497513849, 0.3682645845806254], [0.4670292820856032, 0.3473083393747602, 0.24297199481546788, 0.5167417117377787], [0.5596386765798433, 0.4245128133179757, 0.35917117958709666, 0.37298787062497263], [0.2687211716683019, 0.32060671495250614, 0.4629848356650136, 0.4362158883406708], [0.3164325775005477, 0.4763976007348729, 0.2248155797243182, 0.46988956287325584], [0.5372435831516595, 0.3792517258810455, 0.19988868416380734, 0.4918979700842553], [0.29948586850515235, 0.5137652873034546, 0.18777533636818572, 0.3349595180242658], [0.5642711835127746, 0.25095614597105853, 0.22372576307273764, 0.48207230499222475], [0.31582056136606074, 0.4713319773888114, 0.20668640458858675, 0.48824848928805975], [0.44427993532720267, 0.43034385850548884, 0.20054137409572947, 0.4631043407620007], [0.5368861669568367, 0.5808482938932131, 0.2377732251407293, 0.2688094376834539], [0.4268585872400544, 0.3115944117451061, 0.31401651208975245, 0.4907106479042381], [0.5217083652910993, 0.4494931021675752, 0.5981328083970613, 0.3975386682241967], [0.24289752868899675, 0.2393280126749689, 0.3848739878652949, 0.48830638932954123], [0.5852636127330451, 0.5216152758235034, 0.48843847786005035, 0.4189603998293979]]


# compose data
ratio_var_util_t05 = [[max(utils_ratio_001_threshold_05[i]) for i in range(len(utils_ratio_001_threshold_05))], [max(utils_ratio_002_threshold_05[i]) for i in range(len(utils_ratio_002_threshold_05))], [max(utils_ratio_003_threshold_05[i]) for i in range(len(utils_ratio_003_threshold_05))], [max(utils_ratio_004_threshold_05[i]) for i in range(len(utils_ratio_004_threshold_05))]]
ratio_var_util_t06 = [[max(utils_ratio_001_threshold_06[i]) for i in range(len(utils_ratio_001_threshold_06))], [max(utils_ratio_002_threshold_06[i]) for i in range(len(utils_ratio_002_threshold_06))], [max(utils_ratio_003_threshold_06[i]) for i in range(len(utils_ratio_003_threshold_06))], [max(utils_ratio_004_threshold_06[i]) for i in range(len(utils_ratio_004_threshold_06))]]

thre_var_util_r001 = [[max(utils_ratio_001_threshold_05[i]) for i in range(len(utils_ratio_001_threshold_05))], [max(utils_ratio_001_threshold_06[i]) for i in range(len(utils_ratio_001_threshold_06))]]
thre_var_util_r002 = [[max(utils_ratio_002_threshold_05[i]) for i in range(len(utils_ratio_002_threshold_05))], [max(utils_ratio_002_threshold_06[i]) for i in range(len(utils_ratio_002_threshold_06))]]
thre_var_util_r003 = [[max(utils_ratio_003_threshold_05[i]) for i in range(len(utils_ratio_003_threshold_05))], [max(utils_ratio_003_threshold_06[i]) for i in range(len(utils_ratio_003_threshold_06))]]
thre_var_util_r004 = [[max(utils_ratio_004_threshold_05[i]) for i in range(len(utils_ratio_004_threshold_05))], [max(utils_ratio_004_threshold_06[i]) for i in range(len(utils_ratio_004_threshold_06))]]

ratio_var_sync_t05 = [syncs_ratio_001_threshold_05, syncs_ratio_002_threshold_05, syncs_ratio_003_threshold_05, syncs_ratio_004_threshold_05]
ratio_var_sync_t06 = [syncs_ratio_001_threshold_06, syncs_ratio_002_threshold_06, syncs_ratio_003_threshold_06, syncs_ratio_004_threshold_06]

thre_var_sync_r001 = [syncs_ratio_001_threshold_05, syncs_ratio_001_threshold_06]
thre_var_sync_r002 = [syncs_ratio_002_threshold_05, syncs_ratio_002_threshold_06]
thre_var_sync_r003 = [syncs_ratio_003_threshold_05, syncs_ratio_003_threshold_06]
thre_var_sync_r004 = [syncs_ratio_004_threshold_05, syncs_ratio_004_threshold_06]



import matplotlib
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter, MultipleLocator
import os
import matplotlib.pylab as pylab

from matplotlib.ticker import FormatStrFormatter

COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf']

font_size = '12'
params = {
    'axes.labelsize' : font_size,
    'xtick.labelsize' : font_size,
    'ytick.labelsize' : font_size,
    # 'lines.linewidth' : '0.2',
    'legend.fontsize' : font_size,
    'figure.figsize' : '4, 2.8',
}
pylab.rcParams.update(params)




def plot_bar(data, xticks, xlabel, ylabel, filename):

    plt.close('all')
    plt.figure()

    x_pos = np.arange(1, len(data) + 1)
    xticks = x_pos
    # for i in range(len(data)):
    plt.bar(x_pos, data, color=COLORS[0])

    
    # plt.xticks(x_pos, xticks)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout(True)

    filename = filename
    
    plt.savefig('{}.pdf'.format(filename), format='pdf', dpi=900)
    # plt.show()

# ratio001 thresh05 06
plot_bar(np.multiply(thre_var_util_r001[0], 100.0), '', 'Epoch', 'Maximum link utilization (\%)', 'thre_05_util_r001')
plot_bar(np.multiply(thre_var_util_r001[1], 100.0), '', 'Epoch', 'Maximum link utilization (\%)', 'thre_06_util_r001')

# ratio002 thresh05 06
plot_bar(np.multiply(thre_var_util_r002[0], 100.0), '', 'Epoch', 'Maximum link utilization (\%)', 'thre_05_util_r002')
plot_bar(np.multiply(thre_var_util_r002[1], 100.0), '', 'Epoch', 'Maximum link utilization (\%)', 'thre_06_util_r002')

# ratio003 thresh05 06
plot_bar(np.multiply(thre_var_util_r003[0], 100.0), '', 'Epoch', 'Maximum link utilization (\%)', 'thre_05_util_r003')
plot_bar(np.multiply(thre_var_util_r003[1], 100.0), '', 'Epoch', 'Maximum link utilization (\%)', 'thre_06_util_r003')

# ratio004 thresh05 06
plot_bar(np.multiply(thre_var_util_r004[0], 100.0), '', 'Epoch', 'Maximum link utilization (\%)', 'thre_05_util_r004')
plot_bar(np.multiply(thre_var_util_r004[1], 100.0), '', 'Epoch', 'Maximum link utilization (\%)', 'thre_06_util_r004')
