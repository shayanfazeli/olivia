__author__ = ["Shayan Fazeli"]
__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

"""
querying:

```
out = db.session.query(Election).order_by(Election.state).filter(Election.county=="New York")
out = list(out)
```
"""


from app import db


class Election(db.Model):
    __tablename__ = "election"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255), index=True)
    county = db.Column(db.String(255))
    democrat = db.Column(db.Float, nullable=True)
    republican = db.Column(db.Float, nullable=True)
    other = db.Column(db.Float, nullable=True)
    democrat_percentage = db.Column(db.Float, nullable=True)
    republican_percentage = db.Column(db.Float, nullable=True)
    other_than_democrat_or_republican_percentage = db.Column(db.Float, nullable=True)
    __table_args__ = (db.Index('myindex_election', 'county', 'state', unique=True), )


class Census(db.Model):
    __tablename__ = "census"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255))
    county = db.Column(db.String(255))
    total_population = db.Column(db.Float, nullable=True)
    number_of_men = db.Column(db.Float, nullable=True)
    number_of_women = db.Column(db.Float, nullable=True)
    men_percentage = db.Column(db.Float, nullable=True)
    women_percentage = db.Column(db.Float, nullable=True)
    race_hispanic = db.Column(db.Float, nullable=True)
    race_white = db.Column(db.Float, nullable=True)
    race_black = db.Column(db.Float, nullable=True)
    race_native = db.Column(db.Float, nullable=True)
    race_asian = db.Column(db.Float, nullable=True)
    pacific = db.Column(db.Float, nullable=True)
    voting_age_citizens = db.Column(db.Float, nullable=True)
    normalized_voting_age_citizens = db.Column(db.Float, nullable=True)
    census_income_average = db.Column(db.Float, nullable=True)
    census_income_margin = db.Column(db.Float, nullable=True)
    census_income_per_capita = db.Column(db.Float, nullable=True)
    census_income_per_capita_margin = db.Column(db.Float, nullable=True)
    census_poverty = db.Column(db.Float, nullable=True)
    census_child_poverty = db.Column(db.Float, nullable=True)
    professional_job_percentage = db.Column(db.Float, nullable=True)
    service_job_percentage = db.Column(db.Float, nullable=True)
    office_job_percentage = db.Column(db.Float, nullable=True)
    construction_job_percentage = db.Column(db.Float, nullable=True)
    production_job_percentage = db.Column(db.Float, nullable=True)
    commute_drive_percentage = db.Column(db.Float, nullable=True)
    commute_carpool_percentage = db.Column(db.Float, nullable=True)
    commute_transit_percentage = db.Column(db.Float, nullable=True)
    commute_walk_percentage = db.Column(db.Float, nullable=True)
    commute_other_percentage = db.Column(db.Float, nullable=True)
    commute_noneed_percentage = db.Column(db.Float, nullable=True)
    number_of_employed_people = db.Column(db.Float, nullable=True)
    employment_private_percentage = db.Column(db.Float, nullable=True)
    employment_public_percentage = db.Column(db.Float, nullable=True)
    employment_self_percentage = db.Column(db.Float, nullable=True)
    employment_family_percentage = db.Column(db.Float, nullable=True)
    unemployment_percentage = db.Column(db.Float, nullable=True)

    __table_args__ = (db.Index('myindex_census', 'county', 'state', unique=True), )


class ICUBeds(db.Model):
    __tablename__ = "icu_beds"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255))
    county = db.Column(db.String(255))
    icu_beds = db.Column(db.Float, nullable=True)
    senior_population_percentage = db.Column(db.Float, nullable=True)
    seniors_per_icubed = db.Column(db.Float, nullable=True)

    __table_args__ = (db.Index('myindex_icubeds', 'county', 'state', unique=True),)


class Mortality(db.Model):
    __tablename__ = "mortality"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255))
    county = db.Column(db.String(255))
    mortality_rate = db.Column(db.Float, nullable=True)
    min_mortality_rate = db.Column(db.Float, nullable=True)
    max_mortality_rate = db.Column(db.Float, nullable=True)
    change_in_mortality_rate = db.Column(db.Float, nullable=True)
    min_change_in_mortality_rate = db.Column(db.Float, nullable=True)
    max_change_in_mortality_rate = db.Column(db.Float, nullable=True)

    __table_args__ = (db.Index('myindex_mortality', 'county', 'state', unique=True),)


class LandAndWater(db.Model):
    __tablename__ = "land_and_water"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255))
    county = db.Column(db.String(255))
    ALAND = db.Column(db.Float, nullable=True)
    AWATER = db.Column(db.Float, nullable=True)
    ALAND_SQMI = db.Column(db.Float, nullable=True)
    AWATER_SQMI = db.Column(db.Float, nullable=True)

    __table_args__ = (db.Index('myindex_landandwater', 'county', 'state', unique=True),)


class Diversity(db.Model):
    __tablename__ = "diversity"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255))
    county = db.Column(db.String(255))
    diversity_index = db.Column(db.Float, nullable=True)
    diversity_black_race = db.Column(db.Float, nullable=True)
    diversity_native_race = db.Column(db.Float, nullable=True)
    diversity_asian_race = db.Column(db.Float, nullable=True)
    diversity_pacific_race = db.Column(db.Float, nullable=True)
    diversity_two_or_more_races = db.Column(db.Float, nullable=True)
    diversity_hispanic_race = db.Column(db.Float, nullable=True)
    diversity_white_race = db.Column(db.Float, nullable=True)

    __table_args__ = (db.Index('myindex_diversity', 'county', 'state', unique=True),)


class StateRestaurants(db.Model):
    __tablename__ = "restaurant_business"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255))
    state_eating_and_drinking_locations = db.Column(db.Float, nullable=True)
    state_restaurant_worker_population = db.Column(db.Float, nullable=True)
    state_restaurant_employment_percentage = db.Column(db.Float, nullable=True)
    state_restaurants_annual_sale = db.Column(db.Float, nullable=True)
    restaurants_table_service_to_state_contribution = db.Column(db.Float, nullable=True)
    restaurants_limited_service_to_state_contribution = db.Column(db.Float, nullable=True)
    __table_args__ = (db.Index('myindex_staterestaurants', 'state', unique=True),)


class GoogleMobility(db.Model):
    __tablename__ = "google_mobility"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255))
    county = db.Column(db.String(255))
    confirmed_date = db.Column(db.DateTime)
    retail_and_recreation_percent_change_from_baseline = db.Column(db.Float, nullable=True)
    grocery_and_pharmacy_percent_change_from_baseline = db.Column(db.Float, nullable=True)
    parks_percent_change_from_baseline = db.Column(db.Float, nullable=True)
    transit_stations_percent_change_from_baseline = db.Column(db.Float, nullable=True)
    workplaces_percent_change_from_baseline = db.Column(db.Float, nullable=True)
    residential_percent_change_from_baseline = db.Column(db.Float, nullable=True)
    compliance = db.Column(db.Float, nullable=True)
    __table_args__ = (db.Index('myindex_googlemobility', 'county', 'state', 'confirmed_date', unique=True), db.UniqueConstraint('county', 'state', 'confirmed_date'))


class Cases(db.Model):
    __tablename__ = "cases"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255))
    county = db.Column(db.String(255))
    confirmed_date = db.Column(db.DateTime)
    confirmed_count = db.Column(db.Float, nullable=True)
    death_count = db.Column(db.Float, nullable=True)
    recovered_count = db.Column(db.Float, nullable=True)
    confirmed_count_cumsum = db.Column(db.Float, nullable=True)
    death_count_cumsum = db.Column(db.Float, nullable=True)
    recovered_count_cumsum = db.Column(db.Float, nullable=True)
    confirmed_count_cumsum_per100k = db.Column(db.Float, nullable=True)
    death_count_cumsum_per100k = db.Column(db.Float, nullable=True)
    recovered_count_cumsum_per100k = db.Column(db.Float, nullable=True)
    __table_args__ = (db.Index('myindex_cases', 'county', 'state', 'confirmed_date', unique=True), db.UniqueConstraint('county', 'state', 'confirmed_date'))


class InfluenzaActivityLevel(db.Model):
    __tablename__ = "influenza_activity_level"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255))
    confirmed_date = db.Column(db.DateTime)
    state_infleunza_activity_level = db.Column(db.Float, nullable=True)
    __table_args__ = (db.Index('myindex_influenzaactivitylevel', 'state', 'confirmed_date', unique=True), db.UniqueConstraint('state', 'confirmed_date'))


class CovidHospitalizations(db.Model):
    __tablename__ = "covid_hospitalizations"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255))
    confirmed_date = db.Column(db.DateTime)
    state_cumulative_covid_hospitalization_rate_per_100k_ag0_4 = db.Column(db.Float, nullable=True)
    state_weekly_covid_hospitalization_rate_per_100k_ag0_4 = db.Column(db.Float, nullable=True)
    state_cumulative_covid_hospitalization_rate_per_100k_ag18_49 = db.Column(db.Float, nullable=True)
    state_weekly_covid_hospitalization_rate_per_100k_ag18_49 = db.Column(db.Float, nullable=True)
    state_cumulative_covid_hospitalization_rate_per_100k_ag5_17 = db.Column(db.Float, nullable=True)
    state_weekly_covid_hospitalization_rate_per_100k_ag5_17 = db.Column(db.Float, nullable=True)
    state_cumulative_covid_hospitalization_rate_per_100k_ag50_64 = db.Column(db.Float, nullable=True)
    state_weekly_covid_hospitalization_rate_per_100k_ag50_64 = db.Column(db.Float, nullable=True)
    state_cumulative_covid_hospitalization_rate_per_100k_ag65p = db.Column(db.Float, nullable=True)
    state_weekly_covid_hospitalization_rate_per_100k_ag65p = db.Column(db.Float, nullable=True)
    state_cumulative_covid_hospitalization_rate_per_100k_ag65_74 = db.Column(db.Float, nullable=True)
    state_weekly_covid_hospitalization_rate_per_100k_ag65_74 = db.Column(db.Float, nullable=True)
    state_cumulative_covid_hospitalization_rate_per_100k_ag75_84 = db.Column(db.Float, nullable=True)
    state_weekly_covid_hospitalization_rate_per_100k_ag75_84 = db.Column(db.Float, nullable=True)
    state_cumulative_covid_hospitalization_rate_per_100k_ag85p = db.Column(db.Float, nullable=True)
    state_weekly_covid_hospitalization_rate_per_100k_ag85p = db.Column(db.Float, nullable=True)
    state_cumulative_covid_hospitalization_rate_per_100k_agoverall = db.Column(db.Float, nullable=True)
    state_weekly_covid_hospitalization_rate_per_100k_agoverall = db.Column(db.Float, nullable=True)

    __table_args__ = (db.Index('myindex_covidhospitalization', 'state', 'confirmed_date', unique=True), db.UniqueConstraint('state', 'confirmed_date'))


class Alcohol(db.Model):
    __tablename__ = "alcohol"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255), index=True)
    county = db.Column(db.String(255))
    alcohol_prevalence_type_any_sex_both_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_heavy_sex_both_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_binge_sex_both_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_prop_heavy_sex_both_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_prop_binge_sex_both_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_any_sex_female_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_heavy_sex_female_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_binge_sex_female_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_prop_heavy_sex_female_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_prop_binge_sex_female_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_any_sex_male_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_heavy_sex_male_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_binge_sex_male_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_prop_binge_sex_male_2012 = db.Column(db.Float, nullable=True)
    alcohol_prevalence_type_prop_heavy_sex_male_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_any_sex_both_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_heavy_sex_both_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_binge_sex_both_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_prop_heavy_sex_both_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_prop_binge_sex_both_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_any_sex_female_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_heavy_sex_female_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_binge_sex_female_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_prop_heavy_sex_female_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_prop_binge_sex_female_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_any_sex_male_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_heavy_sex_male_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_binge_sex_male_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_prop_heavy_sex_male_2005_2012 = db.Column(db.Float, nullable=True)
    alcohol_change_type_prop_binge_sex_male_2005_2012 = db.Column(db.Float, nullable=True)
    __table_args__ = (db.Index('myindex_alcohol', 'county', 'state', unique=True), )


class Diabetes(db.Model):
    __tablename__ = "diabetes"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255), index=True)
    county = db.Column(db.String(255))
    diabetes_diagnosed_prevalence_sex_male_2012 = db.Column(db.Float, nullable=True)
    diabetes_undiagnosed_prevalence_sex_male_2012 = db.Column(db.Float, nullable=True)
    diabetes_total_prevalence_sex_male_2012 = db.Column(db.Float, nullable=True)
    diabetes_awareness_prevalence_sex_male_2012 = db.Column(db.Float, nullable=True)
    diabetes_control_prevalence_sex_male_2012 = db.Column(db.Float, nullable=True)
    diabetes_diagnosed_prevalence_sex_female_2012 = db.Column(db.Float, nullable=True)
    diabetes_undiagnosed_prevalence_sex_female_2012 = db.Column(db.Float, nullable=True)
    diabetes_total_prevalence_sex_female_2012 = db.Column(db.Float, nullable=True)
    diabetes_awareness_prevalence_sex_female_2012 = db.Column(db.Float, nullable=True)
    diabetes_control_prevalence_sex_female_2012 = db.Column(db.Float, nullable=True)
    diabetes_diagnosed_prevalence_sex_both_2012 = db.Column(db.Float, nullable=True)
    diabetes_undiagnosed_prevalence_sex_both_2012 = db.Column(db.Float, nullable=True)
    diabetes_total_prevalence_sex_both_2012 = db.Column(db.Float, nullable=True)
    diabetes_awareness_prevalence_sex_both_2012 = db.Column(db.Float, nullable=True)
    diabetes_control_prevalence_sex_both_2012 = db.Column(db.Float, nullable=True)
    diabetes_diagnosed_change_sex_male_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_undiagnosed_change_sex_male_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_total_change_sex_male_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_awareness_change_sex_male_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_control_change_sex_male_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_diagnosed_change_sex_female_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_undiagnosed_change_sex_female_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_total_change_sex_female_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_awareness_change_sex_female_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_control_change_sex_female_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_diagnosed_change_sex_both_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_undiagnosed_change_sex_both_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_total_change_sex_both_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_awareness_change_sex_both_1999_2012 = db.Column(db.Float, nullable=True)
    diabetes_control_change_sex_both_1999_2012 = db.Column(db.Float, nullable=True)
    __table_args__ = (db.Index('myindex_diabetes', 'county', 'state', unique=True), )


class ObesityAndLife(db.Model):
    __tablename__ = "obesity_and_life"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255), index=True)
    county = db.Column(db.String(255))
    obesity_change_female_2001_2009 = db.Column(db.Float, nullable=True)
    obesity_change_male_2001_2009 = db.Column(db.Float, nullable=True)
    obesity_prevalence_female_2011 = db.Column(db.Float, nullable=True)
    obesity_prevalence_male_2011 = db.Column(db.Float, nullable=True)
    physical_activity_sufficient_prevalence_male_2011 = db.Column(db.Float, nullable=True)
    physical_activity_sufficient_prevalence_female_2011 = db.Column(db.Float, nullable=True)
    physical_activity_sufficient_difference_male_2001_2009 = db.Column(db.Float, nullable=True)
    physical_activity_sufficient_difference_female_2001_2009 = db.Column(db.Float, nullable=True)
    life_expectancy_male_2010 = db.Column(db.Float, nullable=True)
    life_expectancy_female_2010 = db.Column(db.Float, nullable=True)
    life_expectancy_difference_1985_2010_male = db.Column(db.Float, nullable=True)
    life_expectancy_difference_1985_2010_female = db.Column(db.Float, nullable=True)
    __table_args__ = (db.Index('myindex_obesity', 'county', 'state', unique=True), )






