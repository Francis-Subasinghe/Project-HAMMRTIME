# config.py – Constants and mapping dictionaries

# List of driver names
driver_names = [
    "Max Verstappen", "Sergio Perez", "Lewis Hamilton", "George Russell",
    "Charles Leclerc", "Carlos Sainz", "Lando Norris", "Oscar Piastri",
    "Fernando Alonso", "Lance Stroll", "Pierre Gasly", "Esteban Ocon",
    "Yuki Tsunoda", "Daniel Ricciardo", "Kevin Magnussen", "Nico Hülkenberg",
    "Valtteri Bottas", "Zhou Guanyu", "Alex Albon", "Logan Sargeant"
]

# Driver to team mapping
driver_team_map = {
    "Max Verstappen": "Red Bull",
    "Sergio Perez": "Red Bull",
    "Lewis Hamilton": "Mercedes",
    "George Russell": "Mercedes",
    "Charles Leclerc": "Ferrari",
    "Carlos Sainz": "Ferrari",
    "Lando Norris": "McLaren",
    "Oscar Piastri": "McLaren",
    "Fernando Alonso": "Aston Martin",
    "Lance Stroll": "Aston Martin",
    "Pierre Gasly": "Alpine",
    "Esteban Ocon": "Alpine",
    "Yuki Tsunoda": "AlphaTauri",
    "Daniel Ricciardo": "AlphaTauri",
    "Kevin Magnussen": "Haas",
    "Nico Hülkenberg": "Haas",
    "Valtteri Bottas": "Alfa Romeo",
    "Zhou Guanyu": "Alfa Romeo",
    "Alex Albon": "Williams",
    "Logan Sargeant": "Williams"
}

# Encoders for driver, team, and tire types
driver_to_id = {name: idx for idx, name in enumerate(driver_names)}
teams = sorted(set(driver_team_map.values()))
team_to_id = {team: idx for idx, team in enumerate(teams)}
tire_types = ['SOFT', 'MEDIUM', 'HARD']
tire_to_id = {tire: idx for idx, tire in enumerate(tire_types)}
