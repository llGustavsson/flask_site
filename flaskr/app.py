from flask import Flask, render_template, request, session, redirect, url_for
import json
import random

app = Flask(__name__)
app.secret_key = "test_key_001"

# Load all questions
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Index page
@app.route("/")
def index():
    return render_template("index.html")

# Articles page
@app.route("/articles")
def articles():
    return render_template("articles.html")

# Quiz page and logic
@app.route("/quiz", methods=["GET","POST"])
def quiz():
    # Initialize quiz on first visit or after reset
    if 'selected_questions' not in session:
        session['selected_questions'] = random.sample(questions, 5)
        session['current'] = 0
        session['score'] = 0
        session['answers'] = []

    current = session['current']
    selected_questions = session['selected_questions']

    # All questions answered → redirect to results
    if current >= len(selected_questions):
        return redirect(url_for("result"))

    # POST → user submitted an answer
    if request.method == "POST":
        user_answer = request.form.get('answer')
        q = selected_questions[current]

        # Record the answer regardless of correctness
        session['answers'].append({
            'question': q['question'],
            'user_answer': user_answer,
            'correct_answer': q['answer'],
            'is_correct': user_answer == q['answer']
        })

        if user_answer == q['answer']:
            session['score'] += 1

        session['current'] = current + 1
        current = session['current']

        if current >= len(selected_questions):
            return redirect(url_for("result"))

    # Show current question
    question = selected_questions[current]
    return render_template("quiz.html", question=question)

@app.route("/result")
def result():
    # Show results
    score = session.get('score', 0)
    results = session.get('answers', [])
    total = len(session.get('selected_questions', []))

    # Clear session to reset quiz when user clicks "Try Again"
    session.clear()
    return render_template("result.html", score=score, results=results, total=total)

if __name__ == "__main__":
    app.run(debug=True)
