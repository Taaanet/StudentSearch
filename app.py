from flask import Flask, render_template, request
import pandas as pd
from utils.excel_reader import load_data

app = Flask(__name__)

# 📊 تحميل البيانات
df = load_data("students.xlsx")


# -----------------------
# 🧑 صفحة الطالب
# -----------------------
@app.route("/", methods=["GET", "POST"])
def student_search():
    if request.method == "POST":
        try:
            student_id = int(request.form["id"])

            student_rows = df[df["ID"] == student_id]

            if student_rows.empty:
                return render_template("login.html", error="❌ ID غير موجود")

            subject = student_rows["SUBJECT"].iloc[0]

            filtered = df[
                (df["ID"] == student_id) &
                (df["SUBJECT"] == subject)
            ]

            return render_template(
                "student.html",
                name=filtered["NAME"].iloc[0],
                class_name=filtered["CLASS"].iloc[0],
                stage=filtered["STAGE"].iloc[0],
                subject=subject,
                table=filtered.to_dict(orient="records")
            )

        except:
            return render_template("login.html", error="⚠️ خطأ في الإدخال")

    return render_template("login.html")


# -----------------------
# 🔐 Admin Panel
# -----------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form["password"]

        if password == "admin":
            return render_template(
                "admin.html",
                table=df.to_dict(orient="records")
            )
        else:
            return render_template(
                "admin.html",
                error="❌ كلمة المرور غير صحيحة"
            )

    return render_template("admin.html")


if __name__ == "__main__":
    app.run(debug=True)
