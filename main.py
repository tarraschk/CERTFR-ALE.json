import requests
import json
import os
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_alerts():
    time.sleep(5)
    url = "https://www.cert.ssi.gouv.fr/alerte/json/"
    logging.info(f"Fetching alerts from {url}")
    response = requests.get(url)
    response.raise_for_status()
    logging.info("Successfully fetched alerts.")
    return response.json()

def fetch_alert_details(json_url):
    base_url = "https://www.cert.ssi.gouv.fr"
    full_url = base_url + json_url
    logging.info(f"Fetching alert details from {full_url}")
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(full_url)
            response.raise_for_status()
            break
        except requests.RequestException as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(5*(attempt + 1))
            else:
                raise
    logging.info(f"Successfully fetched details for {json_url}")
    return response.json()

def parse_alerts(alerts):
    consolidated_data = []
    logging.info("Parsing alerts...")
    for alert in alerts:
        json_url = alert.get("json_url", "")
        if json_url:
            alert_details = fetch_alert_details(json_url)
            alert_id = alert.get("reference", "")
            published_at = alert.get("last_revision_date", "")
            cves = [cve.get("name") for cve in alert_details.get("cves", []) if cve.get("name", "").startswith("CVE")]

            if cves:
                consolidated_data.append({
                    "alert": alert_id,
                    "published_at": published_at,
                    "cves": cves
                })
                logging.info(f"Added alert {alert_id} with CVEs: {cves}")
    logging.info("Finished parsing alerts.")
    return consolidated_data

def save_to_json(data, filename="cert-fr-ale_with_cves.json"):
    logging.info(f"Saving consolidated data to {filename}")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info(f"Successfully saved data to {filename}")

def main():
    logging.info("Starting the script...")
    alerts = fetch_alerts()
    consolidated_data = parse_alerts(alerts)
    save_to_json(consolidated_data)
    logging.info("Script finished successfully.")

if __name__ == "__main__":
    main()
