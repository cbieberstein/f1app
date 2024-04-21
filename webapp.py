from datetime import datetime, date

import fastf1
import pandas as pd
import plotly.express as px
import solara
import PIL.Image

from fantasy_teams import fantasy_teams_df

# Make printing a dataframe complete for debugging purposes.
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# Data download from the API is time consuming, cache race data so its only downloaded once.
fastf1.Cache.enable_cache(cache_dir="cache/")


def get_completed_races(year: int):
    """
    get_completed_races - function to get all GP race events that have completed before today.
    year - int for the GP season you are interested in
    returns - pd.DataFrame containing all the race events (conventional and shootout_sprint)
    """
    events = fastf1.get_event_schedule(year=year)[
        ["RoundNumber", "EventDate", "EventName", "EventFormat"]
    ]

    # Races happen in both conventional and sprint formats
    finished_races = events[
        (
            (events["EventFormat"] == "conventional")
            | (events["EventFormat"].str.contains("sprint"))
        )
        & (events["EventDate"] <= date.today().strftime("%Y-%m-%d"))
    ]
    return finished_races


def get_completed_sprints(year: int):
    """
    get_completed_sprints - function to get all GP sprint events that have completed before today.
    year - int for the GP season you are interested in
    returns - pd.DataFrame containing all the sprint events (shootout_sprint)
    """
    events = fastf1.get_event_schedule(year=year)[
        ["RoundNumber", "EventDate", "EventName", "EventFormat"]
    ]

    finished_sprints = events[
        (events["EventFormat"].str.contains("sprint"))
        & (events["EventDate"] <= date.today().strftime("%Y-%m-%d"))
    ]
    return finished_sprints


def get_event_points(year: int, event_type: str, events_df: pd.DataFrame):
    """
    get_event_points - returns all drivers / teams and point results for the event
    year - GP season to use
    event_type - 'R' for race, 'S' for sprint_shootout event
    events_df - list of events (returned from get_completed_races() or get_completed_sprints() )
    returns - pd.DataFrame with the points winners (driver and team) for the event
    """
    # Empty Datafram7e to collect point scorers in races / sprints
    points_df = pd.DataFrame.from_dict(
        {
            "RaceNumber": [],
            "BroadcastName": [],
            "Abbreviation": [],
            "TeamName": [],
            "TeamColor": [],
            "HeadshotUrl": [],
            "CountryCode": [],
            "ClassifiedPosition": [],
            "Points": [],
            "Time": [],
        }
    )

    for rnd, racename in events_df["EventName"].items():
        race = fastf1.get_session(year, racename, event_type)
        race.load()
        # Include all results including 0 point
        race_points_df = race.results
        # Leave out 0 point results (P11-P20)
        # race_points_df = race.results[race.results['Points'] >= 1.0]
        race_points_df["RaceNumber"] = int(rnd)
        points_df = pd.concat(objs=[points_df, race_points_df])

    return points_df


def get_race_points(year: int):
    """
    get_race_points - returns a row per race for each driver/team.
    year - GP season to inspect
    returns - pd.DataFrame with the all sprint points winners (all events to date)
    """
    completed_races_df = get_completed_races(year=year)
    return get_event_points(year=year, event_type="R", events_df=completed_races_df)


def get_sprint_points(year: int):
    """
    get_sprint_points - returns a row per print for each driver/team.
    year - GP season to inspect
    returns - pd.DataFrame with the all sprint points winners (all events to date)
    """
    completed_sprints_df = get_completed_sprints(year=year)
    return get_event_points(year=year, event_type="S", events_df=completed_sprints_df)


def save_dataframe(df: pd.DataFrame, filename: str):
    df.to_parquet(path=f"./data/{filename}", compression="zstd")


def load_dataframe(filename: str):
    df = pd.read_parquet(path=f"./data/{filename}")
    return df


def display_hack():
    print(f"{YEAR} DRIVER STANDINGS")
    print("\nRACE:")
    print(driver_race_points_df.sort_values(by="Points", ascending=False))
    print("\nSPRINT:")
    print(driver_sprint_points_df.sort_values(by="Points", ascending=False))
    print("\nTOTAL:")
    print(driver_total_points_df.sort_values(by="Points", ascending=False))

    print(f"\n\n{YEAR} CONSTRUCTOR STANDINGS")
    print("\nRACE:")
    print(constructor_race_points_df.sort_values(by="Points", ascending=False))
    print("\nSPRINT:")
    print(constructor_sprint_points_df.sort_values(by="Points", ascending=False))
    print("\nTOTAL:")
    print(constructor_total_points_df.sort_values(by="Points", ascending=False))


@solara.component
def fantasy_team_standings():
    with solara.Card(title=f"{YEAR} F1 Fantasy Pool - Team Standings"):
        fig4 = px.bar(data_frame=fantasy_pool_df, 
                #text='Abbreviation',
                text_auto=False,
                title='Points by Fantasy Pool Team, Driver, and RaceNumber',
                x='FantasyTeam', 
                y='Points', 
                hover_data=['RaceNumber','Abbreviation','TeamName','Points'],
                color='RaceNumber', 
                height=600
                )
        solara.FigurePlotly(fig4)

@solara.component
def your_team_points():
    with solara.Card(title=fantasy_team.value):
        team_drivers = fantasy_teams_df[fantasy_teams_df['Team'] == fantasy_team.value].iloc[0]
        filtered_df = total_df[total_df['Abbreviation'].isin(team_drivers['Drivers'])]
        fig3 = px.bar(data_frame=filtered_df, 
                    text='Abbreviation',
                    text_auto=False,
                    title='Points by Race and Driver',
                    x='RaceNumber', 
                    y='Points', 
                    color='Abbreviation', 
                    height=600
                    )
        solara.FigurePlotly(fig3)
        with solara.CardActions():
            solara.Select(label="Fantasy Team", values=fantasy_teams_df['Team'].to_list(), value=fantasy_team, dense=True)

@solara.component
def driver_champ_standings():
    with solara.Card(title=f"{YEAR} Driver's Championship Standings"):
        fig1 = px.bar(data_frame=total_df, 
            #text='RaceNumber',
            text_auto=False,
            title="",
            x='Abbreviation', 
            y='Points', 
            hover_data=['BroadcastName', 'TeamName', 'Abbreviation','RaceNumber','Points'],
            color='RaceNumber',
            height=600
        ) 
        solara.FigurePlotly(fig1)


@solara.component
def constructor_champ_standings():
    with solara.Card(title=f"{YEAR} Constructor's Championship Standings"):
                fig2 = px.bar(data_frame=total_df, 
                    #text='RaceNumber',
                    text_auto=False,
                    title="",
                    x='TeamName', 
                    y='Points', 
                    hover_data=['BroadcastName', 'TeamName', 'Abbreviation','RaceNumber','Points'],
                    color='RaceNumber',
                    height=600
                ) 
                solara.FigurePlotly(fig2)


@solara.component
def Page():
    solara.Title(title="Colin's F1 Fantasy App")
    with solara.Row(gap="10px", justify="space-around"):
        with solara.Columns():
            fantasy_team_standings()
            your_team_points()
    with solara.Row(gap="10px", justify="space-around"):
        with solara.Columns():
            driver_champ_standings()
            constructor_champ_standings()


if __name__ == "__main__":
    # Data download from the API is time consuming, cache race data so its only downloaded once.
    fastf1.Cache.enable_cache(cache_dir="cache/")

    YEAR = 2024
    recompute = True
    f1_image = PIL.Image.open('./images/F1-Logo.png')

    fantasy_team = solara.reactive('underDOGS')

    if recompute == True:
        race_df = get_race_points(year=YEAR) 
        sprint_df = get_sprint_points(year=YEAR)
        total_df = pd.concat([race_df, sprint_df])

        save_dataframe(df=race_df, filename=f"{YEAR}_race_df.parquet")
        save_dataframe(df=sprint_df, filename=f"{YEAR}_sprint_df.parquet")
        save_dataframe(df=total_df, filename=f"{YEAR}_total_df.parquet")
    else:
        race_df = load_dataframe(filename=f"{YEAR}_race_df.parquet")
        sprint_df = load_dataframe(filename=f"{YEAR}_sprint_df.parquet")
        total_df = load_dataframe(filename=f"{YEAR}_total_df.parquet")

    # Derive our race stats for display
    fantasy_pool_df = pd.DataFrame()
    for record in fantasy_teams_df.itertuples():
        team_race_point_details_df = total_df.loc[ 
            total_df["Abbreviation"].isin(record.Drivers)
        ]
        team_race_point_details_df['FantasyTeam'] = record.Team

        fantasy_pool_df = pd.concat([fantasy_pool_df, team_race_point_details_df])
    # Convert to string so that we get discrete instead of continuous colors
    fantasy_pool_df['RaceNumber'] = fantasy_pool_df['RaceNumber'].astype(int).astype(str)
    total_df['RaceNumber'] = total_df['RaceNumber'].astype(int).astype(str)
    fantasy_pool_df['RaceNumber'] = fantasy_pool_df['RaceNumber'].astype(int).astype(str)

