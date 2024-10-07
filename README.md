# CERTFR-ALE.json

A single JSON file with all CERT-FR ALE entries and their CVE data.

## Why?

The CERT-FR is the official CERT of the French National Agency for the Security of Information Systems (ANSSI - Agence Nationale de la Sécurité des Systèmes d'Information).

The CERT-FR provides very interesting data, like the [CERT-FR ALE](https://www.cert.ssi.gouv.fr/alerte/), which are national alerts on the most dangerous vulnerabilities.

In some way, CERT-FR ALE is like a CISA KEV (Known Exploited Vulnerabilities) for France.

CISA KEV provides all of its data in the JSON format, in one file. For CERT-FR ALE however, you have only an official JSON index, and you must then make multiple calls to fetch all its data.

This repo fetches all CERT-FR ALE data and combines alerts with their CVEs, in one file, so that you can easily use this data like for CISA KEV.

## How to use?

Just use the [https://raw.githubusercontent.com/tarraschk/CERTFR-ALE.json/refs/heads/main/cert-fr-ale_with_cves.json](https://raw.githubusercontent.com/tarraschk/CERTFR-ALE.json/refs/heads/main/cert-fr-ale_with_cves.json) URL as your data feed.

## How often is the repo updated?

The repo is updated every day at midnight UTC.

## License

GPLv3, see the LICENSE file.

## Authors

Maxime ALAY-EDDINE, for [https://galeax.com](https://galeax.com) 🇫🇷.

