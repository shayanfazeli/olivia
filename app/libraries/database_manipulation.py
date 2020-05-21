__author__ = ["Shayan Fazeli"]
__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

import pickle
from tqdm import tqdm
from datetime import datetime
from app import db, application_directory
import pandas
import numpy
import os
from erlab_coat.preprocessing import remove_county_word, get_cdc_data, parse_erlab_covid19_glance_collection, \
    add_cumsums_to_cases_table, prepare_google_mobility_data
from erlab_coat.meta import preprocessings, state_abbreviations
from app.entities import Election, InfluenzaActivityLevel, GoogleMobility, Cases, Diversity, Census, StateRestaurants, \
    ICUBeds, CovidHospitalizations, Mortality, LandAndWater
from app.libraries.utilities import floatify_df, floatify_dict, get_as_datetime


def preprocess_collection_for_database(path):
    collection = parse_erlab_covid19_glance_collection(path)

    # preprocessing
    for key in preprocessings.keys():
        for table_name in preprocessings[key].keys():
            table = collection[key][table_name].copy()
            lambdas = preprocessings[key][table_name]['lambdas']
            renames = preprocessings[key][table_name]['rename']
            remove = preprocessings[key][table_name]['remove']
            for column in lambdas.keys():
                table[column] = table[column].apply(lambdas[column])
            table.rename(renames, inplace=True, axis="columns", errors="raise")
            table.drop(columns=remove, inplace=True)
            collection[key][table_name] = table.copy()
            table = None

    # income
    def income_check1(x):
        try:
            output = x.split(',')[1]
        except:
            output = 'bad'
        return output

    collection['county']['diversityindex']['state'] = collection['county']['diversityindex']['Location'].apply(
        income_check1)
    collection['county']['diversityindex'] = collection['county']['diversityindex'][
        collection['county']['diversityindex']['state'] != 'bad']
    collection['county']['diversityindex']['county'] = collection['county']['diversityindex']['Location'].apply(
        lambda x: remove_county_word(x.split(', ')[0]))
    collection['county']['diversityindex'].drop(columns=['Location'], inplace=True)

    # diversity
    collection['county']['diversityindex']['state'] = collection['county']['diversityindex']['state'].apply(
        lambda x: x.strip())

    # mortality
    def mortality_check1(x):
        try:
            output = x.split(', ')[1]
        except:
            output = 'bad'
        return output

    collection['county']['mortality']['state'] = collection['county']['mortality']['county'].apply(
        mortality_check1).copy()
    collection['county']['mortality'] = collection['county']['mortality'][
        collection['county']['mortality']['state'] != 'bad']
    collection['county']['mortality']['county'] = collection['county']['mortality']['county'].apply(
        lambda x: remove_county_word(x.split(',')[0]))
    collection['county']['mortality']['state'] = collection['county']['mortality']['state'].apply(
        lambda x: state_abbreviations[x])

    # election
    collection['county']['election'].drop(columns=['state_po'], inplace=True)
    collection['county']['election'] = collection['county']['election'][
        collection['county']['election']['year'] == 2016]
    collection['county']['election']['state'] = collection['county']['election']['state'].apply(
        lambda x: state_abbreviations[x])
    output = {
        'state': [],
        'county': [],
        'democrat': [],
        'republican': [],
        'other': [],
    }

    for i in range(collection['county']['election'].shape[0]):
        row = collection['county']['election'].iloc[i, :]
        output['state'] += [row['state']]
        output['county'] += [row['county']]
        if row['party'] == 'democrat':
            output['democrat'] += [row['candidatevotes']]
            output['republican'] += [0]
            output['other'] += [0]
        elif row['party'] == 'republican':
            output['republican'] += [row['candidatevotes']]
            output['democrat'] += [0]
            output['other'] += [0]
        else:
            output['republican'] += [0]
            output['democrat'] += [0]
            output['other'] += [row['candidatevotes']]

    collection['county']['election'] = pandas.DataFrame(output)

    ## icu beds
    collection['county']['icu_beds']['state'] = collection['county']['icu_beds']['state'].apply(
        lambda x: state_abbreviations[x])

    ## income [removed]
    # collection['county']['income'] = collection['county']['income'].groupby(
    #     ['county', 'state']).mean().reset_index().copy()

    ## land and water
    collection['county']['land_and_water'] = collection['county']['land_and_water'].loc[:,
                                             ['state', 'county', 'ALAND', 'AWATER', 'ALAND_SQMI', 'AWATER_SQMI']]

    mortality = collection['county']['mortality'].copy().drop(columns=[
        'Mortality Rate, 1980*',
        'Mortality Rate, 1980* (Min)',
        'Mortality Rate, 1980* (Max)',
        'Mortality Rate, 1985*',
        'Mortality Rate, 1985* (Min)',
        'Mortality Rate, 1985* (Max)',
        'Mortality Rate, 1990*',
        'Mortality Rate, 1990* (Min)',
        'Mortality Rate, 1990* (Max)',
        'Mortality Rate, 1995*',
        'Mortality Rate, 1995* (Min)',
        'Mortality Rate, 1995* (Max)',
        'Mortality Rate, 2000*',
        'Mortality Rate, 2000* (Min)',
        'Mortality Rate, 2000* (Max)',
        'Mortality Rate, 2005*',
        'Mortality Rate, 2005* (Min)',
        'Mortality Rate, 2005* (Max)',
        'Mortality Rate, 2010*',
        'Mortality Rate, 2010* (Min)',
        'Mortality Rate, 2010* (Max)'
    ]).rename({
        'Mortality Rate, 2014*': 'mortality_rate',
        'Mortality Rate, 2014* (Min)': 'min_mortality_rate',
        'Mortality Rate, 2014* (Max)': 'max_mortality_rate',
        '% Change in Mortality Rate, 1980-2014': "change_in_mortality_rate",
        '% Change in Mortality Rate, 1980-2014 (Min)': "min_change_in_mortality_rate",
        '% Change in Mortality Rate, 1980-2014 (Max)': "max_change_in_mortality_rate"
    }, inplace=False, axis="columns", errors="raise")
    mortality = mortality.groupby(['county', 'state']).mean().copy().reset_index()

    # census
    census_full = collection['county']['census_full'].copy()
    census_full = census_full.groupby(['county', 'state']).mean().reset_index()

    tmp = (census_full['number_of_men'] + census_full['number_of_women']).copy()
    census_full.loc[~(tmp == 0), 'men_percentage'] = census_full.loc[~(tmp == 0), 'number_of_men'].copy() / tmp[~(tmp == 0)]
    census_full.loc[~(tmp == 0), 'women_percentage'] = census_full.loc[~(tmp == 0), 'number_of_women'].copy() / tmp[~(tmp == 0)]
    census_full['men_percentage'] *= (~(tmp == 0))
    census_full['women_percentage'] *= (~(tmp == 0))

    census_full['normalized_voting_age_citizens'] = census_full['voting_age_citizens'].copy() / census_full['total_population'].copy()

    land_and_water = collection['county']['land_and_water'].copy()
    land_and_water = land_and_water.groupby(['county', 'state']).sum().reset_index()

    election = collection['county']['election'].copy()
    election = election.groupby(['county', 'state']).sum().reset_index()

    tmp = (election['democrat'] + election['republican'] + election['other']).copy()
    election.loc[~(tmp == 0), 'democrat_percentage'] = election.loc[~(tmp == 0), 'democrat'].copy() / tmp[~(tmp == 0)]
    election.loc[~(tmp == 0), 'republican_percentage'] = election.loc[~(tmp == 0), 'republican'].copy() / tmp[~(tmp == 0)]
    election.loc[~(tmp == 0), 'other_than_democrat_or_republican_percentage'] = election.loc[~(tmp == 0), 'other'].copy() / tmp[
        ~(tmp == 0)]
    election['democrat_percentage'] *= (~(tmp == 0))
    election['republican_percentage'] *= (~(tmp == 0))
    election['other_than_democrat_or_republican_percentage'] *= (~(tmp == 0))

    icu_beds = collection['county']['icu_beds'].copy()
    icu_beds = icu_beds.groupby(['county', 'state']).sum().reset_index()

    diversity = collection['county']['diversityindex'].copy()
    diversity = diversity.groupby(['county', 'state']).sum().reset_index()

    covid_hospitalizations_df, influenza_activity_level_df = get_cdc_data(
        os.path.join(path, 'resolution/state/cdc_covid')
    )

    covid_hospitalizations_df.drop(columns = ['location', 'day_of_the_year'], inplace=True)
    influenza_activity_level_df.drop(columns=['location', 'day_of_the_year'], inplace=True)

    cases = collection['county']['cases'].copy().groupby(['state', 'county', 'confirmed_date']).sum().reset_index()
    cases = add_cumsums_to_cases_table(cases)
    cases = normalize_with_census(cases, census_full, [
        ('confirmed_count_cumsum', 'confirmed_count_cumsum_per100k', 100000.0),
        ('death_count_cumsum', 'death_count_cumsum_per100k', 100000.0),
        ('recovered_count_cumsum', 'recovered_count_cumsum_per100k', 100000.0)
    ])

    google_mobility = prepare_google_mobility_data(os.path.join(path, 'resolution/county/google_mobility.csv'))

    cases = floatify_df(cases)
    google_mobility = floatify_df(google_mobility)
    covid_hospitalizations_df = floatify_df(covid_hospitalizations_df)
    influenza_activity_level_df = floatify_df(influenza_activity_level_df)
    diversity = floatify_df(diversity)
    icu_beds = floatify_df(icu_beds)
    election = floatify_df(election)
    land_and_water = floatify_df(land_and_water)
    census_full = floatify_df(census_full)
    mortality = floatify_df(mortality)

    cases.dropna(inplace=True)
    google_mobility.dropna(inplace=True)
    covid_hospitalizations_df.dropna(inplace=True)
    influenza_activity_level_df.dropna(inplace=True)
    diversity.dropna(inplace=True)
    icu_beds.dropna(inplace=True)
    election.dropna(inplace=True)
    land_and_water.dropna(inplace=True)
    census_full.dropna(inplace=True)
    mortality.dropna(inplace=True)

    state_restaurants = pandas.read_csv(os.path.join(path, 'resolution/state/restaurant_business.csv'))



    return cases, google_mobility, covid_hospitalizations_df, influenza_activity_level_df, diversity, icu_beds, election, land_and_water, census_full, mortality, state_restaurants


def normalize_with_census(
        df,
        census,
        columns_to_normalize
):
    census = census.loc[:, ['total_population', 'state', 'county']]
    df = pandas.merge(left=df, right=census, on=['county', 'state'], how='outer')
    for c1, c2, coef in columns_to_normalize:
        df[c2] = coef * (df[c1].copy() / df['total_population'].copy())
    df.drop(columns=['total_population'], inplace=True)
    return df


def update_variable_to_entity(variable_to_entity, row, entity):
    main_columns = list(set(row.keys()) - set(['day_of_the_year', 'location', 'confirmed_date', 'state', 'county']))
    for m in main_columns:
        if m not in variable_to_entity.keys():
            variable_to_entity[m] = entity
        else:
            raise Exception("already assigned to an entity: {} -> {} / not to {}".format(m, variable_to_entity[m], entity))
    return variable_to_entity


def populate_database_with_glance(
        path=os.path.abspath(os.path.join(application_directory, '../warehouse/erlab_covid19_glance'))):

    cases, google_mobility, covid_hospitalizations_df, influenza_activity_level_df, diversity, icu_beds, election, land_and_water, census, mortality, state_restaurants = preprocess_collection_for_database(
        path)

    path_to_variable_to_entity = os.path.join(application_directory, '../warehouse/variable_to_entity.pkl')

    if os.path.isfile(path_to_variable_to_entity):
        with open(path_to_variable_to_entity, 'rb') as handle:
            variable_to_entity = pickle.load(handle)
    else:
        variable_to_entity = dict()

    # # ---
    # items = []
    # print("covid_hospitalizations_df...\n")
    #
    # for i in tqdm(range(covid_hospitalizations_df.shape[0])):
    #     row = covid_hospitalizations_df.iloc[i, :].to_dict()
    #     row = floatify_dict(row)
    #     try:
    #         row['confirmed_date'] = get_as_datetime(row['confirmed_date'])
    #     except:
    #         continue
    #     items.append(CovidHospitalizations(**row))
    #
    # variable_to_entity = update_variable_to_entity(variable_to_entity, row, CovidHospitalizations)
    #
    # db.session.add_all(items)
    # db.session.commit()
    #
    # # ---
    # items = []
    # print("influenza_activity_level_df...\n")
    #
    # for i in tqdm(range(influenza_activity_level_df.shape[0])):
    #     row = influenza_activity_level_df.iloc[i, :].to_dict()
    #     row = floatify_dict(row)
    #
    #     try:
    #         row['confirmed_date'] = get_as_datetime(row['confirmed_date'])
    #     except:
    #         continue
    #     items.append(InfluenzaActivityLevel(**row))
    # variable_to_entity = update_variable_to_entity(variable_to_entity, row, InfluenzaActivityLevel)
    #
    # db.session.add_all(items)
    # db.session.commit()
    #
    # # ---
    # items = []
    # print("diversity...\n")
    #
    # for i in tqdm(range(diversity.shape[0])):
    #     row = diversity.iloc[i, :].to_dict()
    #     row = floatify_dict(row)
    #     items.append(Diversity(**row))
    # variable_to_entity = update_variable_to_entity(variable_to_entity, row, Diversity)
    #
    # db.session.add_all(items)
    # db.session.commit()
    #
    # # ---
    # items = []
    # print("icu_beds...\n")
    #
    # for i in tqdm(range(icu_beds.shape[0])):
    #     row = icu_beds.iloc[i, :].to_dict()
    #     row = floatify_dict(row)
    #     items.append(ICUBeds(**row))
    # variable_to_entity = update_variable_to_entity(variable_to_entity, row, ICUBeds)
    #
    # db.session.add_all(items)
    # db.session.commit()
    #
    # # ---
    # items = []
    # print("election...\n")
    # for i in tqdm(range(election.shape[0])):
    #     row = election.iloc[i, :].to_dict()
    #     row = floatify_dict(row)
    #     items.append(Election(**row))
    # variable_to_entity = update_variable_to_entity(variable_to_entity, row, Election)
    #
    # db.session.add_all(items)
    # db.session.commit()
    # # ---
    # items = []
    # print("land_and_water...\n")
    #
    # for i in tqdm(range(land_and_water.shape[0])):
    #     row = land_and_water.iloc[i, :].to_dict()
    #     row = floatify_dict(row)
    #     items.append(LandAndWater(**row))
    # variable_to_entity = update_variable_to_entity(variable_to_entity, row, LandAndWater)
    #
    # db.session.add_all(items)
    # db.session.commit()
    #
    # # ---
    # items = []
    # print("census...\n")
    #
    # for i in tqdm(range(census.shape[0])):
    #     row = census.iloc[i, :].to_dict()
    #     row = floatify_dict(row)
    #     items.append(Census(**row))
    # variable_to_entity = update_variable_to_entity(variable_to_entity, row, Census)
    #
    # db.session.add_all(items)
    # db.session.commit()
    #
    # # ---
    # items = []
    # print("mortality...\n")
    #
    # for i in tqdm(range(mortality.shape[0])):
    #     row = mortality.iloc[i, :].to_dict()
    #     row = floatify_dict(row)
    #     items.append(Mortality(**row))
    # variable_to_entity = update_variable_to_entity(variable_to_entity, row, Mortality)
    #
    # db.session.add_all(items)
    # db.session.commit()
    #
    # # ---
    # items = []
    # print("google_mobility...\n")
    #
    # for i in tqdm(range(google_mobility.shape[0])):
    #     row = google_mobility.iloc[i, :].to_dict()
    #     row = floatify_dict(row)
    #     try:
    #         row['confirmed_date'] = get_as_datetime(row['confirmed_date'])
    #     except:
    #         continue
    #     items.append(GoogleMobility(**row))
    # variable_to_entity = update_variable_to_entity(variable_to_entity, row, GoogleMobility)
    #
    # db.session.add_all(items)
    # db.session.commit()
    #
    # # ---
    # items = []
    # print("cases...\n")
    # for i in tqdm(range(cases.shape[0])):
    #     row = cases.iloc[i, :].to_dict()
    #     row = floatify_dict(row)
    #     try:
    #         row['confirmed_date'] = get_as_datetime(row['confirmed_date'])
    #     except:
    #         continue
    #     items.append(Cases(**row))
    # variable_to_entity = update_variable_to_entity(variable_to_entity, row, Cases)
    #
    # db.session.add_all(items)
    # db.session.commit()

    # ---
    items = []
    print("state restaurant businesses...\n")
    for i in tqdm(range(state_restaurants.shape[0])):
        row = state_restaurants.iloc[i, :].to_dict()
        row = floatify_dict(row)
        items.append(StateRestaurants(**row))
    variable_to_entity = update_variable_to_entity(variable_to_entity, row, StateRestaurants)

    db.session.add_all(items)
    db.session.commit()

    with open(os.path.join(application_directory, '../warehouse/variable_to_entity.pkl'), 'wb') as handle:
        pickle.dump(variable_to_entity, handle)
