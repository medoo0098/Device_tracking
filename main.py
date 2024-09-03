from config import db, app



# creating all databases if not existing
with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
