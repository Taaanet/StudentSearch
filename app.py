from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

# 📁 تحميل ملف Excel (غير الاسم حسب ملفك)
EXCEL_FILE = "students.xlsx"

# قراءة البيانات مرة واحدة
df = pd.read_excel(EXCEL_FILE)

@app.route("/", methods=["GET", "POST"])
def search():
    result = None

    if request.method == "POST":
        student_id = request.form.get("student_id")

        # البحث داخل Excel
        match = df[df["ID"].astype(str) == str(student_id)]

        if not match.empty:
            result = match.to_dict(orient="records")[0]
        else:
            result = {"error": "لا يوجد طالب بهذا الرقم"}

    return render_template_string("""
    <h2>🔍 نظام بحث الطلاب</h2>

    <form method="post">
        <input name="student_id" placeholder="ادخل رقم الطالب">
        <button type="submit">بحث</button>
    </form>

    <hr>

    {% if result %}
        {% if result.error %}
            <p style="color:red">{{ result.error }}</p>
        {% else %}
            <p>👤 الاسم: {{ result['NAME'] }}</p>
            <p>🏫 المرحلة: {{ result['STAGE'] }}</p>
            <p>📚 الصف: {{ result['CLASS'] }}</p>
            <p>📝 الملاحظات: {{ result['NOTES'] }}</p>
        {% endif %}
    {% endif %}
    """, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
