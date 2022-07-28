FUZZY_VALUES = dict()
FUZZY_VALUES["NB"] = dict()
FUZZY_VALUES["NB"]["NB"] = "NVVB"
FUZZY_VALUES["NB"]["N"] = "NVB"
FUZZY_VALUES["NB"]["ZO"] = "NB"
FUZZY_VALUES["NB"]["P"] = "N"
FUZZY_VALUES["NB"]["PB"] = "Z"
FUZZY_VALUES["N"] = dict()
FUZZY_VALUES["N"]["NB"] = "NVB"
FUZZY_VALUES["N"]["N"] = "NB"
FUZZY_VALUES["N"]["ZO"] = "N"
FUZZY_VALUES["N"]["P"] = "Z"
FUZZY_VALUES["N"]["PB"] = "P"
FUZZY_VALUES["ZO"] = dict()
FUZZY_VALUES["ZO"]["NB"] = "NB"
FUZZY_VALUES["ZO"]["N"] = "N"
FUZZY_VALUES["ZO"]["ZO"] = "Z"
FUZZY_VALUES["ZO"]["P"] = "P"
FUZZY_VALUES["ZO"]["PB"] = "PB"
FUZZY_VALUES["P"] = dict()
FUZZY_VALUES["P"]["NB"] = "N"
FUZZY_VALUES["P"]["N"] = "Z"
FUZZY_VALUES["P"]["ZO"] = "P"
FUZZY_VALUES["P"]["P"] = "PB"
FUZZY_VALUES["P"]["PB"] = "PVB"
FUZZY_VALUES["PB"] = dict()
FUZZY_VALUES["PB"]["NB"] = "Z"
FUZZY_VALUES["PB"]["N"] = "P"
FUZZY_VALUES["PB"]["ZO"] = "PB"
FUZZY_VALUES["PB"]["P"] = "PVB"
FUZZY_VALUES["PB"]["PB"] = "PVVB"
FUZZY_VALUES["PVB"] = dict()
FUZZY_VALUES["PVB"]["NB"] = "P"
FUZZY_VALUES["PVB"]["N"] = "PB"
FUZZY_VALUES["PVB"]["ZO"] = "PVB"
FUZZY_VALUES["PVB"]["P"] = "PVVB"
FUZZY_VALUES["PVB"]["PB"] = "PVVB"
FUZZY_VALUES["NVB"] = dict()
FUZZY_VALUES["NVB"]["N"] = "NVVB"
FUZZY_VALUES["NVB"]["ZO"] = "NVB"
FUZZY_VALUES["NVB"]["P"] = "NB"
FUZZY_VALUES["NVB"]["PB"] = "N"
FUZZY_VALUES["NVB"]["NB"] = "NVVB"



THETA_RANGE = {
    "NVB": (None, -40, -25),
    "NB": (-40, -25, -10),
    "N": (-20, -10, 0),
    "ZO": (-5, 0, 5),
    "P": (0, 10, 20),
    "PB": (10, 25, 40),
    "PVB": (25, 40, None)
}

OMEGA_RANGE = {
    "NB": (None, -8, -3),
    "N": (-6, -3, 0),
    "ZO": (-1, 0, 1),
    "P": (0, 3, 6),
    "PB": (3, 8, None)
}

F_RANGE = {
    "NVVB": (None, -32, -24),
    "NVB": (-32, -24, -16),
    "NB": (-24, -16, -8),
    "N": (-16, -8, 0),
    "Z": (-4, 0, 4),
    "P": (0, 8, 16),
    "PB": (8, 16, 24),
    "PVB": (16, 24, 32),
    "PVVB": (24, 32, None)
}