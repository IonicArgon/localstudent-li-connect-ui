import sys
import threading
import time
import os
import json
import datetime
from gui import GUI_MainWindow
from PyQt5.QtWidgets import QApplication

from app.leadsScraper import LeadsScraper
from app.leadsFilterer import LeadsFilterer
from app.leadsConnector import LeadsConnector

# globals
app = QApplication([])
window = GUI_MainWindow()
json_data = None


# thread for the actual work
def scrape_filter_connect():
    global window

    while True:
        # check if running
        if not window.get_has_started():
            continue

        # ? we already checked if any of the fields are empty in the gui

        # get the url
        url = window.get_link()

        # get the credentials for scraper
        headers_scrape = window.get_recruiterlite_header_file()
        cookies_scrape = window.get_recruiterlite_cookie_file()

        # get the credentials for connector
        headers_connect = window.get_header_file()
        cookies_connect = window.get_cookie_file()

        # get the message
        base_message = window.get_message_file()
        with open(base_message, "r", encoding="utf-8") as f:
            base_message = f.read()

        # get scraping parameters
        can_count = window.get_can_count()
        can_start = window.get_can_start()
        can_end = window.get_can_end()

        # set up scraper
        scraper = LeadsScraper(headers=headers_scrape, cookies=cookies_scrape)

        # set up filterer
        filterer = LeadsFilterer()

        # set up connector
        connector = LeadsConnector(headers=headers_connect, cookies=cookies_connect)

        # scrape
        window.add_status_text("Scraping with parameters:")
        window.add_status_text(f"\tcan_count: {can_count}")
        window.add_status_text(f"\tcan_start: {can_start}")
        window.add_status_text(f"\tcan_end: {can_end}")
        return_ = scraper.scrape(url, can_count=can_count, can_start=can_start, can_end=can_end)

        # check if we got a 307
        if return_ == -1:
            window.add_status_text("WARNING: Got HTTP 307. LinkedIn thinks the account is being shared. It's recommended that you stop for a while.")
            window.add_status_text("Stopping...")
            window.reset_start_button()
            continue

        # check if we got a -2
        if return_ == -2:
            window.add_status_text("ERROR: Failed to make request. Stopping...")
            window.reset_start_button()
            continue

        window.add_status_text("Scraping complete.")

        # filter
        window.add_status_text("Filtering leads...")
        leads = scraper.get_leads()
        filtered_leads = filterer.filter_leads(leads)
        window.add_status_text("Initial filtering complete.")
        window.add_status_text("Attempting to look for duplicates...")

        # check if we already generated a connected leads csv
        connected_leads_csv = None
        try:
            connected_leads_csv = os.path.join(os.getcwd(), "connected_leads.csv")
            with open(connected_leads_csv, "r", encoding="utf-8") as f:
                pass
            window.add_status_text("Found connected leads csv. Ignoring duplicates...")
        except:
            connected_leads_csv = None
            window.add_status_text("No connected leads csv found. Continuing...")

        # ignore duplicates
        filterer.ignore_duplicates(connected_leads_csv=connected_leads_csv)

        # we got this far, check to see if a stop was requested
        if not window.get_has_started():
            window.add_status_text("Request to stop received before connecting. Stopping...")
            continue

        # connect
        window.add_status_text("Connecting...")
        leads = filterer.get_filtered_leads()
        successful_connections = []
        failed_connections = []
        connect_count = 0

        # check if we have any leads
        if len(leads) == 0:
            window.add_status_text("No leads found. Stopping...")
            window.reset_start_button()
            continue

        for lead in leads:
            # check if we've reached the connection limit
            if connect_count >= window.get_connect_count():
                window.add_status_text("Connection limit reached. Stopping...")
                break

            formatted_message = base_message.format(
                recruiter_name=window.get_recruiter_name(),
                lead_name=lead["first_name"],
            )
            
            # check if a stop was requested
            if not window.get_has_started():
                window.add_status_text("Request to stop received while connecting. Stopping...")
                break

            # connect
            profile = connector.get_profile(lead["profile_id"])
            profile_urn = connector.get_profile_urn(profile)
            response_connection = connector.connect_to_profile(profile_urn, message=formatted_message)

            if response_connection.status_code == 200:
                successful_connections.append(lead["profile_id"])
                window.add_status_text(f"Successfully connected to {lead['profile_id']}.")
                connect_count += 1
            else:
                failed_connections.append(lead["profile_id"])
                window.add_status_text(f"Failed to connect to {lead['profile_id']}.")
                window.add_status_text(f"Response code: {response_connection.status_code}")

        # dump to csv
        window.add_status_text("Dumping successful connections...")
        with open("connected_leads.csv", "a", encoding="utf-8", newline='') as f:
            for lead in successful_connections:
                f.write(f"{lead}\n")

        window.add_status_text("Dumping failed connections...")
        with open("failed_leads.csv", "a", encoding="utf-8", newline='') as f:
            for lead in failed_connections:
                f.write(f"{lead}\n")
        
        # update the json data
        json_data["connections_sent_this_week"] += connect_count
        json_data["connections_sent_today"] += connect_count
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

        # reset the start button
        window.add_status_text("Done.")
        window.reset_start_button()

# this thread is to update saved credentials
def update_credentials():
    while True:
        recruiter_name = window.get_recruiter_name()
        recruiterlite_header_file = window.get_recruiterlite_header_file()
        recruiterlite_cookie_file = window.get_recruiterlite_cookie_file()
        header_file = window.get_header_file()
        cookie_file = window.get_cookie_file()
        message_file = window.get_message_file()

        json_data["recruiter_name"] = recruiter_name
        json_data["recruiterlite_header_file"] = recruiterlite_header_file
        json_data["recruiterlite_cookie_file"] = recruiterlite_cookie_file
        json_data["header_file"] = header_file
        json_data["cookie_file"] = cookie_file
        json_data["message_file"] = message_file

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

        # sleep for 5 seconds
        time.sleep(5)

if __name__ == "__main__":    
    # check if the data.json file exists, and load it
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except:
        json_data = {}

    # if it's empty, set up the json data
    if len(json_data) == 0:
        json_data = {
            "connections_sent_this_week": 0,
            "connections_sent_today": 0,
            "start_of_week": "",
            "last_ran": "",
            "recruiter_name": "",
            "recruiterlite_header_file": "",
            "recruiterlite_cookie_file": "",
            "header_file": "",
            "cookie_file": "",
            "message_file": "",
        }
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

    # automatically get the start of the week if it's empty
    if json_data["start_of_week"] == "":
        today = datetime.datetime.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        json_data["start_of_week"] = start_of_week.strftime("%Y-%m-%d")
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

    # automatically get the last ran if it's empty
    if json_data["last_ran"] == "":
        today = datetime.datetime.today()
        json_data["last_ran"] = today.strftime("%Y-%m-%d")
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

    # if it's been a week, reset the connections sent this week, and update the start of the week
    today = datetime.datetime.today()
    current_start_of_week = datetime.datetime.strptime(json_data["start_of_week"], "%Y-%m-%d")
    if today - current_start_of_week >= datetime.timedelta(days=7):
        json_data["connections_sent_this_week"] = 0
        new_start_of_week = today - datetime.timedelta(days=today.weekday())
        json_data["start_of_week"] = new_start_of_week.strftime("%Y-%m-%d")
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

    # if it's a new day, reset the connections sent today and update the last ran
    today = datetime.datetime.today()
    current_last_ran = datetime.datetime.strptime(json_data["last_ran"], "%Y-%m-%d")
    if today - current_last_ran >= datetime.timedelta(days=1):
        json_data["connections_sent_today"] = 0
        json_data["last_ran"] = today.strftime("%Y-%m-%d")
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

    # attempt to load any saved credentials
    window.fill_previous_data(
        recruiter_name=json_data["recruiter_name"],
        recruiterlite_header_file=json_data["recruiterlite_header_file"],
        recruiterlite_cookie_file=json_data["recruiterlite_cookie_file"],
        header_file=json_data["header_file"],
        cookie_file=json_data["cookie_file"],
        message_file=json_data["message_file"],
    )

    main_working_thread = threading.Thread(target=scrape_filter_connect)
    main_working_thread.daemon = True
    main_working_thread.start()

    update_credentials_thread = threading.Thread(target=update_credentials)
    update_credentials_thread.daemon = True
    update_credentials_thread.start()

    window.set_json_data(json_data)
    window.show()
    sys.exit(app.exec_())
