from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)

app.config["SECRET_KEY"] = "supersecretpassword"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.route("/")
def root():
    return render_template('base.html')

@app.route("/home")
def base_page():
    """
    returns base page template, pulls title and instructions out of Survey obj passes to template
    """
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("home.html", title=title, instructions=instructions)

@app.route("/questions/<int:id>", methods=["POST", "GET"])
def show_form(id):
    """selects question from survey and displays choices for that question"""
    selected_question = satisfaction_survey.questions[id].question
    selected_question_choices = satisfaction_survey.questions[id].choices
    
    flash(f"Your question has been answered")
    return render_template("questions.html", id=id, selected_question=selected_question, satisfaction_survey=satisfaction_survey, selected_question_choices=selected_question_choices)


@app.route("/answers", methods=["POST", "GET"])
def save_answers():
    """ save answers to RESPONSES"""
    question_count = len(satisfaction_survey.questions)
    
    choice = request.form.get("choice")
    RESPONSES.append(choice)
    id = int(request.form["id"])
    if id < (len(satisfaction_survey.questions) -1 ):
        return redirect(f"/questions/{id +1}")
    else: return redirect("/thanks")

@app.route("/thanks")
def show_thanks():
    """ shows thanks message"""
    survey_title = satisfaction_survey.title
    responses = RESPONSES
    return render_template("thanks.html", survey_title=survey_title, responses=responses)

# ! Questions from app exercise
# ? Line 34 "for some reason I kept getting a "method not allowed" error, what would cause the "method not allowed" error in this instance?"
# ? Line 39  i used .get method incase a radio button isn't selected, will pass "None" as choice value, is this right?
# ? Line Step 6 could not complete step 6, protecting questions. not sure what is meant by or how to do that. 
# ? Line 42 id is sent as a hidden input on the form to get the index of the current question