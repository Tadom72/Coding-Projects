"This dict holds the rank name and their associated average ssr"
srr_value = {
  "bronze_5": 550,
  "bronze_4": 650,
  "bronze_3": 750,
  "bronze_2": 850,
  "bronze_1": 950,
  "silver_5": 1050,
  "silver_4": 1150,
  "silver_3": 1250,
  "silver_2": 1350,
  "silver_1": 1450,
  "gold_5": 1550,
  "gold_4": 1650,
  "gold_3": 1750,
  "gold_2": 1850,
  "gold_1": 1950,
  "platinum_5": 2050,
  "platinum_4": 2150,
  "platinum_3": 2250,
  "platinum_2": 2350,
  "platinum_1": 2450,
  "emerald_5": 2550,
  "emerald_4": 2650,
  "emerald_3": 2750,
  "emerald_2": 2850,
  "emerald_1": 2950,
  "diamond_5": 3050,
  "diamond_4": 3150,
  "diamond_3": 3250,
  "diamond_2": 3350,
  "diamond_1": 3450,
  "master_5": 3550,
  "master_4": 3650,
  "master_3": 3750,
  "master_2": 3850,
  "master_1": 3950,
  "grandMaster_5": 4050,
  "grandMaster_4": 4150,
  "grandMaster_3": 4250,
  "grandMaster_2": 4350,
  "grandMaster_1": 4450,
  "champion_5": 4550,
  "champion_4": 4650,
  "champion_3": 4750,
  "champion_2": 4850,
  "champion_1": 4950,
}

def get_srr(rank):
    srr = srr_value[rank]
    return srr

def get_rank(srr):
    "Makes it so the srr is rounded to the nearest 50 so it can find the closets rank"
    srr = 50 * round(srr/50)
    "If the  srr ends with 100 being the nearest multiple of 50 then minus 50 as that should be closest rank"
    if srr % 100 != 50:
        srr = srr - 50
    rank = (list(srr_value.keys())[list(srr_value.values()).index(srr)])
    return rank 

def get_lobby_srr(bottom_rank, top_rank):
    bottom_srr = get_srr(bottom_rank)
    top_srr = get_srr(top_rank)
    avg_srr = (top_srr + bottom_srr) // 2
    round(avg_srr)
    return avg_srr

print(get_srr("gold_1"))
print(get_lobby_srr("silver_1", "gold_1"))


