# Data bronnen:
    - CBS
    - Veiligheid NL
    - NHG standaard valpreventie/risico
    - Wetenschappelijke literatuur 

populatieNL = 17811291
percentage_ouderenNL = 0.2 
ernstige_valincidenten = 105000 # veiligheidNL

direct_costs = 1100000000 # 2020 veiligheidNL
direct_cost_pp = round(direct_costs / ernstige_valincidenten)

valrisico_incidentie = 0.33 # veiligheidNL
percentage_severe = 0.10 #veiligheidNL
percentage_onbekende_visusproblematiek = 0.2 
odds_ratio_val_door_visus =  1.21
# Risk factors for falls in community-dwelling older people: a systematic review and meta-analysis
#Vision and hearing impairment also increased risk, especially vision problems (1.4 for all fallers and 1.6 for recurrent fallers).
# for all fallers OR 1.35, multivariate OR = 1.21

risico_ernstig_valincident = ernstige_valincidenten / (populatieNL * percentage_ouderenNL * valrisico_incidentie)
gemiddeld_aantal_vallen = 3.6
# gemiddeld aantal vallen (3.6 volgens stevig staan / VeiligheidNL)
percentage_sterfgevallen = (17*365) / ernstige_valincidenten
# aantal sterfgevallen (17 per dag van de 0.33 * ouderen met verhoogd valrisico)



Berekening potentieel aantal vallen / potentiële associatie sterfgeval:
n_vallen_65plus = round(n_65plus_at_risk_met_visusproblematiek * gemiddeld_aantal_vallen)

potentieel_vallen_door_visusproblematiek_65plus = round(
    n_vallen_65plus - n_vallen_65plus / odds_ratio_val_door_visus
    ),

 vallen_visusproblematiek_gerelateerd_aan_potentieel_sterfgeval_65plus =  round(potentieel_vallen_door_visusproblematiek_65plus * 
    risico_ernstig_valincident * percentage_sterfgevallen), 
