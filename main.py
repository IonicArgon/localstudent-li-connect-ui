import sys
import threading
import csv
import os
import json
import datetime
from gui import GUI_MainWindow
from gui_help import GUI_Help
from PyQt5.QtWidgets import QApplication

from app.leadsScraper import LeadsScraper
from app.leadsFilterer import LeadsFilterer
from app.leadsConnector import LeadsConnector

# globals
app = QApplication([])
help_window = GUI_Help()
window = GUI_MainWindow(help_window=help_window)
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

        # get the credentials
        headers = window.get_header_file()
        cookies = window.get_cookie_file()

        # get the message
        base_message = window.get_message_file()
        with open(base_message, "r", encoding="utf-8") as f:
            base_message = f.read()

        # get scraping parameters
        can_count = window.get_can_count()
        can_start = window.get_can_start()
        can_end = window.get_can_end()

        # set up scraper
        scraper = LeadsScraper(headers=headers, cookies=cookies)

        # set up filterer
        filterer = LeadsFilterer()

        # set up connector
        connector = LeadsConnector(headers=headers, cookies=cookies)

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

        # filter and export to csv
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

        # write to csv
        window.add_status_text("Writing to csv...")
        with open("filtered_leads.csv", "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["first_name", "last_name", "profile_id"])
            for lead in filterer.get_filtered_leads():
                writer.writerow(
                    [lead["first_name"], lead["last_name"], lead["profile_id"]]
                )
        window.add_status_text("Writing to csv complete.")

        # we got this far, check to see if a stop was requested
        if not window.get_has_started():
            window.add_status_text("Request to stop received before connecting. Stopping...")
            continue


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
            "start_of_week": "",
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

    # if it's been a week, reset the connections sent this week, and update the start of the week
    today = datetime.datetime.today()
    start_of_week = datetime.datetime.strptime(json_data["start_of_week"], "%Y-%m-%d")
    if today - start_of_week > datetime.timedelta(days=7):
        json_data["connections_sent_this_week"] = 0
        json_data["start_of_week"] = today.strftime("%Y-%m-%d")
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

    main_working_thread = threading.Thread(target=scrape_filter_connect)
    main_working_thread.daemon = True
    main_working_thread.start()

    window.set_json_data(json_data)
    window.show()
    sys.exit(app.exec_())
