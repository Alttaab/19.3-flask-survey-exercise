from distutils.log import debug
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "password"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

SESSION_RES = 'response'

@app.route('/')
def index():
    """Show homepage"""
    return render_template("surveys.html")

@app.route('/start', methods=["POST"])
def setup_session():
    """Sets up a session if one is not already made"""
    if session.get(SESSION_RES) == None:
        session[SESSION_RES] = []
    return redirect(f"/satisfaction_survey/questions/0")

@app.route('/<survey_name>/questions/<q_num>')
def survey_questions(survey_name, q_num):
    """Checks if question number is valid and if it is generate a page from surveys.py"""
    responses = session[SESSION_RES]
    survey_str = str(survey_name)
    survey = getattr(surveys, survey_str)
    survey_length = len(survey.questions)
    
    if len(responses) != int(q_num):
        question_num = len(responses)
        flash("Attempting to access an invalid question")
        return render_template("error-msg.html",
                               question_num = question_num)
        
    elif survey_length == int(q_num) or len(responses) == survey_length:
        return render_template("thanks.html")
        
    question_num = int(q_num)
    
    question = survey.questions[question_num].question
    choices = survey.questions[question_num].choices
     
    return render_template("question.html",
                           survey = survey,
                           question = question,
                           choices = choices,
                           question_num = question_num,
                           survey_length = survey_length)

@app.route('/<survey_name>/answer/<q_num>')
def survey_answers(survey_name, q_num):
    """Adds users response to session response list."""
    responses = session[SESSION_RES]
    responses.append(request.args.get(next(iter(request.args))))
    session[SESSION_RES] = responses
    return redirect(f"/{survey_name}/questions/{int(q_num)+1}")

