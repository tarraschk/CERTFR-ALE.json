import requests
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_alerts():
    url = "https://www.cert.ssi.gouv.fr/alerte/json/"
    logging.info(f"Fetching alerts from {url}")
    for attempt in range(3):
        try:
            response = requests.get(url)
            response.raise_for_status()
            logging.info("Successfully fetched alerts.")
            return response.json()
        except HTTPError as http_err:
            if 500 <= response.status_code < 600:
                logging.warning(f"Server error {response.status_code} on attempt {attempt + 1}. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                logging.error(f"HTTP error occurred: {http_err}")
                raise
        except Exception as err:
            logging.error(f"Other error occurred: {err}")
            raise
    logging.error("Failed to fetch alerts after 3 attempts.")
    raise Exception("Failed to fetch alerts after 3 attempts.")

def fetch_alert_details(json_url):
    base_url = "https://www.cert.ssi.gouv.fr"
    full_url = base_url + json_url
    logging.info(f"Fetching alert details from {full_url}")
    for attempt in range(3):
        try:
            response = requests.get(full_url)
            response.raise_for_status()
            logging.info(f"Successfully fetched details for {json_url}")
            return response.json()
        except HTTPError as http_err:
            if 500 <= response.status_code < 600:
                logging.warning(f"Server error {response.status_code} on attempt {attempt + 1}. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                logging.error(f"HTTP error occurred: {http_err}")
                raise
        except Exception as err:
            logging.error(f"Other error occurred: {err}")
            raise
    logging.error(f"Failed to fetch alert details for {json_url} after 3 attempts.")
    raise Exception(f"Failed to fetch alert details for {json_url} after 3 attempts.")

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
