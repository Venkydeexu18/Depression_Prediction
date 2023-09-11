# VenkyDeexu18
from flask import Flask, render_template, request, session
app = Flask(__name__)
app.secret_key = 'VenkyDeexu_17'

questions = [
    {
        "id": 1,
        "question": "Do you feel sad or lonely?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 2,
        "question": "Do you feel incapable or pessimistic?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 3,
        "question": "Do you regret past failures?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 4,
        "question": "Do you feel like crying (about life)?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 5,
        "question": "Do you feel restless and anxious?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 6,
        "question": "Do you think of punishing yourself or others?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 7,
        "question": "Do you feel you're alone?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 8,
        "question": "Do you hate yourself?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 9,
        "question": "Do you feel criticizing yourself is better?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 10,
        "question": "Do you think or dream of suicidal thoughts?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 11,
        "question": "Do you share your highs and lows or keep them to yourself?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 12,
        "question": "Do you feel tired or have low energy?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 13,
        "question": "Do you feel less hungry or have no interest in eating?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 14,
        "question": "Trouble concentrating on tasks or activities?",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    },
    {
        "id": 15,
        "question": "I think my life isn't worth living",
        "options": [
            {"option": "Never", "score": 0},
            {"option": "Sometimes", "score": 1},
            {"option": "Often", "score": 2},
            {"option": "Always", "score": 3}
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def prediction():
    question_index = int(request.form.get('question_index', 0))

    if request.method == 'POST':
        answer = request.form.get('answer')
        selected_option = next(option for option in questions[question_index]['options'] if option['option'] == answer)
        score = selected_option['score']
        question_index += 1

        if 'total_score' not in session:
            session['total_score'] = 0

        if question_index == 1:
            session['total_score'] = 0

        session['total_score'] += score

        if question_index == len(questions):
            result = classify_score(session['total_score'])
            recommendations = prediction(session['total_score'])
            total_score = session['total_score'] 
            percent = (total_score / (len(questions) * 3)) * 100 
            return render_template('result.html', result=result, percent=percent, recommendations=recommendations)

    return render_template('questions.html', question=questions[question_index], question_index=question_index)
 
def prediction(scores):
    if scores <= 5:
        recommendations = "Engage in regular physical exercise to boost mood and overall well-being." \
            "Maintain a healthy and balanced diet to support your mental health." \
            "Connect with friends and family regularly to maintain social support."
        
    elif scores <= 15:
        recommendations = "Consider talking to a mental health professional to discuss your emotions and concerns. " \
               "Practice mindfulness or meditation to help reduce stress and promote emotional well-being. " \
               "Seek support from friends and family, and share your feelings with trusted individuals. " 
    elif scores <= 30:
        recommendations = "Reach out to a mental health professional for a proper assessment and guidance. " \
               "Build a support system of friends, family, or support groups who understand and can provide emotional support. " \
               "Engage in regular physical activity, as exercise has been shown to have positive effects on mood. "
    else:
        recommendations = "Make an appointment with a mental health specialist or a general practitioner to discuss your concerns in detail. "\
               "Reach out to a trusted friend or family member for support during this time. " \
               "Prioritize self-care and engage in activities that promote relaxation, stress reduction, and overall well-being."
    
    recommendation_list = recommendations.split(" ")
    formatted_recommendations = " ".join(recommendation_list)

    return formatted_recommendations


def classify_score(score):
    if score <= 5:
        return "You are perfectly alright."
    elif score <= 15:
        return "You are slightly depressed."
    elif score <= 30:
        return "You are depressed."
    else:
        return "We suggest you to consult a doctor."

@app.route('/contact', methods=['GET', 'POST'])
def contact_us():
    return render_template('contact.html')
if __name__ == '__main__':
    app.run()


