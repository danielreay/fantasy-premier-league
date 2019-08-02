# scrape player data from Fantasy Premier League API and make calculations on value added
# output file is fpl_player_data.csv
# v1.0 - 2 August 2019

import requests, csv

url = 'https://fantasy.premierleague.com/api/bootstrap-static'
json_data = requests.get(url).json()

# open CSV file to write data
with open('fpl_player_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvfile.write('\ufeff') # tells Excel to recognise the utf-8 encoding
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['first_name', 'second_name', 'element_type', 'total_points', 'minutes',
        'goals_scored', 'assists', 'goals_conceded', 'bonus', 'clean_sheets', 'red_cards',
        'yellow_cards', 'now_cost', 'value_added', 'value_added_per_90', 'value_added_per_million',
        'vapm_per_90'])

    # collect player data from FPL API
    for i in range (len(json_data['elements'])):
        first_name = json_data['elements'][i]['first_name']
        second_name = json_data['elements'][i]['second_name']
        element_type = json_data['elements'][i]['element_type']
        total_points = json_data['elements'][i]['total_points']
        minutes = json_data['elements'][i]['minutes']
        goals_scored = json_data['elements'][i]['goals_scored']
        assists = json_data['elements'][i]['assists']
        goals_conceded = json_data['elements'][i]['goals_conceded']
        bonus = json_data['elements'][i]['bonus']
        clean_sheets = json_data['elements'][i]['clean_sheets']
        red_cards = json_data['elements'][i]['red_cards']
        yellow_cards = json_data['elements'][i]['yellow_cards']
        now_cost = json_data['elements'][i]['now_cost'] / 10.0

        # VALUE ADDED (VA): the amount of total points gained by a player NOT from appearances
        value_added = (assists * 3) + bonus - yellow_cards - (red_cards * 3)
        if (element_type <= 2):
            value_added += (goals_scored * 6) + (clean_sheets * 4)
        elif (element_type == 3):
            value_added += (goals_scored * 5) + clean_sheets
        elif (element_type == 4):
            value_added += (goals_scored * 4)

        # VALUE ADDED PER 90 (VAP90): the amount of points gained by a player NOT from appearances
        # per 90 minutes on the pitch
        if (minutes > 0):
            value_added_per_90 = round((value_added / minutes) * 90, 3)
        else:
            value_added_per_90 = 0

        # VALUE ADDED PER MILLION (VAPM): the amount of points gained by a player per million cost
        # above the cheapest alternative in that position
        if (element_type <= 2):
            if (now_cost > 4.0):
                value_added_per_million = round(value_added / (now_cost - 4.0), 3)
            else:
                # avoids divide by zero error - players at minimum price are almost always
                # benchwarmers and so usually aren't relevant to discussions around value
                value_added_per_million = 0
        elif (element_type >= 3):
            if (now_cost > 4.5):
                value_added_per_million = round(value_added / (now_cost - 4.5), 3)
            else:
                value_added_per_million = 0

        # VALUE ADDED PER MILLION PER 90 (VAPM90): value added per million above the cheapest
        # alternative in that position, per 90 minutes on the pitch
        if (minutes > 0):
            vapm_per_90 = round((value_added_per_million / minutes) * 90, 3)
        else:
            vapm_per_90 = 0

        # write player data to csv if they have played at all during the season
        if (minutes > 0):
            writer.writerow([first_name, second_name, element_type, total_points, minutes,
                goals_scored, assists, goals_conceded, bonus, clean_sheets, red_cards,
                yellow_cards, now_cost, value_added, value_added_per_90, value_added_per_million,
                vapm_per_90])
