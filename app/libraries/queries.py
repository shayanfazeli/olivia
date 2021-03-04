import pickle
import os
import pandas
from functools import reduce
from datetime import datetime, date, timedelta
import numpy
from erlab_coat.meta import label2description
from erlab_coat.preprocessing import doty_to_date, olivia_interpolation, add_location_to_df, \
    add_day_of_the_year_to_cases_table
from app.entities import Election, InfluenzaActivityLevel, GoogleMobility, Cases, Diversity, Census, StateRestaurants, \
    ICUBeds, CovidHospitalizations, Mortality, LandAndWater, ObesityAndLife, Alcohol, Diabetes, TweetTable1
from app import application_directory
from app.libraries.utilities import floatify_df
import sys
import time
from typing import Union, List


def get_datetime_object_from_date_string(
        date_string: str,
        separator: str = '-',
        output_format: str = 'date'
) -> Union[datetime, date]:
    """
    The :func:`get_datetime_object_from_date_string` is a helper for converting a date
    string to a datetime library object.

    Parameters
    ----------
    date_string: `str`, required
        The input date string, for example: '2020-05-25'

    separator: `str`, optional (default='-')
        The separator for the `date_string` variable.

    output_format: `str`, optional (default=date)
        The optional output format customization, the default is `date` and the
        other option is `datetime`. The main reason the second option has been
        made available is through its wide usage with the DateTime object in the
        Amazon Aurora instance of Olivia.

    Returns
    -----------
    The output is an instance of `Union[datetime, date]`, which can either
    be an instance of `date` or `datetime`.
    """
    assert separator in date_string, "error: separator is not observed."
    date_parts = [int(e) for e in date_string.split(separator)]
    if output_format == 'date':
        output = date(year=date_parts[0], month=date_parts[1], day=date_parts[2])
    elif output_format == 'datetime':
        output = datetime(year=date_parts[0], month=date_parts[1], day=date_parts[2])
    else:
        raise ValueError

    return output


def get_tweets_df_from_table1(
        db,
        place_names: List[str],
        min_date: str,
        max_date: str,
):
    def fix_place_names(x: str) -> str:
        out1 = [e for e in x.split(' ')]
        out = []
        for e in out1:
            out.append(e[0].upper() + e[1:].lower())
        return " ".join(out)

    place_names = [fix_place_names(e) for e in place_names]
    df = db.session.query(
        TweetTable1.place_name,
        TweetTable1.tweet_id,
        TweetTable1.confirmed_date,
        TweetTable1.hate_prob,
        TweetTable1.counterhate_prob,
        TweetTable1.neutral_prob,
        TweetTable1.other_prob,
        TweetTable1.text
    )
    assert min_date is not None
    assert max_date is not None
    df = df.filter(TweetTable1.confirmed_date >= get_datetime_object_from_date_string(min_date))
    df = df.filter(TweetTable1.confirmed_date <= get_datetime_object_from_date_string(max_date))
    if len(place_names) > 0:
        df = df.filter(TweetTable1.place_name.in_(place_names))

    df = df.limit(10000)

    columns = ['place_name', 'tweet_id', 'confirmed_date', 'hate_prob', 'counterhate_prob', 'neutral_prob', 'other_prob', 'text']
    df = pandas.DataFrame(data=df.all(), columns=columns)

    df.rename({'confirmed_date': 'date'}, axis=1, inplace=True)

    return df


def get_df_for_county_scoring(
        db,
        focus_cases: float,
        focus_deaths: float,
        focus_recoveries: float,
        min_date: str,
        max_date: str,
        normalize: bool = True
) -> pandas.DataFrame:
    """
    The :func:`get_df_for_county_scoring` obtains COVID-19 Region Health Scores

    Parameters
    ----------
    db: required
        The database instance

    focus_cases:  'float', required
        Focus value

    focus_deaths:  'float', required
        Focus value

    focus_recoveries: 'float', required
        Focus value

    min_date: `str`, required
        The minimum date, before which all the records will be neglected.

    max_date: `str`, required
        The maximum date, before which all the records will be neglected.

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
    assert min_date is not None
    assert max_date is not None
    df = df.filter(Cases.confirmed_date >= get_datetime_object_from_date_string(min_date))
    df = df.filter(Cases.confirmed_date <= get_datetime_object_from_date_string(max_date))
    columns = ['county', 'state', 'confirmed_date', 'confirmed_count', 'confirmed_count_cumsum_per100k', 'death_count',
               'death_count_cumsum_per100k', 'recovered_count', 'recovered_count_cumsum_per100k']

    df = pandas.DataFrame(data=df.all(), columns=columns)

    def integral_score_compute_for_subdf(subdf):
        subdf = subdf.copy()
        def compute_integral_score(x):
            if x.shape[0] < 5:
                return 0
            c_0 = x[0]
            T = x.shape[0]
            Tc_0 = float(T * c_0)
            Tx_T = float(T * x[-1])
            blue = float(numpy.sum(x) - Tc_0)
            red = float(Tx_T - Tc_0)
            if red == 0:
                return 0
            orange = Tc_0
            try:
                score = - (blue / red) * (red / (red + orange)) * 1000.0
            except Exception as e:
                score = 0
            return score

        confirmed_count_cumsum_per100k = subdf.confirmed_count_cumsum_per100k.to_numpy()
        death_count_cumsum_per100k = subdf.death_count_cumsum_per100k.to_numpy()
        recovered_count_cumsum_per100k = subdf.recovered_count_cumsum_per100k.to_numpy()

        score_cases = compute_integral_score(x=confirmed_count_cumsum_per100k)
        score_deaths = compute_integral_score(x=death_count_cumsum_per100k)
        score_recoveries = compute_integral_score(x=recovered_count_cumsum_per100k)

        score = (focus_cases * score_cases + focus_deaths * score_deaths - focus_recoveries * score_recoveries) / (
                    focus_cases + focus_deaths + focus_recoveries)

        return pandas.DataFrame({'score': [score]})

    df = df.groupby(['county', 'state']).apply(integral_score_compute_for_subdf)
    df.reset_index(inplace=True)

    sorted_df = df.copy().sort_values(by='score', ascending=False)

    sorted_counties = sorted_df['county'].tolist()
    sorted_states = sorted_df['state'].tolist()

    if normalize:
        score_lower = df.score.quantile(0.02)
        score_upper = df.score.quantile(0.98)
        df.loc[df.score < score_lower, 'score'] = score_lower
        df.loc[df.score > score_upper, 'score'] = score_upper
        df.score -= df.score.min()
        df.score /= df.score.max()
        df.score *= 100.0

    return df, sorted_counties, sorted_states


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
        output_df.confirmed_date = output_df.day_of_the_year.copy().apply(lambda x: str(date(2020, 1, 1) + timedelta(days=x)))

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
