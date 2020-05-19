import pickle
import os
import pandas
from functools import reduce
from datetime import datetime, date, timedelta
import numpy
from erlab_coat.meta import label2description
from erlab_coat.preprocessing import interpolate_by_location, add_location_to_df, add_day_of_the_year_to_cases_table
from app.entities import Election, InfluenzaActivityLevel, GoogleMobility, Cases, Diversity, Census, StateRestaurants, \
    ICUBeds, CovidHospitalizations, Mortality, LandAndWater
from app import application_directory
from app.libraries.utilities import floatify_df


def get_df_for_variable_query(db, var, variable2entity, county_filter, state_filter):
    entity = variable2entity[var]
    if 'confirmed_date' in dir(entity):
        columns = ['county', 'state', 'confirmed_date']
    else:
        columns = ['county', 'state']

    attributes = [getattr(entity, e) for e in columns + [var]]

    df = db.session.query(*attributes)#.add_columns(*attributes)
    if county_filter is not None:
        df = df.filter(entity.county.in_(county_filter))
    if state_filter is not None:
        df = df.filter(entity.state.in_(state_filter))

    df = pandas.DataFrame(data=df.all(), columns=columns + [var])
    return df


def special_reduce(left, right):
    merge_on = list(set(left.columns.tolist()).intersection(set(right.columns.tolist())))

    df = pandas.merge(left, right, on=merge_on, how='outer')
    df.dropna(inplace=True)
    return df


def get_data_for_query(
        db,
        var1,
        var2,
        var3,
        var4,
        county_filter='',
        state_filter='',
        resolution = 'county',
        interpolate = True
):
    # todo: make it quicker
    accepted_counties = [e.strip() for e in county_filter.split(',') if not e == '']

    for i in range(len(accepted_counties)):
        if ' ' in accepted_counties[i]:
            elements = accepted_counties[i].split(' ')
            for j in range(len(elements)):
                elements[j] = elements[j][0].upper() + elements[j][1:].lower()
            accepted_counties[i] = ' '.join(elements)
    if len(accepted_counties) == 0:
        accepted_counties = None

    accepted_states = [e.strip() for e in state_filter.split(',') if not e == '']
    if len(accepted_states) == 0:
        accepted_states = None

    with open(os.path.join(application_directory, '../warehouse/variable_to_entity.pkl'), 'rb') as handle:
        variable2entity = pickle.load(handle)

    dfs = [
        get_df_for_variable_query(db, e, variable2entity, accepted_counties, accepted_states) for e in [var1, var2, var3, var4]
        ]

    output_df = reduce(lambda left, right: special_reduce(left, right), dfs)

    output_df.confirmed_date = output_df.confirmed_date.apply(lambda x: str(x.date()))

    if interpolate:
        output_df = add_location_to_df(output_df)
        output_df = add_day_of_the_year_to_cases_table(output_df)
        output_df.dropna(inplace=True)
        max_day = output_df.day_of_the_year.max()
        output_df = interpolate_by_location(output_df, max_day=max_day)
        output_df.drop(columns=['location', 'day_of_the_year'], inplace=True)

    output_df = floatify_df(output_df)

    if resolution == 'state':
        try:
            output_df = output_df.groupby(['state', 'confirmed_date']).mean().reset_index()
        except:
            import pdb
            pdb.set_trace()

    return output_df


def process_for_d3_json(df):
    # todo: make it quicker
    df = add_day_of_the_year_to_cases_table(df)
    df = add_location_to_df(df)
    output = list()
    t_var = "day_of_the_year"

    unique_locations = df.location.unique().tolist()
    for unique_location in unique_locations:
        tmp = {
            'Name': unique_location,
            'location': unique_location,
        }

        for column in df.columns.tolist():
            if column in ['Name', 'day_of_the_year', 'confirmed_date']:
                continue
            tmp[label2description[column]] = list()

        tmp_df = df[df['location'] == unique_location].copy()
        tmp_df.sort_values(by=t_var, inplace=True)

        for i in range(tmp_df.shape[0]):
            row = tmp_df.iloc[i]
            row[t_var] = doty_to_date(row[t_var])

            for column in label2description.keys():
                if column in row.keys():
                    assert not pandas.isna(row[column]), "it is nan: \n{}\n".format(tmp_df)
                    tmp[label2description[column]].append([row["day_of_the_year"], row[column]])

        output.append(tmp.copy())

    return output


def doty_to_date(day_of_the_year):
    days = day_of_the_year - 1
    out = str(date(2020, 1, 1) + timedelta(days=int(days))).replace('-', '/')
    return out