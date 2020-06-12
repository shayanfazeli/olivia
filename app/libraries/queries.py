import pickle
import os
import pandas
from functools import reduce
from datetime import datetime, date, timedelta
from oliver.data.utilities.date_manipulation import get_datetime_object_from_date_string
import numpy
from erlab_coat.meta import label2description
from erlab_coat.preprocessing import doty_to_date, olivia_interpolation, add_location_to_df, \
    add_day_of_the_year_to_cases_table
from app.entities import Election, InfluenzaActivityLevel, GoogleMobility, Cases, Diversity, Census, StateRestaurants, \
    ICUBeds, CovidHospitalizations, Mortality, LandAndWater, ObesityAndLife, Alcohol, Diabetes
from app import application_directory
from app.libraries.utilities import floatify_df
import sys
import time


def get_df_for_county_scoring(
        db,
        past_focus_factor: float = 0.9,
        focus_cases: float = 1.0,
        focus_deaths: float = 0.5,
        focus_recoveries: float = 0,
        min_date: str = "2020-06-01",
        normalize: bool = True
) -> pandas.DataFrame:
    """
    The :func:`get_df_for_county_scoring` obtains COVID-19 Region Health Scores

    Parameters
    ----------
    db: required
        The database instance

    past_focus_factor: 'float', optional (default=0.9)
        Float value indicating how much focus should be put on previous ith day.

    focus_cases:  'float', optional (default=1.0)
        Focus value

    focus_deaths:  'float', optional (default=0.5)
        Focus value

    focus_recoveries: 'float', optional (default=0.0)
        Focus value

    min_date: `str`, optional (default='2020-06-01')
        The minimum date, before which all the records will be neglected.

    normalize: `bool`, optional (default=True)
        If set to true, returned scores will be between 0 and 100.

    Returns
    ----------
    The `pandas.DataFrame` object that includes counties, states, and their score.
    """
    df = db.session.query(
        Cases.county,
        Cases.state,
        Cases.confirmed_date,
        Cases.confirmed_count,
        Cases.confirmed_count_cumsum_per100k,
        Cases.death_count,
        Cases.death_count_cumsum_per100k,
        Cases.recovered_count,
        Cases.recovered_count_cumsum_per100k
    )
    if min_date is not None:
        df = df.filter(Cases.confirmed_date >= get_datetime_object_from_date_string(min_date))
    columns = ['county', 'state', 'confirmed_date', 'confirmed_count', 'confirmed_count_cumsum_per100k', 'death_count',
               'death_count_cumsum_per100k', 'recovered_count', 'recovered_count_cumsum_per100k']

    df = pandas.DataFrame(data=df.all(), columns=columns)

    def score_compute(subdf):
        assert past_focus_factor <= 1.0
        if subdf.shape[0] < 2:
            return pandas.DataFrame({'score': [0]})
        else:
            subdf = subdf.copy()
            subdf.reset_index(drop=True, inplace=True)
            subdf['historical_value'] = past_focus_factor ** (numpy.arange(subdf.shape[0] - 1, -1, -1) - 1)
            subdf['confirmed_count_t_minus_tprev'] = subdf.confirmed_count.diff()
            subdf.loc[1:, 'confirmed_count_tprev'] = subdf.confirmed_count.to_numpy()[:-1]
            subdf.loc[1:, 'confirmed_count_cumsum_per100k_tprev'] = subdf.confirmed_count_cumsum_per100k.to_numpy()[:-1]

            subdf['death_count_t_minus_tprev'] = subdf.death_count.diff()
            subdf.loc[1:, 'death_count_tprev'] = subdf.death_count.to_numpy()[:-1]
            subdf.loc[1:, 'death_count_cumsum_per100k_tprev'] = subdf.death_count_cumsum_per100k.to_numpy()[:-1]

            subdf['recovered_count_t_minus_tprev'] = subdf.recovered_count.diff()
            subdf.loc[1:, 'recovered_count_tprev'] = subdf.recovered_count.to_numpy()[:-1]
            subdf.loc[1:, 'recovered_count_cumsum_per100k_tprev'] = subdf.recovered_count_cumsum_per100k.to_numpy()[:-1]

            subdf = subdf.iloc[1:]
            subdf['score_cases'] = (-1) * (subdf.confirmed_count_t_minus_tprev) * (
                    1.0 / (subdf.confirmed_count_cumsum_per100k_tprev + 1.0)) * subdf.historical_value
            subdf['score_deaths'] = (-1) * (subdf.death_count_t_minus_tprev) * (
                            1.0 / (subdf.death_count_cumsum_per100k_tprev + 1.0)) * subdf.historical_value
            subdf['score_recoveries'] = (subdf.recovered_count_t_minus_tprev) * (
                            1.0 / (subdf.recovered_count_cumsum_per100k_tprev + 1.0)) * subdf.historical_value

            def get_score(x):
                x = x[~numpy.isinf(x)]
                x.dropna(inplace=True)
                if x.shape[0] == 0:
                    return 0
                else:
                    return x.mean()
            score_cases = get_score(subdf['score_cases'])
            score_deaths = get_score(subdf['score_deaths'])
            score_recoveries = get_score(subdf['score_recoveries'])

            score = (focus_cases * score_cases + focus_deaths * score_deaths + focus_recoveries * score_recoveries) / (focus_cases + focus_deaths + focus_recoveries)

            return pandas.DataFrame({'score': [score]})

    df = df.groupby(['county', 'state']).apply(score_compute)
    df.reset_index(inplace=True)

    if normalize:
        score_lower = df.score.quantile(0.05)
        score_upper = df.score.quantile(0.95)
        df.loc[df.score < score_lower, 'score'] = score_lower
        df.loc[df.score > score_upper, 'score'] = score_upper
        df.score -= df.score.min()
        df.score /= df.score.max()
        df.score *= 100.0

    return df


def get_df_of_all_features_for_two_region_groups(
        db,
        var,
        county_filter1,
        state_filter1,
        start_date1,
        end_date1,
        county_filter2,
        state_filter2,
        start_date2,
        end_date2
):
    with open(os.path.join(application_directory, '../warehouse/variable_to_entity.pkl'), 'rb') as handle:
        variable2entity = pickle.load(handle)
    entity = variable2entity[var]
    if 'confirmed_date' in dir(entity):
        columns = ['state', 'confirmed_date']
    else:
        columns = ['state']

    def process_county_filter(county_filter):
        county_filter = [e.strip() for e in county_filter.split(',') if not e == '']

        for i in range(len(county_filter)):
            if ' ' in county_filter[i]:
                elements = county_filter[i].split(' ')
                for j in range(len(elements)):
                    elements[j] = elements[j][0].upper() + elements[j][1:].lower()
                county_filter[i] = ' '.join(elements)
        if len(county_filter) == 0:
            county_filter = None
        return county_filter

    def turn_to_date(x: str) -> date:
        tmp = str(x)
        date_parts = [int(e) for e in tmp.split('-')]
        return date(date_parts[0], date_parts[1], date_parts[2])

    start_date1 = turn_to_date(start_date1)
    start_date2 = turn_to_date(start_date2)
    end_date1 = turn_to_date(end_date1)
    end_date2 = turn_to_date(end_date2)

    county_filter1 = process_county_filter(county_filter1)
    county_filter2 = process_county_filter(county_filter2)

    state_filter1 = [e.strip() for e in state_filter1.split(',') if not e == '']
    if len(state_filter1) == 0:
        state_filter1 = None

    state_filter2 = [e.strip() for e in state_filter2.split(',') if not e == '']
    if len(state_filter2) == 0:
        state_filter2 = None

    if 'county' in dir(entity):
        columns = ['county'] + columns
    else:
        assert county_filter1 is None
        assert county_filter2 is None

    mobility_related_renames = dict()
    if var.startswith('google_mobility_'):
        mobility_related_renames[var[len('google_mobility_'):]] = var
        var = var[len('google_mobility_'):]

    attributes = [getattr(entity, e) for e in columns + [var]]

    df1 = db.session.query(*attributes)  # .add_columns(*attributes)
    df2 = db.session.query(*attributes)
    if county_filter1 is not None:
        df1 = df1.filter(entity.county.in_(county_filter1))
    if state_filter1 is not None:
        df1 = df1.filter(entity.state.in_(state_filter1))
    if county_filter2 is not None:
        df2 = df2.filter(entity.county.in_(county_filter2))
    if state_filter2 is not None:
        df2 = df2.filter(entity.state.in_(state_filter2))

    if 'confirmed_date' in dir(entity):
        df1 = df1.filter(entity.confirmed_date >= start_date1).filter(entity.confirmed_date <= end_date1)
        df2 = df2.filter(entity.confirmed_date >= start_date2).filter(entity.confirmed_date <= end_date2)

    df1 = pandas.DataFrame(data=df1.all(), columns=columns + [var])
    df1.rename(mobility_related_renames, axis=1, inplace=True, errors='raise')
    df2 = pandas.DataFrame(data=df2.all(), columns=columns + [var])
    df2.rename(mobility_related_renames, axis=1, inplace=True, errors='raise')
    df1['type'] = 'region_group1'
    df2['type'] = 'region_group2'
    df = pandas.concat([df1, df2])
    return df


def get_df_for_variable_query(db, var, variable2entity, county_filter, state_filter):
    entity = variable2entity[var]
    # todo: fix for those without county
    if 'confirmed_date' in dir(entity):
        columns = ['state', 'confirmed_date']
    else:
        columns = ['state']

    if 'county' in dir(entity):
        columns = ['county'] + columns

    mobility_related_renames = dict()
    if var.startswith('google_mobility_'):
        mobility_related_renames[var[len('google_mobility_'):]] = var
        var = var[len('google_mobility_'):]

    attributes = [getattr(entity, e) for e in columns + [var]]

    df = db.session.query(*attributes)  # .add_columns(*attributes)
    if county_filter is not None:
        df = df.filter(entity.county.in_(county_filter))
    if state_filter is not None:
        df = df.filter(entity.state.in_(state_filter))

    df = pandas.DataFrame(data=df.all(), columns=columns + [var])
    df.rename(mobility_related_renames, axis=1, inplace=True, errors='raise')

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
        resolution='county',
        interpolate=True
):
    # todo: make it quicker
    print('\nSTART OF QUERY\n', file=sys.stderr)
    t0 = time.time()
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
        get_df_for_variable_query(db, e, variable2entity, accepted_counties, accepted_states) for e in
        [var1, var2, var3, var4]
    ]

    t1 = time.time()
    print("\nqueries received - time spent: {}\n".format(t1 - t0), file=sys.stderr)

    output_df = reduce(lambda left, right: special_reduce(left, right), dfs)

    t2 = time.time()
    print("\nmerged - time spent: {}\n".format(t2 - t1), file=sys.stderr)

    output_df.confirmed_date = output_df.confirmed_date.apply(lambda x: str(x.date()))

    if interpolate:
        output_df = olivia_interpolation(output_df)

    t3 = time.time()
    print("\ninterpolated - time spent: {}\n".format(t3 - t2), file=sys.stderr)

    output_df = floatify_df(output_df)

    if resolution == 'state':
        try:
            output_df = output_df.groupby(['state', 'confirmed_date']).mean().reset_index()
        except:
            import pdb
            pdb.set_trace()

    return output_df


def process_for_d3_json(df):
    print("\n creating json\n")
    t0 = time.time()

    if not 'location' in df.columns:
        df = add_location_to_df(df)

    if not 'day_of_the_year' in df.columns:
        df = add_day_of_the_year_to_cases_table(df)

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
                    tmp[label2description[column]].append([row[t_var], row[column]])

        output.append(tmp.copy())
    t1 = time.time()
    print("\njson completed: time spent: {}\n".format(t1 - t0))

    return output


def process_for_d3_json_ultrafast(df):
    print("\n creating json\n")
    t0 = time.time()

    if not 'location' in df.columns:
        df = add_location_to_df(df)

    if not 'day_of_the_year' in df.columns:
        df = add_day_of_the_year_to_cases_table(df)

    if 'confirmed_date' in df.columns:
        df.drop(columns=['confirmed_date'], inplace=True)

    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)

    t_var = "day_of_the_year"
    df[t_var] = df[t_var].apply(doty_to_date)
    df['Name'] = df.location.copy()

    unique_locations = df.location.unique().tolist()
    output = list()
    for unique_location in unique_locations:
        output.append(
            convert_subdf_to_dict(df[df.location == unique_location].copy(), unique_location)
        )

    t1 = time.time()
    print("\njson completed: time spent: {}\n".format(t1 - t0))

    return output


def convert_subdf_to_dict(sub_df, location):
    sub_df.drop(columns=['Name'], inplace=True)
    t_var = "day_of_the_year"
    rename_dict = dict()
    for column in sub_df.columns:
        if column in [t_var]:
            continue
        else:
            rename_dict[column] = label2description[column]

    sub_df.rename(rename_dict, axis=1, errors='raise', inplace=True)

    sub_df = sub_df.to_dict()
    sub_df = {x: list(sub_df[x].values()) for x in sub_df.keys() if x not in ['Name', 'location']}
    sub_df = {x: list(zip(sub_df['day_of_the_year'], sub_df[x])) for x in sub_df.keys() if
              x not in ['Name', 'location', 'day_of_the_year']}
    sub_df = {x: [list(e) for e in sub_df[x]] for x in sub_df.keys() if
              x not in ['Name', 'location', 'day_of_the_year']}
    sub_df['Name'] = location
    sub_df['location'] = location

    out = dict()
    out['Name'] = sub_df['Name']
    out['location'] = sub_df['location']
    for key in sub_df.keys():
        if key in ['Name', 'location']:
            continue
        else:
            out[key] = sub_df[key]

    return out
