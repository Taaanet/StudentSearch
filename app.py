from flask import Flask, request, render_template_string
import pandas as pd
import os

app = Flask(__name__)

# 📁 ملف Excel
EXCEL_FILE = "students.xlsx"
df = pd.read_excel(EXCEL_FILE)

# 🔥 تصميم احترافي
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Search System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Arial;
            background: #eef2f7;
            margin: 0;
        }

        .container {
            max-width: 800px;
            margin: 40px auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }

        h2 {
            text-align: center;
            color: #2c3e50;
        }

        input {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            border-radius: 10px;
            border: 1px solid #ccc;
            font-size: 16px;
        }

        button {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #2980b9;
        }

        .card {
            margin-top: 25px;
            padding: 20px;
            border-radius: 12px;
            background: #f8f9fb;
            border-right: 5px solid #3498db;
        }

        .row {
            padding: 6px 0;
            border-bottom: 1px solid #ddd;
        }

        .label {
            font-weight: bold;
            color: #2c3e50;
        }

        .error {
            color: red;
            text-align: center;
            font-weight: bold;
        }
    </style>
</head>

<body>

<div class="container">

    <h2>🔍 Student Search System</h2>

    <form method="post">
        <input name="student_id" placeholder="Enter Student ID">
        <button type="submit">Search</button>
    </form>

    {% if result %}
        <div class="card">

            {% if result.error %}
                <div class="error">{{ result.error }}</div>
            {% else %}
                {% for key, value in result.items() %}
                    <div class="row">
                        <span class="label">{{ key }}:</span> {{ value }}
                    </div>
                {% endfor %}
            {% endif %}

        </div>
    {% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def search():
    result = None

    if request.method == "POST":
        student_id = request.form.get("student_id")

        match = df[df["ID"].astype(str) == str(student_id)]

        if not match.empty:
            result = match.iloc[0].to_dict()  # 🔥 عرض كل الأعمدة تلقائيًا
        else:
            result = {"error": "❌ لا يوجد طالب بهذا الرقم"}

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
