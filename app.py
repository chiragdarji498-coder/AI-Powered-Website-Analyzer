from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Replace with your Groq API Key
client = Groq(
    api_key="YOUR API KEY"
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        data = request.get_json()
        website = data.get("website", "").strip()

        if not website:
            return jsonify({
                "error": "Please enter a website URL."
            }), 400

        prompt = f"""
        Analyze this website: {website}

        Return EXACTLY in this format:

        PURPOSE:
        Explain what the website does and its purpose.

        COMPETITORS:
        List the main competitors.

        STRATEGY:
        Explain the business strategy.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=1000
        )

        result = response.choices[0].message.content

        purpose = ""
        competitors = ""
        strategy = ""

        try:
            if "PURPOSE:" in result:
                purpose_part = result.split("COMPETITORS:")[0]
                purpose = purpose_part.replace("PURPOSE:", "").strip()

            if "COMPETITORS:" in result:
                competitors_part = result.split("COMPETITORS:")[1]

                if "STRATEGY:" in competitors_part:
                    competitors = competitors_part.split("STRATEGY:")[0].strip()

            if "STRATEGY:" in result:
                strategy = result.split("STRATEGY:")[1].strip()

        except:
            purpose = result

        return jsonify({
            "purpose": purpose,
            "competitors": competitors,
            "strategy": strategy
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)