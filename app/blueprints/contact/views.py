from flask import Blueprint, render_template, redirect
from app.blueprints.contact.forms import SendFindingForm
from app.libraries.queries import get_data_for_query, process_for_d3_json
from erlab_coat.meta import label2description
from app import db, application_directory, mail
from flask_mail import Message

contact_blueprint = Blueprint("contact", __name__)


@contact_blueprint.route('/send_finding', methods=['GET', 'POST'])
def send_finding():
    form = SendFindingForm()

    if form.validate_on_submit():
        mail.send_message("OLIVIA: NEW FINDING FILED",
                          sender='erlabgpu1@gmail.com',
                          recipients=['shayan.fazeli@gmail.com'],
                          body="finder email: {}\n\ntitle: {}\n\nexplanation:{}\n\nsteps to reproduce:{}\n\n".format(
                              form.email.data, form.finding_title.data, form.explanation.data,
                              form.reproduce_instructions.data))
        return redirect("/")

    return render_template("contact/send_finding.html", form=form)