from flask import Flask, request, render_template_string
from rag_query import query_offers

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Promo Sensei</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
        }
        .sensei-card {
            max-width: 500px;
            margin: 60px auto;
            border-radius: 1.5rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.18);
            background: rgba(255,255,255,0.95);
            padding: 2.5rem 2rem 2rem 2rem;
        }
        .sensei-title {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(90deg, #6366f1, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.2rem;
            letter-spacing: 1px;
        }
        .sensei-btn {
            background: linear-gradient(90deg, #6366f1, #06b6d4);
            border: none;
            color: #fff;
            font-weight: 600;
            transition: background 0.2s;
        }
        .sensei-btn:hover {
            background: linear-gradient(90deg, #06b6d4, #6366f1);
        }
        .sensei-answer {
            margin-top: 2rem;
            background: #f1f5f9;
            border-radius: 1rem;
            padding: 1.2rem;
            font-size: 1.1rem;
            color: #334155;
            box-shadow: 0 2px 8px 0 rgba(99,102,241,0.07);
        }
        .sensei-logo {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="sensei-card">
        <div class="text-center">
            <div class="sensei-logo"></div>
            <div class="sensei-title">Promo Sensei</div>
            <p class="mb-4 text-secondary">Find the best shopping deals instantly.<br>Ask me anything about offers, brands, or discounts!</p>
        </div>
        <form method="post" class="mb-3">
            <div class="input-group">
                <input name="query" class="form-control form-control-lg" placeholder="e.g. Flat 50% on cosmetics?" autofocus required />
                <button class="btn sensei-btn btn-lg" type="submit">Ask</button>
            </div>
        </form>
        {% if answer %}
        <div class="sensei-answer">
            <strong>Promo Sensei says:</strong><br>
            {{ answer|safe }}
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    answer = None
    if request.method == "POST":
        answer = query_offers(request.form["query"])
    return render_template_string(HTML, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)