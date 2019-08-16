#!/usr/local/bin/python3

from box_plot import plot_box

# 1op data
# u1op_ratio_001_threshold_05=[[], [], [], [0.5505624284584748, 0.4895328839544929, 0.542598557901768], [0.4895328839544929, 0.48723437174841283], [0.6442395123152432, 0.6239438972421628], [0.4421720820957011], [0.5385111643173484, 0.573658857866843], [], [], [0.48937798891886675, 0.48141477210259914, 0.5657701088482815], [0.49448503316153597, 0.5152263835909945, 0.5720314342367797], [0.6247821307642207], [], [0.4647310947322637], [0.5330530132023218, 0.4987920957963322], [0.5210427935823102, 0.4656982551945019, 0.5755714497105469], [0.500423977093172], [0.44945591234298377], [0.6148017079560663]]
# u1op_ratio_001_threshold_06=[[], [], [], [0.516107058376455, 0.5317478317962525], [0.5894240163218587, 0.693199856470007], [0.7272041331179229, 0.5770492007044351, 0.5934541598621973], [0.6734691041299108, 0.7391551306834607], [], [0.5769730465023726], [0.7354078044122754], [0.6666940569918566], [], [0.5688648497961006, 0.6446774935890054], [0.6227761981277646, 0.5970718715909376], [0.7491545451200425], [0.6022233934546675], [], [], [0.5870633715948229, 0.5963840637724895], [0.6128153313944904, 0.7874783040351836, 0.7429900806293177]]
# u1op_ratio_002_threshold_05=[[], [0.5536514293843928, 0.47920287538105855, 0.6065544414091266], [0.6543317498067839, 0.6348570567780799], [0.686174751585242, 0.6852904481171896], [], [0.607862500184327, 0.5528120629517301, 0.6540627979261012, 0.6171308846003053], [], [0.6323887645452063, 0.7115022280816152], [0.5071206590110483, 0.6097723918160314], [0.5659731756629012, 0.707247815446935], [], [0.6153776592485122, 0.5480942834455995, 0.6536182385614386, 0.6308310725674171], [], [0.5267212769451919, 0.627950728316566], [0.5004775191754459, 0.6552302697836063], [0.5429263095866651, 0.7347638716344597], [], [0.5612081138524645, 0.532058089976386, 0.715804370125688, 0.6491035433357931], [], [0.5017241408494395, 0.6747078374386387]]
# u1op_ratio_002_threshold_06=[[], [0.47513145673233403, 0.6052495236068243], [0.6514745472897248, 0.5922108548069347, 0.650785068946773], [0.7406293461530404, 0.7424559175550296], [], [0.7031615701950729, 0.7450500631398531, 0.6703976013043852], [0.5812113842886102], [0.8346181566131949, 0.7005342655178449], [0.6955014983973495, 0.6520130811387495], [0.7221625500216847], [0.5949874039915486], [0.732210735736867, 0.644846728568339, 0.7259330771031909, 0.578024906968368], [0.7611358083552832], [0.5994321008191236], [0.6708442149418712, 0.5682654310631168, 0.8598964574509214], [0.8075167257575966, 0.7005068111074552], [0.6964097834487495], [0.7286579122765678], [0.566377629983883, 0.6538001160398845, 0.680622369974499], [0.8316015493401197]]
# u1op_ratio_003_threshold_05=[[0.6300446381148882], [0.6600453879425963, 0.9520465415814091, 0.5695302226362909], [0.6505715893151397, 0.7030870442527125], [0.7536385966173551, 0.6660705478020436, 0.6693612549395829], [0.7223948157163167, 0.6731023451775597], [0.7224195011779018, 0.6307904508994712, 0.7741940978181295], [0.588555873865641, 0.6337812540842319, 0.6484792134839215], [0.7041296831474546, 0.7594478749638455], [0.7094002182073951, 0.6702372809384809], [0.907205158386958, 0.6758531393835066], [0.7315522770569992, 0.6832696710194355, 0.5619629159570438], [0.5986705020968598, 0.7323314229692097], [0.6916193358324276, 0.6769166872064392, 0.5013258038345693], [0.5890814116683537, 0.6894117844453336], [0.6349425109271504, 0.57138286530411, 0.5495242775760715], [0.6473563249944256, 0.5863701009251637], [0.7132876413010807, 0.611308880123168, 0.6412346457217631], [0.6470554200090906, 0.740039353232541], [0.7178175920882519, 0.6795493014516535, 0.5505748734610104], [0.6699335863294014]]
# u1op_ratio_003_threshold_06=[[], [0.7500081639233229, 0.646456954888382, 0.9853594223396329, 0.7496047048977877], [], [0.7781068164396409, 0.5595367236502526, 1.0047035484045121, 0.7768643310051774], [0.941393894994198, 0.7833026121280101], [0.7145051953667011, 0.739964228725942], [0.6818440494136201, 1.070033254072567], [0.6557846646245823, 0.6591692202440236], [0.7037532605621544, 1.1285877615229385], [0.769835208218628, 0.7091271880496226, 0.6510663388558159], [0.7039852988571202], [0.7418970751631196, 1.087176165272841, 0.6885455449823116], [0.5800808411094929, 0.6602490817968343], [0.758950400623636, 0.9479756283634936, 0.7162258383741328], [1.0817834007409055], [0.7528595386138447, 0.6098837969766702], [0.7971855656387569, 1.1526366467003426], [0.7110646962577085, 0.7027000632228766, 0.8026645964294843], [0.5984385822711441, 0.651994304989377], [0.7218526464874008, 0.9480576302004144, 0.7295319831298265]]
# u1op_ratio_004_threshold_05=[[0.5689729875866332, 0.7573703146156784, 0.7625739160468092], [0.7077115370463349, 0.8967145745718836, 0.7415148694993887], [0.7809156210411484, 0.805387832768753, 0.9261796463333446], [0.6857973909145116, 0.6435508426676224, 0.8092148934923967], [0.6865591477582165, 0.8271051759395242, 0.7414351984725552], [0.6586726175745938, 0.6093162831727161, 0.9255965317975028, 0.9059445729632079], [0.7399555630597225, 0.7298379953447615], [0.7980351277176817, 0.8365382511786246, 0.841989230003548, 0.8901266921710284], [0.7159106339912237, 0.5869015134320831, 0.8655578570960722], [0.5721555401036196, 0.8720033023948257, 0.901712459349483], [0.7247294590141562, 0.8726267900778354, 0.9318001668511251], [0.6865557414022945, 0.8593694669204445, 0.8286007267799473], [0.732450207714822, 0.8419606013425297, 1.1229590144309591], [0.5628829957554057, 0.6756885385114529, 0.9716693046629714, 0.8135104714265393], [0.734173766146482, 0.7740240402513331], [0.7153985465036116, 0.9217869333606407, 0.8960509176279213, 0.8082481676006131], [0.7170686769072989, 0.7915485819971352], [0.9165451514692342, 0.8242702577246989, 0.9329394590316277, 0.8578281841235703], [0.5815869299375915, 0.8138751848285632], [0.5334090906508577, 0.8136717379070801, 0.8698755307432718, 0.8568949490212769]]
# u1op_ratio_004_threshold_06=[[0.5995452490735786, 0.7511706075949658, 0.8397598241861495], [1.1780044375363203, 0.9177219179352494, 0.8841053669027535], [0.7837845660618029, 0.7169062839805168, 0.8946509155857362], [0.7633611248464308, 0.8339273067646673], [0.9356753592522894, 0.7392305408862732, 0.7170354036916744], [0.8477537848946893, 0.8289458284662893], [0.9563562071840483, 0.620377583094416, 0.8636228351049874], [0.6813833973282758, 0.871779552181219], [0.9732235635280602, 0.8316530361386586, 0.690813093731604], [0.8358380380744558, 0.7069275850394992, 0.9134990764991977], [0.7859480110391338, 0.9005559500459459], [0.9290125789573638, 0.8883875218039001, 0.9155193379283308], [0.8851839981220668, 0.8151850571194686], [0.9591539453971599, 0.8548560266295748, 0.8701910333362188], [0.7059715130830243, 0.6717679645395253, 0.8563040402706467], [0.8805524938437155, 0.7683696751937167], [0.9335989772906067, 0.6875071565130016, 0.7664045634415504], [0.8426136265668208], [0.9071804711891039, 0.8926232401536083, 1.163158183146741], [0.9597478545712698, 0.8115142128231592]]


# 2op data
u2op_ratio_001_threshold_05=[[], [], [], [0.4469935626373997, 0.4604244963205995, 0.5544879624415917], [0.5945195301788582, 0.5381019014693436], [0.6109032293385904], [0.43666707116623155], [0.6197748743706257], [0.4813703607110508], [0.6552412757258739, 0.49212657390722214], [0.47260909318988636, 0.42361436046813983, 0.5965000039111349], [0.5674885507646182, 0.581768269850916], [], [0.5021211551676945], [0.44034797982424234], [0.5847177161468043, 0.5438438220391326], [0.46658932655316676], [0.4865792968490553, 0.5734387833732925], [0.5852714027429644, 0.4979679766853712], [0.5690193769221794]]
u2op_ratio_001_threshold_06=[[], [], [], [0.4956916816821558, 0.5196285089329966], [0.5888485231503627, 0.7771820335206002], [0.7379691628289091, 0.6409489063853759, 0.5879369895514698], [0.707835161579117], [], [0.5019116682236096], [0.5172935572144113, 0.6510599054547523], [0.6324556749106679], [0.5708602991867736], [0.6626451464018557, 0.6133409883496392], [0.5640490094391891], [0.7593532695687664], [0.5884236261973774], [0.7553813089225312], [], [0.591021236619552, 0.540793615566737, 0.583866134372802], [0.6988744120190367, 0.7725814747708987, 0.712280573405152]]
u2op_ratio_002_threshold_05=[[], [0.4346287259289039, 0.5859122850393249], [0.6754084575700361, 0.65530870091774, 0.582846936816755], [0.6003598968128431], [0.4735901480984461], [0.7226647592514583, 0.4695442039177481, 0.6357768156598249, 0.6263121822485772], [0.7580315091269364], [0.48301430552559077, 0.6158206489668566], [0.7820066198757875, 0.666970558736005], [0.559855265027327, 0.6110452603713431], [0.4677473179825251], [0.6806612331740353, 0.647569153411164, 0.6369227639696811], [0.5894612893331049], [0.5610262009377616, 0.6134677327876712], [0.6826567189885395], [0.4751545864585587, 0.5980883109941325, 0.5549514044180348], [0.7497526531595214], [0.6267433900701134, 0.5901165034455516], [0.47012098332601676, 0.5436235835347473], [0.653967764029911, 0.6581028723581646]]
u2op_ratio_002_threshold_06=[[], [0.4156932892328244, 0.5352802940164207], [0.6920046419540073, 0.6784565623009376, 0.6808227380186157, 0.6643612935193118], [], [0.5643831644020623], [0.8022937863434014, 0.5153236737205916, 0.7216094232941532, 0.6328217892505815], [0.6934856226445022], [0.5923154896084758], [0.7268670670958042, 0.9107875376731217, 0.706214582840031], [0.5234600890947675], [0.7124589958690806, 0.6630259898878788], [0.706063504378158, 0.5842963056954863], [0.5573622438450182, 0.8376569344063228], [0.5203034531776378, 0.8253118009494299], [0.7298186452902947, 0.7525186341912904], [0.5270179848330877, 0.5978312459840758], [0.9001615988521949, 0.8610591119368063], [0.7284193374963601, 0.5548513628404735], [0.7099413334875226, 0.6100925257423115], [0.6782347469301324]]
u2op_ratio_003_threshold_05=[[0.5698331315699613], [0.7400740392652447, 0.9385872378246949, 0.5908633623825386], [0.6160686423910949, 0.6879866657685582], [0.8006459274015518, 0.5242799255293882, 0.6892614844649583], [0.6088467159436168, 0.4227955790301496], [0.8636771931430374, 0.8394616600544852, 0.6252643184332914], [0.6120444229279501, 0.6162544123166788], [0.6869545872615271, 0.48700815018940635, 0.6112211267346813], [0.6000586873539223, 0.8162725287215308], [0.7408704770451425, 0.5552745951341257, 0.6557963201732872], [0.5945299926488273, 0.5105194224653702], [0.8965172765160806, 0.5061248090576338, 0.5613921130332094], [0.6761562658023931, 0.48510079046596544], [0.7519726326248048, 0.8305233997050073, 0.6197737913987488], [0.557563466264196, 0.5426563614954475], [0.6536222307913587, 0.5223190177342555, 0.6380389896516604], [0.5997882675849096, 0.5372002893947859, 0.5834063713064839], [0.4479760798033094, 0.5764033286065144, 0.6742837885933015], [0.7079253164527948, 0.6059946549366387, 0.5266072862460438], [0.49333684803182043, 0.5020208584912326, 0.7497139263042119]]
u2op_ratio_003_threshold_06=[[0.5376462803779498], [0.7387743890404257, 0.7427779162838638, 0.8627692519935194, 0.6723629413107806], [], [0.7614131969967481, 0.6192033613523539, 0.8687134640297858, 0.7401217207266478], [], [0.7100978329448596, 0.6257979958469706, 0.8902858497406709, 0.7647467308544417], [], [0.7388932858406027, 0.5923941553414098, 0.7986034791932541, 0.7126979585691382], [0.8288428041595993], [0.6443148833414688, 0.9397772293217624, 0.6657314821438586], [0.5251869879927261, 0.5905750478408472], [0.7503075097795553, 0.9669849819012426, 0.9621519368735288, 0.6476031973078126], [], [0.7368288105243993, 0.4903552692542164, 0.9449554818482758, 0.6665641953128422], [0.9374495488381674, 0.5976822060126769], [0.7392802287656121, 0.8481317782603295, 0.6689501723139116], [0.5691933424068297, 0.5739893664849894], [0.7260296354960537, 0.8491244014754054, 0.8697560930064083, 0.6462857488359584], [], [0.8389778414191474, 0.6306137348711301, 0.9664858473907897, 0.6501644934365668]]
u2op_ratio_004_threshold_05=[[0.6095271438920432, 0.7326160928365757, 0.5440006026045928], [0.5357017415784192, 0.48763956673932685, 0.6797447395869111, 0.7189375809199745], [0.6712003672446317, 0.729952632112733, 0.7060904219251019, 0.5774059100922496], [0.687426655598, 0.7223025739923594], [0.5044422751958277, 0.8069631206540907, 0.7203124688382988, 0.821243462731854], [0.5120342368945804, 0.6744732406300659, 0.5464855431928887], [0.5155160461266886, 0.8414121363429833, 0.5641801460260287], [0.6427226769682927, 0.567635376774155, 0.6512154977134338, 0.8376742321198308], [0.5631423494366637, 0.6827445015240092, 0.5844860401820628], [0.526812567510967, 0.841069058153686, 0.7140643252668155], [0.5078113435182532, 0.6443279746331393, 0.8677777516453217], [0.6084412262201249, 0.6668018911138465, 0.5806845573080913], [0.5191525439509671, 0.6442778733902924, 0.7770639879917408], [0.5391216462862048, 0.7084033331440488, 0.7750284559054251], [0.7205334532689692, 0.8163586419116261], [1.1615033506924113, 0.8982714726662893, 0.651526932149496], [0.6469176663406052, 0.7222988601120138, 1.0232096950604022], [0.6178805450238603, 0.9126494563268079, 0.749684567049847], [0.4857883009539654, 0.7398727062951684, 1.0014987364217862], [0.9032965049057623, 0.8375407934502741, 0.60277950270653]]
u2op_ratio_004_threshold_06=[[0.6737411560262839, 0.694220629422901], [0.963023662591025, 0.6654625863532472, 0.8271781584449327], [0.570370573328162, 0.7377912026939218, 0.5795406145747727], [0.9905148860903079, 1.0372175785839561, 0.9939173026997706], [0.5522800504225721, 0.7621470805690191, 0.7203280460316386], [0.9942569555156932, 0.5779347576682484, 0.901668014712864], [0.7863976225921206, 1.0775570559773537], [0.9808335071100215, 0.757223262905645, 0.8985175851710951], [0.6246765844462445, 0.690483315655968, 0.6978191446391823], [0.6054222669492854, 0.8637045362596864], [0.953771032772129, 0.8853035283370432, 0.7500121055707983], [0.6516482991169203, 0.8648133928789008], [0.9483844450424521, 0.7720325791218691, 0.6837420235513396], [0.5834354707120026, 0.6595473890893032, 0.8577580636108653], [0.9056294096075976, 0.8409169255553934, 0.5811018523462422], [1.101463565939232, 0.8229898968754429], [0.9015507018478809, 0.910252705529841, 0.6574324442892916], [0.5772509488783597, 0.6431348853420333, 0.8646446253532938], [1.1156179581237935, 0.9394436705383771, 0.6276589951521924], [0.7637599832957657, 0.9724956070128133]]


# 1 op times data
u1optimes_ratio_001_threshold_05=[0, 0, 0, 3, 2, 1, 1, 1, 1, 2, 3, 2, 0, 1, 1, 2, 1, 2, 2, 1]
u1optimes_ratio_001_threshold_06=[0, 0, 0, 2, 2, 3, 1, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 0, 3, 3]
u1optimes_ratio_002_threshold_05=[0, 2, 3, 1, 1, 4, 1, 2, 2, 2, 1, 3, 1, 2, 1, 3, 1, 2, 2, 2]
u1optimes_ratio_002_threshold_06=[0, 2, 4, 0, 1, 4, 1, 1, 3, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
u1optimes_ratio_003_threshold_05=[1, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 3, 3, 3, 3]
u1optimes_ratio_003_threshold_06=[1, 4, 0, 4, 0, 4, 0, 4, 1, 3, 2, 4, 0, 4, 2, 3, 2, 4, 0, 4]
u1optimes_ratio_004_threshold_05=[3, 4, 4, 2, 4, 3, 3, 4, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3]
u1optimes_ratio_004_threshold_06=[2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2]

# compose data
# 1op times
# cmp_1opdata = [u1op_ratio_003_threshold_05, u1op_ratio_004_threshold_05, u1op_ratio_003_threshold_06, u1op_ratio_004_threshold_06]
# t1opdata = []
# for i in range(len(cmp_1opdata)):
#     tmp = []
#     for j in cmp_1opdata[i]:
#         tmp.append(len(j))
#     # data.append(sum(tmp))
#     t1opdata.append(tmp)
t1opdata = [u1optimes_ratio_003_threshold_05, u1optimes_ratio_004_threshold_05, u1optimes_ratio_003_threshold_06, u1optimes_ratio_004_threshold_06]

# 2op times
cmp_2opdata = [u2op_ratio_003_threshold_05, u2op_ratio_004_threshold_05, u2op_ratio_003_threshold_06, u2op_ratio_004_threshold_06]
t2opdata = []
for i in range(len(cmp_2opdata)):
    tmp = []
    for j in cmp_2opdata[i]:
        tmp.append(len(j))
    # data.append(sum(tmp))
    t2opdata.append(tmp)








# threshold 5 ratio variable
plot_box(t1opdata, ['R0.03T0.5', 'R0.04T0.5', 'R0.03T0.6', 'R0.04T0.6'], '', 'Times of first optimalization', '1opcmp_35_45_36_46')

# 2op times
plot_box(t2opdata, ['R0.03T0.5', 'R0.04T0.5', 'R0.03T0.6', 'R0.04T0.6'], '', 'Times of first optimalization', '2opcmp_35_45_36_46')

