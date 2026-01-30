from flask import Flask, render_template, redirect, request, url_for, make_response, send_file
import uuid
import json
import pandas as pd
import io

app = Flask(
    __name__,
    template_folder="template",
            )

tasks_list = [{"id": "f217cfe5-98e5-4164-afe6-80d9c54bab11",
            "title":"hello",
          "status":"pending",
          "content": "this is a test"}]

@app.get("/")
def index_view():
    return render_template("index.html", tasks = tasks_list)


@app.post("/create")
def create_task():
    tasks_list.append({
        "id" : str(uuid.uuid4()),
        "title" : request.form.get("title"),
        "status" : request.form.get("status"),
        "content" : request.form.get("content")
    })

    return redirect(url_for("index_view"))

@app.post("/delete/<id>")
def delete_task(id):
    global tasks_list

    tasks_list = [task for task in tasks_list if task["id"] != id]

    return redirect(url_for("index_view"))

@app.post("/edit/<id>")
def edit_task(id):
    for task in tasks_list:
        if task["id"] == id:
            task["title"] = request.form.get("title")
            task["status"] = request.form.get("status")
            task["content"] = request.form.get("content")

    return redirect(url_for("index_view"))

@app.get("/view/<id>")
def view_task(id):
    task = next((task for task in tasks_list if task["id"] == id), None)

    if not task:
        return "Task not found", 404
    
    return render_template("view.html", task=task)

@app.get("/download/json")
def download_json():
    response = make_response(json.dumps(tasks_list, ensure_ascii=False, indent=2))

    response.headers["Content-Type"] = "application/json"
    response.headers["Content-Disposition"] = "attachment; filename=tasks_backup.json"

    return response

@app.get("/download/excel")
def download_excel():
    if not tasks_list:
        return "No tasks to export", 400
    df = pd.DataFrame(tasks_list)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Tasks")

    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name="tasks_backup.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    app.run(debug=True)