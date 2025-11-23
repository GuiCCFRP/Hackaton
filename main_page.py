import requests
from flask import Blueprint, render_template, request
from flask_login import login_required
from stuff import API_KEY

main_bp = Blueprint('main', __name__)
strands = []

@main_bp.route("/generate_reflection", methods=["POST"])
@login_required
def generate_reflection():
    strand = request.form.getlist("strand")
    q1  = request.form.get("q1", "")
    q2  = request.form.get("q2", "")
    q3  = request.form.get("q3", "")
    q4  = request.form.get("q4", "")
    q5  = request.form.get("q5", "")
    q6  = request.form.get("q6", "")
    q7  = request.form.get("q7", "")
    q8  = request.form.get("q8", "")
    q9  = request.form.get("q9", "")
    q10 = request.form.get("q10", "")
    q11 = request.form.get("q11", "")
    q12 = request.form.get("q12", "")
    lo1 = request.form.get("lo1", "")
    lo2 = request.form.get("lo2", "")
    lo3  = request.form.get("lo3", "")
    lo4 = request.form.get("lo4", "")
    lo5 = request.form.get("lo5", "")
    lo6 = request.form.get("lo6", "")
    lo7 = request.form.get("lo7", "")


    prompt = build_cas_prompt(
        title=q1,
        date_duration=q2,
        strands=q3,
        what_you_did=q4,
        goal=q5,
        challenges=q6,
        skills_developed=q7,
        collaboration=q8,
        impact=q9,
        personal_growth=q10,
        next_steps=q11,
        learnings=q12,
    )

    reflection_text = ask_ai(prompt, API_KEY)


    return render_template("display.html", reflection=reflection_text)


def build_cas_prompt(
    title,
    date_duration,
    strands,
    what_you_did,
    goal,
    challenges,
    skills_developed,
    collaboration,
    impact,
    personal_growth,
    next_steps,
    learnings,
):
    return f"""
You are an assistant that writes IB CAS reflections that follow the official CAS learning outcomes and reflective expectations.

Using the student's answers below, produce a well-structured CAS reflection that:

- is written in first person
- connects thoughts, emotions, challenges, and personal growth
- demonstrates awareness, initiative, perseverance, and collaboration where applicable
- highlights which CAS strands apply (Creativity, Activity, Service)
- references IB CAS learning outcomes naturally (not as a list)
- avoids sounding like AI, overly formal writing, or bullet points , NO EMDASHES
- is between 250–450 words

Here are the student’s responses:
0.) Cas strand(s) {[strand for strand in strands]}
1. CAS Experience Title:
{title}

2. Date / Duration:
{date_duration}

3. Which CAS strand(s) apply (Creativity, Activity, Service)?
{strands}

4. What was the experience or activity? Describe what you did:
{what_you_did}

5. What was your goal or intention?
{goal}

6. What challenges or difficulties did you face?
{challenges}

7. What skills, attitudes, or strengths did you develop?
{skills_developed}

8. Did you collaborate with others? If yes, how?
{collaboration}

9. What impact did this experience have on others or the community?
{impact}

10. How did this experience help you grow personally?
{personal_growth}

11. What will you do next or how will you continue developing?
{next_steps}

12. What did you learn?
{learnings}

Write the CAS reflection now based on these answers.
"""


API_URL = "https://ai.hackclub.com/proxy/v1/chat/completions"

def ask_ai(prompt: str, api_key: str) -> str:
    """
    Sends a prompt to the HackClub AI proxy and returns the response text.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "qwen/qwen3-32b",
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]

@main_bp.route("/set-strand", methods=["POST"])
@login_required
def set_strand():
    global strands
    strands.appends(request.form.get("strand"))
    return 0
