# fall risk elderly analysis

Analysis of fall risk among elderly (65+) in the Netherlands, including an estimation
of the number of falls attributable to vision problems.

## Data sources
- **CBS / StatLine** — population and demographic data
- **VeiligheidNL** — injury and fall incidence data
- **Scientific literature** — risk factors and epidemiological estimates
- **NHG standaard valpreventie/risico**

## License
© 2026 M.B. Muijzer. Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
You are free to share and adapt this work for non-commercial purposes, provided appropriate credit is given. Commercial use is not permitted without explicit written permission.

## Assumptions

### VeiligheidNL
- valrisico_incidentie = 0.33 
- ernstige_valincidenten = 105000 
- percentage_severe = 0.10 
- direct_costs = 1100000000
- gemiddeld_aantal_vallen = 3.6 **(gemiddeld aantal vallen volgens stevig staan / VeiligheidNL)**

### scientific literature and other sources
- percentage_onbekende_visusproblematiek = 0.2 
- OR risk of falls due to vision problems: for all fallers OR 1.35, multivariate OR = 1.21 **(Risk factors for falls in community-dwelling older people: a systematic review and meta-analysis)**

### berekeningen
- direct_cost_pp = round(direct_costs / ernstige_valincidenten)
- risico_ernstig_valincident = ernstige_valincidenten / (populatieNL * - - percentage_ouderenNL * valrisico_incidentie)
- percentage_sterfgevallen = (17*365) / ernstige_valincidenten **(aantal sterfgevallen (17 per dag van de 0.33 * ouderen met verhoogd valrisico))**
- Berekening potentieel aantal vallen / potentiële associatie sterfgeval:
n_vallen_65plus = round(n_65plus_at_risk_met_visusproblematiek * gemiddeld_aantal_vallen)
- potentieel_vallen_door_visusproblematiek_65plus = round(n_vallen_65plus - n_vallen_65plus / odds_ratio_val_door_visus),
- vallen_visusproblematiek_gerelateerd_aan_potentieel_sterfgeval_65plus =  round(potentieel_vallen_door_visusproblematiek_65plus *  risico_ernstig_valincident * percentage_sterfgevallen), 
