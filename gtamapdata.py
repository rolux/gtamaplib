import os
import zipfile

DIRNAME = os.path.dirname(__file__)

for name in ("fonts", "frames", "maps"):
    dirname = f"{DIRNAME}/{name}"
    filename = f"{DIRNAME}/{name}.zip"
    if not os.path.exists(dirname) and os.path.exists(filename):
        print(f"Extracting {name}", end=" ... ", flush=True)
        with zipfile.ZipFile(filename) as z:
            z.extractall(dirname)
        print("Done")


### CAMERAS ########################################################################################

cameras = {
    # "[id] name": ((px, py, pz), (cx, cy, cz), (yaw, pitch, roll), (hfov, vfov), (w, h))
    "[L1/2] AI World Editor Map (4K)": (None, (-6526.350, 2989.138, 1_000_000.000), (0.000, -90.000, 0.000), (0.161776, 0.085944), (3840, 2040)),
    "[L1/4] Diner (N)": ((-6187.800, 4504.800, 14.600), (-6188.800, 4501.900, 16.200), (327.845, -16.355, 0.000), (None, 50.800), (1920, 1080)),
    "[L1/4] Diner (W)": ((-6185.800, 4502.700, 14.300), (-6179.600, 4500.100, 16.600), (63.337, -7.836, 0.000), (None, 51.300), (1920, 1080)),
    "[L1/4] Diner (E)": ((-6164.100, 4468.100, 14.800), (-6169.600, 4472.500, 16.800), (232.000, -5.810, 0.000), (None, 54.000), (1920, 1080)),
    "[L1/4] Car Wash": ((-6220.800, 4316.200, 20.500), (-6216.700, 4321.600, 21.800), (146.326, 0.350, 0.000), (None, 51.300), (1920, 1080)),
    # "[L1/6] Sidewalk (Jason) (E)": ((-461.500, 1233.400, 3.200), (-464.000, 1233.800, 4.600), (244.475, -19.200, -1.000), (None, 50.800), (1920, 1080)),
    "[L1/6] Sidewalk (Jason) (E)": ((-461.500, 1233.400, 3.200), (-464.000, 1233.800, 4.600), (244.800, -19.865, 0.000), (None, 50.800), (1920, 1080)),
    "[L1/7] Port": ((1185.700, -429.100, 5.200), (1190.000, -426.900, 7.200), (302.500, 14.100, 0.000), (None, 49.600), (1376, 776)),
    "[L1/8] Gas Station (Lucia)": ((-6319.500, 2749.100, 12.500), (-6319.100, 2748.300, 13.100), (359.830, -0.250, 0.000), (57.350, 34.200), (1920, 1080), (1920, 1080)),
    "[L1/9] Motel": ((-5358.200, 3486.200, 66.700), (-5359.900, 3484.000, 66.500), (313.000, 13.000, 0.000), (None, 49.600), (1920, 1080)),
    "[L1/10] Pawn Shop (W)": ((-6423.000, 3060.100, 5.800), (-6421.600, 3061.600, 6.700), (125.104, -8.885, 0.000), (None, 49.600), (1376, 776)),
    "[L1/10] Pawn Shop (S)": ((-6420.100, 3062.300, 5.900), (-6420.300, 3064.700, 6.500), (173.193, -4.990, 0.000), (None, 49.600), (1376, 776)),
    "[L1/11] Sidewalk (Lucia)": ((1931.500, 274.000, 3.200), (1931.700, 270.400, 5.800), (10.000, -20.000, 0.000), (None, 49.600), (1920, 1080)),
    "[L1/13] House with Boat (X)": ((-2342.500, -5542.900, 2.800), (-2342.100, -5545.800, 3.600), (0.000, -5.000, 0.000), (None, 49.600), (3840, 2160)),
    "[L1/14] Shootout (S)": ((-1355.500, 735.400, 4.100), (-1355.700, 737.800, 4.900), (169.000, -7.500, 0.000), (None, 50.800), (1920, 1080)),
    "[L1/15] Park": ((2009.900, 454.900, 3.300), (2010.300, 452.400, 3.700), (0.000, 0.000, 0.000), (None, 49.600), (1920, 1080)),
    "[L1/15] Bar": ((2092.800, 1153.200, 6.000), (2095.400, 1153.500, 6.400), (87.802, 0.000, 0.000), (None, 49.600), (1920, 1080)),
    "[L1/15] Glitch (A)": ((1410.700, 1371.600, 2.900), (1411.600, 1379.700, -58.500), (29.000, -14.397, 0.000), (None, 49.600), (1920, 1080)),
    "[L1/16] Boat (Jason)": ((-3852.600, -344.300, 6.000), (-3853.900, -344.000, 7.300), (240.000, -27.000, 0.000), (None, 51.400), (1920, 1020)),
    "[L1/17] Hotel (E)": ((1955.600, 1566.800, 4.600), (1951.500, 1565.300, 5.700), (284.767, 0.000, 0.000), (None, 49.600), (1920, 1080)),
    "[L1/17] Hotel (W)": ((1954.400, 1559.600, 4.600), (1957.500, 1559.700, 5.500), (84.000, -8.250, 0.000), (None, 49.600), (1920, 1080)),
    "[L1/19] Farm": ((-3466.800, -4462.600, 2.400), (-3466.300, -4469.700, 3.700), (11.400, -17.200, 0.000), (None, 49.600), (1920, 1020)),
    "[L1/20] Gas Station (Jason)": ((-6319.400, 2749.900, 12.600), (-6318.700, 2746.900, 13.387), (0.084, -5.275, 0.000), (80.339, 50.800), (1920, 1080)),
    "[L1/21] Ocean near Keys (N)": ((-3442.800, -7188.300, -0.100), (-3442.900, -7191.000, 0.500), (358.679, -2.164, -1.300), (81.856, 52.000), (1920, 1080)),
    "[L1/21] Ocean near Keys (E)": ((-3427.400, -7191.100, -0.200), (-3430.100, -7190.500, 0.600), (257.800, -6.831, 0.000), (None, 49.600), (1920, 1080)),
    "[L1/21] Metro (NE) (B)": ((-1553.500, -301.000, 19.800), (-1554.500, -302.100, 20.900), (305.704, -15.194, 0.000), (None, 49.600), (1920, 1020)),
    "[L1/22] Metro (SE) (A) (4K)": ((-1555.100, -308.000, 19.700), (-1555.200, -307.700, 20.600), (183.753, -9.908, 0.000), (None, 49.600), (3840, 2040)),
    "[L1/22] Metro (SE) (B)": ((-1555.100, -308.500, 19.800), (-1555.200, -308.100, 20.700), (185.000, -10.000, 0.000), (None, 49.600), (1920, 1020)),
    "[L1/26] Loading Zone near Prison (SW)": ((-4727.000, 1852.200, 11.500), (-4725.300, 1853.800, 12.200), (122.973, -5.000, 0.000), (None, 49.600), (1920, 1020)),
    "[L1/27] Highway (N)": ((-584.000, 1601.300, 12.200), (-587.400, 1596.000, 13.400), (324.500, -9.000, 0.000), (None, 51.300), (1920, 1080)),
    "[L1/27] Highway (NE)": ((-503.300, 1716.900, 13.300), (-506.700, 1712.000, 15.400), (326.000, -16.300, 0.000), (None, 51.400), (1920, 1080)),
    "[L1/29] Welcome Center (E)": ((2016.000, 588.900, 3.200), (2013.800, 588.100, 4.500), (282.000, -22.034, 0.000), (None, 50.800), (1920, 1080)),
    "[L1/29] Welcome Center (W)": ((2023.900, 587.400, 3.200), (2026.300, 586.900, 4.700), (71.823, -26.284, 0.000), (None, 50.800), (1920, 1080)),
    "[L1/30] Store": ((-6332.400, 2750.500, 12.400), (-6331.100, 2750.200, 14.200), (86.623, -42.601, 0.000), (None, 49.600), (1904, 1080)),
    "[L1/32] Police Chase (A)": ((-2588.800, -3567.800, 9.700), (-2588.900, -3566.700, 10.300), (201.396, -2.565, -1.500), (None, 54.100), (1920, 1080)),
    "[L1/32] Police Chase (D)": ((-2582.400, -3437.700, 10.000), (-2582.300, -3436.600, 10.400), (201.105, -7.000, 0.000), (None, 37.600), (1920, 1080)),
    "[L1/32] Police Chase (J)": ((-2568.900, -3273.700, 10.200), (-2568.700, -3272.600, 11.300), (190.275, -8.500, 0.000), (None, 37.600), (1920, 1080)),
    "[L1/36] Alley (W)": ((1954.000, 861.300, 4.000), (1955.100, 851.600, 5.000), (66.400, -11.700, 0.000), (None, 49.600), (1920, 1080)),
    #"[L1/37] Airport (X)": ((-2582.000, -122.700, 5.200), (-2589.500, -123.500, 7.300), (278.294, -17.180, 0.000), (None, 51.300), (1920, 1080)),
    "[L1/37] Airport (X)": ((-2582.000, -122.700, 5.200), (-2589.500, -123.500, 7.300), (276.700, -17.180, 0.000), (None, 51.300), (1920, 1080)),
    "[L1/42] Tennis Court (SE)": ((-315.400, 1174.200, 3.500), (-317.232, 1174.859, 5.021), (258.590, -9.921, 0.009), (None, 37.600), (1824, 1080)),
    "[L1/43] Pool": ((-5325.300, 3473.200, 66.900), (-5327.700, 3476.600, 67.900), (208.500, -8.000, 0.000), (None, 49.600), (1920, 1080)),
    "[L1/44] Tennis Stadium (4K)": ((-152.600, -1748.900, 36.300), (-155.600, -1748.600, 36.300), (84.936, -0.100, 0.000), (None, 45.000), (3840, 2160)),
    "[L1/48] Hangar (A)": ((-2630.900, -116.800, 4.300), (-2631.700, -113.900, 4.600), (313.300, 15.400, 0.000), (None, 50.900), (1920, 1080)),
    "[T1/1] Prison":  (None, (-3355.000, -2758.000, 32.639), (281.653, -2.500, 0.000), (80.600, 51.006), (3840, 2160)),
    "[T1/6] Vice Beach": (None, (2255.000, 1069.000, 69.334), (112.655, -5.800, 0.000), (62.600, 37.762), (3840, 2160)),
    "[T1/10] Beach": (None, (2158.000, -5.000, 3.687), (16.106, -0.900, 0.000), (45.000, 26.231), (3840, 2160)),
    "[T1/16] Venetian Islands": (None, (-16.000, 1095.000, 71.746), (286.720, -13.400, 0.000), (64.200, 38.871), (3840, 2160)),
    "[T1/19] Keys": (None, (-6107.000, -7097.000, 195.642), (276.904, -19.500, 0.000), (55.000, 32.642), (3840, 2160)),
    "[T1/20] Rooftop Party": (None, (1929.000, 1953.000, 104.661), (162.326, -7.500, 0.000), (58.700, 35.105), (3840, 2160)),
    "[T1/44] U-Turn (NW)": (None, (-6288.000, 3358.000, 5.500), (62.000, -1.000, 0.000), (50.000, None), (3840, 2160)),
    "[T1/44] U-Turn (NE)": (None, (-6288.000, 3358.000, 5.500), (340.500, -3.000, 0.000), (45.000, None), (3840, 2160)),
    "[T2/1] Key Lento": (None, (-1808.000, -5256.000, 33.685), (134.337, -8.100, 0.000), (62.500, 30.546), (3840, 1728)),
    "[T2/67] Television": (None, (-2352.500, -5527.900, 8.000), (26.554, -4.908, 0.000), (60.000, None), (3840, 1728)),
    "[T2/77] Chase (2)": (None, (-6480.000, 3300.000, 6.000), (350.941, 3.600, 0.000), (57.682, None), (3840, 1728)),
    "[S2/39] Vice City 03 (Basketball)": (None, (1950.000, 1650.000, 30.000), (111.000, -8.000, 0.000), (55.000, None), (3840, 2160)),
    "[S2/46] Leonida Keys 01 (Airplane) (X)": (None, (-4369.000, -7582.000, 78.319), (318.646, -9.400, 0.000), (62.600, 37.762), (3840, 2160)),
    "[S2/56] Ambrosia 01 (Bikers)": (None, (-3900.000, 3900.000, 10.000), (45.000, 0.000, 0.000), (60.000, None), (3840, 2160)),
    "[S2/57] Ambrosia 02 (Panorama)": (None, (-3915.000, 4997.000, 50.000), (178.354, -2.750, 0.000), (40.300, None), (3840, 2160)),
    "[S2/59] Ambrosia 04 (Fires)": (None, (-3443.000, 3394.000, 20.000), (109.586, -3.000, 0.000), (81.000, None), (3840, 2160)),
    "[S2/62] Grassrivers 02 (Watson Bay)": (None, (-5218.000, -3355.000, 27.233), (282.302, -6.000, 0.000), (49.600, 29.139), (3840, 2160)),
    "[S2/71] Vice City Postcard": (None, (220.000, 1730.000, 17.208), (154.114, 3.600, 0.000), (65.000, 45.148), (2458, 1604)),
    "[S2/72] Leonida Keys Postcard (X)": (None, (-3813.000, -6798.000, 149.816), (300.041, -12.000, 0.000), (47.000, 32.337), (2563, 1709)),
    "[S2/73] Port Gellhorn Postcard (X)": (None, (-6550.000, 3550.000, 25.000), (56.000, -0.300, 0.000), (56.000, None), (3240, 2160)),
    "[S2/74] Ambrosia Postcard": (None, (-3810.000, 3785.000, 25.000), (162.678, -1.000, 0.000), (56.000, None), (3240, 2160)),
}

cameras = {
    " ".join(id_name.split(" ")[1:]): {
        "id": id_name.split(" ")[0],
        "player": data[0],
        "xyz": data[1],
        "ypr": data[2],
        "fov": data[3],
        "size": data[4]
    }
    for id_name, data in cameras.items()
}


### PIXELS #########################################################################################

pixels = {
    "[L1/2] AI World Editor Map (4K)": [
        ((1484, 308), "AIWE"),
        ((1853, 316), "Waldo Station (SE)"),
        ((2295, 323), "1703 E 5th St (Warehouse) (NW)"),
        ((2276, 352), "1703 E 5th St (Shack) (SE)"),
        ((2260, 353), "1703 E 5th St (Shack) (SW)"),
        ((1946, 370), "Transformer Station (SW)"),
        ((2152, 383), "Lucky Plucker (NE)"),
        ((1799, 384), "Pier (L945) (SW)"),
        ((2302, 385), "1703 E 5th St (Warehouse) (SW)"),
        ((2155, 400), "Lucky Plucker (SE)"),
        ((2138, 404), "Lucky Plucker (SW)"),
        ((1849, 407), "? (L944) (SE)"),
        ((1782, 426), "Pier (L946) (NE)"),
        ((2159, 434), "Port Gellhorn Smokestack"),
        ((2176, 476), "6232 E Hwy 98 (NE)"),
        ((1781, 479), "Leslie Porter Wayside Park"),
        ((1889, 510), "? (L664) (SE)"),
        ((2176, 511), "6232 E Hwy 98 (SE)"),
        ((2191, 521), "Large White Billboard"),
        ((2142, 539), "? (L954) (SE)"),
        ((2005, 552), "Wildfire Scooters (NW)"),
        ((1921, 555), "? (L663) (SE)"),
        ((2035, 557.5), "Wildfire Scooters (SE)"),
        ((2058, 564), "3401 E Hwy 98 (SW)"),
        ((2009, 564.5), "Wildfire Scooters (SW)"),
        ((2192, 576), "? (L952) (NE)"),
        ((2026, 606), "2533 E Hwy 98 (N)"),
        ((2019, 615), "2533 E Hwy 98 (W)"),
        ((2132, 627), "? (L953) (NE)"),
        ((2195, 646), "6246 E Hwy 98 (NE)"),
        ((2020, 651), "Twice The Ice (N)"),
        ((2017, 657), "Twice The Ice (W)"),
        ((2092, 727), "Goodwill Career Training Center (SW)"),
        ((1996, 778), "Red Bird Café (NW)"),
        ((1888, 809), "Rodeo's (SE)"),
        ((1850, 816), "King Slayer Charters (NE)"),
        ((1848, 844), "King Slayer Charters (SE)"),
        ((2301, 848), "Parker Community Center (SW)"),
        ((1899, 856), "Pier 98 (NE)"),
        ((2036, 857.5), "3210 E Hwy 98 (NE)"),
        ((2352, 879), "Parker Public Library (SW)"),
        ((2055, 898), "Dan's Pawn (NE)"),
        ((1952, 919), "? (L958) (SW)"),
        ((2218, 922), "Coyote's (SE)"),
        ((1881, 932), "6218 E Hwy 98 (E)"),
        ((2158, 932), "Coyote's (SW)"),
        ((2071, 932), "Dan's Pawn (SE)"),
        ((2300, 943.5), "Parker City Hall (SW)"),
        ((1842, 947), "? (L957) (NE)"),
        ((2333, 951), "Parker Police Station (SW)"),
        ((1789, 1037), "Seclusion Bay"),
        ((1833, 1037), "? (L956) (N)"),
        ((1937, 1124), "? (L669) (SE)"),
        ((1941, 1161), "? (L668) (SW)"),
        ((1946, 1189), "? (L667) (SW)"),
        ((2243, 1200), "Welcome to Port Gellhorn Sign"),
        ((1978, 1219), "? (L666) (SE)"),
        ((2035, 1239), "? (L665) (SE)"),
        ((2097, 1243), "Mr. Bingo (SW)"),
        ((2167, 1243), "Mr. Bingo (SE)"),
        ((2200, 1300), "4937 E Hwy 98 (Gas Station) (NE)"),
        ((2185, 1325), "4937 E Hwy 98 (Gas Station) (SE)"),
        ((2184, 1341), "4937 E Hwy 98 (Store) (NE)"),
        ((2184, 1365), "4937 E Hwy 98 (Store) (SE)"),
        ((1730.5, 1465.5), "Centerplate"),
        ((2048, 1555), "Wine Country Motor Sports"),
        ((2121, 1565), "Guardhouse"),
        ((1787, 1611), "Sebring International Raceway (T17)"),
        ((2129, 1861), "Sebring International Raceway (T7)"),
        #((2268, 347), "1703 E 5th St (Shack)"),
        #((2144, 393), "Lucky Plucker"),
        #((2164, 494), "6232 E Hwy 98"),
        #((2314, 353), "1703 E 5th St (Warehouse)"),
        #((2021, 553), "Wildfire Scooters"),
    ],
    "[L1/4] Diner (N)": [
        ((721.5, 791), "Player"),
        ((1075, 15), "Mount Waffles (TW)"),
        ((1225, 90), "Train Tunnel (W)"),
        ((1544, 50), "Mount Mountain (T)"),
    ],
    "[L1/4] Diner (W)": [
        ((549, 155), "Sunshine Skyway Bridge (N)"),
        ((713, 171), "Water Tower (North Port Gellhorn)"),
        ((885, 721), "Player"),
    ],
    "[L1/4] Car Wash": [
        # ((670, 450), "Pylon (77)"),
        ((685, 466), "Pylon (C)"),
        ((734, 507), "Springfield Community Church"),
        ((743, 405), "Tall Double Billboard"),
        #((1011, 641), "Player")
        ((1029, 685), "Player")
    ],
    "[L1/6] Sidewalk (Jason) (E)": [
        ((167, 86), "W South Beach (SE)"),
        ((174, 129), "Hotel (E)"),
        ((607.5, 19.5), "1000 Venetian Way (SW)"),
        # ((646, 380), "Player"),
        ((715.5, 84), "Flamingo South Beach (RS)"),
        ((741, 89), "Flamingo South Beach (S)"),
        ((771, 107), "Old City Hall"),
        ((967, 65), "The Floridian"),
        ((970, 101), "West Venetian Causeway Bridge"),
        ((1073, 53), "Continuum on South Beach (S)"),
        ((1119, 59), "Portofino Tower (NE)"),
        ((1133, 59), "Portofino Tower (NW)"),
        ((1253, 107), "Margaret Pace Park"),
    ],
    "[L1/7] Port": [
        ((295, 344), "Murano Grande"),
        ((469, 540), "Blackstone Apartments"),
        ((817, 399), "Portofino Tower (NW)"),
        ((862, 401), "Portofino Tower (S)"),
    ],
    "[L1/8] Gas Station (Lucia)": [
        ((18, 415), "Pylon (A)"),
        # ((106, 871), "Player"),
        ((546, 392), "Pylon (B)"),
        ((807, 453), "Pylon (C)"),
        #((840, 458), "Pylon (77)"),
        ((853, 311), "4937 E Hwy 98 (Gas Station) (NE)"),
        ((868, 422), "Port Gellhorn Smokestack"),
        ((893.5, 543.5), "6232 E Hwy 98 (SE)"),
        ((924, 490.5), "Large White Billboard"),
        ((930, 479), "Oval Yellow Sign"),
        ((946, 511), "Springfield Community Church"),
        ((965, 499), "Tall Yellow Sign"),
        ((978.5, 491), "Tall Double Billboard"),
        ((1023, 548), "Coyote's (SE)"),
        ((1113, 536), "1703 E 5th St (Warehouse) (NW)"),
        ((1134.5, 536), "1703 E 5th St (Warehouse) (SW)"),
        ((1181, 492), "Billboard (Hank's Waffles)"),
        ((1214, 489), "Waffles Ridge"),
        ((1305, 558), "Parker Community Center (SW)"),
        ((1356, 352), "Billboard (Delights)"),
        ((1376, 559), "Parker City Hall (SW)"),
        ((1451, 458.5), "Welcome to Port Gellhorn Sign"),
        ((1541, 559.5), "Parker Police Station (SW)"),
        ((1529, 438), "Mount Waffles (W)"),
        ((1597, 417), "Mount Waffles (TW)"),
    ],
    "[L1/10] Pawn Shop (W)": [
        ((514, 400), "Player"),
    ],
    "[L1/10] Pawn Shop (S)": [
        ((518, 459), "Player"),
    ],
    "[L1/13] House with Boat (X)": [
        ((2996.5, 599), "House D (W)"),
        ((3054, 616), "House D (SW)"),
    ],
    "[L1/15] Park": [
        ((325, 307), "Hotel Breakwater"),
        ((781.5, 695), "Player"),
        ((1033, 536), "Art Deco Welcome Center (S)"),
        ((1142, 409.5), "1500 Ocean Dr")
    ],
    "[L1/15] Bar": [
        ((779.5, 702), "Player"),
    ],
    "[L1/15] Glitch (A)": [
        ((243, 121.5), "112 NE 41st St"),
    ],
    "[L1/17] Hotel (E)": [
        ((851, 496), "Player"),
    ],
    "[L1/17] Hotel (W)": [
        ((48, 801), "Minimap (TL)"),
        ((378, 887), "Minimap (N)"),
        ((386, 1026), "Minimap (BR)"),
        ((800, 712), "Player"),
        ((834, 343), "Brown Hotel Sign"),
    ],
    "[L1/20] Gas Station (Jason)": [
        ((212, 159), "4937 E Hwy 98 (Gas Station) (SE)"),
        ((351, 360), "Pylon (A)"),
        ((466, 398), "Ferris Wheel (Port Gellhorn)"),
        ((555, 413), "Mr. Bingo (SE)"),
        ((671, 710), "Player"),
        ((694, 362), "Pylon (B)"),
        ((883, 305), "4937 E Hwy 98 (Gas Station) (NE)"),
        ((903, 372), "Port Gellhorn Smokestack"),
        ((1109, 410), "Billboard (Hank's Waffles)"),
        ((1132, 406), "Waffles Ridge"),
        ((1223.5, 318), "Billboard (Delights)"),
        ((1233, 454), "Parker City Hall (SW)"),
        ((1277.5, 390), "Welcome to Port Gellhorn Sign"),
        ((1339, 372), "Mount Waffles (W)"),
    ],
    "[L1/21] Ocean near Keys (N)": [
        ((87, 444), "Seven Mile Bridge (6T)"),
        ((448, 475), "Seven Mile Bridge (3T)"),
        ((953, 435.5), "Blue Billboard (Key Lento)"),
        ((1138, 302), "99353 Overseas Hwy"),
        ((1417, 459), "Four Seasons Hotel Miami (BW)"),
        ((1685, 478), "102180 Overseas Hwy"),
    ],
    "[L1/21] Ocean near Keys (E)": [
        ((782, 403), "Sombrero Key Light (B)"),
        ((781, 299), "Sombrero Key Light (T)"),
    ],
    "[L1/22] Metro (NE) (B)": [
        ((757, 937), "Player")
    ],
    #"[L1/22] Metro (SE) (A)": [
    #    ((878, 272), "Park Grove Condominium (S)"),
    #    ((894, 267), "Park Grove Condominium (N)"),
    #],
    "[L1/22] Metro (SE) (A) (4K)": [
        ((346, 244), "Four Seasons Hotel Miami (40NE)"),
        ((420, 237.5), "Four Seasons Hotel Miami (40NW)"),
        ((486, 248.5), "Four Seasons Hotel Miami (40W)"),
        #((350, 316), "Four Seasons Hotel Miami (32NE)"),
        ((356, 302), "Nine at Mary Brickell Village (A)"),
        ((405, 307), "Nine at Mary Brickell Village (B)"),
        ((454, 311), "Nine at Mary Brickell Village (C)"),
        ((474, 313), "Nine at Mary Brickell Village (D)"),
    ],
    "[L1/22] Metro (SE) (B)": [
        ((175, 160), "Nine at Mary Brickell Village (A)")
    ],
    "[L1/26] Loading Zone near Prison (SW)": [
        ((764, 740), "Player"),
        ((927, 233), "Water Tower near Prison"),
    ],
    "[L1/27] Highway (N)": [
        ((1128, 356.5), "112 NE 41st St"),
    ],
    "[L1/27] Highway (NE)": [
        ((1219, 125), "112 NE 41st St"),
        ((1554, 156), "The Ritz-Carlton Bal Harbour"),
        ((1685, 125), "Akoya Condominium"),
        ((1818, 82), "Jade Ocean Condos"),
    ],
    "[L1/29] Welcome Center (E)": [
        ((167, 149), "Art Deco Welcome Center (S)"),
        ((821, 717), "Player"),
    ],
    "[L1/29] Welcome Center (W)": [
        ((852, 681), "Player"),
        ((1518, 72), "Art Deco Welcome Center (S)"),
    ],
    "[L1/30] Store": [
        ((1112, 416), "Player")
    ],
    "[L1/32] Police Chase (A)": [
        ((63, 839), "Minimap (TL)"),
        ((165, 1010), "Minimap (N)"),
        ((334, 1010), "Minimap (BR)"),
        ((1410, 383), "White Billboard (Hamlet)"),
    ],
    #"[L1/32] Police Chase (B)": [
    #    ((1094, 185), "White Billboard (Hamlet)"),
    #],
    #"[L1/32] Police Chase (C)": [
    #    ((1621, 245), "White Billboard (Hamlet)"),
    #],
    "[L1/32] Police Chase (D)": [
        ((63, 839), "Minimap (TL)"),
        ((165.5, 1010), "Minimap (N)"),
        ((334, 1010), "Minimap (BR)"),
        ((577, 45), "Red Billboard (Hamlet)")
    ],
    "[L1/32] Police Chase (J)": [
        ((63, 839), "Minimap (TL)"),
        ((183, 1010), "Minimap (N)"),
        ((334, 1010), "Minimap (BR)"),
    ],
    "[L1/36] Alley (W)": [
        ((617, 64), "Flamingo South Beach (TE)"),
    ],
    "[L1/37] Airport (X)": [
        ((63, 839), "Minimap (TL)"),
        ((64, 903.5), "Minimap (N)"),
        ((334, 1010), "Minimap (BR)"),
        ((187, 34), "Pole near Signature Hangar 2"),
        ((319, 248), "Signature Hangar 2 (NW)"),
        ((460, 195), "Signature Hangar 2 (W)"),
        ((1118, 145), "Bank of America Financial Center"),
        ((1641.5, 122.5), "Latitude on the River (S) (NW)"),
        ((1678.5, 122), "Latitude on the River (S) (SW)"),
        ((1815.5, 96), "Nine at Mary Brickell Village (A)"),
        ((1829.5, 96), "Nine at Mary Brickell Village (B)"),
        ((1846, 95), "Nine at Mary Brickell Village (C)"),
        ((1852.5, 95), "Nine at Mary Brickell Village (D)"),
        ((1897, 96), "Nine at Mary Brickell Village (E)")
    ],
    "[L1/42] Tennis Court (SE)": [
        ((759.25, 91.75), "1000 Venetian Way (SW)"),
        ((1039, 226), "Old City Hall"),
        ((1158.5, 159), "Icon at South Beach"),
        ((1555, 165), "Portofino Tower (NE)"),
        ((1581, 164), "Portofino Tower (NW)"),
    ],
    "[L1/44] Tennis Stadium (4K)": [
        ((434, 1040), "Homestead Water Tower"),
        ((434, 1096), "Homestead Water Tower (B)"),
        ((453, 1076), "Prison Tower (4)"),
        ((512.5, 1076), "Prison Tower (3)"),
        ((547.5, 1076), "Prison Tower (5)"),
        ((666, 1076), "Prison Tower (2)"),
        ((694.5, 1076), "Prison Tower (6)"),
        ((787, 936), "Park Grove Condominium (S)"),
        ((3267, 315.5), "Four Seasons Hotel Miami (SW)"),
        ((3310, 263), "Four Seasons Hotel Miami (SE)"),
        ((3323, 684), "Four Seasons Hotel Miami (HB28SE)"),
        ((3338, 985), "Four Seasons Hotel Miami (HB8SE)"),
        ((3354, 222), "Four Seasons Hotel Miami (HB58SE)"),
        ((3364, 225.5), "Four Seasons Hotel Miami (HB58NE)"),
        ((3396, 499.5), "Four Seasons Hotel Miami (40E)"),
        ((3501, 230.5), "Four Seasons Hotel Miami (NE)"),
        ((3500.929, 250), "Four Seasons Hotel Miami (56NE)"),
        ((3509.5, 492), "Four Seasons Hotel Miami (40NE)"),
        ((3509.048, 615), "Four Seasons Hotel Miami (32NE)"),
        ((3616, 851.5), "Nine at Mary Brickell Village (E)"),
    ],
    "[L1/48] Hangar (A)": [
        ((1312, 726), "Pole near Signature Hangar 2"),
        ((1425, 864), "Signature Hangar 2 (NW)"),
        ((1555, 823), "Signature Hangar 2 (W)"),
    ],
    "[T1/1] Prison": [
        ((64, 874.5), "Opera Tower"),
        ((583, 882), "Miami Tower"),
        ((645, 867.5), "Wells Fargo Center (N)"),
        ((779, 832), "Southeast Financial Center"),
        ((1124, 797), "Four Seasons Hotel Miami (NW)"),
        ((1141, 792), "Four Seasons Hotel Miami (BW)"),
        ((1173, 794), "Four Seasons Hotel Miami (BE)"),
        ((1179, 801), "Four Seasons Hotel Miami (SE)"),
        ((1204, 43), "WDNA FM"),
        ((1701, 911), "Park Grove Condominium (S)"),
        ((2058, 985), "Prison Tower (1)"),
        ((2224, 983), "Prison Tower (2)"),
        ((2503, 980), "Prison Tower (3)"),
        ((2538, 984), "Prison Tower (6)"),
        ((2555, 986), "Keys Bridge (C)"),
        ((2747, 981), "Prison Tower (4)"),
        ((2993, 976), "Tall Billboard"),
        ((3063, 981), "Prison Tower (5)"),
        ((3381, 945), "Turkey Point Nuclear Power Station (N)"),
        ((3481, 945), "Turkey Point Nuclear Power Station (S)"),
        ((3670, 912), "Turkey Point Nuclear Power Station (1)"),
        ((3731, 912), "Turkey Point Nuclear Power Station (2)"),
        ((3797, 912), "Turkey Point Nuclear Power Station (3)"),
    ],
    "[T1/6] Vice Beach": [
        ((38, 570), "Murano Grande"),
        ((61, 1172), "Congress Hotel"),
        ((141, 1152), "Cavalier Hotel"),
        ((225, 1144), "Leslie Hotel"),
        ((247, 556), "Icon at South Beach"),
        ((452, 754), "Container Crane (1)"),
        ((552, 791), "Construction Crane (1) (Vice Beach)"),
        ((675, 1244), "The Villa Casa Casuarina"),
        ((705, 975), "Miami Beach Parking Garage (SE)"),
        ((829, 1166), "Winter Haven"),
        ((945, 1221), "McAlpin Ocean Plaza"),
        ((961, 633), "Asia Brickell Key"),
        ((991, 840), "Old City Hall"),
        ((1059.5, 592.5), "Four Seasons Hotel Miami (BE)"),
        ((1110, 597.5), "Four Seasons Hotel Miami (NW)"),
        ((1159, 830), "Cruise Terminal G (B)"),
        ((1301, 688), "The Floridian"),
        ((1354, 1334), "Cardozo South Beach"),
        ((1537, 575), "Southeast Financial Center"),
        ((1582, 879), "1500 Ocean Dr"),
        ((1681.5, 643.5), "Wells Fargo Center (N)"),
        ((1710, 631), "The Waverly South Beach (SE)"),
        ((1972, 741), "FAA Miami ATCT (MIA)"),
        ((2079, 708.5), "Miami-Dade County Courthouse"),
        ((2275, 752), "Unknown Building near VCIA (S)"),
        ((2294, 752), "Unknown Building near VCIA (N)"),
        ((2625, 805), "Royal Palm South Beach (S)"),
        ((2724, 606), "Flamingo South Beach (TE)"),
        ((2742, 602), "Flamingo South Beach (TC)"),
        ((2764, 606), "Flamingo South Beach (TNE)"),
        ((2882, 797), "Royal Palm South Beach (N) (S)"),
        ((2978, 797), "Royal Palm South Beach (N) (N)"),
        ((2982, 594), "Opera Tower"),
        ((3082, 615), "The Grand"),
        ((3288, 829), "Flamingo South Beach (NENE)"),
        #((3320, 575), "Quantum on the Bay (S)"),
        ((3321, 760), "1000 Venetian Way (SW)"),
        ((3340, 575), "Quantum on the Bay Condominium (S) (NE)"),
        ((3350, 760), "1000 Venetian Way (SE)"),
        ((3384, 613), "Quantum on the Bay Condominium (N) (NE)"),
        ((3475, 807), "Capri South Beach (SE)"),
        ((3715, 1028), "Loews Miami Beach (S)"),
    ],
    "[T1/10] Beach": [
        ((601, 427), "101 Ocean Dr (SE)"),
        ((1231.5, 549.5), "Royal Atlantic Condominium (SE)"),
        ((1517, 786), "Jenny Hostel"),
        ((1672, 800), "Bank of America Financial Center (SW)"),
        ((1773, 738), "Bank of America Financial Center"),
        ((1834, 863), "Hotel Breakwater"),
        ((1994, 734), "Akoya Condominium"),
        ((2163, 601), "Jade Ocean Condos (NW)"),
        ((2198.5, 596), "Jade Ocean Condos (SW)"),
        ((2244.5, 596), "Jade Ocean Condos (SE)"),
        ((2326, 699), "1st St Lifeguard Tower"),
        ((2436, 672), "Green Diamond"),
        ((2444.5, 680), "Loews Miami Beach"),
        ((2510, 688), "Trésor Tower"),
        ((2578, 732), "Royal Palm South Beach (S)"),
        ((2655, 907), "3rd St Lifeguard Tower"),
        ((2687, 734), "Royal Palm South Beach (N) (S)"),
        ((2718, 1206), "Beach (B)"),
        ((2798, 929), "4th St Lifeguard Tower"),
        ((2937, 734), "1500 Ocean Dr"),
        ((3123.5, 956.5), "5th St Lifeguard Tower"),
        ((3177, 1063), "Beach (D)"),
        ((3208, 1031), "Beach (E)"),
        ((3279, 964), "6th St Lifeguard Tower"),
        ((3340, 973), "8th St Lifeguard Tower"),
        ((3409, 989), "14th St Lifeguard Tower"),
        ((3422, 1095), "Beach (C)"),
        ((3461, 980.5), "10th St Lifeguard Tower"),
        ((3514.5, 986.5), "12th St Lifeguard Tower"),
        ((3664, 1020), "Beach (F)"),
        ((3840, 1741), "Beach (A)"),
    ],
    "[T1/16] Venetian Islands": [
        ((133.5, 219), "Akoya Condominium"),
        ((452, 131), "Jade Ocean Condos"),
        ((640, 702), "Di Lido Island (N)"),
        ((660, 575), "Pelican Harbor Marina (E)"),
        ((841, 573), "Pelican Harbor Marina (D)"),
        ((900, 274), "Pelican Harbor Radio Tower"),
        ((1177, 233), "Green Diamond"),
        ((1262, 550), "Pelican Harbor Marina (C)"),
        ((1270, 546), "Pelican Harbor Marina (B)"),
        ((1310.5, 235), "Blue Diamond"),
        ((1654, 321), "Sunset Harbour South Condo"),
        ((1476, 276), "Trésor Tower"),
        ((1598, 522), "Pelican Harbor Marina (A)"),
        ((1838, 298), "Construction Crane (3) (Vice Beach)"),
        ((1906, 321), "Construction Crane (2) (Vice Beach)"),
        ((1984, 495), "East Venetian Causeway Bridge"),
        ((2099, 348), "W South Beach (SE)"),
        ((2326, 361.5), "Bank of America Financial Center (NW)"),
        ((2332.5, 328.5), "Bank of America Financial Center"),
        ((2351, 585), "Rivo Alto Island (S)"),
        ((2359, 361.5), "Bank of America Financial Center (SW)"),
        ((2716, 384), "1000 Venetian Way (SW)"),
        ((2781, 328), "Loews Miami Beach"),
        ((2902, 402), "Flamingo South Beach (NWNW)"),
        ((2917, 1089), "Biscayne Island (S)"),
        ((3056, 368), "1500 Ocean Dr"),
        ((3248, 638), "Flagler Memorial Island (N)"),
        ((3255.5, 249), "Flamingo South Beach (TNE)"),
        ((3309, 246), "Flamingo South Beach (TW)"),
        ((3335, 738), "Di Lido Island (S)"),
        ((3568, 548), "Flagler Memorial Monument"),
        ((3625, 564), "Pier (Flamingo)"),
        ((3681.5, 387), "Flamingo South Beach (RS)"),
        ((3807, 405), "Flamingo South Beach (S)"),
    ],
    "[T1/19] Keys": [
        ((667, 98), "Island V (S)"),
        ((856, 94), "Island W (N)"),
        ((960, 1371.5), "US Coast Guard Station Islamorada"),
        ((1611, 1159), "New Bahia Honda Bridge (W)"),
        ((1915, 172), "Unnamed Building #1 (Blimp Key)"),
        ((1965, 176), "Unnamed Building #2 (Blimp Key)"),
        ((2026, 74), "Seven Mile Bridge (E)"),
        ((2075, 184), "Unnamed Building #3 (Blimp Key)"),
        ((2125.5, 92), "Seven Mile Bridge (5B)"),
        ((2171, 1141), "Old Bahia Honda Bridge (WB)"),
        ((2176, 1080), "Old Bahia Honda Bridge (W)"),
        ((2412, 134.5), "Seven Mile Bridge (20B)"),
        ((2534, 33.5), "Sombrero Key Light (B)"),
        ((2558, 147), "Seven Mile Bridge (W)"),
        ((2763, 339), "New Bahia Honda Bridge (E)"),
        ((2830, 146), "Blimp Bay"),
        ((3033, 627), "Old Bahia Honda Bridge (EB)"),
        ((3038.5, 559), "Old Bahia Honda Bridge (E)"),
    ],
    "[T1/20] Rooftop Party": [
        ((161, 795), "1500 Ocean Dr"),
        ((663, 700), "Villa del Mare"),
        ((667, 717), "Loews Miami Beach"),
        ((698, 1476), "W South Beach (BNW)"),
        ((764, 563), "Continuum on South Beach (S)"),
        #((834, 1504), "W South Beach (BNW)"),
        ((852, 692), "Palazzo del Sol"),
        ((929, 671), "South Pointe Tower"),
        ((1178, 564), "Portofino Tower (NW)"),
        ((1354, 950), "Park@420 Lincoln Rd (SE)"),
        ((1412, 1279), "Portugal Tower Condominium (SE)"),
        ((1475, 768), "Old City Hall"),
        ((2394, 613), "The Waverly South Beach (SE)"),
        ((2789, 744), "Cruise Terminal G (D)"),
        ((2612, 610), "Flamingo South Beach (TE)"),
        ((2817, 815), "Flamingo South Beach (NENE)"),
        ((2862, 868), "1111 Lincoln Rd (SE)"),
        ((2909, 743), "Cruise Terminal G (C)"),
        ((2980, 744), "Cruise Terminal G (B)"),
        #((3047, 580), "Asia Brickell Key"),
        ((3053, 546), "Asia Brickell Key"),
        ((3058, 798), "Capri South Beach (SE)"),
        ((3099, 741), "Cruise Terminal G (A)"),
        ((3129, 880), "1111 Lincoln Rd (NW)"),
        ((3160, 794), "Flamingo South Beach (NWNE)"),
        ((3201, 767), "Flagler Memorial Monument"),
        ((3262, 762), "Dodge Island (N)"),
        ((3350, 489), "Four Seasons Hotel Miami (BE)"),
        ((3391, 489), "Four Seasons Hotel Miami (BW)"),
        ((3491, 597), "InterContinental Miami (N)"),
    ],
    "[T1/44] U-Turn (NW)": [
        ((447, 642), "6232 E Hwy 98 (SE)"),
        ((2312, 709), "6232 E Hwy 98 (NE)"),
        ((2384, 224), "Radio Tower (Port Gellhorn)"),
        ((3693, 841), "Lucky Plucker (SW)"),
    ],
    "[T1/44] U-Turn (NE)": [
        ((237, 494), "Tall Yellow Sign"),
        ((277, 661), "Tall Double Billboard"),
        ((744, 735), "1703 E 5th St (Shack) (SW)"),
        ((1231, 747), "1703 E 5th St (Shack) (SE)"),
        ((1513, 723), "1703 E 5th St (Warehouse) (NW)"),
    ],
    "[T2/1] Key Lento": [
        ((328, 521), "Island G (E)"),
        ((519, 515), "Island G (W)"),
        ((743, 743), "164 Pompano Dr"),
        ((849, 855), "200 Pompano Dr"),
        ((891, 723), "180 Pompano Dr"),
        ((900, 488), "Island J (E)"),
        ((966, 484), "Island J (W)"),
        ((909, 468.5), "Tree on Island J"),
        ((1440, 327), "Radio Tower (Key Lento)"),
        ((1508, 681), "Unknown Residential Building"),
        ((1788, 448), "Billboard #1 (Key Lento)"),
        ((1893, 428.5), "Billboard #2 (Key Lento)"),
        ((1923, 357), "99353 Overseas Hwy"),
        ((1987, 428), "Blue Billboard (Key Lento)"),
        ((2009, 389), "102180 Overseas Hwy"),
        ((2101.5, 468), "Marina Club at Blackwater Sound (S)"),
        ((2249, 470), "Marina Club at Blackwater Sound (N)"),
        ((2571, 733), "500 Pompano Dr"),
        ((2733, 434), "New Bahia Honda Bridge (E)"),
        ((2961, 543), "House C (E)"),
        ((3077, 523), "House D (E)"),
        ((3117, 434), "New Bahia Honda Bridge (W)"),
        ((3138, 430), "US Coast Guard Station Islamorada"),
        ((3311, 470.5), "Island V (S)"),
        ((3432, 417), "Naval Air Station Key West (1)"),
        ((3506, 419), "Naval Air Station Key West (2)"),
        ((3631, 422), "Naval Air Station Key West (3)"),
        ((3764.5, 421), "Naval Air Station Key West (4)"),
        ((3799.5, 423), "SFUWO School"),
    ],
    "[T2/67] Television": [
        ((3582, 609), "Bridge Island (W)"),
    ],
    "[T2/77] Chase (2)": [
        ((0, 932), "New Foundation Church"),
        ((73, 923), "Juice Fruit Sign"),
        ((302, 676), "Sunshine Skyway Bridge (N)"),
        ((373, 597), "Sunshine Skyway Bridge (S)"),
        ((788, 39), "Radio Tower (Port Gellhorn)"),
        # ((1894, 498), "Pylon (77)"),
        ((1834, 586), "Pylon (C)"),
        ((2447, 775), "Wildfire Scooters (NW)"),
        ((3787.5, 457.5), "Oval Yellow Sign"),
    ],
    "[S2/39] Vice City 03 (Basketball)": [
        ((109, 276), "Bank of America Financial Center (NW)"),
        ((198.5, 371), "One Miami Condominium East (NE)"),
        ((248.5, 371), "One Miami Condominium West (NE)"),
        ((272.5, 507.5), "Flamingo South Beach (NENE)"),
        ((287, 440), "InterContinental Miami (N)"),
        ((360, 508), "Flamingo South Beach (NENW)"),
        ((392, 419), "Citigroup Center (NE)"),
        ((475, 304), "Southeast Financial Center"),
        ((748.5, 477), "Capri South Beach"),
        ((756.5, 1402.5), "Brown Hotel Sign"),
        ((577, 514), "Flamingo South Beach (NWNE)"),
        ((594, 515), "Flamingo South Beach (NWNW)"),
        ((624, 485), "Capri South Beach (SE)"),
        ((669.5, 388), "Wells Fargo Center (S)"),
        ((694.5, 388), "Wells Fargo Center (N)"),
        ((880, 461.5), "1111 Lincoln Rd (SE)"),
        ((935.5, 544), "New World Center"),
        ((984, 1833), "W South Beach (BNW)"),
        ((1092, 452), "Loft Downtown II"),
        ((1150, 382.5), "Vizcayne South Condiminium (S)"),
        ((1210, 382.5), "Vizcayne South Condiminium (N)"),
        ((1230, 466.5), "1111 Lincoln Rd (NW)"),
        ((1345, 426.5), "Stephen P. Clark Government Center (NW)"),
        ((1463.5, 371), "Marina Blue (NE)"),
        ((1597, 375), "Marquis Miami (SE)"),
        ((1645.5, 375), "Marquis Miami (NE)"),
        ((1649, 363), "Marquis Miami (TNE)"),
        ((1778, 410), "The Gates Hotel South Beach (NE)"),
        #((1850, 1786), "W South Beach (BNW)"),
        ((1880, 395), "Marriott Miami Biscayne Bay (S)"),
        ((1920, 392), "Marriott Miami Biscayne Bay (E)"),
        ((1949, 392), "Marriott Miami Biscayne Bay (NE)"),
        ((2043.5, 322.5), "Opera Tower"),
        ((2100, 343), "The Grand"),
        ((2264, 373), "1800 Club"),
        ((2359, 552), "Venetian Isle Condominium"),
        ((2414, 300), "Quantum on the Bay Condominium (S) (NE)"),
        ((2479, 346), "Quantum on the Bay Condominium (N) (NE)"),
        ((2543, 695), "Rivo Alto Island (N)"),
        ((2560, 581), "419 NE 4th Ave (W)"),
        ((2613.5, 440), "The Crimson (CC)"),
        ((2618, 582), "333 S Miami Ave (SE)"),
        ((2661, 582), "333 S Miami Ave (NE)"),
        ((2667, 1034), "Motel Ankara"),
        ((2680.5, 555), "Uptown Lofts (SE)"),
        ((2709, 555), "Uptown Lofts (NE)"),
        ((2737, 552), "Uptown Lofts"),
        ((2770, 512), "22 Biscayne Bay"),
        ((2861, 661), "Di Lido Island (N)"),
        ((2879, 628), "Marina (Stockyard) (NE)"),
        ((2884, 443), "New Wave Condominiums"),
        ((3009, 556.5), "2800 Biscayne Blvd (SE)"),
        ((3264, 1592), "Canal (Hotel Valetta)"),
        ((3604.5, 505), "2421 Lake Pancoast Dr (SE)"),
        ((3406, 183), "Sunset Harbour South Condo"),
    ],
    "[S2/46] Leonida Keys 01 (Airplane) (X)": [
        ((31, 911), "Unnamed Building #1 (Blimp Key)"),
        ((56.5, 546), "Titan America (?)"),
        ((173, 694), "Island S (E)"),
        ((428, 548), "FAA Miami ATCT (MIA)"),
        ((498, 564.5), "Homestead Water Tower"),
        ((415, 592), "Prison Tower (6)"),
        ((465, 591), "Prison Tower (1)"),
        ((514.5, 591.5), "Prison Tower (5)"),
        ((585, 590.5), "Prison Tower (2)"),
        ((687, 590), "Prison Tower (4)"),
        ((699, 590), "Prison Tower (3)"),
        ((458, 693.5), "Island U (S)"),
        ((609, 349), "WDNA FM"),
        ((709, 927), "Island N (W)"),
        ((777, 713), "Island V (S)"),
        ((925, 592), "Red Billboard (Hamlet)"),
        ((998.5, 598.5), "White Billboard (Hamlet)"),
        ((1224, 471), "Four Seasons Hotel Miami (BW)"),
        ((1196.5, 546), "Park Grove Condominium (N)"),
        ((1215, 546), "Park Grove Condominium (C)"),
        ((1233, 546), "Park Grove Condominium (S)"),
        ((1246, 471), "Four Seasons Hotel Miami (BE)"),
        ((1350, 916), "Island N (E)"),
        ((1413, 512), "Asia Brickell Key"),
        # ((1466, 715), "Island W (S)"),
        ((1483, 584), "Turkey Point Nuclear Power Station (CNW)"),
        ((1503.5, 584), "Turkey Point Nuclear Power Station (CNE)"),
        ((1519.5, 585), "Turkey Point Nuclear Power Station (CSW)"),
        ((1528, 571), "Turkey Point Nuclear Power Station (N)"),
        ((1537.5, 585), "Turkey Point Nuclear Power Station (CSE)"),
        ((1553, 571), "Turkey Point Nuclear Power Station (S)"),
        ((1652.5, 556), "Turkey Point Nuclear Power Station (1)"),
        ((1669, 556), "Turkey Point Nuclear Power Station (2)"),
        ((1685, 556), "Turkey Point Nuclear Power Station (3)"),
        ((1711.5, 1022), "Seven Mile Bridge (W)"),
        ((1753, 636), "Bridge Island (W)"),
        ((1814, 534), "Portofino Tower (NW)"),
        ((1878.5, 590), "Keys Bridge (C)"),
        ((1899, 540), "Continuum on South Beach (S)"),
        ((1990, 651.5), "Island A (W)"),
        ((1994.5, 951), "Seven Mile Bridge (20B)"),
        ((2059, 657), "Key Lento (A)"),
        #((2080, 627.5), "House D (W)"),
        ((2084, 629), "House D (SW)"),
        ((2109, 641), "House with Boat (X)"),
        ((2295, 609), "102180 Overseas Hwy"),
        ((2311, 789), "Seven Mile Bridge (6T)"),
        # ((2324, 789), "Seven Mile Bridge (5T)"),
        ((2327, 813.5), "Seven Mile Bridge (5B)"),
        ((2351.5, 786.5), "Seven Mile Bridge (3T)"),
        ((2363, 702.5), "Blue Billboard (Key Lento)"),
        ((2383.5, 770), "Seven Mile Bridge (E)"),
        ((2477, 568), "99353 Overseas Hwy"),
        ((2809, 719), "Key Lento (J)"),
        ((2833, 1131), "Blimp Bay"),
        ((3081.5, 683.5), "Island J (E)"),
        ((3097.5, 669), "Tree on Island J"),
        ((1237, 745), "Pin A01L"),
        ((1388, 744), "Pin A01R"),
        ((1506, 723), "Pin A02L"),
        ((1653, 722), "Pin A02R"),
        ((1700, 706), "Pin A03L"),
        ((1796, 706), "Pin A03R"),
        ((1822, 690), "Pin A04L"),
        ((1947, 689), "Pin A04R"),
        ((1886, 683), "Pin A05L"),
        ((2004, 682), "Pin A05R"),
        ((1920, 677), "Pin A06L"),
        ((2032, 675), "Pin A06R"),
        ((1907, 668), "Pin A07L"),
        ((1987, 666), "Pin A07R"),
        ((1853, 658), "Pin A08L"),
        ((1926, 655), "Pin A08R"),
        ((2105, 720), "Pin B01L"),
        ((2152, 717), "Pin B01R"),
        ((2039, 715), "Pin B02L"),
        ((2085, 713), "Pin B02R"),
        ((1975, 711), "Pin B03L"),
        ((2020, 709), "Pin B03R"),
        ((1909, 707), "Pin B04L"),
        ((1952, 706), "Pin B04R"),
        ((2102, 731), "Pin C01R"),
        ((2102, 738), "Pin C01R (B)"),
        ((1969, 737), "Pin C02L"),
        ((1986, 732), "Pin C02R"),
        ((1848, 739), "Pin C03L"),
        ((1867, 733), "Pin C03R"),
        ((1704, 739), "Pin C04L"),
        ((1729, 733), "Pin C04R"),
        ((2889, 669), "Pin D01L"),
        ((2929, 670), "Pin D01R"),
        ((2750, 652), "Pin D02L"),
        ((2787, 652), "Pin D02R"),
    ],
    "[S2/56] Ambrosia 01 (Bikers)": [
        ((491, 795), "Wide Billboard #2 (Ambrosia)"),
        ((580, 645), "Billboard with Oval Motif"),
        ((1355, 637), "Wide Billboard #1 (Ambrosia)"),
        ((1357, 730), "Billboard with Irregular Shape"),
        ((1574, 28), "Billboard with Diversity Motif"),
    ],
    "[S2/57] Ambrosia 02 (Panorama)": [
        ((338.5, 807), "Tall Water Tower"),
        ((442, 783), "Wheelabrator South Broward (T)"),
        ((474, 791), "FAA Miami ATCT (MIA)"),
        ((535, 854), "Wheelabrator South Broward (W)"),
        ((575, 839), "WDNA FM"),
        ((812, 824.5), "Flat Water Tower"),
        ((1344, 859), "1500 Sonora Ave (Silo)"),
        #((1388, 819), "Homestead Water Tower"),
        ((1422.5, 791.5), "Titan America (?)"),
        ((1664, 771), "USSM Smokestack (4)"),
        ((1726, 813), "USSM Smokestack (5)"),
        ((1742, 805), "USSM Smokestack (6)"),
        ((1749, 763), "US Sugar Mill (Factory)"),
        #((1751, 831), "US Sugar Mill (Factory)"),
        ((1798, 775), "USSM Smokestack (7)"),
        ((1884, 910), "1500 Sonora Ave (Tank)"),
        ((1895, 860), "USSM Smokestack (8)"),
        ((1907, 886), "USSM Smokestack (9)"),
        ((1961, 886), "USSM Smokestack (10)"),
        ((1976.5, 861), "USSM Smokestack (11)"),
        ((2335.5, 978), "Billboard with Diversity Motif"),
        ((2577, 788), "Very Tall Water Tower"),
        ((2714, 944), "Billboard with Irregular Shape"),
        ((2770, 937), "Billboard with Hat-Shaped Motif"),
        ((2921, 847), "Sebring Water Tower (B)"),
        ((2922, 818), "Sebring Water Tower (T)"),
        ((2995.5, 899), "Billboard with Oval Motif"),
        ((3109.5, 792), "Water Tower near Prison"),
        ((3329, 870), "Billboard with Unknown Motif"),
        ((3453, 1083), "Hendry County Motorsports Park"),
    ],
    "[S2/59] Ambrosia 04 (Fires)": [
        ((108, 947), "Wheelabrator South Broward (W)"),
        ((1848, 463), "Radio Tower (Ambrosia)"),
        ((2148, 899), "Sebring Water Tower (T)"),
        ((2148, 922.5), "Sebring Water Tower (B)"),
        # ((2750, 888), "US Sugar Mill (Factory)"),
        ((2751, 821), "US Sugar Mill (Factory)"),
        ((3279.5, 817), "USSM Smokestack (7)"),
        ((3283, 863), "USSM Smokestack (5)"),
        ((3287, 850), "USSM Smokestack (6)"),
        ((3372, 808), "USSM Smokestack (4)"),
        ((3447, 947), "USSM Smokestack (8)"),
        ((3451, 920), "USSM Smokestack (9)"),
        ((3535, 875), "Sunshine Skyway Bridge (S)"),
        ((3688, 968), "1500 Sonora Ave (Tank)"),
        ((3729, 874), "Sunshine Skyway Bridge (N)"),
    ],
    "[S2/62] Grassrivers 02 (Watson Bay)": [
        ((57.5, 594.5), "Unknown Billboard #1"),
        ((301.5, 532.5), "Miami Tower"),
        ((354, 513), "Wells Fargo Center (N)"),
        ((514, 586), "Latitude on the River (S) (NW)"),
        ((538, 585), "Latitude on the River (S) (SW)"),
        ((604.5, 561.5), "Nine at Mary Brickell Village (A)"),
        ((613, 561.5), "Nine at Mary Brickell Village (B)"),
        ((652, 560), "Nine at Mary Brickell Village (E)"),
        ((771, 562), "Unknown Billboard #2"),
        ((919, 416), "Watson Bay Water Tower"),
        ((945.5, 497), "Four Seasons Hotel Miami (W)"),
        ((1018, 528), "Shark Valley Observation Tower"),
        ((1039, 580), "Portofino Tower (S)"),
        ((1049.5, 532.5), "Unknown Radio Tower (Vice City)"),
        #((1094.5, 547), "Continuum on South Beach (N)"),
        ((1168, 548), "Continuum on South Beach (S)"),
        ((1242, 263), "WDNA FM"),
        ((1245, 592), "Unknown Billboard #3"),
        ((1408.5, 572), "Park Grove Condominium (N)"),
        ((1470.5, 573), "Park Grove Condominium (C)"),
        ((1545, 573), "Park Grove Condominium (S)"),
        ((1657, 634), "Prison Tower (1)"),
        ((1767, 633), "Prison Tower (6)"),
        ((1769, 632.5), "Prison Tower (2)"),
        ((1865, 637), "Tall Billboard"),
        ((1884, 622), "Very Tall Billboard"),
        ((1941, 634), "Prison Tower (3)"),
        ((1990, 633), "Prison Tower (5)"),
        ((2034.5, 634), "Prison Tower (4)"),
        ((2214, 565), "Homestead Water Tower"),
        ((2916.5, 632), "Turkey Point Nuclear Power Station (CNE)"),
        ((2924.5, 632), "Turkey Point Nuclear Power Station (CNW)"),
        ((2957, 608), "Turkey Point Nuclear Power Station (N)"),
        ((3012, 636), "Red Billboard (Hamlet)"),
        ((3034, 608), "Turkey Point Nuclear Power Station (S)"),
        ((3216, 580), "Turkey Point Nuclear Power Station (1)"),
        ((3265, 580), "Turkey Point Nuclear Power Station (2)"),
        ((3316, 580), "Turkey Point Nuclear Power Station (3)"),
        ((3366, 636), "Turkey Point Nuclear Power Station (CSE)"),
        ((3396, 636.5), "Turkey Point Nuclear Power Station (CSW)"),
        #((3454, 646), "Seminole Theatre"),
    ],
    "[S2/71] Vice City Postcard": [
        ((67, 898), "Unknown Building (1) (Virgina Key)"),
        ((155, 898), "Unknown Building (2) (Virgina Key)"),
        ((176.5, 898), "Unknown Structure (1) (Virginia Key)"),
        ((181, 898), "Unknown Structure (2) (Virginia Key)"),
        ((189.5, 896), "Unknown Building (3) (Virginia Key)"),
        ((305, 813), "1000 Venetian Way (SE)"),
        ((449, 817), "1000 Venetian Way (SW)"),
        ((677, 858), "Skyviews Miami Observation Wheel"),
        ((789, 786), "One Miami Condominium East (NE)"),
        ((844, 785.5), "One Miami Condominium West (NE)"),
        ((1018, 774.5), "Four Seasons Hotel Miami (BW)"),
        ((1019, 775.5), "Four Seasons Hotel Miami (NW)"),
        ((1122, 786), "Wells Fargo Center (N)"),
        ((1192, 807.5), "Miami Tower"),
        ((1277.5, 932), "West Venetian Causeway Bridge"),
        ((1328, 726), "Marriott Miami Biscayne Bay (NE)"),
        ((1473, 670), "The Grand"),
        ((1483, 1080), "Picnic Island B (S)"),
        ((1568, 660), "Opera Tower"),
        ((1616, 946), "Margaret Pace Park"),
        ((1720, 1023), "Picnic Island A (N)"),
        ((1805, 589), "Quantum on the Bay Condominium (S) (NE)"),
        ((1908, 635), "Quantum on the Bay Condominium (N) (NE)"),
        ((1973, 1049), "Picnic Island C (S)"),
        ((2007, 903), "419 NE 4th Ave (W)"),
        ((2008, 884), "Embassy Suites Miami Airport (?)"),
        ((2017, 985), "Marina (Stockyard) (SE)"),
        ((2043, 880), "Uptown Lofts (SE)"),
        ((2072, 880), "Uptown Lofts (NE)"),
        ((2087, 732), "The Crimson (CC)"),
        ((2136, 986.5), "Marina (Stockyard) (SW)"),
        ((2137, 874), "Uptown Lofts"),
        ((2148, 995), "Marina (Stockyard) (NE)"),
        ((2159.5, 860), "Unknown Structure (Vice City)"),
        ((2162, 816), "22 Biscayne Bay (SE)"),
        ((2293, 705), "New Wave Condominiums"),
        ((1158, 874), "Venetian Isle Condominium"),
        ((2426.5, 836.5), "Smokestack (1) (Rockridge)"),
        ((2432, 876), "Unknown Building near VCIA (S)"),
        ((2453, 876), "Unknown Building near VCIA (N)"),
        ((2454, 866), "Flat Water Tower"),
    ],
    "[S2/72] Leonida Keys Postcard (X)": [
        ((6, 285), "Turkey Point Nuclear Power Station (1)"),
        ((28, 285), "Turkey Point Nuclear Power Station (2)"),
        ((52, 285), "Turkey Point Nuclear Power Station (3)"),
        ((24, 225), "Icon at South Beach"),
        ((52, 231), "Murano Grande"),
        # ((174, 277), "Central District Wastewater Treatment Plant (1)"),
        ((174, 277), "WTP (1)"),
        # ((174, 277), "Central District Wastewater Treatment Plant (2)"),
        ((181, 277), "WTP (2)"),
        ((180, 224), "Portofino Tower (NW)"),
        ((189.5, 440), "Bridge Island (W)"),
        ((244, 315), "Keys Bridge (N)"),
        ((257, 703), "Island X (S)"),
        ((265, 282), "Miami Marine Stadium (SW)"),
        ((283, 221), "Continuum on South Beach (S)"),
        ((292, 311), "Keys Bridge (C)"),
        ((293.5, 557), "Island Z (S)"),
        ((294, 282), "Miami Marine Stadium (SE)"),
        ((344, 323), "Keys Bridge (S)"),
        ((338.5, 656.5), "Island Y (S)"),
        ((431, 309), "Stiltsville (1)"),
        ((434, 429), "Key Lento (E)"),
        ((442, 312), "Stiltsville (2)"),
        ((522, 302), "Stiltsville (3)"),
        ((531.5, 313.5), "Stiltsville (4)"),
        ((556, 309), "Stiltsville (5)"),
        ((617, 306), "Stiltsville (6)"),
        ((546, 260), "Palazzo del Sol"),
        ((589, 499), "Island A (W)"),
        #((682, 438), "House D (W)"),
        ((686.5, 440.5), "House D (SW)"),
        ((694, 436), "House D (E)"),
        ((697, 450), "House C (W)"),
        ((713.5, 448.5), "House C (E)"),
        ((714, 519), "Key Lento (A)"),
        ((753, 336.5), "Radio Tower (Key Lento)"),
        ((731, 459), "House with Boat (X)"),
        ((874, 392), "500 Pompano Dr"),
        ((917.5, 490), "Marina Club at Blackwater Sound (N)"),
        ((950, 402.5), "Unknown Residential Building"),
        ((970, 401), "200 Pompano Dr"),
        ((990, 402), "180 Pompano Dr"),
        ((1014, 493.5), "Marina Club at Blackwater Sound (S)"),
        ((1131, 471), "102180 Overseas Hwy"),
        ((1380, 792), "Key Lento (W)"),
        ((1383, 424), "Island F (E)"),
        ((1567, 436), "Island F (W)"),
        ((1687, 1130), "Key Lento (V)"),
        ((1707, 686), "Billboard #2 (Key Lento)"),
        ((1848, 486), "Island G (E)"),
        ((1941, 499), "Island G (W)"),
        ((1960, 1190), "Key Lento (U)"),
        ((2326, 581), "Island J (E)"),
        ((2355, 564), "Tree on Island J"),
        ((2486, 613), "Island J (W)"),
        ((2525, 828), "Key Lento (J)"),
        ((196, 1162), "Pin A02R"),
        ((262, 926), "Pin A03L"),
        ((503, 916), "Pin A03R"),
        ((470, 753), "Pin A04L"),
        ((715, 731), "Pin A04R"),
        ((566, 695), "Pin A05L"),
        ((781, 676), "Pin A05R"),
        ((597, 648), "Pin A06L"),
        ((792, 633), "Pin A06R"),
        ((539, 603), "Pin A07L"),
        ((666, 586), "Pin A07R"),
        ((404, 545), "Pin A08L"),
        ((518, 532), "Pin A08R"),
        ((291, 512), "Pin A09L"),
        ((417, 499), "Pin A09R"),
        ((185, 486), "Pin A10L"),
        ((295, 473), "Pin A10R"),
        ((127, 466), "Pin A11L"),
        ((211, 456), "Pin A11R"),
        ((1344, 1004), "Pin B01L"),
        ((1415, 965), "Pin B01R"),
        ((1139, 965), "Pin B02L"),
        ((1216, 930), "Pin B02R"),
        ((949, 931), "Pin B03L"),
        ((1031, 899), "Pin B03R"),
        ((768, 901), "Pin B04L"),
        ((849, 872), "Pin B04R"),
        ((1520, 1163), "Pin C01R"),
        ((1520.5, 1184), "Pin C01R (B)"),
        ((1262, 1307), "Pin C02L"),
        ((1235, 1211), "Pin C02R"),
        ((916, 1378), "Pin C03L"),
        ((910, 1269), "Pin C03R"),
        ((447, 1469), "Pin C04L"),
        ((496, 1344), "Pin C04R"),
        ((1967, 538), "Pin D01L"),
        ((2020, 539), "Pin D01R"),
        ((1631, 475), "Pin D02L"),
        ((1674, 473), "Pin D02R"),
        ((1398, 438), "Pin D03L"),
        ((1433, 436), "Pin D03R"),
        ((1227, 411), "Pin D04L"),
        ((1257, 410), "Pin D04R"),
    ],
    "[S2/73] Port Gellhorn Postcard (X)": [
        ((944, 897), "Water Tower (West Port Gellhorn)"),
        ((1481, 1001), "Port of Tampa Container Crane (1)"),
        ((1500.5, 995), "Port of Tampa Container Crane (2)"),
        ((1706.5, 983.5), "Port of Tampa Container Crane (3)"),
        ((3058, 1094), "New Foundation Church"),
    ],
    "[S2/74] Ambrosia Postcard": [
        ((75, 1021), "Tall Billboard (Ambrosia)"),
        ((307, 988), "USSM Smokestack (1)"),
        ((378, 1107), "USSM Smokestack (2)"),
        #((578, 851), "1500 Sonora Ave (Silo)"),
        ((579, 931), "1500 Sonora Ave (Silo)"),
        ((805, 1059), "USSM Smokestack (3)"),
        ((1013, 915), "Radio Tower (Ambrosia)"),
        ((1463.5, 791), "US Sugar Mill (Factory)"),
        #((1463, 902), "US Sugar Mill"),
        ((1513, 707), "USSM Smokestack (4)"),
        ((1647, 848), "USSM Smokestack (5)"),
        ((1693, 821), "USSM Smokestack (6)"),
        ((1844, 737), "USSM Smokestack (7)"),
        #((2090, 987), "Water Tower near Prison"),
        ((2233, 1442), "US Sugar Mill (Warehouse)"),
        ((2414, 1063), "USSM Smokestack (8)"),
        ((2568, 1512), "US Sugar Mill (Office)"),
        ((2459, 995), "USSM Smokestack (9)"),
        ((2459, 1147), "1500 Sonora Ave (Tank)"),
        ((2835, 967), "USSM Smokestack (10)"),
        ((2904, 986), "Sebring Water Tower (B)"),
        ((2905, 945), "Sebring Water Tower (T)"),
        ((2907, 1073), "USSM Smokestack (11)"),
    ]
}

pixels = {
    " ".join(id_name.split(" ")[1:]): {
        lm_name: xy for (xy, lm_name) in items
    }
    for id_name, items in pixels.items()
}


### LINES ##########################################################################################

lines = {
    "[L1/4] Diner (N)": ([
        #((536, 84), (672, 135.5)),
        ((585, 0), (639, 46)),
        ((504, 0), (562, 37))
    ], []),
    "[L1/4] Diner (W)": ([
        ((1882, 0), (1446, 180)),
        ((1920, 184), (1432, 285)),
        #((1890, 333.5), (1488, 355)),
    ], []),
    "[L1/4] Car Wash": ([
        ((956, 460), (913, 478)),
        ((961, 528), (915, 532)),
        #((961, 549), (915, 546)),
    ], []),
    # "[L1/6] Sidewalk (Jason) (E)": (
    #     ((1783, 24), (1613, 35)),
    #     ((1765, 109), (1612, 110.5)),
    # ),
    "[L1/6] Sidewalk (Jason) (E)": ([], [
        ((171, 0), (203, 164)),
        ((471, 0), (492.5, 187)),
        # ((912, 0), (912, 218)),
        #((1044, 0), (1036.5, 363)),
        ((1413, 0), (1387, 193)),
        #((1433, 0), (1409.5, 170)),
        ((1759.5, 0), (1721, 170)),
        ((1847, 0), (1799.5, 187)),
    ]),
    "[L1/7] Port (SE)": ([
        ((1862, 172), (1524, 257)),
        ((1858, 587), (1561, 575.5)),
    ], []),
    "[L1/8] Gas Station (Lucia)": ([
        ((0, 102), (853, 311)),
        ((0, 215), (853, 369)),
    ], []),
    # "[L1/10] Pawn Shop": (
    #     ((880, 0), (39, 259)),
    #     ((1640, 18), (355, 271.5))
    # ),
    "[L1/10] Pawn Shop (W)": ([
        ((404, 7), (510, 73)),
        ((1126, 0), (1056, 56)),
    ], []),
    "[L1/10] Pawn Shop (S)": ([
        ((900, 15), (455, 185)),
        ((929, 740), (754, 648.5))
    ], []),
    "[L1/13] House with Boat (X)": ([
        #((3470, 456.5), (3367, 483.5)),
        #((3463, 599), (3360, 618)),
        ((3840, 251), (3360, 409)),
        ((3520, 695), (3345, 713)),
    ], [
        #((3360, 409), (3345, 713))
    ]),
    "[L1/15] Park": ([
        ((203, 495), (271, 498)),
        ((203, 426.5), (303, 439.5)),
    ], [
        ((335.5, 95), (336, 1031))
    ]),
    # "[L1/20] Gas Station (Jason)" : (
    #     ((254, 256), (888, 402)),
    #     ((254, 339), (884, 441))
    # ),
    "[L1/20] Gas Station (Jason)" : ([
        # ((212, 159), (883, 305)),
        # ((216, 237), (883, 342))
        ((307, 260), (825, 338)),
        ((0, 304.5), (546, 353)),
    ], []),
    "[L1/22] Metro (NE) (B)": ([], [
        ((250, 199), (282, 398)),
        ((1701, 199), (1667, 398)),
    ]),
    "[L1/29] Welcome Center (E)": ([
        ((0, 630), (566, 405)),
        ((219, 1030), (1187, 241))
    ], [
        ((730, 0), (749.5, 290.5))
    ]),
    "[L1/29] Welcome Center (W)": ([
        ((991, 299), (837.5, 114)),
        ((1613, 443), (1252, 254))
    ], [
        ((1347, 0), (1314, 248))
    ]),
    "[L1/30] Store": ([
        ((52, 827), (83, 778)),
        ((582.5, 818), (594, 771)),
    ], []),
    "[L1/32] Police Chase (A)": ([], [
        ((27, 6), (44, 446))
    ]),
    # "[L1/32] Police Chase (D)": ([], [
    #     ((1206, 141), (1204.5, 258))
    # ]),
    "[T1/1] Prison": ([], [
        ((1204, 43), (1216.5, 880)),
    ]),
    "[T1/20] Rooftop Party": ([
        ((0, 1515), (352, 1492)),
        ((0, 2000), (381, 1960))
    ], [
       ((3764.5, 0), (3696, 983)),
    ]),
    "[T2/67] Television": ([
        ((3650.5, 1200), (3628.5, 1005)),
        ((2857.5, 1110), (3037, 978)),
    ], []),
    # "[S2/46] Leonida Keys 01 (Airplane) (X)": ([], [
    #     ((609, 349), (624, 578)),
    # ]),
    "[S2/62] Grassrivers 02 (Watson Bay)": ([
        ((3186, 1069), (2481, 993.5)),
        ((3168, 1404), (2748, 1322.5))
    ], [
        ((1242, 263), (1248, 592)),
        # ((918.5, 416), (926, 758))
    ]),
}

lines = {
    " ".join(id_name.split(" ")[1:]): items
    for id_name, items in lines.items()
}


### LANDMARKS ######################################################################################

landmarks = {
    "Art Deco Welcome Center (S)": (2019.131, 593.508, 4.124),  # d=0.069 via Welcome Center (E) & Welcome Center (W)
    "Akoya Condominium": (1442.563, 2608.672, 144.117),  # d=2.633 via Venetian Islands & Highway (NE)
    "Asia Brickell Key": (-119.683, -881.354, 185.477),  # d=1.275 via Vice Beach & Leonida Keys 01 (Airplane) (X)
    "Beach (A)": (2160.823, 19.986, 0.000),  # via Beach
    "Beach (B)": (2148.416, 81.443, 0.000),  # via Beach
    "Beach (C)": (2164.590, 198.311, 0.000),  # via Beach
    "Beach (D)": (2152.913, 309.416, 0.000),  # via Beach
    "Beach (E)": (2150.714, 724.551, 0.000),  # via Beach
    "Beach (F)": (2265.994, 1362.246, 0.000),  # via Beach
    "Billboard #2 (Key Lento)": (-3056.172, -6496.183, 25.615),  # d=0.606 via Leonida Keys Postcard (X) & Key Lento
    "Biscayne Island (S)": (297.158, 1085.080, 0.000),  # via Venetian Islands
    "Blimp Bay": (-3990.437, -7343.033, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Blue Billboard (Key Lento)": (-3436.718, -6780.155, 23.305),  # d=0.238 via Ocean near Keys (N) & Leonida Keys 01 (Airplane) (X)
    "Capri South Beach (SE)": (1304.217, 1126.932, 56.105),  # d=0.547 via Vice City 03 (Basketball) & Vice Beach
    "Di Lido Island (N)": (522.400, 1536.923, 0.000),  # via Venetian Islands
    "Di Lido Island (S)": (618.392, 1004.390, 0.000),  # via Venetian Islands
    "FAA Miami ATCT (MIA)": (-2367.083, -771.087, 96.293),  # d=1.362 via Vice Beach & Leonida Keys 01 (Airplane) (X)
    "Flagler Memorial Island (N)": (838.192, 995.963, 0.000),  # via Venetian Islands
    "Flamingo South Beach (NENE)": (1354.704, 1080.222, 50.837),  # d=0.509 via Vice City 03 (Basketball) & Vice Beach
    "Flamingo South Beach (TE)": (1365.815, 936.164, 110.803),  # d=0.138 via Vice Beach & Alley (W)
    "The Floridian": (1262.637, 408.346, 96.422),  # d=2.404 via Vice Beach & Sidewalk (Jason) (E)
    "Four Seasons Hotel Miami (BE)": (-814.289, -1306.504, 263.568),  # Handlebar (SE)
    "Four Seasons Hotel Miami (BW)": (-859.904, -1289.449, 263.568),  # Handlebar (SW)
    "Four Seasons Hotel Miami (E)": (-817.997, -1316.422, 258.306),  # Penthouse (SE)
    "Four Seasons Hotel Miami (NE)": (-802.124, -1273.968, 258.306),  # Penthouse (NE)
    "Four Seasons Hotel Miami (NW)": (-847.739, -1256.913, 258.306),  # Penthouse (NW)
    "Four Seasons Hotel Miami (SE)": (-817.997, -1316.422, 253.608),  # Rooftop (SE)
    "Four Seasons Hotel Miami (SW)": (-863.612, -1299.367, 253.608),  # Penthouse (SW)
    "Four Seasons Hotel Miami (W)": (-817.997, -1316.422, 258.306),  # Penthouse (SW)
    "The Grand": (-273.896, 953.167, 177.028),  # d=2.059 via Vice City 03 (Basketball) & Vice Beach
    "Homestead Water Tower": (-2940.669, -3024.103, 69.913),  # d=4.125 via Tennis Stadium (4K) & Leonida Keys 01 (Airplane) (X)
    "Island A (W)": (-2561.894, -5618.294, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Island F (E)": (-1786.271, -5718.466, 0.000), # via Leonida Keys Postcard (X)
    "Island F (W)": (-1837.483, -5897.036, 0.000), # via Leonida Keys Postcard (X)
    "Island G (E)": (-2142.519, -6218.571, 0.000), # via Leonida Keys Postcard (X)
    "Island G (W)": (-2197.904, -6292.396, 0.000), # via Leonida Keys Postcard (X)
    "Island J (E)": (-2507.148, -6567.983, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Island J (W)": (-2577.286, -6635.502, 0.000), # via Leonida Keys Postcard (X)
    "Island N (E)": (-4004.740, -6977.705, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Island N (W)": (-4118.974, -6905.147, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Island S (E)": (-3912.734, -5535.023, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Island U (S)": (-3786.870, -5636.794, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Island V (S)": (-3738.939, -5987.790, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Island W (N)": (-3743.862, -6117.335, 0.000),  # via Keys
    "Island X (S)": (-3173.824, -6061.079, 0.000), # via Leonida Keys Postcard (X)
    "Island Y (S)": (-3086.466, -6002.597, 0.000), # via Leonida Keys Postcard (X)
    "Island Z (S)": (-2867.519, -5735.394, 0.000), # via Leonida Keys Postcard (X)
    "Jade Ocean Condos": (1565.948, 2488.531, 200.377),  # d=1.547 via Venetian Islands & Highway (NE)
    "Key Lento (A)": (-2620.476, -5762.622, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Key Lento (E)": (-2194.499, -5133.273, 0.000), # via Leonida Keys Postcard (X)
    "Key Lento (J)": (-3016.386, -6703.864, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Key Lento (U)": (-3379.887, -6681.060, 0.000), # via Leonida Keys Postcard (X)
    "Key Lento (V)": (-3371.828, -6631.645, 0.000), # via Leonida Keys Postcard (X)
    "Key Lento (W)": (-3128.605, -6441.724, 0.000), # via Leonida Keys Postcard (X)
    "Keys Bridge (C)": (-408.951, -2964.775, 20.880),  # d=10.108 via Leonida Keys 01 (Airplane) (X) & Prison
    "Latitude on the River (S) (NW)": (-964.195, -812.128, 91.375),  # d=1.513 via Airport (X) & Grassrivers 02 (Watson Bay)
    "Latitude on the River (S) (SW)": (-978.260, -850.237, 91.571),  # d=0.273 via Airport (X) & Grassrivers 02 (Watson Bay)
    "Loews Miami Beach": (1962.510, 1144.431, 85.228),  # d=0.650 via Rooftop Party & Venetian Islands
    "Marina Club at Blackwater Sound (N)": (-2575.262, -5864.326, 16.394),  # d=0.938 via Leonida Keys Postcard (X) & Key Lento
    "Marina Club at Blackwater Sound (S)": (-2573.282, -5923.209, 16.669),  # d=0.677 via Leonida Keys Postcard (X) & Key Lento
    "Miami Tower": (-775.668, -424.119, 159.972),  # d=5.605 via Grassrivers 02 (Watson Bay) & Prison
    "Mount Waffles (TW)": (-5225.002, 5750.498, 228.719),  # d=39.915 via Gas Station (Lucia) & Diner (N)
    "Murano Grande": (1438.245, -21.340, 138.361),  # d=0.050 via Vice Beach & Port
    #"Nine at Mary Brickell Village (A)": (-1035.341, -973.492, 119.968),  # via Metro (SE) (A) (4K) & Tennis Stadium (4K)
    #"Nine at Mary Brickell Village (B)": (-1042.495, -984.399, 119.968),  # via Metro (SE) (A) (4K) & Tennis Stadium (4K)
    #"Nine at Mary Brickell Village (E)": (-1072.159, -1029.655, 119.968),  # via Metro (SE) (A) (4K) & Tennis Stadium (4K)
    "Nine at Mary Brickell Village (A)": (-1039.793, -967.786, 117.476),  # d=3.259 via Metro (SE) (A) (4K) & Grassrivers 02 (Watson Bay)
    "Nine at Mary Brickell Village (B)": (-1045.069, -980.992, 117.573),  # d=3.764 via Metro (SE) (A) (4K) & Grassrivers 02 (Watson Bay)
    "Nine at Mary Brickell Village (E)": (-1061.939, -1037.599, 117.902),  # d=2.271 via Tennis Stadium (4K) & Grassrivers 02 (Watson Bay)
    "1500 Ocean Dr": (2092.684, 979.958, 62.376),  # d=0.016 via Vice Beach & Park
    "Old City Hall": (1681.604, 604.660, 50.889),  # d=0.729 via Vice Beach & Tennis Court (SE)
    "Opera Tower": (-405.995, 871.722, 200.572),  # d=2.407 via Vice Beach & Prison
    "99353 Overseas Hwy": (-3369.349, -6779.484, 74.152),  # d=0.467 via Ocean near Keys (N) & Leonida Keys 01 (Airplane) (X)
    # "102180 Overseas Hwy": (-2653.070, -6040.028, 39.913),  # d=2.823 via Ocean near Keys (N) & Leonida Keys 01 (Airplane) (X)
    "102180 Overseas Hwy": (-2678.565, -6063.121, 41.579),  # d=0.594 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Park Grove Condominium (C)": (-1310.987, -2053.385, 96.905),  # d=3.590 via Leonida Keys 01 (Airplane) (X) & Grassrivers 02 (Watson Bay)
    "Park Grove Condominium (N)": (-1316.937, -1991.705, 97.522),  # d=2.636 via Leonida Keys 01 (Airplane) (X) & Grassrivers 02 (Watson Bay)
    "Park Grove Condominium (S)": (-1318.394, -2135.744, 97.341),  # d=2.284 via Tennis Stadium (4K) & Leonida Keys 01 (Airplane) (X)
    "Pelican Harbor Marina (A)": (1222.495, 1611.267, 0.000),  # via Venetian Islands
    "Pelican Harbor Marina (B)": (1033.011, 1665.745, 0.000),  # via Venetian Islands
    "Pelican Harbor Marina (C)": (1010.818, 1657.043, 0.000),  # via Venetian Islands
    "Pelican Harbor Marina (D)": (862.948, 1732.029, 0.000),  # via Venetian Islands
    "Pelican Harbor Marina (E)": (837.884, 1783.220, 0.000),  # via Venetian Islands
    "Pier (Flamingo)": (1177.128, 838.739, 0.000),  # via Venetian Islands
    "Pin A02R": (-3511.084, -6424.389, 4.505),  # d=0.599 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin A03L": (-3390.904, -6302.366, 3.752),  # d=0.487 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin A03R": (-3360.184, -6341.872, 4.257),  # d=0.007 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin A04L": (-3212.072, -6183.382, 3.280),  # d=0.001 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin A04R": (-3148.011, -6218.810, 3.225),  # d=0.067 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin A05L": (-3120.575, -6133.368, 3.524),  # d=0.362 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin A05R": (-3055.152, -6167.251, 3.561),  # d=0.650 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin A06L": (-3033.760, -6065.890, 3.209),  # d=0.721 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin A06R": (-2972.466, -6104.395, 4.027),  # d=0.589 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin A07L": (-2953.462, -5961.154, 4.188),  # d=0.289 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin A07R": (-2884.297, -5965.747, 4.087),  # d=0.230 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin A08L": (-2819.097, -5745.862, 3.293),  # d=1.126 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin A08R": (-2755.355, -5756.676, 4.445),  # d=0.829 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin B01L": (-3331.612, -6533.631, 3.590),  # d=0.021 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin B01R": (-3298.761, -6531.887, 3.880),  # d=0.107 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin B02L": (-3326.025, -6483.220, 3.800),  # d=0.164 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin B02R": (-3293.431, -6481.457, 3.869),  # d=0.426 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin B03L": (-3320.492, -6431.754, 3.610),  # d=0.344 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin B03R": (-3288.777, -6430.563, 3.854),  # d=0.484 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin B04L": (-3318.823, -6380.903, 3.852),  # d=0.012 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin B04R": (-3286.305, -6377.515, 3.553),  # d=0.922 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin C01R": (-3405.178, -6606.171, 4.070),  # d=0.089 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    #"Pin C01R (B)": (-3391.458, -6592.361, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Pin C01R (B)": (-3405.838, -6606.736, 0.985),  # d=0.409 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin C02L": (-3479.817, -6602.593, 3.875),  # d=0.787 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin C02R": (-3448.135, -6578.962, 4.094),  # d=0.042 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin C03L": (-3523.841, -6576.341, 3.578),  # d=0.999 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin C03R": (-3492.064, -6551.285, 3.901),  # d=0.829 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin C04L": (-3576.278, -6546.336, 4.312),  # d=1.647 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin C04R": (-3544.472, -6522.608, 4.664),  # d=1.159 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin D01L": (-2404.976, -6368.944, 1.809),  # d=0.726 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin D01R": (-2389.723, -6390.640, 1.210),  # d=0.458 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin D02L": (-2142.392, -6078.395, 1.888),  # d=0.604 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Pin D02R": (-2114.591, -6094.978, 1.768),  # d=0.718 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "500 Pompano Dr": (-1914.537, -5324.281, 21.231),  # d=0.008 via Leonida Keys Postcard (X) & Key Lento
    "200 Pompano Dr": (-1875.738, -5390.187, 13.952),  # d=0.258 via Leonida Keys Postcard (X) & Key Lento
    "180 Pompano Dr": (-1896.308, -5424.708, 15.680),  # d=0.813 via Leonida Keys Postcard (X) & Key Lento
    "Portofino Tower (NW)": (1720.414, -196.295, 142.142),  # d=0.503 via Port & Sidewalk (Jason) (E)
    #"Prison Tower (1)": (-2884.895, -2690.586, 30.682),  # d=3.203 via Leonida Keys 01 (Airplane) (X) & Grassrivers 02 (Watson Bay)
    #"Prison Tower (2)": (-2722.635, -2714.152, 32.085),  # d=6.438 via Tennis Stadium (4K) & Leonida Keys 01 (Airplane) (X)
    #"Prison Tower (3)": (-2583.596, -2793.730, 32.316),  # d=6.093 via Tennis Stadium (4K) & Leonida Keys 01 (Airplane) (X)
    #"Prison Tower (4)": (-2627.470, -2864.290, 32.730),  # d=5.236 via Tennis Stadium (4K) & Leonida Keys 01 (Airplane) (X)
    #"Prison Tower (5)": (-2878.070, -2886.888, 32.571),  # d=5.353 via Tennis Stadium (4K) & Leonida Keys 01 (Airplane) (X)
    #"Prison Tower (6)": (-2980.129, -2782.345, 32.140),  # d=6.126 via Tennis Stadium (4K) & Leonida Keys 01 (Airplane) (X)
    "Prison Tower (1)": (-2885.482, -2690.723, 32.007),  # d=0.550 via Grassrivers 02 (Watson Bay) & Prison
    "Prison Tower (2)": (-2711.160, -2712.997, 32.763),  # d=1.573 via Grassrivers 02 (Watson Bay) & Prison
    "Prison Tower (3)": (-2586.836, -2795.382, 32.848),  # d=0.010 via Grassrivers 02 (Watson Bay) & Prison
    "Prison Tower (4)": (-2631.080, -2864.993, 32.628),  # d=0.189 via Grassrivers 02 (Watson Bay) & Prison
    "Prison Tower (5)": (-2880.118, -2886.336, 32.672),  # d=0.201 via Grassrivers 02 (Watson Bay) & Prison
    "Prison Tower (6)": (-2983.035, -2781.496, 32.350),  # d=0.483 via Grassrivers 02 (Watson Bay) & Prison
    "Pylon (C)": (-6407.044, 3797.365, 60.367),  # d=0.350 via Gas Station (Lucia) & Car Wash
    "Red Billboard (Hamlet)": (-2542.919, -3495.137, 27.400),  # d=8.899 via Police Chase (D) & Leonida Keys 01 (Airplane) (X)
    "Rivo Alto Island (S)": (953.700, 1244.700, 0.000),  # via Venetian Islands
    "Seven Mile Bridge (3T)": (-3572.582, -6892.863, 3.488),  # d=0.101 via Ocean near Keys (N) & Leonida Keys 01 (Airplane) (X)
    "Seven Mile Bridge (6T)": (-3637.196, -6932.511, 8.104),  # d=0.278 via Ocean near Keys (N) & Leonida Keys 01 (Airplane) (X)
    "Seven Mile Bridge (20B)": (-3940.429, -7117.949, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Seven Mile Bridge (5B)": (-3629.187, -6932.164, 0.000),  # via Leonida Keys 01 (Airplane) (X)
    "Southeast Financial Center": (-448.897, -461.264, 247.468),  # d=3.765 via Vice Beach & Prison
    "Springfield Community Church": (-6325.114, 4058.129, 30.115),  # d=2.949 via Gas Station (Lucia) & Car Wash
    "Sunset Harbour South Condo": (1445.928, 1671.871, 85.810),  # d=0.219 via Vice City 03 (Basketball) & Venetian Islands
    "Sunshine Skyway Bridge (N)": (-6843.266, 4580.690, 141.185),
    "Sunshine Skyway Bridge (S)": (-6759.214, 4351.692, 141.185),
    "Sunshine Skyway Bridge (C)": (-6801.240, 4466.191, 31.185), # Road Level
    "Tall Double Billboard": (-6299.540, 4125.617, 46.603),  # d=3.130 via Gas Station (Lucia) & Car Wash
    "Tree on Island J": (-2479.572, -6563.116, 7.921),  # d=0.674 via Leonida Keys 01 (Airplane) (X) & Leonida Keys Postcard (X)
    "Turkey Point Nuclear Power Station (N)": (-1548.858, -3459.523, 56.586),  # d=0.203 via Leonida Keys 01 (Airplane) (X) & Grassrivers 02 (Watson Bay)
    "Turkey Point Nuclear Power Station (S)": (-1546.175, -3523.098, 56.642),  # d=0.090 via Leonida Keys 01 (Airplane) (X) & Grassrivers 02 (Watson Bay)
    "Turkey Point Nuclear Power Station (1)": (-1470.456, -3677.071, 80.112),  # d=1.428 via Leonida Keys 01 (Airplane) (X) & Grassrivers 02 (Watson Bay)
    "Turkey Point Nuclear Power Station (2)": (-1469.572, -3717.393, 80.051),  # d=1.319 via Leonida Keys 01 (Airplane) (X) & Grassrivers 02 (Watson Bay)
    "Turkey Point Nuclear Power Station (3)": (-1470.928, -3758.932, 79.971),  # d=1.175 via Leonida Keys 01 (Airplane) (X) & Grassrivers 02 (Watson Bay)
    "Unnamed Building #1 (Blimp Key)": (-4238.667, -6868.495, 8.856),  # d=0.647 via Keys & Leonida Keys 01 (Airplane) (X)
    "1000 Venetian Way (SW)": (301.587, 1108.759, 68.530),  # d=0.300 via Vice Beach & Tennis Court (SE)
    "W South Beach (BNW)": (1941.706, 1656.135, 34.456),  # d=0.005 via Vice City 03 (Basketball) & Rooftop Party
    "The Waverly South Beach (SE)": (1274.731, 582.071, 112.450),  # d=0.872 via Rooftop Party & Vice Beach
    "WDNA FM": (-2517.727, -2295.470, 407.215),  # d=123.048 via Leonida Keys 01 (Airplane) (X) & Grassrivers 02 (Watson Bay)
    "Wells Fargo Center (N)": (-642.090, -403.002, 187.267),  # d=2.755 via Vice Beach & Prison
    "White Billboard (Hamlet)": (-2593.855, -3818.706, 31.675),  # d=10.156 via Police Chase (A) & Leonida Keys 01 (Airplane) (X)
    #### AIWE MAP ####
    "1703 E 5th St (Shack) (SE)": (-6264.218, 3479.946, 10.000),  # via AI World Editor Map (4K)
    "1703 E 5th St (Shack) (SW)": (-6275.983, 3479.211, 10.000),  # via AI World Editor Map (4K)
    "1703 E 5th St (Warehouse) (NW)": (-6251.006, 3501.332, 11.315),  # d=0.758 via AI World Editor Map (4K) & Gas Station (Lucia)
    "1703 E 5th St (Warehouse) (SW)": (-6246.447, 3455.814, 11.423),  # d=1.350 via AI World Editor Map (4K) & Gas Station (Lucia)
    "2533 E Hwy 98 (N)": (-6448.041, 3293.182, 10.000),  # via AI World Editor Map (4K)
    "2533 E Hwy 98 (W)": (-6453.188, 3286.564, 10.000),  # via AI World Editor Map (4K)
    "3210 E Hwy 98 (NE)": (-6440.688, 3108.256, 10.000),  # via AI World Editor Map (4K)
    "3401 E Hwy 98 (SW)": (-6424.512, 3324.064, 10.000),  # via AI World Editor Map (4K)
    "4937 E Hwy 98 (Gas Station) (NE)": (-6321.092, 2782.835, 17.442),  # d=0.990 via AI World Editor Map (4K) & Gas Station (Lucia)
    "4937 E Hwy 98 (Gas Station) (SE)": (-6330.736, 2764.765, 17.649),  # d=0.943 via AI World Editor Map (4K) & Gas Station (Jason)
    "4937 E Hwy 98 (Store) (NE)": (-6331.865, 2752.741, 10.000),  # via AI World Editor Map (4K)
    "4937 E Hwy 98 (Store) (SE)": (-6331.865, 2735.094, 10.000),  # via AI World Editor Map (4K)
    "6218 E Hwy 98 (E)": (-6554.659, 3053.476, 10.000),  # via AI World Editor Map (4K)
    "6232 E Hwy 98 (NE)": (-6337.747, 3388.770, 10.000),  # via AI World Editor Map (4K)
    "6232 E Hwy 98 (SE)": (-6340.386, 3362.940, 9.018),  # d=2.638 via AI World Editor Map (4K) & Gas Station (Lucia)
    "6246 E Hwy 98 (NE)": (-6323.777, 3263.770, 10.000),  # via AI World Editor Map (4K)
    "? (L663) (SE)": (-6525.247, 3330.682, 10.000),  # via AI World Editor Map (4K)
    "? (L664) (SE)": (-6548.776, 3363.770, 10.000),  # via AI World Editor Map (4K)
    "? (L665) (SE)": (-6441.424, 2827.741, 10.000),  # via AI World Editor Map (4K)
    "? (L666) (SE)": (-6483.335, 2842.447, 10.000),  # via AI World Editor Map (4K)
    "? (L667) (SW)": (-6506.865, 2864.506, 10.000),  # via AI World Editor Map (4K)
    "? (L668) (SW)": (-6510.541, 2885.094, 10.000),  # via AI World Editor Map (4K)
    "? (L669) (SE)": (-6513.482, 2912.300, 10.000),  # via AI World Editor Map (4K)
    "? (L944) (SE)": (-6578.188, 3439.505, 10.000),  # via AI World Editor Map (4K)
    "? (L952) (NE)": (-6325.983, 3315.241, 10.000),  # via AI World Editor Map (4K)
    "? (L953) (NE)": (-6370.100, 3277.741, 10.000),  # via AI World Editor Map (4K)
    "? (L954) (SE)": (-6362.747, 3342.447, 10.000),  # via AI World Editor Map (4K)
    "? (L956) (N)": (-6589.953, 2976.271, 10.000),  # via AI World Editor Map (4K)
    "? (L957) (NE)": (-6583.335, 3042.447, 10.000),  # via AI World Editor Map (4K)
    "? (L958) (SW)": (-6502.453, 3063.035, 10.000),  # via AI World Editor Map (4K)
    "AIWE": (-6846.570, 3512.299, 10.000),  # via AI World Editor Map (4K)
    "Centerplate": (-6665.320, 2661.197, 10.000),  # via AI World Editor Map (4K)
    "Coyote's (SE)": (-6306.869, 3060.828, 10.223),  # d=0.002 via AI World Editor Map (4K) & Gas Station (Lucia)
    "Coyote's (SW)": (-6350.983, 3053.476, 10.000),  # via AI World Editor Map (4K)
    "Dan's Pawn (NE)": (-6426.718, 3078.476, 10.000),  # via AI World Editor Map (4K)
    "Dan's Pawn (SE)": (-6414.953, 3053.476, 10.000),  # via AI World Editor Map (4K)
    "Goodwill Career Training Center (SW)": (-6399.512, 3204.211, 10.000),  # via AI World Editor Map (4K)
    "Guardhouse": (-6378.188, 2588.036, 10.000),  # via AI World Editor Map (4K)
    "King Slayer Charters (NE)": (-6577.453, 3138.770, 10.000),  # via AI World Editor Map (4K)
    "King Slayer Charters (SE)": (-6578.923, 3118.182, 10.000),  # via AI World Editor Map (4K)
    "Leslie Porter Wayside Park": (-6628.188, 3386.564, 10.000),  # via AI World Editor Map (4K)
    "Large White Billboard": (-6329.580, 3355.622, 27.401),  # d=2.857 via AI World Editor Map (4K) & Gas Station (Lucia)
    "Lucky Plucker (NE)": (-6355.394, 3457.152, 10.000),  # via AI World Editor Map (4K)
    "Lucky Plucker (SE)": (-6353.188, 3444.652, 10.000),  # via AI World Editor Map (4K)
    "Lucky Plucker (SW)": (-6365.688, 3441.711, 10.000),  # via AI World Editor Map (4K)
    "Mr. Bingo (SE)": (-6344.365, 2824.800, 10.000),  # via AI World Editor Map (4K)
    "Mr. Bingo (SW)": (-6395.835, 2824.800, 10.000),  # via AI World Editor Map (4K)
    "Parker City Hall (SW)": (-6247.698, 3045.290, 8.501),  # d=1.157 via AI World Editor Map (4K) & Gas Station (Lucia)
    "Parker Community Center (SW)": (-6245.747, 3115.222, 7.628),  # d=0.092 via AI World Editor Map (4K) & Gas Station (Lucia)
    "Parker Police Station (SW)": (-6221.732, 3039.312, 8.510),  # d=0.608 via AI World Editor Map (4K) & Gas Station (Lucia)
    "Parker Public Library (SW)": (-6208.336, 3092.447, 10.000),  # via AI World Editor Map (4K)
    "Pier (L945) (SW)": (-6614.953, 3456.417, 10.000),  # via AI World Editor Map (4K)
    "Pier (L946) (NE)": (-6627.453, 3425.535, 10.000),  # via AI World Editor Map (4K)
    "Pier 98 (NE)": (-6541.424, 3109.359, 10.000),  # via AI World Editor Map (4K)
    "Port Gellhorn Smokestack": (-6351.527, 3419.566, 49.861),  # d=2.545 via AI World Editor Map (4K) & Gas Station (Jason)
    "Red Bird Café (NW)": (-6470.100, 3166.712, 10.000),  # via AI World Editor Map (4K)
    "Rodeo's (SE)": (-6549.512, 3143.917, 10.000),  # via AI World Editor Map (4K)
    "Sebring International Raceway (T17)": (-6623.776, 2554.212, 10.000),  # via AI World Editor Map (4K)
    "Sebring International Raceway (T7)": (-6372.306, 2370.389, 10.000),  # via AI World Editor Map (4K)
    "Seclusion Bay": (-6622.306, 2976.271, 10.000),  # via AI World Editor Map (4K)
    "Transformer Station (SW)": (-6506.865, 3466.711, 10.000),  # via AI World Editor Map (4K)
    "Twice The Ice (N)": (-6452.453, 3260.094, 10.000),  # via AI World Editor Map (4K)
    "Twice The Ice (W)": (-6454.659, 3255.682, 10.000),  # via AI World Editor Map (4K)
    "Waldo Station (SE)": (-6575.247, 3506.417, 10.000),  # via AI World Editor Map (4K)
    "Welcome to Port Gellhorn Sign": (-6288.487, 2856.420, 17.620),  # d=0.000 via AI World Editor Map (4K) & Gas Station (Lucia)
    "Wildfire Scooters (NW)": (-6463.482, 3332.888, 10.000),  # via AI World Editor Map (4K)
    "Wildfire Scooters (SE)": (-6441.424, 3328.844, 10.000),  # via AI World Editor Map (4K)
    "Wildfire Scooters (SW)": (-6460.541, 3323.697, 10.000),  # via AI World Editor Map (4K)
    "Wine Country Motor Sports": (-6431.865, 2595.389, 10.000),  # via AI World Editor Map (4K)
}


### MAPS ###########################################################################################

maps = {
    "aiwe": (0, 0.680, (4655.668, 2388.364)),
    "dupzor": (51, 0.558, (9037, 6693)),
    "martipk": (5, 0.558, (9037-5500, 6693-5500)),
    "rickrick": (2, 2.500, (5000, 7500)),
    "yanis": (7, 1.000, (16341, 12139)),
}
maps = {
    name: {
        "version": data[0],
        "scale": data[1],
        "zero": data[2],
        "filename": f"{DIRNAME}/maps/{name},{data[0]}.png"
    } for name, data in maps.items()
}


### MAP SECTIONS ###################################################################################

map_sections = {
    "Vice City": (-4000, -3000, 3000, 4000),
    "Port Gellhorn": (-9000, 1000, -5000, 6000),
    "Leonida Keys": (-8000, -8000, -1000, -4000),
    "Grassrivers": (-6000, -5000, 0, -2000),
    "Ambrosia": (-5000, 1000, -2000, 5000),
}
