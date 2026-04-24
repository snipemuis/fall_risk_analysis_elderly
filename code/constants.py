ernstige_valincidenten = 105000  # veiligheidNL

direct_costs = 1_100_000_000  # 2020 veiligheidNL
direct_cost_pp = round(direct_costs / ernstige_valincidenten)

valrisico_incidentie = 0.33  # veiligheidNL
percentage_severe = 0.10  # veiligheidNL
percentage_onbekende_visusproblematiek = 0.2

# gemiddeld aantal vallen (3.6 volgens nicole / VeiligheidNL)
gemiddeld_aantal_vallen = 3.6

# Risk factors for falls in community-dwelling older people: a systematic review and meta-analysis
# Vision and hearing impairment also increased risk, especially vision problems
# (1.4 for all fallers and 1.6 for recurrent fallers).
# for all fallers OR 1.35, multivariate OR = 1.21
odds_ratio_val_door_visus = 1.21
