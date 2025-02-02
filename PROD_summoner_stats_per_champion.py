import json
from tabulate import tabulate
from termcolor import colored

# Set the value of detailed_version (True) for more info/to analyze more in depth, but might overwhelm your terminal
detailed_version = True

# Read the JSON file
with open('NA1_4698549616.json') as file:
    data = json.load(file)

# Extract the participant data
participants = data['info']['participants']

# Function to deduce the rank based on the metrics
def deduce_rank(participant):
    rank_score = 0
    metrics = participant['challenges']

    # Function to safely access metrics
    def get_metric(metrics, metric_name):
        return metrics.get(metric_name, 0)

    # Extracting additional metrics
    kda = get_metric(metrics, 'kda')
    takedowns = get_metric(metrics, 'takedowns')
    deaths = participant.get('deaths', 0)
    kills = participant.get('kills', 0)
    damagePerMinute = get_metric(metrics, 'damagePerMinute')
    damageTakenOnTeamPercentage = get_metric(metrics, 'damageTakenOnTeamPercentage')
    killParticipation = get_metric(metrics, 'killParticipation')
    turretTakedowns = get_metric(metrics, 'turretTakedowns')
    goldPerMinute = get_metric(metrics, 'goldPerMinute')
    healingAndShielding = get_metric(metrics, 'effectiveHealAndShielding')
    totalDamageDealtToChampions = participant.get('totalDamageDealtToChampions', 0)
    totalTimeCCDealt = participant.get('totalTimeCCDealt', 0)
    totalDamageTaken = participant.get('totalDamageTaken', 0)
    totalUnitsHealed = participant.get('totalUnitsHealed', 0)

    # Deduction based on the metrics
    if takedowns >= 40:
        rank_score += 2
    elif takedowns >= 30:
        rank_score += 1.5
    elif takedowns >= 20:
        rank_score += 1

    if deaths <= 3:
        rank_score += 2
    elif deaths <= 5:
        rank_score += 1.5
    elif deaths <= 7:
        rank_score += 1

    if kda >= 6:
        rank_score += 2
    elif kda >= 4:
        rank_score += 1.5
    elif kda >= 2:
        rank_score += 1

    if kills >= 15:
        rank_score += 2
    elif kills >= 10:
        rank_score += 1.5
    elif kills >= 5:
        rank_score += 1

    if damagePerMinute >= 2000:
        rank_score += 2
    elif damagePerMinute >= 1500:
        rank_score += 1.5
    elif damagePerMinute >= 1000:
        rank_score += 1

    if damageTakenOnTeamPercentage <= 0.1:
        rank_score += 2
    elif damageTakenOnTeamPercentage <= 0.15:
        rank_score += 1.5
    elif damageTakenOnTeamPercentage <= 0.2:
        rank_score += 1

    if killParticipation >= 0.8:
        rank_score += 2
    elif killParticipation >= 0.6:
        rank_score += 1.5
    elif killParticipation >= 0.4:
        rank_score += 1

    if goldPerMinute >= 800:
        rank_score += 0.5
    elif goldPerMinute >= 600:
        rank_score += 0.25

    if healingAndShielding >= 5000:
        rank_score += 1.5
    elif healingAndShielding >= 3000:
        rank_score += 1

    if totalDamageDealtToChampions >= 30000:
        rank_score += 1.5
    elif totalDamageDealtToChampions >= 20000:
        rank_score += 1

    if totalTimeCCDealt >= 1000:
        rank_score += 0.5

    if totalDamageTaken <= 20000:
        rank_score += 1
    elif totalDamageTaken <= 30000:
        rank_score += 0.5

    if totalUnitsHealed >= 10:
        rank_score += 0.5
    
    # Deduce the rank based on the rank score
    if rank_score >= 27:
        return 'S+'
    elif rank_score >= 24:
        return 'S'
    elif rank_score >= 21:
        return 'S-'
    elif rank_score >= 18:
        return 'A+'
    elif rank_score >= 15:
        return 'A'
    elif rank_score >= 12:
        return 'A-'
    elif rank_score >= 9:
        return 'B+'
    elif rank_score >= 6:
        return 'B'
    elif rank_score >= 3:
        return 'B-'
    elif rank_score >= 2.5:
        return 'C+'
    elif rank_score >= 2:
        return 'C'
    elif rank_score >= 1.5:
        return 'C-'
    elif rank_score >= 1:
        return 'D+'
    elif rank_score >= 0.5:
        return 'D'
    else:
        return 'D-'

# Calculate the rank score based on the metrics
def calculate_rank_score(kda, takedowns, deaths, damagePerMinute,
                         damageTakenOnTeamPercentage, killParticipation,
                         turretTakedowns, goldPerMinute, healingAndShielding,
                         totalDamageDealtToChampions, totalTimeCCDealt,
                         totalDamageTaken, totalUnitsHealed):
    rank_score = 0

    rank_score += kda
    rank_score += takedowns / 10
    rank_score -= deaths / 10
    rank_score += damagePerMinute / 100
    rank_score -= damageTakenOnTeamPercentage * 10
    rank_score += killParticipation
    rank_score += turretTakedowns
    rank_score += goldPerMinute / 100
    rank_score += healingAndShielding / 1000
    rank_score += totalDamageDealtToChampions / 1000
    rank_score += totalTimeCCDealt / 100
    rank_score -= totalDamageTaken / 1000
    rank_score += totalUnitsHealed / 10

    return rank_score

# Display the data in a tabular format
print("\n")
if detailed_version:
    headers = ["Summoner Name", "Champion Name", "KDA", "Takedowns", "Deaths", "Kills",
               "Damage Taken Percentage", "Kill Participation", "Turret Takedowns",
               "Gold Per Minute", "Damage Per Minute", "Healing and Shielding",
               "Total Damage Dealt to Champions", "Total Time CC Dealt",
               "Total Damage Taken", "Total Units Healed", "Estimated Rank"]
else:
    headers = ["Summoner Name", "Champion Name", "KDA", "Kill Participation",
               "Gold Per Minute", "Damage Per Minute",
               "Total Damage Dealt to Champions", "Estimated Rank"]
    
table_data = []
for participant in participants:
    # Extract relevant data based on the value of detailed_version
    summoner_name = participant['summonerName']
    champion_name = participant['championName']
    kda = participant['challenges'].get('kda', 0)
    kill_participation = participant['challenges'].get('killParticipation', 0)
    gold_per_minute = participant['challenges'].get('goldPerMinute', 0)
    damage_per_minute = participant['challenges'].get('damagePerMinute', 0)
    total_damage_dealt = participant.get('totalDamageDealtToChampions', 0)
    estimated_rank = deduce_rank(participant)

    if detailed_version:
        takedowns = participant['challenges'].get('takedowns', 0)
        deaths = participant.get('deaths', 0)
        kills = participant.get('kills', 0)
        damage_taken_percentage = participant['challenges'].get('damageTakenOnTeamPercentage', 0)
        turret_takedowns = participant['challenges'].get('turretTakedowns', 0)
        healing_and_shielding = participant['challenges'].get('effectiveHealAndShielding', 0)
        total_time_cc_dealt = participant.get('totalTimeCCDealt', 0)
        total_damage_taken = participant.get('totalDamageTaken', 0)
        total_units_healed = participant.get('totalUnitsHealed', 0)

        table_data.append([summoner_name, champion_name, kda, takedowns, deaths, kills,
                           damage_taken_percentage, kill_participation, turret_takedowns,
                           gold_per_minute, damage_per_minute, healing_and_shielding,
                           total_damage_dealt, total_time_cc_dealt, total_damage_taken,
                           total_units_healed, estimated_rank])
    else:
        table_data.append([summoner_name, champion_name, kda, kill_participation,
                           gold_per_minute, damage_per_minute, total_damage_dealt,
                           estimated_rank])

# Add color to table_data based on certain columns
colored_table_data = []
for row in table_data:
    colored_row = []
    for i, value in enumerate(row):
        # Define color thresholds for specific columns
        if headers[i] == "KDA":
            if value >= 6:
                colored_value = colored(value, "green")
            elif value >= 4:
                colored_value = colored(value, "yellow")
            else:
                colored_value = colored(value, "blue")
        elif headers[i] == "Estimated Rank":
            if value in ["S+", "S", "S-"]:
                colored_value = colored(value, "green")
            elif value in ["A+", "A", "A-"]:
                colored_value = colored(value, "yellow")
            else:
                colored_value = colored(value, "blue")
        else:
            colored_value = value
        colored_row.append(colored_value)
    colored_table_data.append(colored_row)

table = tabulate(colored_table_data, headers, tablefmt="pipe")
print(table)
print("\n")
