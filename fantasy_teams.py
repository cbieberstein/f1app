import pandas as pd

# Teams - list of dicts
fantasy_teams_lod = [
    {
        "User": "Colin B.",
        "Team": "underDOGS",
        "PIN": 999,
        "Drivers": ["ALO", "LEC", "PIA", "GAS", "HUL", "ZHO", "RIC", "SAR", "MAG"],
        "Score": 0.0,
    },
    {
        "User": "Mitz",
        "Team": "Maxing Maximum Maxs Maxima",
        "PIN": 42069,
        "Drivers": ["BOT", "RIC", "TSU", "VER", "ZHO"],
        "Score": 0.0,
    },
    {
        "User": "Susan Tiffin",
        "Team": "Cheering for Red and Riccardo",
        "PIN": 16,
        "Drivers": ["LEC", "SAI", "BEA", "RIC", "PIA", "MAG", "TSU", "GAS", "HUL"],
        "Score": 0.0,
    },
    {
        "User": "Mark Fitzowich",
        "Team": "Mark F1tzowich",
        "PIN": 805,
        "Drivers": ["LEC", "NOR", "RUS", "ALB"],
        "Score": 0.0,
    },
    {
        "User": "Chapman Sun",
        "Team": "Mastercard CashApp",
        "PIN": 2024,
        "Drivers": ["HAM", "NOR", "PIA", "GAS"],
        "Score": 0.0,
    },
    {
        "User": "Hayley G.",
        "Team": "Papaya Pit Crew",
        "PIN": 4040,
        "Drivers": ["NOR", "PER", "PIA", "RIC", "ZHO"],
        "Score": 0.0,
    },
    {
        "User": "Jesse",
        "Team": "Crypto CashApp",
        "PIN": 1111,
        "Drivers": ["VER", "ALB", "BOT", "RIC", "MAG"],
        "Score": 0.0,
    },
    {
        "User": "Michael Kissinger",
        "Team": "The WiQed Fasts",
        "PIN": 9876,
        "Drivers": ["VER", "ALB", "BOT", "HUL"],
        "Score": 0.0,
    },
    {
        "User": "Richard Stuivenberg",
        "Team": "Flying Slap",
        "PIN": 1997,
        "Drivers": ["ALO", "NOR", "RUS", "ALB"],
        "Score": 0.0,
    },
    {
        "User": "Alan Brazendale",
        "Team": "BrazenF1",
        "PIN": 2468,
        "Drivers": ["LEC", "SAI", "BEA", "NOR"],
        "Score": 0.0,
    },
]

fantasy_teams_df = pd.DataFrame.from_records(data=fantasy_teams_lod)
