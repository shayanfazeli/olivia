from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired
from datetime import date
import operator
from app.blueprints.regional_visualizations.forms import fetch_latest_descriptions_for_choices


class RegionalComparisonForm(FlaskForm):
    var_choices = [
        ('total_population', 'x'),
        ('number_of_men', 'x'),
        ('number_of_women', 'x'),
        ('men_percentage', 'x'),
        ('women_percentage', 'x'),
        ('race_hispanic', 'x'),
        ('race_white', 'x'),
        ('race_black', 'x'),
        ('race_native', 'x'),
        ('race_asian', 'x'),
        ('pacific', 'x'),
        ('voting_age_citizens', 'x'),
        ('census_income_average',
         'x'),
        ('census_income_margin', 'x'),
        ('census_income_per_capita',
         'x'),
        ('census_income_per_capita_margin',
         'x'),
        ('census_poverty', 'x'),
        ('census_child_poverty', 'x'),
        ('professional_job_percentage', 'x'),
        ('service_job_percentage', 'x'),
        ('office_job_percentage', 'x'),
        ('construction_job_percentage', 'x'),
        ('production_job_percentage', 'x'),
        ('commute_drive_percentage', 'x'),
        ('commute_carpool_percentage', 'x'),
        ('commute_transit_percentage', 'x'),
        ('commute_walk_percentage', 'x'),
        ('commute_other_percentage', 'x'),
        ('commute_noneed_percentage', 'x'),
        ('number_of_employed_people', 'x'),
        ('employment_private_percentage', 'x'),
        ('employment_public_percentage', 'x'),
        ('employment_self_percentage', 'x'),
        ('employment_family_percentage', 'x'),
        ('unemployment_percentage', 'x'),
        ('icu_beds', 'x'),
        ('seniors_population_percentage',
         'x'),
        ('seniors_per_icubed',
         'x'),
        ('diversity_index', 'x'),
        ('diversity_black_race', 'Diversity Black Race Ratio'),
        ('diversity_native_race', 'Diversity Native Race Ratio'),
        ('diversity_asian_race', 'Diversity Asian Race Ratio'),
        ('diversity_pacific_race', 'Diversity Pacific Islander Race Ratio'),
        ('diversity_two_or_more_races', 'Diversity Two or More Race Combined Ratio'),
        ('diversity_hispanic_race', 'Diversity Hispanic Rce Ratio'),
        ('diversity_white_race', 'Diversity White Race Ratio'),
        ('ALAND_SQMI', 'Land Area in Square Miles'),
        ('AWATER_SQMI', 'Water Area in Square Miles'),
        # ('mean_land_area', 'Average Land Area'),
        # ('mean_land_water', 'Average Water Area'),
        # ('mean_income_mean', 'Average of Average Income'),
        # ('mean_income_median', 'Average of Median Income'),
        # ('mean_income_std', 'Average Income Standard Deviation'),
        ('mortality_rate', 'Mortality Rate'),
        ('min_mortality_rate', 'Minimum Mortality Rate'),
        ('max_mortality_rate', 'Maximum Mortality Rate'),
        ('change_in_mortality_rate', 'Change in Mortality Rate'),
        ('min_change_in_mortality_rate', 'Minimum Change in Mortality Rate'),
        ('max_change_in_mortality_rate', 'Maximum Change in Mortality Rate'),
        ('democrat_percentage', 'Democrat Vote Percentage'),
        ('republican_percentage', 'Republican Vote Percentage'),
        ('other_than_democrat_or_republican_percentage',
         'Votes other than democrat/republican - Percentage'),
        ('population_density', 'Population Density'),
        ('compliance', 'Compliance with the Shelter at Home Criteria'),
        ('state_cumulative_covid_hospitalization_rate_per_100k_ag0_4',
         'State Cumulative Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 0-4'),
        ('state_cumulative_covid_hospitalization_rate_per_100k_ag18_49',
         'State Cumulative Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 18-49'),
        ('state_cumulative_covid_hospitalization_rate_per_100k_ag5_17',
         'State Cumulative Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 5-17'),
        ('state_cumulative_covid_hospitalization_rate_per_100k_ag50_64',
         'State Cumulative Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 50-64'),
        ('state_cumulative_covid_hospitalization_rate_per_100k_ag65p',
         'State Cumulative Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 65+'),
        ('state_cumulative_covid_hospitalization_rate_per_100k_ag65_74',
         'State Cumulative Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 65-74'),
        ('state_cumulative_covid_hospitalization_rate_per_100k_ag75_84',
         'State Cumulative Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 75-84'),
        ('state_cumulative_covid_hospitalization_rate_per_100k_ag85p',
         'State Cumulative Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 85+'),
        ('state_cumulative_covid_hospitalization_rate_per_100k_agoverall',
         'State Cumulative Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: Overall'),
        ('state_weekly_covid_hospitalization_rate_per_100k_ag0_4',
         'State Weekly Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 0-4'),
        ('state_weekly_covid_hospitalization_rate_per_100k_ag18_49',
         'State Weekly Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 18-49'),
        ('state_weekly_covid_hospitalization_rate_per_100k_ag5_17',
         'State Weekly Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 5-17'),
        ('state_weekly_covid_hospitalization_rate_per_100k_ag50_64',
         'State Weekly Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 50-64'),
        ('state_weekly_covid_hospitalization_rate_per_100k_ag65p',
         'State Weekly Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 65+'),
        ('state_weekly_covid_hospitalization_rate_per_100k_ag65_74',
         'State Weekly Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 65-74'),
        ('state_weekly_covid_hospitalization_rate_per_100k_ag75_84',
         'State Weekly Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 75-84'),
        ('state_weekly_covid_hospitalization_rate_per_100k_ag85p',
         'State Weekly Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: 85+'),
        ('state_weekly_covid_hospitalization_rate_per_100k_agoverall',
         'State Weekly Lab Confirmed COVID-19 Hospitalization per 100,000 people - Age: Overall'),
        ('state_infleunza_activity_level', 'x'),
        ('state_eating_and_drinking_locations', 'x'),
        ('state_restaurant_worker_population', 'x'),
        ('state_restaurant_employment_percentage', 'x'),
        ('state_restaurants_annual_sale', 'x'),
        ('restaurants_table_service_to_state_contribution',
         'x'),
        ('restaurants_limited_service_to_state_contribution',
         'x'),
        ('google_mobility_retail_and_recreation_percent_change_from_baseline', 'x'),
        ('google_mobility_grocery_and_pharmacy_percent_change_from_baseline', 'x'),
        ('google_mobility_parks_percent_change_from_baseline', 'x'),
        ('google_mobility_transit_stations_percent_change_from_baseline', 'x'),
        ('google_mobility_workplaces_percent_change_from_baseline', 'x'),
        ('google_mobility_residential_percent_change_from_baseline', 'x'),

        # - health data
        # ('obesity_change_female_2001_2009', 'x'),
        # ('obesity_change_male_2001_2009', 'x'),
        # ('obesity_prevalence_female_2011', 'x'),
        # ('obesity_prevalence_male_2011', 'x'),
        # ('physical_activity_sufficient_prevalence_male_2011', 'x'),
        # ('physical_activity_sufficient_prevalence_female_2011', 'x'),
        # ('physical_activity_sufficient_difference_male_2001_2009', 'x'),
        # ('physical_activity_sufficient_difference_female_2001_2009', 'x'),
        # ('life_expectancy_male_2010', 'x'),
        # ('life_expectancy_female_2010', 'x'),
        # ('life_expectancy_difference_1985_2010_male', 'x'),
        # ('life_expectancy_difference_1985_2010_female', 'x'),
        # ('diabetes_diagnosed_prevalence_sex_male_2012', 'x'),
        # ('diabetes_undiagnosed_prevalence_sex_male_2012', 'x'),
        # ('diabetes_total_prevalence_sex_male_2012', 'x'),
        # ('diabetes_awareness_prevalence_sex_male_2012', 'x'),
        # ('diabetes_control_prevalence_sex_male_2012', 'x'),
        # ('diabetes_diagnosed_prevalence_sex_female_2012', 'x'),
        # ('diabetes_undiagnosed_prevalence_sex_female_2012', 'x'),
        # ('diabetes_total_prevalence_sex_female_2012', 'x'),
        # ('diabetes_awareness_prevalence_sex_female_2012', 'x'),
        # ('diabetes_control_prevalence_sex_female_2012', 'x'),
        # ('diabetes_diagnosed_prevalence_sex_both_2012', 'x'),
        # ('diabetes_undiagnosed_prevalence_sex_both_2012', 'x'),
        # ('diabetes_total_prevalence_sex_both_2012', 'x'),
        # ('diabetes_awareness_prevalence_sex_both_2012', 'x'),
        # ('diabetes_diagnosed_change_sex_male_1999_2012', 'x'),
        # ('diabetes_undiagnosed_change_sex_male_1999_2012', 'x'),
        # ('diabetes_total_change_sex_male_1999_2012', 'x'),
        # ('diabetes_awareness_change_sex_male_1999_2012', 'x'),
        # ('diabetes_control_change_sex_male_1999_2012', 'x'),
        # ('diabetes_diagnosed_change_sex_female_1999_2012', 'x'),
        # ('diabetes_undiagnosed_change_sex_female_1999_2012', 'x'),
        # ('diabetes_total_change_sex_female_1999_2012', 'x'),
        # ('diabetes_awareness_change_sex_female_1999_2012', 'x'),
        # ('diabetes_control_change_sex_female_1999_2012', 'x'),
        # ('diabetes_diagnosed_change_sex_both_1999_2012', 'x'),
        # ('diabetes_undiagnosed_change_sex_both_1999_2012', 'x'),
        # ('diabetes_total_change_sex_both_1999_2012', 'x'),
        # ('diabetes_awareness_change_sex_both_1999_2012', 'x'),
        # ('diabetes_control_change_sex_both_1999_2012', 'x'),
        # ('alcohol_prevalence_type_any_sex_both_2012', 'x'),
        # ('alcohol_prevalence_type_heavy_sex_both_2012', 'x'),
        # ('alcohol_prevalence_type_binge_sex_both_2012', 'x'),
        # ('alcohol_prevalence_type_prop_heavy_sex_both_2012', 'x'),
        # ('alcohol_prevalence_type_prop_binge_sex_both_2012', 'x'),
        # ('alcohol_prevalence_type_any_sex_female_2012', 'x'),
        # ('alcohol_prevalence_type_heavy_sex_female_2012', 'x'),
        # ('alcohol_prevalence_type_binge_sex_female_2012', 'x'),
        # ('alcohol_prevalence_type_prop_heavy_sex_female_2012', 'x'),
        # ('alcohol_prevalence_type_prop_binge_sex_female_2012', 'x'),
        # ('alcohol_prevalence_type_any_sex_male_2012', 'x'),
        # ('alcohol_prevalence_type_heavy_sex_male_2012', 'x'),
        # ('alcohol_prevalence_type_binge_sex_male_2012', 'x'),
        # ('alcohol_prevalence_type_prop_binge_sex_male_2012', 'x'),
        # ('alcohol_prevalence_type_prop_heavy_sex_male_2012', 'x'),
        # ('alcohol_change_type_any_sex_both_2005_2012', 'x'),
        # ('alcohol_change_type_heavy_sex_both_2005_2012', 'x'),
        # ('alcohol_change_type_binge_sex_both_2005_2012', 'x'),
        # ('alcohol_change_type_prop_heavy_sex_both_2005_2012', 'x'),
        # ('alcohol_change_type_prop_binge_sex_both_2005_2012', 'x'),
        # ('alcohol_change_type_any_sex_female_2005_2012', 'x'),
        # ('alcohol_change_type_heavy_sex_female_2005_2012', 'x'),
        # ('alcohol_change_type_binge_sex_female_2005_2012', 'x'),
        # ('alcohol_change_type_prop_heavy_sex_female_2005_2012', 'x'),
        # ('alcohol_change_type_prop_binge_sex_female_2005_2012', 'x'),
        # ('alcohol_change_type_any_sex_male_2005_2012', 'x'),
        # ('alcohol_change_type_heavy_sex_male_2005_2012', 'x'),
        # ('alcohol_change_type_binge_sex_male_2005_2012', 'x'),
        # ('alcohol_change_type_prop_heavy_sex_male_2005_2012', 'x'),
        # ('alcohol_change_type_prop_binge_sex_male_2005_2012', 'x')
    ]
    var_choices = fetch_latest_descriptions_for_choices(var_choices)
    var_choices.sort(key=operator.itemgetter(1))
    var = SelectField('Anchor Variable', default='commute_drive_percentage', choices=var_choices)
    county_filter1 = TextAreaField('Region Group 1 County Filter [Example: Los Angeles,Alameda]', validators=[])
    state_filter1 = TextAreaField('Region Group 1 State Filter [Example: NY,NJ]', validators=[])
    start_date1 = DateField("Region Group 1 - Start Date", validators=[DataRequired()])
    end_date1 = DateField("Region Group 1 - End Date", validators=[DataRequired()])

    county_filter2 = TextAreaField('Region Group 2 County Filter [Example: Los Angeles,Alameda]', validators=[])
    state_filter2 = TextAreaField('Region Group 2 State Filter [Example: NY,NJ]', validators=[])
    start_date2 = DateField("Region Group 2 - Start Date", validators=[DataRequired()])
    end_date2 = DateField("Region Group 2 - End Date", validators=[DataRequired()])
    bin_count = SelectField('Bin Count', default=100, choices=[('50', '50'), ('100', '100'), ('1000', '1000')], validators=[])
    prepare_json = SelectField('Automatic Distribution Report', default='no', choices=[('yes', 'Yes'), ('no', 'No')],
                            validators=[])

    submit = SubmitField('Compare')

    def validate(self):
        if not super(RegionalComparisonForm, self).validate():
            return False

        if (self.county_filter1.data == '') and (self.state_filter1.data == ''):
            self.county_filter1.errors.append("Region group 1 cannot be empty.")
            return False

        if (self.county_filter2.data == '') and (self.state_filter2.data == ''):
            self.county_filter2.errors.append("Region group 2 cannot be empty.")
            return False

        def turn_to_date(x: str) -> date:
            tmp = str(x)
            date_parts = [int(e) for e in tmp.split('-')]
            return date(date_parts[0], date_parts[1], date_parts[2])

        start_date1 = turn_to_date(self.start_date1.data)
        end_date1 = turn_to_date(self.end_date1.data)
        start_date2 = turn_to_date(self.start_date2.data)
        end_date2 = turn_to_date(self.end_date2.data)
        date_delta1 = end_date1 - start_date1
        date_delta2 = end_date2 - start_date2

        if date_delta1.days < 0:
            msg = "Please check the specified dates again."
            self.start_date1.errors.append(msg)
            self.end_date1.errors.append(msg)
            return False

        if date_delta2.days < 0:
            msg = "Please check the specified dates again."
            self.start_date2.errors.append(msg)
            self.end_date2.errors.append(msg)
            return False

        return True
