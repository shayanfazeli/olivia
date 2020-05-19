from flask import Blueprint, render_template, redirect
from app.blueprints.contact.forms import SendFindingForm
from app.libraries.queries import get_data_for_query, process_for_d3_json
from erlab_coat.meta import label2description
from app import db, application_directory, mail
from flask_mail import Message

results_blueprint = Blueprint("results", __name__)


@results_blueprint.route('/findings', methods=['GET', 'POST'])
def findings():
    """
    {
            "title": "Result 2",
            "animation": False,
            "filename": "result_files/ak.png",
            "description":
           ,
            "date": "April 21st, 2020"

        }
    :return:
    """
    results = [
        {
            "title": "Republican/Democratic Voting Tendencies",
            "animation": False,
            "filename": "result_files/11.png",
            "description": """
                                    This is a very interesting plot across counties, showing interesting
                                    findings in a high resolution region-feature plot. The shape of the curve
                                    fitted to the scattered points is really interesting, and a finding is that
                                    the states closer to a 50-50 voting partitioning tend to do worse than the
                                    more polarized ones. Also, democratic regions tend to, on average, exhibit
                                    a quicker spread of the novel coronavirus.
                            """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Region Age and Spread Speed",
            "animation": False,
            "filename": "result_files/12.png",
            "description": """
                                            This is another plot that clearly indicates the somehow negative
                                            relationships between the percentage of elderly and the speed of the spread.
                                    """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Change in Mortality Rate in General",
            "animation": False,
            "filename": "result_files/14.png",
            "description": """
                                                This interesting result shows that in general, regions exhibiting a lower
                                                value of change in the mortality rate (mortality that is not related to coronavirus)
                                                tend to be more adversely affected by the COVID-19 outbreak. The fitted line
                                                clearly corroborates this hypothesis, and one could observe the animation
                                                to notice the temporal patterns as well.
                                        """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Thinking on Compliance and Public Transit",
            "animation": False,
            "filename": "result_files/1.png",
            "description": """
                This plot is an snapshot of the animation with the same configuration. The shape and positioning
                of the points, along with the temporal relationships visible as the animation plays, indicate
                that:<br>

                <ol>
                <li>
                It appears that the regions with roughly the same degree of compliance with the shelter at home criteria
                have various COVID-19 spread speed, which might be associated with the degree to which they are initially affected by it.<br>
                One thing to notice is that there are many counties and regions that do not comply that much, however, since they
                are not affected by the virus severely the speed of the spread seems to remain low. This is expected, since
                in normal every day life people shall not comply with this criteria. Nevertheless, the animation
                and the plot paints a picture of how quickly a pandemic would spread across different regions of the US.
                </li>
                <li>
                A considerable correlation is observed between the percentage of public transit in daily commute and the
                speed of COVID-19 spread. It appears that the regions that spread it faster, also use the means of public transit more.
                </li>
                </ol>
            """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Age in COVID-19 Spread Speed - County Level",
            "animation": False,
            "filename": "result_files/2.png",
            "description": """
                    This plot (and also, if you are interested, try rendering the animation as it is more informative)
                    has signs that indicate the states, counties, and regions that are more "mobile" are also "younger".
                    This, for example, manifests itself in the animation as larger balls (indicating age seniority) tend
                    to be generally heavier, thus being lifted upward by the COVID-19 spread slowly. Also, the larger
                    size of points in the cohort below the fitted line is interesting.
                """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Age in COVID-19 Spread Speed - State Level",
            "animation": False,
            "filename": "result_files/3.png",
            "description": """
                        This plot is the more high level version of the result on the relationship between age and
                        COVID-19 spread. The same intuitive idea comes to mind by observing that the points that are
                        smaller tend to be more mobile in the plot, indicating that the spread of the novel coronavirus
                        is quicker in them in general.
                    """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Higher Mortality Rate, Slower the Spread",
            "animation": False,
            "filename": "result_files/4.png",
            "description": """
                            This plot indicates signs of a somehow unexpected result, and that is
                            the states with higher mortality rate exhibit a somewhat slower spread compared
                            to those of low mortality rate. Nevertheless, this corroborates the previous finding since
                            the regions with higher mortality rate have higher elderly population percentage, and one could
                            argue that they are less mobile.<br>
                            From the plot, it is understandable that the points on the bottom are generally brighter, and
                            since the color is associated with the mortality rate, the more they tend to be close
                            to light green, the higher the mortality rate associated with that region is.
                        """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Higher Mortality Rate, Slower the Spread - Cont'd",
            "animation": False,
            "filename": "result_files/5.png",
            "description": """
                                This plot is a snapshot of the corresponding animation. In the animation, it is more
                                noticeable that in the higher resolution plot, those with lower mortality rate exhibit
                                a higher speed in going upward.
                            """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Income and Unemployment",
            "animation": False,
            "filename": "result_files/6.png",
            "description": """
                                    The figure shown here indicates that there is a somewhat negative relationship between
                                    the average income and the speed of COVID-19 spread. Note that to observe it better, 
                                    it is best to try the interactive animation rather than focusing on the picture. However,
                                    the static result also shows that points that are brighter (those that exhibit higher
                                    average of median income) ended up lower than those with the same average level of compliance.
                                    <br>
                                    <br>
                                    Regarding the income, note that "median" is the proper typical value since, for example,
                                    if we consider Bill Gates in the mean, the value will not be a good representative
                                    of the population. The values here, are the averages of these medians, therefore,
                                    would properly represent the region they are associated with.
                            """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Income and Unemployment - Cont'd",
            "animation": False,
            "filename": "result_files/7.png",
            "description": """
                                        This is a more high-level graph on states which also gives the impression
                                        that the larger points, which are associated with a higher unemployment percentage, that
                                        are closer to bright red in color, which indicates a lower average value for the median region income, seems
                                        to be driving upward quicker. For more information and better noticeability, animation can be used instead
                                        of the plot.
                                """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Types of Poverty",
            "animation": False,
            "filename": "result_files/8.png",
            "description": """
                                            An interesting plot on both poverty level and child poverty level can be seen
                                            in this result. It shows that the points below the fitted line tend to be 
                                            smaller and approach green more than the ones above. This trend can be seen
                                            to be somehow in contradiction with the result on the average income. Nevertheless,
                                            it is mainly focused on poverty, and one can say that those that spread COVID-19
                                            very quickly tend to be the regions exhibiting lower values of poverty and child
                                            poverty measurements.
                                    """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Professional Jobs and Pandemic",
            "animation": False,
            "filename": "result_files/9.png",
            "description": """
                                                This plot, especially when looking at the colors (since in this
                                                graph it is more noticeable than the minute size differences), shows that
                                                regions with more percentage of professional jobs tend to be on top of the bars
                                                in each compliance level.
                                        """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Construction Jobs and Pandemic",
            "animation": False,
            "filename": "result_files/10.png",
            "description": """
                                    Given this result, one could argue that perhaps regions that are less affluent tend to
                                    have a higher percentage of construction jobs. Points representing such regions
                                    are found below the fitted line.
                            """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Water Area",
            "animation": False,
            "filename": "result_files/13.png",
            "description": """
                                        This plot somehow gives the impression that the regions that are more adversely affected by the virus (measured
                                        with regards to the speed of the coronavirus spread which is more noticeable in the animations), do not lie in the cluster
                                        of regions with high water resources.
                                """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Production Jobs",
            "animation": False,
            "filename": "result_files/15.png",
            "description": """
                                            This is one of the plots regarding job type percentages, and it shows that
                                            the regions that are more adversely impacted by the COVID-19 outbreak tend
                                            to have a generally lower percentage of Production job type in their
                                            employment partitioning.
                                    """,
            "date": "April 11th, 2020"
        },
        {
            "title": "Diversity Index",
            "animation": False,
            "filename": "result_files/16.png",
            "description": """
                                                It appears that most of the areas that are <<severely>> affected by
                                                COVID-19 outbreak (severeness defined by the higher values of population-normalized case count) also
                                                happen to have a high diversity index, which is intuitively expected. However, as shown
                                                in the plot there are areas such as Cleburne Arizona that do not have a high diversity index, yet 
                                                are more severely impacted by the outbreak than the baseline. One could argue that
                                                it is useful to do a research on the idiosyncratic features of this area and figure
                                                in what other characteristic does it stand out amongst areas similar to it.

                                        """,
            "date": "April 11th, 2020"
        },

    ]
    return render_template('results/findings.html', results=results)
