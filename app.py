from flask import Flask, render_template, request, redirect, session, flash
from surveys import surveys
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret key"
RESPONSE_KEY = "responses"
SURVEY_NAME_KEY = "survey_name"
#debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    session['survey_name'] = None
    return render_template("index.html", surveys=surveys )

@app.route("/begin", methods=["POST"])
def begin():
    session[RESPONSE_KEY] = []
    survey_name = request.form.get('survey_name')
    if survey_name is None:
        flash("Please select a survey")
        return redirect('/')
    session['survey_name']=survey_name
    return redirect("/questions/0")

@app.route("/questions/<int:id>")
def get_question(id):
    survey_name = session['survey_name']
    # if no survey is active
    if survey_name is None:
        flash("Please select a survey")
        return redirect('/')

    questions = get_questions(session)
    responses = session[RESPONSE_KEY]
    # if accessing the wrong question
    if len(responses) != id:
        flash("Invalid question. Redirected to current question.")
        return redirect_to_current_question(session)

    return render_template("question.html", q_num=id+1, question=questions[id])

@app.route("/answer", methods=["POST"])
def answer():
    responses = session[RESPONSE_KEY]
    response = request.form.get('answer')
    # if no response
    if response is None:
        flash("Please choose a response")
        return redirect_to_current_question(session)

    responses.append(response)
    session[RESPONSE_KEY] = responses

    questions = get_questions(session)
    if len(responses) == len(questions):
        return redirect("/complete")
    else:
        return redirect_to_current_question(session)
        

@app.route("/complete")
def complete():
    return render_template("completion.html")

def get_questions(session):
    survey_name = session[SURVEY_NAME_KEY]
    questions = surveys[survey_name].questions
    return questions

def redirect_to_current_question(session):
    responses = session[RESPONSE_KEY]
    return redirect(f"/questions/{len(responses)}")