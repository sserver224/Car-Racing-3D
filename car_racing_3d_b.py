import math
import time
from XInput import *
import engine
from engine.events import *
from engine.operators import *
from engine.types import *
from elm import *
from elm import plugins
emulator=elm.Elm()
emulator.net_port=35000
emulator.scenario='car'
r=Thread(target=emulator.run)
r.daemon=True
r.start()
emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * 0)</exec><writeln />'
emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int(4 * 0)</exec><writeln />'
set_deadzone(DEADZONE_TRIGGER, 1)
@sprite('Stage')
class Stage(Target):
    """Sprite Stage"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = 0
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "None", [
            {
                'name': "backdrop1",
                'path': "0c4f8f7ed52426227d3b74fb2c25d29c.png",
                'center': (480, 360),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_horizon_x = 0
        self.var_speed = 0
        self.var_car_x = 0
        self.var_road_ang = 0
        self.var_car_sx = 0
        self.var_MPH = 0
        self.var_SOUND_TICK = 0
        self.var_SOUND_ID = 0
        self.var_SOUND_ = 0
        self.var_IsAccellerating = 0
        self.var_tick = 1326
        self.var_car_slide = 0
        self.var_LapTime = "00:00.00"
        self.var_LastLap = ""
        self.var_RPM = 750
        self.var_GEAR = 1
        self.var_MaxRpm = 7500
        self.var_KMH = 0
        self.var_CHANGE = 0
        self.var_ON = 1
        self.var_DMODE = 2
        self.var_Gearbox = 0
        self.var_steering = 0

        self.list_Grass1 = List(
            [-178, -178, -174, -174, -170, -170, -166, -166, -162, -162, -158, -158, -154, -154, -150, -150, -146, -146, -142, -142, -138, -138, -134, -134, -130, -130, -126, -126, -122, -122, -18, -18, -14, -14, -10, -10, -6, -6, -2, -2, 2, 2, 6, 6, 10, 10, 30, 30, 34, 34, 38, 38, 50, 50]
        )
        self.list_Grass2 = List(
            [-118, -118, -114, -114, -110, -110, -106, -106, -102, -102, -98, -98, -94, -94, -90, -90, -86, -86, -82, -82, -78, -78, -74, -74, -70, -70, -66, -66, -62, -62, -58, -58, -54, -54, -50, -50, -46, -46, -42, -42, -38, -38, -34, -34, -30, -30, -26, -26, -22, -22, 14, 14, 18, 18, 22, 22, 26, 26, 42, 42, 46, 46, 54, 54, 58, 58]
        )
        self.list_Grass1X = List(
            [-549.5999999999999, 549.5999999999999, -544.8, 544.8, -540, 540, -535.2, 535.2, -530.4, 530.4, -525.6, 525.6, -520.8, 520.8, -516, 516, -511.2, 511.2, -506.4, 506.4, -501.59999999999997, 501.59999999999997, -496.79999999999995, 496.79999999999995, -492.00000000000006, 492.00000000000006, -487.2, 487.2, -482.4, 482.4, -357.6, 357.6, -352.8, 352.8, -348, 348, -343.2, 343.2, -338.4, 338.4, -333.6, 333.6, -328.8, 328.8, -324, 324, -300, 300, -295.2, 295.2, -290.4, 290.4, -276, 276]
        )
        self.list_Grass2X = List(
            [-477.6, 477.6, -472.8, 472.8, -468, 468, -463.20000000000005, 463.20000000000005, -458.4, 458.4, -453.6, 453.6, -448.8, 448.8, -444, 444, -439.2, 439.2, -434.4, 434.4, -429.6, 429.6, -424.8, 424.8, -420, 420, -415.20000000000005, 415.20000000000005, -410.4, 410.4, -405.6, 405.6, -400.79999999999995, 400.79999999999995, -396, 396, -391.2, 391.2, -386.4, 386.4, -381.6, 381.6, -376.8, 376.8, -372, 372, -367.2, 367.2, -362.4, 362.4, -319.20000000000005, 319.20000000000005, -314.4, 314.4, -309.6, 309.6, -304.8, 304.8, -285.6, 285.6, -280.8, 280.8, -271.2, 271.2, -266.4, 266.4]
        )
        self.list_CarsX = List(
            [112]
        )
        self.list_CarsY = List(
            [1518]
        )
        self.list_CarsPX = List(
            [24.639999999999997, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )
        self.list_CarsPY = List(
            [-999, -999, -999, -999, -999, -999, -999, -999, -999, -999]
        )
        self.list_track_x = List(
            [-107, -107, -107, -107, -107, -107, -107, -107, -107, -107, -107, -106.47664043757057, -105.25794700351908, -101.51188106935996, -95.3552663161034, -86.69501227825901, -76.81812887230764, -66.91544818489194, -59.60191116870024, -53.17403507183485, -47.15588484031437, -41.137734608793885, -35.119584377273405, -28.96296962401682, -22.80635487076024, -16.649740117503654, -10.49312536424707, -4.474975132726589, 1.543175098793892, 7.561325330314373, 13.579475561834856, 19.597625793355338, 25.615776024875817, 31.633926256396293, 37.65207648791677, 43.67022671943725, 49.68837695095773, 55.70652718247821, 61.29845621718568, 65.20576750207842, 65.90333223951967, 64.33898758911737, 62.08947704567872, 58.02211061492072, 52.43018158021325, 45.73887551662467, 37.16720250960354, 27.96215397507914, 18.30289571218846, 8.340948731271004, -1.6346917713272386, -10.021397450781482, -13.767463384940603, -14.116458351965614, -13.941934287592783, -13.767410223219953, -13.592886158847122, -13.418362094474292, -13.24383803010146, -13.06931396572863, -12.8947899013558, -12.72026583698297, -12.54574177261014, -14.282223549279452, -17.86590304473246, -24.02251779798905, -32.50299875955331, -42.28447476689136, -52.27838303708232, -61.188448278966, -68.00843187959099, -70.93214892681836, -70.93214892681836, -70.75762486244552, -70.58310079807269, -70.40857673369986, -70.23405266932703, -70.0595286049542, -69.88500454058136, -69.71048047620853, -69.5359564118357, -69.36143234746287, -69.18690828309003, -69.0123842187172, -68.48902465628777, -66.75254287961846, -63.332341446361774, -57.59657708285131, -49.8251174682816, -40.68966289185559, -30.908186884517537, -21.03130347856616, -11.03130347856616, -1.0313034785661586, 8.894158037847061, 18.597115300607022, 27.93291956557904, 37.06837414200505, 45.89785007059432, 54.644047141988274, 63.30430117983266, 71.59467690538308, 79.78619734827299, 87.5576569628427, 96.69311153926871, 106.61857305568194, 114.81009349857186, 118.55615943273098, 116.64806947896554, 112.26435801107476, 104.83290975630082, 99.09714539279037, 101.17626230096796, 105.87097792882687, 109.45465742427989, 107.37554051610228, 99.94409226132834, 92.06398472526112, 84.18387718919391, 76.3037696531267, 68.42366211705948, 60.54355458099226, 52.66344704492504, 44.783339508857814, 36.90323197279059, 29.02312443672337, 21.14301690065615, 13.262909364588928, 5.382801828521707, -2.4973057075455145, -10.377413243612736, -18.363768344085663, -27.024022381930045, -36.90090578788142, -46.60386305064139, -55.08434401220565, -58.830409946364774, -59.00493401073762, -53.558543660587354, -46.01144785835963, -38.13134032229242, -30.2512327862252, -22.371125250157988, -14.491017714090772, -6.610910178023559, 1.2691973580436553, 9.14930489411087, 15.70989518401594, 18.46626874218593, 15.376098798436455, 6.240644222010449, -3.7349962805877936, -13.710636783186036, -23.68627728578428, -33.661917788382524, -43.63755829098076, -53.485635821102846, -63.098252780486035, -72.30330131501044, -80.49482175790035, -87.31480535852533, -92.9067343932328, -98.05711514233336, -102.44082661022414, -104.86004556622082, -105.38340512865028, -105.73240009567527, -106.08139506270028, -106.43039002972527, -106.7793849967503, -106.95390906112314, -107.128433125496, -107.128433125496, -107.128433125496, -107.128433125496, -107.128433125496]
        )
        self.list_track_y = List(
            [68, 78, 88, 98, 108, 118, 128, 138, 148, 158, 168, 177.9862953475457, 187.91175686395897, 197.1835954096268, 205.063702945694, 210.063702945694, 211.6280475960963, 210.2363165864957, 203.4163329858707, 195.75588855468092, 187.769533454208, 179.78317835373505, 171.79682325326212, 163.9167157171949, 156.0366081811277, 148.15650064506048, 140.27639310899326, 132.29003800852033, 124.3036829080474, 116.31732780757446, 108.33097270710152, 100.3446176066286, 92.35826250615564, 84.37190740568272, 76.38555230520979, 68.39919720473685, 60.41284210426392, 52.42648700379099, 44.13611127824058, 34.931062743716176, 24.955422241117933, 15.078538835166556, 5.334838187314203, -3.800616389111807, -12.090992114662226, -19.52244036943617, -24.672821118536714, -28.580132403429452, -31.168322854454654, -32.03988028193124, -31.34231554448999, -25.89592519433972, -16.62408664867185, -6.630178378480892, 3.3682985730830204, 13.366775524646933, 23.365252476210845, 33.36372942777476, 43.36220637933867, 53.36068333090259, 63.359160282466505, 73.35763723403042, 83.35611418559434, 93.20419171571642, 102.53999598068845, 110.42010351675565, 115.71929615908768, 117.79841306726529, 117.44941810024024, 112.90951310284478, 105.59597608665308, 96.03292852702272, 86.03292852702273, 76.03445157545882, 66.0359746238949, 56.037497672330986, 46.03902072076707, 36.040543769203154, 26.04206681763924, 16.04358986607533, 6.045112914511417, -3.953364037052495, -13.951840988616407, -23.95031794018032, -33.93661328772606, -43.784690817848144, -53.181617025707226, -61.37313746859714, -67.66634137909551, -71.73370780985351, -73.81282471803111, -75.37716936843341, -75.37716936843341, -75.37716936843341, -74.15847593438194, -71.73925697838526, -68.15557748293226, -64.08821105217426, -59.39349542431535, -54.54539922185197, -49.54539922185197, -43.953470187144504, -38.21770582363404, -31.924501913135664, -27.85713548237766, -29.075828916429135, -34.81159327993959, -44.08343182560746, -53.8997036600841, -62.88764412307577, -69.57895018666436, -77.77047062955428, -87.55194663689234, -96.3814225654816, -105.71722683045364, -115.49870283779168, -122.19000890138028, -128.34662365463686, -134.50323840789343, -140.65985316115, -146.8164679144066, -152.97308266766316, -159.12969742091974, -165.28631217417632, -171.4429269274329, -177.59954168068947, -183.75615643394605, -189.91277118720265, -196.0693859404592, -202.22600069371575, -208.38261544697235, -214.40076567849283, -219.40076567849283, -220.96511032889515, -218.54589137289847, -213.2466987305664, -203.97486018489855, -193.97638323333464, -185.5896775538804, -179.02908726397533, -172.87247251071875, -166.71585775746215, -160.5592430042056, -154.40262825094902, -148.24601349769245, -142.08939874443587, -135.9327839911793, -128.38568818895158, -118.7730712295684, -109.26250606661684, -105.19513963585884, -104.4975748984176, -103.80001016097634, -103.10244542353507, -102.40488068609385, -101.70731594865258, -99.97083417198328, -97.21446061381327, -93.30714932892056, -87.5713849654101, -80.2578479492184, -71.96747222366798, -63.395799216646864, -54.40785875365519, -44.704901490895224, -34.71860614334949, -24.724697873158533, -14.730789602967576, -4.736881332776619, 5.257026937414338, 15.25550388897825, 25.25398084054216, 35.25398084054216, 45.25398084054216, 55.25398084054216, 65.25398084054217]
        )
        self.list_track_a = List(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 7, 22, 38, 60, 81, 98, 133, 140, 143, 143, 143, 142, 142, 142, 142, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 146, 157, 176, 189, 193, 204, 214, 222, 239, 247, 255, 265, 274, 303, 338, 358, 361, 361, 361, 361, 361, 361, 361, 361, 361, 350, 339, 322, 302, 282, 268, 243, 223, 197, 180, 179, 179, 179, 179, 179, 179, 179, 179, 179, 179, 179, 177, 170, 160, 145, 129, 114, 102, 99, 90, 90, 83, 76, 69, 66, 62, 61, 60, 56, 55, 51, 66, 97, 125, 158, 191, 206, 228, 215, 168, 152, 159, 192, 228, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 261, 284, 302, 338, 359, 393, 409, 412, 412, 412, 412, 412, 412, 412, 401, 376, 342, 294, 274, 274, 274, 274, 274, 280, 286, 293, 305, 317, 326, 329, 334, 346, 357, 358, 358, 358, 358, 359, 359, 360, 360, 360, 360]
        )
        self.list_track_sx = List(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 15, 15, 22, 22, 22, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 15, 15, 15, 10, 10, 10, 10, 8, 8, 8, 15, 30, 35, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, -11, -11, -20, -20, -20, -20, -20, -20, -20, -20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, -7, -10, -15, -16, -15, -12, -10, -6, -6, -6, -6, -6, -6, -4, -3, -2, -2, -2, -2, 15, 33, 33, 33, 33, 15, 0, -20, -45, -33, 0, 28, 40, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 23, 25, 27, 30, 30, 15, 0, 0, 0, 0, 0, 0, 0, -11, -25, -34, -48, -20, 0, 0, 0, 0, 6, 7, 8, 9, 9, 9, 9, 9, 10, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

        self.sprite.layer = 0




@sprite('Game')
class SpriteGame(Target):
    """Sprite Game"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = -120
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 200, "all around", [
            {
                'name': "red1",
                'path': "11cc2ed9a8813dbccee85c82a69eade4.png",
                'center': (34, 49),
                'scale': 2
            },
            {
                'name': "red2",
                'path': "ef4eb6c99d144e6c45b1c53cfcdec01e.png",
                'center': (37, 49),
                'scale': 2
            },
            {
                'name': "red3",
                'path': "205390231a9ae8f0b29f41572c0b87ef.png",
                'center': (42, 49),
                'scale': 2
            },
            {
                'name': "red4",
                'path': "ead4cadfbbafcb594f11158bb0683824.png",
                'center': (46, 49),
                'scale': 2
            },
            {
                'name': "red5",
                'path': "056a876515a57dd585dd1b86f32534aa.png",
                'center': (64, 48),
                'scale': 2
            },
            {
                'name': "red6",
                'path': "722e23c53f4c4a1c7d6b5864953c2154.png",
                'center': (82, 50),
                'scale': 2
            },
            {
                'name': "red7",
                'path': "d93eb02a226d3cf547332b38630a5953.png",
                'center': (76, 50),
                'scale': 2
            },
            {
                'name': "red8",
                'path': "618dde7a35f15d55c4096644590572ea.png",
                'center': (64, 52),
                'scale': 2
            },
            {
                'name': "red9",
                'path': "e214d7e1546dab7ec6bf784f71809c84.png",
                'center': (48, 51),
                'scale': 2
            },
            {
                'name': "red10",
                'path': "c5fa1ec7a21d17a1292a3f24edb7eb29.png",
                'center': (41, 50),
                'scale': 2
            },
            {
                'name': "red11",
                'path': "580fa326e6c7a408474b84968195512a.png",
                'center': (40, 50),
                'scale': 2
            },
            {
                'name': "red12",
                'path': "c4fde8db8a7ffc273899e98a1827138a.png",
                'center': (36, 48),
                'scale': 2
            },
            {
                'name': "red13",
                'path': "db564c5ca44c71bb4b922d0470811a65.png",
                'center': (36, 48),
                'scale': 2
            },
            {
                'name': "red14",
                'path': "c89da2eab3f03af0f75e1dd3767c6d73.png",
                'center': (40, 48),
                'scale': 2
            },
            {
                'name': "red15",
                'path': "77a366ed7321b587899aa3dbac008743.png",
                'center': (47, 50),
                'scale': 2
            },
            {
                'name': "red16",
                'path': "64dac25e8a89ea1599010a3e3bf2bcf1.png",
                'center': (53, 50),
                'scale': 2
            },
            {
                'name': "red17",
                'path': "7a054fa91dc9804b0acd21e206e90492.png",
                'center': (73, 52),
                'scale': 2
            },
            {
                'name': "red18",
                'path': "3e91795165d382dc87a69cb53ff97a6c.png",
                'center': (88, 51),
                'scale': 2
            },
            {
                'name': "red19",
                'path': "bf69af3e887494737aa419ac5e498379.png",
                'center': (86, 50),
                'scale': 2
            },
            {
                'name': "red20",
                'path': "836bc0cab6c4a6255b742cb0c63e8edf.png",
                'center': (71, 51),
                'scale': 2
            },
            {
                'name': "red21",
                'path': "497cc94ab39b6bbe7bda69021e805472.png",
                'center': (56, 48),
                'scale': 2
            },
            {
                'name': "red22",
                'path': "f7a31ee8a14bedeec4ce61c59b3b5d32.png",
                'center': (47, 49),
                'scale': 2
            },
            {
                'name': "red23",
                'path': "e953e19acdaad7ec999c462083e6f97c.png",
                'center': (43, 49),
                'scale': 2
            },
            {
                'name': "red24",
                'path': "f2cbd2f6f5251c3b9542605bfb3834b7.png",
                'center': (40, 49),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "acc1",
                'path': "490c6e05e5d75f9d57fe1e1b49f371eb.wav"
            },
            {
                'name': "acc2",
                'path': "bc17de5e29d83a3d929541f45372c32a.wav"
            },
            {
                'name': "acc3",
                'path': "ccae7ec5458f6cb504a97b52e432b854.wav"
            }
        ])

        self.var_y = 0
        self.var_i = 0
        self.var_psp = 846.8444444444442
        self.var_yy = 62
        self.var_z = 454.54545454545456
        self.var_x1 = -266.4
        self.var_x2 = 266.4
        self.var_t = 0
        self.var_road_target = 0
        self.var_road_time = 90
        self.var_nextCarY = 1518
        self.var_nextCar = 1
        self.var_debug = -122
        self.var_ecsp = 17.999999999999986
        self.var_ects = 18
        self.var_NextLapY = 70400
        self.var_LapTicks = 0

        self.list_RoadLag = List(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

        self.sprite.layer = 11

    @on_green_flag
    async def green_flag(self, util):
        await self.my_Init(util, )
        self.shown = True
        self.front_layer(util)
        self.gotoxy(0, -120)
        await util.send_broadcast_wait("create clones")
        self.var_y = 0
        util.sprites.stage.var_car_x = 0
        util.sprites.stage.var_car_sx = 0
        self.var_road_time = 90
        util.sprites.stage.var_road_ang = 0
        self.var_road_target = 0
        util.sprites.stage.var_speed = 0
        util.sprites.stage.list_CarsY[toint(self.var_nextCar)] = 20
        self.var_ecsp = 0
        self.var_ects = 18
        util.sprites.stage.var_tick = 0
        self.var_NextLapY = (400 * len(util.sprites.stage.list_track_x))
        while True:
            await self.my_UpdateTimers(util, )
            if util.inputs["p"]:
                while not not util.inputs["p"]:
                    await self.yield_()
                while not util.inputs["p"]:
                    await self.yield_()
                while not not util.inputs["p"]:
                    await self.yield_()
            self.var_y += util.sprites.stage.var_speed
            self.var_i = self.list_RoadLag[1]
            self.list_RoadLag.delete(1)
            self.list_RoadLag.append(util.sprites.stage.var_road_ang)
            util.sprites.stage.var_horizon_x += (util.sprites.stage.var_speed * div(self.var_i, -50))
            util.sprites.stage.var_car_x += (util.sprites.stage.var_speed * div(self.var_i, -75))
            await self.my_Keys(util, )
            util.sprites.stage.var_MPH = toint((util.sprites.stage.var_speed * 7))
            await self.my_UpdateCars(util, )
            await self.my_RoadUpdate(util, )
            await self.my_tick(util, )
            await util.send_broadcast_wait("tick")

            await self.yield_()

    @warp
    async def my_Keys(self, util, ):
        util.sprites.stage.var_car_x += (div(util.sprites.stage.var_speed, 4) * (util.sprites.stage.var_car_sx * div(15, (util.sprites.stage.var_speed + 10))))
        if get_connected()[0]:
            gas=get_trigger_values(get_state(0))[1]
            brake=get_trigger_values(get_state(0))[0]
            if gas>0 and brake==0:
                util.sprites.stage.var_IsAccellerating=gas
            elif brake>0:
                util.sprites.stage.var_IsAccellerating=-1*brake
            else:
                util.sprites.stage.var_IsAccellerating=0
            util.sprites.stage.var_steering=get_thumb_values(get_state(0))[0][0]
        else:
            if util.inputs["down arrow"]:
                util.sprites.stage.var_IsAccellerating = -1
            else:
                if util.inputs["up arrow"]:
                    util.sprites.stage.var_IsAccellerating = 1
                else:
                    util.sprites.stage.var_IsAccellerating = 0
            if (not util.inputs["left arrow"] and util.inputs["right arrow"]):
                util.sprites.stage.var_steering = 1
            else:
                if (not util.inputs["right arrow"] and util.inputs["left arrow"]):
                    util.sprites.stage.var_steering = -1
                else:
                    util.sprites.stage.var_steering = 0
        if gt(abs(util.sprites.stage.var_speed), 0.01):
            if lt(util.sprites.stage.var_steering, 0):
                util.sprites.stage.var_car_sx += (-0.4 * abs(util.sprites.stage.var_steering))
            else:
                if (gt(util.sprites.stage.var_car_slide, 0) and lt(util.sprites.stage.var_car_sx, 0)):
                    util.sprites.stage.var_car_sx += 0.2
            if gt(util.sprites.stage.var_steering, 0):
                util.sprites.stage.var_car_sx += (0.4 * abs(util.sprites.stage.var_steering))
            else:
                if (gt(util.sprites.stage.var_car_slide, 0) and gt(util.sprites.stage.var_car_sx, 0)):
                    util.sprites.stage.var_car_sx += -0.2
        if gt(util.sprites.stage.var_car_slide, 0):
            util.sprites.stage.var_car_sx = (util.sprites.stage.var_car_sx * 0.99)
        else:
            util.sprites.stage.var_car_sx = (util.sprites.stage.var_car_sx * 0.96)
        if lt(util.sprites.stage.var_car_sx, -11):
            util.sprites.stage.var_car_sx = -11
        else:
            if gt(util.sprites.stage.var_car_sx, 11):
                util.sprites.stage.var_car_sx = 11
        await self.my_SetCostume(util, ((toint(div(util.sprites.stage.var_car_sx, 2)) % 24) + 1))
        if gt(util.sprites.stage.var_car_slide, 0):
            if (gt(util.sprites.stage.var_speed, 10) and gt(abs(util.sprites.stage.var_car_sx), 4)):
                util.sprites.stage.var_car_slide = 30
            else:
                util.sprites.stage.var_car_slide += -1
        if lt(util.sprites.stage.var_IsAccellerating, 0):
            util.sprites.stage.var_speed += (-0.27 * abs(util.sprites.stage.var_IsAccellerating))
            util.sprites.stage.var_speed = (util.sprites.stage.var_speed * 0.99)
            if (gt(util.sprites.stage.var_speed, 10) and gt(abs(util.sprites.stage.var_car_sx), 2)):
                util.sprites.stage.var_car_slide = 30
        else:
            if gt(util.sprites.stage.var_IsAccellerating, 0):
                if (eq(util.sprites.stage.var_GEAR, 2) and lt(util.sprites.stage.var_speed, 6)):
                    util.sprites.stage.var_speed += (0.23 * util.sprites.stage.var_IsAccellerating)
                else:
                    if (eq(util.sprites.stage.var_GEAR, 3) and lt(util.sprites.stage.var_speed, 10)):
                        util.sprites.stage.var_speed += (0.22 * util.sprites.stage.var_IsAccellerating)
                    else:
                        if (eq(util.sprites.stage.var_GEAR, 4) and lt(util.sprites.stage.var_speed, 15)):
                            util.sprites.stage.var_speed += (0.22 * util.sprites.stage.var_IsAccellerating)
                        else:
                            if (eq(util.sprites.stage.var_GEAR, 5) and lt(util.sprites.stage.var_speed, 18)):
                                util.sprites.stage.var_speed += (0.22 * util.sprites.stage.var_IsAccellerating)
                            else:
                                if (eq(util.sprites.stage.var_GEAR, 6) and lt(util.sprites.stage.var_speed, 22)):
                                    util.sprites.stage.var_speed += (0.22 * util.sprites.stage.var_IsAccellerating)
                                else:
                                    if (eq(util.sprites.stage.var_GEAR, 7) and lt(util.sprites.stage.var_speed, 25)):
                                        util.sprites.stage.var_speed += (0.22 * util.sprites.stage.var_IsAccellerating)
                                    else:
                                        if (eq(util.sprites.stage.var_GEAR, 8) and lt(util.sprites.stage.var_speed, 29)):
                                            util.sprites.stage.var_speed += (0.22 * util.sprites.stage.var_IsAccellerating)
                util.sprites.stage.var_speed = (util.sprites.stage.var_speed * 0.99)
            else:
                util.sprites.stage.var_speed = (util.sprites.stage.var_speed * 0.995)
        if gt(abs(util.sprites.stage.var_car_x), 106):
            if gt(abs(util.sprites.stage.var_car_x), 132):
                util.sprites.stage.var_speed = (util.sprites.stage.var_speed * 0.98)
            else:
                util.sprites.stage.var_speed = (util.sprites.stage.var_speed * 0.995)

    @warp
    async def my_tick(self, util, ):
        util.sprites.stage.list_Grass1.delete_all()
        util.sprites.stage.list_Grass2.delete_all()
        util.sprites.stage.list_Grass1X.delete_all()
        util.sprites.stage.list_Grass2X.delete_all()
        self.var_i = (util.sprites.stage.var_road_ang * 0.0001)
        self.var_yy = -178
        self.var_nextCar = 1
        util.sprites.stage.list_CarsPY[toint(self.var_nextCar)] = -999
        util.sprites.stage.list_CarsY[toint(self.var_nextCar)] = (tonum(util.sprites.stage.list_CarsY[toint(self.var_nextCar)]) + self.var_ecsp)
        self.var_nextCarY = util.sprites.stage.list_CarsY[toint(self.var_nextCar)]
        for _ in range(60):
            self.var_z = (div(-100, (self.var_yy - 80)) * 100)
            self.var_t = ((tonum(self.var_i) * (self.var_z * self.var_z)) - util.sprites.stage.var_car_x)
            self.var_x1 = (tonum(self.var_t) - 120)
            self.var_x2 = (tonum(self.var_t) + 120)
            self.var_x1 = (div(self.var_x1, div(self.var_z, 100)) - 240)
            self.var_x2 = (div(self.var_x2, div(self.var_z, 100)) + 240)
            if gt((self.var_y + self.var_z), self.var_nextCarY):
                util.sprites.stage.list_CarsPX[toint(self.var_nextCar)] = div((tonum(util.sprites.stage.list_CarsX[toint(self.var_nextCar)]) + tonum(self.var_t)), div(self.var_z, 100))
                util.sprites.stage.list_CarsPY[toint(self.var_nextCar)] = self.var_yy
                self.var_nextCarY = 999999
            if lt(((self.var_z + self.var_y) % 100), 50):
                util.sprites.stage.list_Grass1.append(self.var_yy)
                if gt(self.var_x1, 0):
                    util.sprites.stage.list_Grass1X.append(0)
                else:
                    util.sprites.stage.list_Grass1X.append(self.var_x1)
                util.sprites.stage.list_Grass1.append(self.var_yy)
                if lt(self.var_x2, 0):
                    util.sprites.stage.list_Grass1X.append(0)
                else:
                    util.sprites.stage.list_Grass1X.append(self.var_x2)
            else:
                util.sprites.stage.list_Grass2.append(self.var_yy)
                if gt(self.var_x1, 0):
                    util.sprites.stage.list_Grass2X.append(0)
                else:
                    util.sprites.stage.list_Grass2X.append(self.var_x1)
                util.sprites.stage.list_Grass2.append(self.var_yy)
                if lt(self.var_x2, 0):
                    util.sprites.stage.list_Grass2X.append(0)
                else:
                    util.sprites.stage.list_Grass2X.append(self.var_x2)
            self.var_yy += 4

    @warp
    async def my_RoadUpdate(self, util, ):
        self.var_road_target = (3 * tonum(util.sprites.stage.list_track_sx[toint(((math.floor(div(self.var_y, 400)) % len(util.sprites.stage.list_track_sx)) + 1))]))
        self.var_t = (3 * tonum(util.sprites.stage.list_track_sx[toint((((math.floor(div(self.var_y, 400)) + 1) % len(util.sprites.stage.list_track_sx)) + 1))]))
        self.var_t = (tonum(self.var_t) - self.var_road_target)
        util.sprites.stage.var_road_ang = (self.var_road_target + ((div(self.var_y, 400) % 1) * tonum(self.var_t)))

    @warp
    async def my_UpdateCars(self, util, ):
        self.var_t = util.sprites.stage.list_CarsY[1]
        if lt(self.var_t, (self.var_y - 600)):
            self.var_ects = pick_rand(10, 21.5)
            self.var_ecsp = pick_rand(10, 21)
            self.var_t = (self.var_y + pick_rand(400, 1500))
            util.sprites.stage.list_CarsY[1] = self.var_t
            util.sprites.stage.list_CarsX[1] = pick_rand(-120, 120)
        else:
            if gt(self.var_t, (self.var_y + 1500)):
                util.sprites.stage.list_CarsY[1] = (self.var_y + 1500)
            else:
                pass
        if lt(self.var_ecsp, self.var_ects):
            self.var_ecsp += 0.1
        else:
            if gt(self.var_ecsp, self.var_ects):
                self.var_ecsp += -0.1
            else:
                pass

    @warp
    async def my_UpdateTimers(self, util, ):
        util.sprites.stage.var_tick += 1
        if eq(self.var_LapTicks, ""):
            if not eq(self.var_y, 0):
                self.var_LapTicks = 1
        else:
            self.var_LapTicks += 1
            util.sprites.stage.var_LapTime = ""
            self.var_i = self.var_LapTicks
            await self.my_AppendTime(util, math.floor((div((tonum(self.var_i) % 30), 30) * 100)), "")
            self.var_i = math.floor(div(self.var_i, 30))
            await self.my_AppendTime(util, (tonum(self.var_i) % 60), ".")
            self.var_i = math.floor(div(self.var_i, 60))
            await self.my_AppendTime(util, self.var_i, ":")
            if gt(self.var_y, self.var_NextLapY):
                util.sprites.stage.var_LastLap = util.sprites.stage.var_LapTime
                self.var_NextLapY += (400 * len(util.sprites.stage.list_track_x))
                self.var_LapTicks = 1
                print(util.sprites.stage.var_LastLap)

    @warp
    async def my_AppendTime(self, util, arg_num, arg_sep):
        if lt(arg_num, 10):
            util.sprites.stage.var_LapTime = (("0" + str(arg_num)) + (arg_sep + util.sprites.stage.var_LapTime))
        else:
            util.sprites.stage.var_LapTime = (str(arg_num) + (arg_sep + util.sprites.stage.var_LapTime))

    @warp
    async def my_SetCostume(self, util, arg_costume):
        if not eq(arg_costume, self.costume.number):
            self.costume.switch(arg_costume)

    @warp
    async def my_Init(self, util, ):
        self.list_RoadLag.delete_all()
        for _ in range(10):
            self.list_RoadLag.append(0)
        util.sprites.stage.var_LastLap = ""
        util.sprites.stage.var_LapTime = "00:00.00"
        self.var_LapTicks = 0
        util.sprites.stage.var_car_slide = 0
        pass # hide variable


@sprite('Sprite2')
class Sprite2(Target):
    """Sprite Sprite2"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = 0
        self._direction = 90
        self.shown = False
        self.pen = Pen(self)

        self.costume = Costumes(
           1, 100, "all around", [
            {
                'name': "grass1",
                'path': "12e4e3b737f9796599f649a8452c2fdc.png",
                'center': (480, 4),
                'scale': 2
            },
            {
                'name': "grass2",
                'path': "82b25121d43ae02e53a7a2c9b8bd4830.png",
                'center': (480, 4),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_id = 999
        self.var_x = -999



        self.sprite.layer = 2

    @on_broadcast('create clones')
    async def broadcast_createclones(self, util):
        self.shown = False
        await self.my_createclones(util, )

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if eq(self.costume.number, 1):
            if gt(self.var_id, len(util.sprites.stage.list_Grass1)):
                self.var_x = -999
            else:
                self.var_x = util.sprites.stage.list_Grass1X[toint(self.var_id)]
                self.ypos = tonum(util.sprites.stage.list_Grass1[toint(self.var_id)])
        else:
            if gt(self.var_id, len(util.sprites.stage.list_Grass2)):
                self.var_x = -999
            else:
                self.var_x = util.sprites.stage.list_Grass2X[toint(self.var_id)]
                self.ypos = tonum(util.sprites.stage.list_Grass2[toint(self.var_id)])
        if (gt(self.var_x, -477) and lt(self.var_x, 477)):
            self.xpos = tonum(self.var_x)
            self.shown = True
        else:
            self.shown = False

    @warp
    async def my_createclones(self, util, ):
        self.gotoxy(0, 0)
        self.costume.switch("grass1")
        self.var_id = 0
        for _ in range(95):
            self.var_id += 1
            self.create_clone_of(util, "_myself_")
        self.costume.switch("grass2")
        self.var_id = 0
        for _ in range(95):
            self.var_id += 1
            self.create_clone_of(util, "_myself_")
        self.var_id = 999


@sprite('fog')
class Spritefog(Target):
    """Sprite fog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = 0
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           3, 100, "don't rotate", [
            {
                'name': "Fog",
                'path': "da6c2454574d32be9f3c77cb84a3254d.png",
                'center': (480, 360),
                'scale': 2
            },
            {
                'name': "Gradient2",
                'path': "23d63f1fa4c39033921687cb03b0468e.png",
                'center': (480, 360),
                'scale': 2
            },
            {
                'name': "Gradient3",
                'path': "d57c7e883326eec0ec76d30242fefbcd.png",
                'center': (480, 360),
                'scale': 2
            },
            {
                'name': "Gradient4",
                'path': "ba6354bd04ca6caf47b95c66562f7883.png",
                'center': (480, 122),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 13

    @on_green_flag
    async def green_flag(self, util):
        self.gotoxy(0, 0)
        self.shown = True
        self.front_layer(util)


@sprite('sky')
class Spritesky(Target):
    """Sprite sky"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = 0
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "all around", [
            {
                'name': "sky",
                'path': "e01832dcec3012459f0d90fad414b5cd.png",
                'center': (477, 360),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 1

    @on_green_flag
    async def green_flag(self, util):
        self.change_layer(util, -1000)
        util.sprites.stage.var_horizon_x = 0
        self.gotoxy(0, 0)
        self.shown = True


@sprite('Other Cars')
class SpriteOtherCars(Target):
    """Sprite Other Cars"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 24.639999999999997
        self._ypos = 58
        self._direction = 90
        self.shown = False
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 27, "all around", [
            {
                'name': "red1",
                'path': "11cc2ed9a8813dbccee85c82a69eade4.png",
                'center': (34, 49),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "meow",
                'path': "83c36d806dc92327b9e7049a565c6bff.wav"
            }
        ])

        self.var_carID = 1
        self.var_py = -999
        self.var_z = 370.3703703703704



        self.sprite.layer = 3

    @on_broadcast('create clones')
    async def broadcast_createclones(self, util):
        self.shown = False
        self.var_carID = 1

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        self.var_py = util.sprites.stage.list_CarsPY[toint(self.var_carID)]
        if lt(self.var_py, -177):
            self.shown = False
        else:
            self.gotoxy(tonum(util.sprites.stage.list_CarsPX[toint(self.var_carID)]), tonum(self.var_py))
            self.var_z = (div(-100, (tonum(self.var_py) - 85)) * 100)
            self.costume.size = div(10000, self.var_z)
            self.shown = True


@sprite('car sound')
class Spritecarsound(Target):
    """Sprite car sound"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = -28
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "all around", [
            {
                'name': "costume1",
                'path': "d36f6603ec293d2c2198d3ea05109fe0.png",
                'center': (0, 0),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            50, [
            {
                'name': "acc1",
                'path': "490c6e05e5d75f9d57fe1e1b49f371eb.wav"
            },
            {
                'name': "acc2",
                'path': "bc17de5e29d83a3d929541f45372c32a.wav"
            },
            {
                'name': "acc3",
                'path': "ccae7ec5458f6cb504a97b52e432b854.wav"
            },
            {
                'name': "acc4",
                'path': "efc23827662877f1e41741fac7a3bb30.wav"
            },
            {
                'name': "acc5",
                'path': "05db2b76bff08c2cad37085cfaddff14.wav"
            },
            {
                'name': "acc6",
                'path': "82bd366f9765e9030f3a9bc41873a657.wav"
            },
            {
                'name': "acc7",
                'path': "e71c3b27bef1102c8c99bf7e25320a6f.wav"
            },
            {
                'name': "acc8",
                'path': "81880bd1da37c5d33e1ed5b3d8ce2bd1.wav"
            },
            {
                'name': "acc9",
                'path': "4ce5182353cf719c1d2ef92f047424b3.wav"
            },
            {
                'name': "acc10",
                'path': "4a254cb6208731cc2681731da75408ca.wav"
            },
            {
                'name': "acc11",
                'path': "74eb3e31e149950d46ea448270dbbbc3.wav"
            },
            {
                'name': "dec1",
                'path': "8334f577133d5d8a84bbaa2a9fe6b11f.wav"
            },
            {
                'name': "dec2",
                'path': "52e71b094f9ed90423b3e6704b5c01f5.wav"
            },
            {
                'name': "dec3",
                'path': "c1444550563319a6527b2f14b536b16c.wav"
            },
            {
                'name': "dec4",
                'path': "21734617667bd081713b8712b277ae71.wav"
            },
            {
                'name': "dec5",
                'path': "fa91b3792d640449f0e8a8c302328e7e.wav"
            },
            {
                'name': "dec6",
                'path': "0159adab0bf20710a05792dc4f87bfd6.wav"
            },
            {
                'name': "dec7",
                'path': "10ab10beaf8577976fe0eb2695bccd42.wav"
            },
            {
                'name': "dec8",
                'path': "52936050425b71d1490205d17c42ead3.wav"
            },
            {
                'name': "dec9",
                'path': "a5d8fe54828dd47a3efda20237cf3564.wav"
            },
            {
                'name': "dec10",
                'path': "c930313a99d90d0f601210a5f31dba6c.wav"
            },
            {
                'name': "dec11",
                'path': "60ff4d3ea207192b47a02e5ed39258d1.wav"
            }
        ])

        self.var_ID = 1



        self.sprite.layer = 4

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if (eq(util.sprites.stage.var_SOUND_ID, self.var_ID) and gt(util.sprites.stage.var_tick, util.sprites.stage.var_SOUND_TICK)):
            if gt(div(util.sprites.stage.var_speed, 1.8), util.sprites.stage.var_SOUND_):
                util.sprites.stage.var_SOUND_ += 1
                if gt(util.sprites.stage.var_SOUND_, 11):
                    util.sprites.stage.var_SOUND_ = 5
                self.sounds.play(util.sprites.stage.var_SOUND_)
                util.sprites.stage.var_SOUND_TICK += 30
                util.sprites.stage.var_SOUND_ID = (1 - util.sprites.stage.var_SOUND_ID)
            else:
                if gt(util.sprites.stage.var_speed, 0):
                    util.sprites.stage.var_SOUND_ = math.ceil(div(util.sprites.stage.var_speed, 2))
                    self.sounds.play((util.sprites.stage.var_SOUND_ + 11))
                    util.sprites.stage.var_SOUND_ += -1
                    util.sprites.stage.var_SOUND_TICK += 30
                    util.sprites.stage.var_SOUND_ID = (1 - util.sprites.stage.var_SOUND_ID)

    @on_broadcast('create clones')
    async def broadcast_createclones(self, util):
        self.sounds.set_volume(50)
        self.var_ID = 0
        self.create_clone_of(util, "_myself_")
        self.var_ID = 1

    @on_green_flag
    async def green_flag(self, util):
        util.sprites.stage.var_SOUND_TICK = 0
        util.sprites.stage.var_SOUND_ID = 0
        util.sprites.stage.var_SOUND_ = 0
        util.sprites.stage.var_IsAccellerating = 1


@sprite('map')
class Spritemap(Target):
    """Sprite map"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 150
        self._ypos = 125
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 35, "all around", [
            {
                'name': "circuit1",
                'path': "5365defedaba0783df73887591149591.png",
                'center': (449, 229),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_x = -107.128433125496
        self.var_y = 65.25398084054217
        self.var_a = 360
        self.var_GetDirection = 119.10047741154344
        self.var_i = 175
        self.var_la = 360



        self.sprite.layer = 12

    @on_green_flag
    async def green_flag(self, util):
        self.gotoxy(150, 125)
        self.direction = 90
        self.costume.size = 35
        self.costume.set_effect('ghost', 25)
        self.front_layer(util)

    @warp
    async def my_GetDirection(self, util, arg_dx, arg_dy):
        if eq(arg_dy, 0):
            if gt(arg_dx, 0):
                self.var_GetDirection = 90
            else:
                self.var_GetDirection = -90
        else:
            self.var_GetDirection = math.degrees(math.atan(div(arg_dx, arg_dy)))
            if lt(arg_dy, 0):
                if gt(arg_dx, 0):
                    self.var_GetDirection += 180
                else:
                    if lt(arg_dx, 0):
                        self.var_GetDirection += -180
                    else:
                        self.var_GetDirection = 180

    @on_pressed('m')
    async def key_m_pressed(self, util):
        pass

    @warp
    async def my_Reposition(self, util, ):
        self.gotoxy((((0 - self.var_x) * math.cos(math.radians(tonum(self.var_a)))) - ((0 - self.var_y) * math.sin(math.radians(tonum(self.var_a))))), (((0 - self.var_y) * math.cos(math.radians(tonum(self.var_a)))) + ((0 - self.var_x) * math.sin(math.radians(tonum(self.var_a))))))
        self.direction = (0 - tonum(self.var_a))


@sprite('map trace')
class Spritemaptrace(Target):
    """Sprite map trace"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 173.8
        self._ypos = 162.45
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           1, 100, "all around", [
            {
                'name': "path",
                'path': "cfba1a6258c5c82fb1d2b97b828231f8.png",
                'center': (6, 26),
                'scale': 2
            },
            {
                'name': "red dot",
                'path': "74da904f605317f24e7877d6176e3704.png",
                'center': (8, 8),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_d = 1



        self.sprite.layer = 14

    @on_green_flag
    async def green_flag(self, util):
        self.costume.switch("red dot")
        self.shown = True
        await self.sleep(0.1)
        self.front_layer(util)

    @on_pressed('m')
    async def key_m_pressed(self, util):
        self.costume.switch("path")
        self.gotoxy(0, 0)
        self.shown = True
        await self.sleep(0.1)
        self.front_layer(util)

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        self.var_d = ((math.floor(div(util.sprites["Game"].var_y, 400)) % len(util.sprites.stage.list_track_x)) + 1)
        self.gotoxy((util.sprites["map"].xpos + (tonum(util.sprites.stage.list_track_y[toint(self.var_d)]) * 0.35)), (util.sprites["map"].ypos - (tonum(util.sprites.stage.list_track_x[toint(self.var_d)]) * 0.35)))


@sprite('Sprite_FX_Dust_0013')
class Sprite_FX_Dust_0013(Target):
    """Sprite Sprite_FX_Dust_0013"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = -136
        self._direction = 90
        self.shown = False
        self.pen = Pen(self)

        self.costume = Costumes(
           5, 150, "all around", [
            {
                'name': "Sprite_FX_Dust_2",
                'path': "0f0d5a66b08d76d018d1bf326401be69-fallback.png",
                'center': (33, 17),
                'scale': 1
            },
            {
                'name': "Sprite_FX_Dust_3",
                'path': "8ee6d2d12146f96e4d25b075993febc7-fallback.png",
                'center': (31, 16),
                'scale': 1
            },
            {
                'name': "Sprite_FX_Dust_4",
                'path': "6a96b44e19bbb419df1256f27fc6a88c-fallback.png",
                'center': (32, 17),
                'scale': 1
            },
            {
                'name': "Sprite_FX_Dust_5",
                'path': "7e4968ec7c083dca20ae5d893038fad5-fallback.png",
                'center': (32, 17),
                'scale': 1
            },
            {
                'name': "Sprite_FX_Dust_6",
                'path': "26836955e69114e50890887cb6878d2b-fallback.png",
                'center': (33, 16),
                'scale': 1
            },
            {
                'name': "Sprite_FX_Dust_7",
                'path': "0fcd4618e9f3356e244cfee8960171ee-fallback.png",
                'center': (34, 16),
                'scale': 1
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_frame = 0
        self.var_mode = 0



        self.sprite.layer = 8

    @on_green_flag
    async def green_flag(self, util):
        self.shown = False
        self.costume.size = 150
        self.var_frame = 0
        self.var_mode = 0

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if ((gt(util.sprites.stage.var_IsAccellerating, 0) and lt(util.sprites.stage.var_speed, 5)) or (lt(util.sprites.stage.var_IsAccellerating, 0) and gt(util.sprites.stage.var_speed, 6))):
            if not eq(self.var_mode, 1):
                self.front_layer(util)
                self.var_mode = 1
                self.var_frame = 0
            else:
                self.var_frame += 0.25
            await self.my_SetCostumeA(util, ((math.floor(self.var_frame) % 6) + 1), 150)
            self.gotoxy(util.sprites["Game"].xpos, (util.sprites["Game"].ypos - 16))
            self.shown = True
        else:
            if gt(util.sprites.stage.var_car_slide, 5):
                if not eq(self.var_mode, 2):
                    self.front_layer(util)
                    self.var_mode = 2
                    self.var_frame = 0
                else:
                    self.var_frame += 0.25
                await self.my_SetCostumeA(util, ((math.floor(self.var_frame) % 6) + 1), 200)
                self.gotoxy((util.sprites["Game"].xpos - (util.sprites.stage.var_car_sx * 2)), (util.sprites["Game"].ypos - 16))
                self.shown = True
            else:
                self.var_mode = 0
                self.shown = False

    @warp
    async def my_SetCostumeA(self, util, arg_costume, arg_size):
        if not eq(arg_costume, self.costume.number):
            self.costume.switch(arg_costume)
        if not eq(arg_size, round(self.costume.size)):
            self.costume.size = arg_size


@sprite('TransmissionSettings')
class SpriteTransmissionSettings(Target):
    """Sprite TransmissionSettings"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 80
        self._ypos = 0
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 60, "all around", [
            {
                'name': "costume1",
                'path': "cd21514d0531fdffb22204e0ec5ed84a-fallback.png",
                'center': (0, 0),
                'scale': 1
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 5

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if gt(util.sprites.stage.var_RPM, 3800):
            if ((not gt(util.sprites.stage.var_IsAccellerating, 0) and lt(util.sprites.stage.var_RPM, 4000)) and gt(util.sprites.stage.var_GEAR, 1)):
                util.send_broadcast("GEAR_DOWN")
        if ((not gt(util.sprites.stage.var_IsAccellerating, 0) and lt(util.sprites.stage.var_RPM, 1200)) and gt(util.sprites.stage.var_GEAR, 1)):
            util.send_broadcast("GEAR_DOWN")
        if ((gt(util.sprites.stage.var_IsAccellerating, 0) and (gt(util.sprites.stage.var_RPM, (6700 * util.sprites.stage.var_IsAccellerating)) or gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_MaxRpm + 200) * util.sprites.stage.var_IsAccellerating)))) and lt(util.sprites.stage.var_GEAR, 8)):
            util.send_broadcast("GEAR_UP")
        if (gt(util.sprites.stage.var_IsAccellerating, 0) and eq(util.sprites.stage.var_GEAR, 1)):
            util.send_broadcast("GEAR_UP")


@sprite('ENG-RPM')
class SpriteENGRPM(Target):
    """Sprite ENG-RPM"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -53
        self._ypos = -36
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "all around", [
            {
                'name': "costume1",
                'path': "d36f6603ec293d2c2198d3ea05109fe0.png",
                'center': (0, 0),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            10, [

        ])





        self.sprite.layer = 6

    @on_green_flag
    async def green_flag(self, util):
        util.sprites.stage.var_GEAR = 1
        util.sprites.stage.var_MaxRpm = 7500
        while True:
            if eq(util.sprites.stage.var_GEAR, 1):
                if (eq(util.sprites.stage.var_IsAccellerating, 1) and lt(util.sprites.stage.var_RPM, (util.sprites.stage.var_MaxRpm * util.sprites.stage.var_IsAccellerating))):
                    util.sprites.stage.var_RPM += (416 * util.sprites.stage.var_IsAccellerating)
                else:
                    if gt(util.sprites.stage.var_RPM, 750):
                        util.sprites.stage.var_RPM += -97
            if eq(util.sprites.stage.var_GEAR, 2):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 95) + 750)
            if eq(util.sprites.stage.var_GEAR, 3):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 58) + 750)
            if eq(util.sprites.stage.var_GEAR, 4):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 40.3) + 750)
            if eq(util.sprites.stage.var_GEAR, 5):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 32.6) + 750)
            if eq(util.sprites.stage.var_GEAR, 6):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 27.4) + 750)
            if eq(util.sprites.stage.var_GEAR, 7):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 24.2) + 750)
            if eq(util.sprites.stage.var_GEAR, 8):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 21.3) + 750)
            emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * '+str(util.sprites.stage.var_RPM)+')</exec><writeln />'
            emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int('+str(util.sprites.stage.var_MPH*1.609344)+')</exec><writeln />'
            await self.yield_()

    @on_green_flag
    async def green_flag1(self, util):
        while True:
            if lt(util.sprites.stage.var_RPM, 750):
                util.sprites.stage.var_RPM = 750
            if gt(util.sprites.stage.var_RPM, 8000):
                util.sprites.stage.var_RPM = 8000
            if lt(util.sprites.stage.var_IsAccellerating, 0):
                if gt(util.sprites.stage.var_RPM, 750):
                    util.sprites.stage.var_RPM += (100 * util.sprites.stage.var_IsAccellerating)
            if lt(util.sprites.stage.var_speed, 0):
                util.sprites.stage.var_speed = 0

            await self.yield_()

    @on_broadcast('crash')
    async def broadcast_crash(self, util):
        self.stop_other()
        util.sprites.stage.var_RPM = 0

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        util.sprites.stage.var_KMH = ((util.sprites.stage.var_speed * 7) * 1.609)


@sprite('GEARS')
class SpriteGEARS(Target):
    """Sprite GEARS"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -184
        self._ypos = -118.33953857421875
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "all around", [
            {
                'name': "not",
                'path': "3fa9cbd3b3080ac10f1ef05646785001.png",
                'center': (12, 17),
                'scale': 2
            },
            {
                'name': "not2",
                'path': "25ad044f448f18c29ed3a7ae38bb21fe.png",
                'center': (9, 17),
                'scale': 2
            },
            {
                'name': "not3",
                'path': "7cd9c55717fb6bc46dbafc4fa6ae7562.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "not4",
                'path': "313317402e8f6abda4647f922d7d1eb1.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "not5",
                'path': "a5f9489ae7521258a9e3fc22c0826893.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "not6",
                'path': "d9ddda7ad10ed691c9d15bd8e89a8403.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "not7",
                'path': "c67427ad6ffb9e5838e7cb01e7c0a87b.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "not8",
                'path': "25c1578cfe1944e149aeafc32151ee87.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "not16",
                'path': "f1bce17f3abc785880b6d301ac40d55c.png",
                'center': (12, 17),
                'scale': 2
            },
            {
                'name': "not9",
                'path': "a6b9b2c9512b847425c279f802294edd.png",
                'center': (9, 17),
                'scale': 2
            },
            {
                'name': "not10",
                'path': "123373605b45077085f2ad2ac99cda17.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "not11",
                'path': "d4cb7c82a1657dfe52ef1ed236b8c068.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "not12",
                'path': "3cf56c611a98a3144bfa1004adb22196.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "not13",
                'path': "5cc57fffa70593313cc15cb980e093c8.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "not14",
                'path': "b5c9e020be2af084c162fed78b9b21f4.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "not15",
                'path': "f4e2dde059f0f2fd0496994662190727.png",
                'center': (11, 17),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 10

    @on_green_flag
    async def green_flag(self, util):
        util.sprites.stage.var_RPM = 0
        if eq(util.sprites.stage.var_IsAccellerating, 1):
            util.sprites.stage.var_GEAR = 2
        else:
            util.sprites.stage.var_GEAR = 1
        self.costume.switch("not")
        util.sprites.stage.var_ON = 1
        self.front_layer(util)
        for _ in range(15):
            util.sprites.stage.var_RPM += 50

            await self.yield_()
        util.sprites.stage.var_DMODE = 2
        util.sprites.stage.var_Gearbox = 0
        util.sprites.stage.var_CHANGE = 0

    @on_green_flag
    async def green_flag1(self, util):
        pass

    @on_broadcast('gear_up')
    async def broadcast_gear_up(self, util):
        if lt(util.sprites.stage.var_GEAR, 8):
            util.sprites.stage.var_GEAR += 1
            util.sprites.stage.var_CHANGE = 1
            self.costume.switch(util.sprites.stage.var_GEAR)
            if eq(util.sprites.stage.var_GEAR, 3):
                while not lt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 58) + 750)):
                    util.sprites.stage.var_RPM += -231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 4):
                while not lt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 40.3) + 750)):
                    util.sprites.stage.var_RPM += -231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 5):
                while not lt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 32.6) + 750)):
                    util.sprites.stage.var_RPM += -231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 6):
                while not lt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 27.4) + 750)):
                    util.sprites.stage.var_RPM += -231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 7):
                while not lt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 24.2) + 750)):
                    util.sprites.stage.var_RPM += -231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 8):
                while not lt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 21.3) + 750)):
                    util.sprites.stage.var_RPM += -231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
        await self.sleep(0.2)

    @on_broadcast('gear_down')
    async def broadcast_gear_down(self, util):
        if gt(util.sprites.stage.var_GEAR, 1):
            util.sprites.stage.var_GEAR += -1
            util.sprites.stage.var_CHANGE = 2
            self.costume.switch(util.sprites.stage.var_GEAR)
            if eq(util.sprites.stage.var_GEAR, 7):
                while not gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 21.3) + 750)):
                    util.sprites.stage.var_RPM += 231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 6):
                while not gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 27.4) + 750)):
                    util.sprites.stage.var_RPM += 231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 5):
                while not gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 32.6) + 750)):
                    util.sprites.stage.var_RPM += 231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 4):
                while not gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 40.3) + 750)):
                    util.sprites.stage.var_RPM += 231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 3):
                while not gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 58) + 750)):
                    util.sprites.stage.var_RPM += 231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 2):
                while not gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 151) + 750)):
                    util.sprites.stage.var_RPM += 231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 1):
                util.sprites.stage.var_CHANGE = 0
        await self.sleep(0.2)

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if gt(util.sprites.stage.var_RPM, 6300):
            self.costume.switch((util.sprites.stage.var_GEAR + 8))
        else:
            self.costume.switch(util.sprites.stage.var_GEAR)


@sprite('Rev2')
class SpriteRev2(Target):
    """Sprite Rev2"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -182
        self._ypos = -80
        self._direction = -101.19047619047618
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 50, "all around", [
            {
                'name': "costume1",
                'path': "341bc1610786f269cb95124fb9324ff9.png",
                'center': (38, 27),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 9

    @on_broadcast('crash')
    async def broadcast_crash(self, util):
        self.stop_other()
        self.direction = -126

    @on_green_flag
    async def green_flag(self, util):
        self.front_layer(util)
        self.direction = -101

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if lt(util.sprites.stage.var_RPM, 7800):
            if lt(div(util.sprites.stage.var_RPM, 31.5), (((305 + self.direction) % 720) - 180)):
                self.direction -= div(((((305 + self.direction) % 720) - 180) - div(util.sprites.stage.var_RPM, 31.5)), 5)
            if gt(div(util.sprites.stage.var_RPM, 31.5), (((305 + self.direction) % 720) - 180)):
                self.direction += div((div(util.sprites.stage.var_RPM, 31.5) - (((305 + self.direction) % 720) - 180)), 5)
        else:
            self.direction = 120


@sprite('Sprite10')
class Sprite10(Target):
    """Sprite Sprite10"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -154
        self._ypos = -155
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 200, "all around", [
            {
                'name': "0",
                'path': "b2c88513024d459b754e77d83f61c85e.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "1",
                'path': "25ad044f448f18c29ed3a7ae38bb21fe.png",
                'center': (9, 17),
                'scale': 2
            },
            {
                'name': "2",
                'path': "7cd9c55717fb6bc46dbafc4fa6ae7562.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "3",
                'path': "313317402e8f6abda4647f922d7d1eb1.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "4",
                'path': "a5f9489ae7521258a9e3fc22c0826893.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "5",
                'path': "d9ddda7ad10ed691c9d15bd8e89a8403.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "6",
                'path': "c67427ad6ffb9e5838e7cb01e7c0a87b.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "7",
                'path': "25c1578cfe1944e149aeafc32151ee87.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "8",
                'path': "a5ff3b021382f90770d138e9c1b29fc4.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "9",
                'path': "e0e917a56ad09fde0ff1358972e47cce.png",
                'center': (10, 17),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 17

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        self.front_layer(util)
        self.costume.switch(letter_of(str((math.floor(abs(util.sprites.stage.var_MPH)) % 10)), 1))


@sprite('Sprite12')
class Sprite12(Target):
    """Sprite Sprite12"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -196
        self._ypos = -155
        self._direction = 90
        self.shown = False
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 200, "all around", [
            {
                'name': "1",
                'path': "25ad044f448f18c29ed3a7ae38bb21fe.png",
                'center': (9, 17),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 16

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        self.front_layer(util)
        if gt(math.floor(div(util.sprites.stage.var_MPH, 100)), 0):
            self.shown = True
            self.costume.switch(math.floor(div(util.sprites.stage.var_MPH, 100)))
        else:
            self.shown = False


@sprite('Sprite11')
class Sprite11(Target):
    """Sprite Sprite11"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -177
        self._ypos = -155
        self._direction = 90
        self.shown = False
        self.pen = Pen(self)

        self.costume = Costumes(
           6, 200, "all around", [
            {
                'name': "0",
                'path': "b2c88513024d459b754e77d83f61c85e.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "1",
                'path': "25ad044f448f18c29ed3a7ae38bb21fe.png",
                'center': (9, 17),
                'scale': 2
            },
            {
                'name': "2",
                'path': "7cd9c55717fb6bc46dbafc4fa6ae7562.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "3",
                'path': "313317402e8f6abda4647f922d7d1eb1.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "4",
                'path': "a5f9489ae7521258a9e3fc22c0826893.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "5",
                'path': "d9ddda7ad10ed691c9d15bd8e89a8403.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "6",
                'path': "f0fcf92a5f2b72faa5f7d3c873fdd2d2.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "7",
                'path': "25c1578cfe1944e149aeafc32151ee87.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "8",
                'path': "a5ff3b021382f90770d138e9c1b29fc4.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "9",
                'path': "e0e917a56ad09fde0ff1358972e47cce.png",
                'center': (10, 17),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 15

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        self.front_layer(util)
        if gt(math.floor(div(util.sprites.stage.var_MPH, 10)), 0):
            self.shown = True
            self.costume.switch(letter_of(str((math.floor(div(util.sprites.stage.var_MPH, 10)) % 10)), 1))
        else:
            self.shown = False


@sprite('T1-b')
class SpriteT1b(Target):
    """Sprite T1-b"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -182
        self._ypos = -80
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 50, "all around", [
            {
                'name': "costume1",
                'path': "f64c94a8a4ac40e16de73d59e187c66c.png",
                'center': (229, 230),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 7






if __name__ == '__main__':
    engine.start_program()
