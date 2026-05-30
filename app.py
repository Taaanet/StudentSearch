from flask import Flask, render_template, request, redirect, session
import pandas as pd

app = Flask(__name__)
app.secret_key = "secret123"

FILE = "students.xlsx"

def load_data():
    return pd.read_excel(FILE)

# 🏠 الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("index.html")

# 🔍 البحث عن طالب (مادة واحدة فقط)
@app.route("/search", methods=["POST"])
def search():
    student_id = request.form["id"]
    subject = request.form["subject"]

    df = load_data()

    student = df[(df["ID"].astype(str) == str(student_id)) &
                 (df["SUBJECT"] == subject)]

    if student.empty:
        return render_template("index.html", error="لا توجد بيانات")

    info = student.iloc[0].to_dict()

    # 📊 بيانات الرسم (حسب الأسبوع)
    chart_data = student.sort_values("WEEK")

    labels = chart_data["WEEK"].astype(str).tolist()
    values = chart_data["MARK"].tolist()

    return render_template("result.html",
                           student=info,
                           labels=labels,
                           values=values)

# 🔐 تسجيل دخول الأدمن
@app.route("/admin-login", methods=["POST"])
def admin_login():
    password = request.form["password"]

    if password == "admin":
        session["admin"] = True
        return redirect("/admin")

    return render_template("index.html", error="كلمة المرور خطأ")

# 📊 لوحة الأدمن
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/")

    df = load_data()
    return render_template("admin.html",
                           tables=df.to_dict(orient="records"))

# 🚪 خروج
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
