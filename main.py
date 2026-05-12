from flask import Flask, render_template, request

app = Flask(__name__)

ACTIVITIES = (
    "Walking",
    "Running",
    "Waiting outside",
    "Working outdoors",
)


def heat_risk_level(celsius: float) -> str:
    if celsius >= 42:
        return "Extreme Risk"
    if celsius >= 35:
        return "High Risk"
    if celsius >= 30:
        return "Moderate Risk"
    return "Low Risk"


def safety_advice(risk: str, activity: str) -> str:
    base = {
        "Extreme Risk": (
            "Heat stress and heatstroke are very likely. Avoid outdoor exertion. "
            "If you must be outside, stay in shade, drink water regularly, and watch for "
            "dizziness, confusion, or nausea—seek medical help if symptoms appear."
        ),
        "High Risk": (
            "Heat exhaustion is a real concern. Limit time outside, take frequent breaks in "
            "the shade or air conditioning, wear light loose clothing, and hydrate before you "
            "feel thirsty."
        ),
        "Moderate Risk": (
            "Heat can build up over time. Pace your activity, rest often, use sunscreen and a "
            "hat, and drink water steadily throughout your time outdoors."
        ),
        "Low Risk": (
            "Conditions are relatively comfortable for most people. Still drink water during "
            "activity and take breaks if you start to feel warm or tired."
        ),
    }
    activity_note = {
        "Walking": " Keep walks shorter than usual in strong heat and choose cooler hours when possible.",
        "Running": " Reduce intensity and duration; consider treadmill or indoor options on very hot days.",
        "Waiting outside": " Seek shade, use an umbrella or hat, and move to a cooler place if you feel overheated.",
        "Working outdoors": " Schedule heavy tasks for cooler parts of the day, use buddy checks, and cool down in shade on breaks.",
    }
    return base[risk] + activity_note.get(activity, "")


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    temp_value = ""
    activity_value = ACTIVITIES[0]

    if request.method == "POST":
        temp_value = request.form.get("temperature", "").strip()
        activity_value = request.form.get("activity", ACTIVITIES[0])
        if activity_value not in ACTIVITIES:
            activity_value = ACTIVITIES[0]

        if not temp_value:
            error = "Please enter a temperature."
        else:
            try:
                celsius = float(temp_value.replace(",", "."))
                risk = heat_risk_level(celsius)
                advice = safety_advice(risk, activity_value)
                result = {
                    "celsius": celsius,
                    "risk": risk,
                    "advice": advice,
                    "activity": activity_value,
                }
            except ValueError:
                error = "Please enter a valid number for temperature."

    return render_template(
        "index.html",
        activities=ACTIVITIES,
        result=result,
        error=error,
        temp_value=temp_value,
        activity_value=activity_value,
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000, use_reloader=False)
