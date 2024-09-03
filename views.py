
from flask import render_template, redirect, url_for, flash, request, send_from_directory
from forms import (RegisterForm, LoginForm, ScanForm, AssignForm, RenameUpdateForm, AddForm, SearchForm, ShowDB,
                   ReturnedForm, ExportForm, EditForm)
from models import User, ModDem
from flask_login import login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import os
import datetime
from werkzeug.utils import secure_filename


def inti_routes(app, db):

    # Configure Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)






    # path to the md.csv to populate the database with ipad information, asset id and serial number.
    file_path = r"\\192.168.16.16\MAC\mdAssetList.csv"

    # Route to assign the assets to location.
    asset_list = []





    # user loader decorator for flask app
    @login_manager.user_loader
    def load_user(user_id):
        return db.get_or_404(User, user_id)





    # Register new users into the User database
    @app.route('/register', methods=["GET", "POST"])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            try:
                # Check if user email is already present in the database.
                result = db.session.execute(db.select(User).where(User.name == form.name.data))
                user = result.scalar()
                if user:
                    # User already exists
                    flash("You've already signed up with that name, log in instead!", "success")
                    return redirect(url_for('login'))

                # hashing the password for the user to store as a hash not plain text
                hash_and_salted_password = generate_password_hash(
                    form.password.data,
                    method='pbkdf2:sha256',
                    salt_length=8
                )
                # creating new user on database
                new_user = User(
                    name=form.name.data.lower(),
                    password=hash_and_salted_password,
                )
                db.session.add(new_user)
                db.session.commit()
                # This line will authenticate the user with Flask-Login
                login_user(new_user)
                return redirect(url_for("get_all_assets"))
            except:
                # Handle any IntegrityError exceptions (e.g., duplicate entry)
                db.session.rollback()
                flash("User already exists. Please try different name.", "error")
                return redirect(url_for('register'))
        return render_template("register.html", form=form, current_user=current_user)



    # login route to allow user to login
    @app.route('/login', methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            password = form.password.data
            result = db.session.execute(db.select(User).where(User.name == form.name.data.lower()))
            # Note, email in db is unique so will only have one result.
            user = result.scalar()
            # Email doesn't exist
            if not user:
                flash("That name does not exist, please try again.", "error")
                return redirect(url_for('login'))
            # Password incorrect
            elif not check_password_hash(user.password, password):
                flash('Password incorrect, please try again.', "error")
                return redirect(url_for('login'))
            else:
                login_user(user)
                return redirect(url_for('get_all_assets'))

        return render_template("login.html", form=form, current_user=current_user)





    # log out user when they are finished with the work
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('get_all_assets'))




    # landing page / home page
    @app.route('/', methods=["GET", "POST"])
    def get_all_assets():
        print("HOME")
        form = ShowDB()
        export_form = ExportForm()
        result = db.session.execute(db.select(ModDem))
        assets = result.scalars().all()
        if export_form.validate_on_submit() and export_form.form_type.data == "export":
            print("export")
            all_records = ModDem.query.all()

            # Convert the queried records into a pandas DataFrame
            data = {
                "Serial Number": [],
                "UDID": [],
                "Asset ID": [],
                "Cover Tag": [],
                "Location": [],
                "Technician": [],
                "Time Scanned": [],
                "Owner": [],
                "Returned": []
            }
            for record in all_records:
                data["Serial Number"].append(record.serial_number)
                data["UDID"].append(record.udid)
                data["Asset ID"].append(record.asset_id)
                data["Cover Tag"].append(record.cover_tag)
                data["Location"].append(record.location)
                data["Technician"].append(record.technician)
                data["Time Scanned"].append(record.time_scanned)
                data["Owner"].append(record.owner)
                data["Returned"].append(record.returned)

            df = pd.DataFrame(data)
            print("data frame is set")
            # Export the DataFrame to a CSV file
            csv_filename = "ModDem_records.csv"
            csv_path = os.path.join(os.path.dirname(__file__), csv_filename)
            print("path is set")
            df.to_csv(csv_path, index=False)
            print("csv saved")
            return redirect(url_for("get_all_assets"))
        if form.validate_on_submit() and form.form_type.data == "db":
            print("form")
            print(form.form_type.data)
            return redirect(url_for("show_db"))

        return render_template("index.html", all_assets=assets, current_user=current_user, form=form,
                            export_form=export_form, form_type="export", db_form_type="db")




    # scanning devices to add cover tag to database acording to asset ID
    @app.route("/add_new_asset", methods=["GET", "POST"])
    def add_new_asset():
        print("SCAN ASSET")
        form = ScanForm()
        if form.validate_on_submit():
            if len(form.asset_id.data) < 5 or len(form.cover_tag.data) > 4:
                flash("Scan items again")
                return redirect(url_for("add_new_asset"))
            else:
                result = db.session.execute(db.select(ModDem).where(ModDem.asset_id == form.asset_id.data))
                asset = result.scalar()

                if asset is not None:  # meaning asset exist and can be manipulated

                    try:  # trying to assign cover tag to scanned tag
                        asset.cover_tag = form.cover_tag.data
                        asset.technician = current_user.name
                        asset.time_scanned = datetime.datetime.now()
                        db.session.commit()
                        flash("Asset updated successfully!")
                        print(f"{form.asset_id.data} was assigned cover tag {form.cover_tag.data}")
                        return redirect(url_for("add_new_asset"))
                    except Exception as e:  # if there was a problem adding the cover tag, it will flash a failed message
                        flash("There was a problem assigning the tag, YOU MAY NOT BE LOGGED IN OR Please contact the admin.", "error")
                        return redirect(url_for('add_new_asset'))

                else:  # if the asset is not in the list, check spelling or add manually.
                    flash("Asset ID not found. Please make sure it exists.", "error")
                    return redirect(url_for('add_new_asset'))

        return render_template("add-asset.html", form=form, current_user=current_user)





    @app.route("/assign_asset", methods=["GET", "POST"])
    def assign_asset():
        global asset_list
        print("ASSIGN ASSET TO LOCATION")
        print(f"List containing scanned assets => {asset_list}")
        form = AssignForm()
        cover_form = ReturnedForm()
        # if request.method == "POST" and "custom_action" in request.form:
        #     print("yup")
        if cover_form.validate_on_submit():
            if cover_form.cover_tag.data not in asset_list:
                asset_list.append(cover_form.cover_tag.data)
                print(f"cover {cover_form.cover_tag.data} was added to list")

                print(f"you have scanned {len(asset_list)} items ")
        else:
            # if request.method == "POST" and "custom_action" in request.form:
            #     print("yup")
            if form.validate_on_submit():
                # an empty list for email and identifier to be converted to Miradore
                # template for upload to users list of devices.
                data = {
                    "Email": [],
                    "Identifier": []
                }
                # for all the device ranges , assign the cover number to a user
                # takes cover tag, with that info, takes serial number and created a csv file for that location
                # print(form.locations.data)

                for i in asset_list.copy():
                    # print(i)

                    result = db.session.execute(db.select(ModDem).where(ModDem.cover_tag == i))
                    print(result)
                    asset = result.scalar()
                    print(asset)
                    # print(f"asset {asset} was found")
                    if asset:
                        asset.location = form.locations.data
                        # print(f"location is {form.locations.data}")
                        db.session.commit()
                        # print("location added to DB")
                        serial_number = asset.serial_number
                        print(serial_number)
                        # print(f"serial number is found")
                        data["Email"].append(form.locations.data)
                        data["Identifier"].append(serial_number)
                        asset_list.remove(i)
                        print(f"cover {i} was added to csv")
                        print(f"cover{i} is removed from temp asset list ")
                    else:
                        print(f"    cover {i} didnt add to csv")
                df = pd.DataFrame(data)
                base_dir = os.path.dirname(os.path.abspath(__file__))
                # Specify the relative path to your files directory
                folder_path = os.path.join(base_dir, 'locations')
                # Access the form field correctly: form.location.data
                filename = f"{form.locations.data}.csv"
                path = os.path.join(folder_path, filename)
                df.to_csv(path, index=False)
                print(df)
                return redirect(url_for("assign_asset"))

        if request.method == "POST":
            try:
                if request.form["clear"] == "clear":
                    print("list is empty now")
                    flash("List is cleared")
                    asset_list = []
                else:
                    pass
            except:
                print("Didnt clear the list")

            # Get the current working directory of your Flask app
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Specify the relative path to your files directory
        folder_path = os.path.join(base_dir, 'locations')

        # Get a list of all files in the folder
        files = os.listdir(folder_path)

        return render_template("assign_asset.html", cover_form=cover_form, form=form,
                            current_user=current_user, files=files, asset_list=asset_list)





    # to manually add a device to the database
    @app.route("/add", methods=["GET", "POST"])
    def add():
        form = AddForm()
        if form.validate_on_submit():
            new_device = ModDem(
                asset_id=form.asset_id.data,
                serial_number=form.serial_number.data,
                owner=form.owner.data
            )
            db.session.add(new_device)
            db.session.commit()
            flash("Device added successfully", "success")
            return redirect(url_for("add_new_asset"))
        return render_template("add.html", form=form)





    @app.route("/populate")
    def populate():
        csv_data = pd.read_csv(file_path)
        if current_user.id == 1:
            for index, row in csv_data.iterrows():
                # Extract serial number and asset tag from CSV
                sn = row["serial number"]
                asset_id = row["asset tag"]
                owner = row["owner"]

                # Check if asset_id already exists in the database
                existing_device = ModDem.query.filter_by(asset_id=asset_id).first()

                if existing_device:
                    # Asset ID already exists, handle accordingly
                    print(f"Asset ID {asset_id} already exists in the database.")
                    # You can choose to skip, update, or handle the duplicate in another way
                    continue

                # Asset ID doesn't exist, create a new device
                if len(sn) == 11:
                    serial_number = sn[1:]
                else:
                    serial_number = sn

                # Create and add new device to the database
                new_device = ModDem(serial_number=serial_number, asset_id=asset_id, owner=owner)

                # Add to the session and commit
                db.session.add(new_device)
                try:
                    db.session.commit()
                    print((f"asset {asset_id} added to database"))
                except:
                    # Handle any IntegrityError exceptions (e.g., if another process added the same asset_id concurrently)
                    db.session.rollback()
                    print(f"Error adding device with asset ID {asset_id}")

            return "Data population complete."
        return "you're not admin"



    # takes a csv file containing udid and serial number and updates the database according to serial number with udid
    @app.route("/rename_export", methods=["GET", "POST"])
    def rename_export():
        form = RenameUpdateForm()
        file_path2 = None

        if form.validate_on_submit():
            file = form.file.data  # Get the uploaded file
            if file:
                filename = secure_filename(file.filename)
                file_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
                try:
                    file.save(file_path2)
                    flash('File uploaded successfully!', 'success')
                except Exception as e:
                    flash(f'File upload failed: {str(e)}', 'error')
                    return redirect(request.url)
            else:
                flash('No file selected!', 'error')
                return redirect(request.url)

        if file_path2:
            try:
                df = pd.read_csv(file_path2)
                print(df.head())
                for index, row in df.iterrows():
                    try:
                        result = db.session.execute(db.select(ModDem).where(ModDem.serial_number == row["Serial Number"]))
                        asset = result.scalar()
                        if asset:
                            asset.udid = row["UDID"]
                            db.session.commit()
                            print(f'Updated asset: {asset.serial_number} with UDID: {asset.udid}')
                        else:
                            flash(f'Asset with serial number {row["Serial Number"]} not found!', 'error')
                    except Exception as e:
                        flash(f'Error processing row {index}: {str(e)}', 'error')
            except FileNotFoundError:
                flash('Uploaded file not found!', 'error')
            except pd.errors.EmptyDataError:
                flash('No data in CSV file!', 'error')
            except pd.errors.ParserError:
                flash('Error parsing CSV file!', 'error')
            except Exception as e:
                flash(f'Unexpected error: {str(e)}', 'error')

        return render_template("rename.html", form=form)


    # thgis allows the download of the csv files created with location name adn assets assigned to it.
    @app.route('/download/<path:filename>')
    def download_file(filename):
        folder_path = 'locations'  # Adjust the folder path as per your directory structure
        return send_from_directory(folder_path, filename, as_attachment=True)


    # shows all the assets in the database regardless of their status in the process.
    @app.route("/show_db", methods=["GET", "POST"])
    def show_db():
        result = db.session.execute(db.select(ModDem))
        assets = result.scalars().all()

        table_headers = ['ID', 'Cover Tag', 'Asset Tag', 'Serial Number', 'Location', 'UDID', 'Technician', 'Time']
        return render_template("show_db.html", all_assets=assets, current_user=current_user, table_headers=table_headers)


    scanned_returned_items = []
    @app.route("/returned", methods=["GET", "POST"])
    def returned():
        global scanned_returned_items
        result = db.session.execute(db.select(ModDem).where(ModDem.cover_tag == "5000"))
        asset = result.scalar()
        print("return")
        form = ReturnedForm()
        if form.validate_on_submit():
            existing_cover_tags = {item['cover_tag'] for item in scanned_returned_items}
            if form.cover_tag.data in existing_cover_tags:
                pass
            else:
                try:
                    result = db.session.execute(db.select(ModDem).where(ModDem.cover_tag == form.cover_tag.data))
                    asset = result.scalar()
                    asset.returned = datetime.datetime.now()
                    db.session.commit()
                    dict_item = {
                        "cover_tag" : asset.cover_tag,
                        "location" : asset.location,
                        "owner" : asset.owner,
                    }
                    scanned_returned_items.append(dict_item)
                    flash("Saved Successfully")
                    print(scanned_returned_items)
                    print(len(scanned_returned_items), asset.location)
                    return render_template("return.html", form=form, items=scanned_returned_items, asset=asset)
                except:
                    flash("Asset not found!!!")
        if request.method == "POST":
            try:
                if request.form["clear"] == "clear":
                    print("works")
                    scanned_returned_items=[]
                else:
                    pass
            except:
                print("repeated number")
                flash("repeated number")
        return render_template("return.html", form=form, items=scanned_returned_items, asset=asset)


    @app.route("/edit/<int:asset_id>", methods=["GET", "POST"])
    def edit(asset_id):
        asset = db.get_or_404(ModDem, asset_id)
        edit_form = EditForm(
            asset_id=asset.asset_id,
            cover_tag=asset.cover_tag,
            serial_number=asset.serial_number,
            location=asset.location,
            owner = asset.owner
        )
        if edit_form.validate_on_submit():
            asset.asset_id = edit_form.asset_id.data
            asset.cover_tag = edit_form.cover_tag.data
            asset.serial_number = edit_form.serial_number.data
            asset.location = edit_form.location.data
            asset.owner = edit_form.owner.data
            db.session.commit()
            return redirect(url_for("get_all_assets", asset_id=asset.id))
        return render_template("edit.html", form=edit_form, is_edit=True, current_user=current_user)


    @app.route("/delete/<int:asset_id>", methods=["GET", "POST"])
    def delete(asset_id):
        asset = db.get_or_404(ModDem, asset_id)
        db.session.delete(asset)
        db.session.commit()
        print(f"asset {asset.cover_tag} was deleted")
        return redirect(url_for("get_all_assets"))




    # deleted all data on the asset database, no warning.


    # @app.route("/delete_all")
    # def empty_database():
    #     entries_to_delete = db.session.query(ModDem).all()
    #     if current_user.id == 1 :
    #         # Iterate over the query result and delete each entry
    #         for entry in entries_to_delete:
    #             db.session.delete(entry)
    #
    #         # Commit the changes to persist the deletions
    #         db.session.commit()
    #
    #         return redirect(url_for("get_all_assets"))
    #     return "you're not admin"




