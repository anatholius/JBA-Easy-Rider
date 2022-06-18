import json

years = {
    2020: "leap year", 2021: "regular year", 2022: "regular year",
    2023: "regular year", 2024: "leap year",
}

years_json = json.dumps(years, indent=4)
