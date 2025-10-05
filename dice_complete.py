#!/usr/bin/env python3
"""
Complete Dice Talent Search and Scraping Script
Handles: Login → Filter Application → Data Extraction → Export
"""

import subprocess
import sys
import time
import json
import random
from datetime import datetime
import os
import pandas as pd
from playwright.sync_api import sync_playwright

# ===== Configuration =====
def should_regenerate_query():
    """
    Check if Dice_string.txt should be regenerated based on file timestamps
    Returns True if job_description.txt is newer than Dice_string.txt
    """
    job_desc_file = "job_description.txt"
    dice_string_file = "Dice_string.txt"

    # If either file doesn't exist, return appropriate value
    if not os.path.exists(job_desc_file):
        return False

    if not os.path.exists(dice_string_file):
        return True

    # Compare modification times
    job_desc_mtime = os.path.getmtime(job_desc_file)
    dice_string_mtime = os.path.getmtime(dice_string_file)

    # If job_description.txt is newer, we should regenerate
    return job_desc_mtime > dice_string_mtime

def load_boolean_query():
    """Load Boolean query from Dice_string.txt or use default"""
    dice_string_file = "Dice_string.txt"
    job_desc_file = "job_description.txt"

    # Check if we should regenerate the query
    if should_regenerate_query():
        print(f"🔄 job_description.txt has been updated")
        print(f"📝 Regenerating Boolean query from {job_desc_file}...")
        try:
            from dice_api import generate_dice_query_with_chatgpt
            query = generate_dice_query_with_chatgpt(job_desc_file, dice_string_file)
            if query:
                print(f"✅ Generated new Boolean query")
                return query
        except ImportError:
            print("⚠️ dice_api.py not found, cannot auto-generate query")
        except Exception as e:
            print(f"⚠️ Error generating query: {e}")

    # Try to read from Dice_string.txt
    if os.path.exists(dice_string_file):
        try:
            with open(dice_string_file, 'r', encoding='utf-8') as f:
                query = f.read().strip()
                if query:
                    print(f"✅ Loaded Boolean query from {dice_string_file}")
                    return query
        except Exception as e:
            print(f"⚠️ Error reading {dice_string_file}: {e}")

    # If file doesn't exist or is empty, try to generate it
    print(f"⚠️ {dice_string_file} not found or empty")

    if os.path.exists(job_desc_file):
        print(f"📝 Found {job_desc_file}, attempting to generate Boolean query...")
        try:
            # Import and run dice_api to generate the query
            from dice_api import generate_dice_query_with_chatgpt
            query = generate_dice_query_with_chatgpt(job_desc_file, dice_string_file)
            if query:
                print(f"✅ Generated Boolean query using ChatGPT")
                return query
        except ImportError:
            print("⚠️ dice_api.py not found, cannot auto-generate query")
        except Exception as e:
            print(f"⚠️ Error generating query: {e}")

    # Fallback to default query
    print("📋 Using default Boolean query (Appian Developer)")
    return '(Appian OR "Appian Developer" OR "Appian Engineer" OR "Appian Architect" OR "Appian BPM" OR "Appian Designer" OR "Appian Consultant") AND (SAIL OR "Appian UI" OR "Appian RPA" OR "Appian Integration" OR "Appian Automation") AND ("Business Process Management" OR BPM) AND (Java OR J2EE OR "JavaScript" OR C#) AND ("low-code" OR "low code" OR "low-code development") AND (workflow OR "process modeling" OR "workflow automation") AND (integration OR API OR "third-party systems") AND (SQL OR "data modeling" OR "data management") AND (AWS OR "Amazon Web Services" OR "Cloud Integration")'

# Load the Boolean query at startup
BOOLEAN = load_boolean_query()

# These will be set by user input or defaults
LOCATION = None
DISTANCE_MILES = None
LAST_ACTIVE_DAYS = None

# Login cookies (from dice_login.py)
cookies_json = [
    {
        "domain": "www.dice.com",
        "hostOnly": True,
        "httpOnly": False,
        "name": "cms-gtm-randomNumSample",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": True,
        "storeId": None,
        "value": "4"
    },
    {
        "domain": "www.dice.com",
        "expirationDate": 1791066669,
        "hostOnly": True,
        "httpOnly": False,
        "name": "liveagent_oref",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "https://www.dice.com/employer/login-landing?optin=classic"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1794091015.967887,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_mkto_trk",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "id:318-VQK-428&token:_mch-dice.com-403e7c465b589c81e55e5da5e4e618b9"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1767310178,
        "hostOnly": False,
        "httpOnly": False,
        "name": "ddw24_1stpartycookie",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "{\"OTS\":{\"utm_source\":\"undefined\",\"utm_medium\":\"undefined\",\"utm_term\":\"undefined\",\"utm_content\":\"undefined\",\"utm_campaign\":\"undefined\",\"utm_campaign_id\":\"undefined\",\"dice_web_url\":\"https://www.dice.com/\",\"referrerURL\":\"undefined\",\"date\":\"2025-10-03T22:29:38.221Z\"},\"FC\":{\"utm_source\":\"undefined\",\"utm_medium\":\"undefined\",\"utm_term\":\"undefined\",\"utm_content\":\"undefined\",\"utm_campaign\":\"undefined\",\"utm_campaign_id\":\"undefined\",\"dice_web_url\":\"undefined\",\"referrerURL\":\"undefined\",\"date\":\"undefined\"},\"LC\":{\"utm_source\":\"undefined\",\"utm_medium\":\"undefined\",\"utm_term\":\"undefined\",\"utm_content\":\"undefined\",\"utm_campaign\":\"undefined\",\"utm_campaign_id\":\"undefined\",\"dice_web_url\":\"undefined\",\"referrerURL\":\"undefined\",\"date\":\"undefined\"}}"
    },
    {
        "domain": "www.dice.com",
        "expirationDate": 1791066669,
        "hostOnly": True,
        "httpOnly": False,
        "name": "liveagent_vc",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "2"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1767306579,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gcl_au",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "1.1.333581087.1759530579.1026376842.1759530590.1759530659"
    },
    {
        "domain": "www.dice.com",
        "hostOnly": True,
        "httpOnly": False,
        "name": "liveagent_sid",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": True,
        "storeId": None,
        "value": "4eb30b6b-e4ef-4300-b565-cbcb5601b038"
    },
    {
        "domain": "www.dice.com",
        "expirationDate": 1791066669,
        "hostOnly": True,
        "httpOnly": False,
        "name": "liveagent_ptid",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "4eb30b6b-e4ef-4300-b565-cbcb5601b038"
    },
    {
        "domain": ".www.dice.com",
        "expirationDate": 1762122661,
        "hostOnly": False,
        "httpOnly": False,
        "name": "refreshToken",
        "path": "/",
        "sameSite": None,
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.CC7F33SMcAyDyQ0EQ_wxBS70vL2WexGhPr4AP__oKDylg53wSPPNP2FExjJfkNlMZPvV1imJ035caidQNo69Iu4KG48cn_6sw9-FLBaMyOeCpOQ34QVhQRKghxUZMvG7kh0j7RVVZQzuTK-sja8Ovd4VFXfAhmlU0i209IoolJaTiRXw1oY3aKCRM_y9MXYOtO9S_7GNLvkqVuo90NBiggCS1gykauSjRprb0Qe5BCSB1romqz_LrB8lYLzSZHlEd38V-zXaVqkz0sdrmAi4C7BZnNDwLjwfWwSdn4k5C_GWL9_Q2KsWjHCSQUi7rRTbxPRbtTaIaYNeiuGXnGKyMQ.92Uh7MD5TUkOFvKL.JL33QrGj5aaWa5xVOhzmxVvpDBBa51DCTpqNnyuQEVYhnXdpbtpZQ8R3tySHwi4BjtThFGbuz-TdxLMxwMUwoYbqvb24_zvc19KH5qTeUdaMBTYVF-5wXSmrK8QSqwfzvLLr14YlQ3aBPOpi_PpZDS6U6Sg3C5xy5-t3SeAgMk-BEokuk5kGM9bIaD4zt21acjewGaIwDPHDXawkCrZQHYwr2rTj8Vn5BniKfDF4qDvxm9GQGBtdtV24LxENuv2LhhD2ewJXUzq1zfCp932JoHZKXdzCykuuobL_PVXf1dnnr65P4Wzt3L1DkMslyiZM9LBmrrWXJi0r0sV2RaGcgaJmoIiuTibDmZysh91RkZtVZPhp0QqUzRJU82z6qEfpleGimecpiQ0KeKxEKeDNL7ZuFQuF49Q6A5jff9pJ6yGz-faun3ZeV5oZCbUYVetrtZ6zDTEK9XQjRoX1AbVG5ITCaTzWELW7JQWjafiylsk1t_JZuVm9kiY8mW-q72zzInkgN2nL99PF0I6jEsHAFlaUsdVzwEdmF9RAgkD9Wu4dZaqHgKM1iYSwB8OdJFCy-HvTrvQceVoH0UZ7w6iX70j-ZNH9LC0eRkGOX8WMZ4D8klM7Kkb3HnZiFrBujz-op3pA-0wgx7LsGayb2cQfuHSaIhs05MWJ71_tN3bJZc8sg7BjNSMaJ1gCLBk5z45-alUkFuOCjRWz1FLQ7jXnpTAw5W3ahcjl-9EsVAhsV6AXqm1AcxXOe2wQPLVdxXLLGo5JICaViegzCBhaQf85nNZmSbHN_VRDJT2ITGmwkgjBijQlURt6kHrXlDnRAE9tLBttG9Brg28bmh_tjZzDH7K5Bw-I9sOBq80EaiYOTzvYywkwTS836EZJjPv7jxBzkVLXB4-T2-uZuXwn49CpIxtBM_PVkbJEx3Rlv3S23ppGnEYT9yb6E8_ObZsxU6ZDJJGBTTbWeDCsLjuJOsSTkbaz6CjO7k7CGSK-lZhvxgHaurR25czpvhZIHxdA15AIdpFmAj_MY7J_B7I7Y62gecStQ2HdfcIoes-GCcBmC83SsxWKxMfjhTet5l9ifSUb3q-hcOGIqdxA2c9gf7OzPottKutntLAm2Hpe34awbie07T8KTcbhIp1bG46-b-cgjHpj4x2DsvWGe2TuaJQfGPROtbF5cTtOO-eCaXd0KE8zVAwRY9u6De5WebEjhLF2h8YIDG64ssDSbMRv6biYSmW16upH0q2FYjCF9KSdJsxvZLhsqMjgbdapPkRJiozXBTqNeayjjaoigNcrg-m8PsMIa7S2qOPHtnRbf0rHLdOZ3HpBY-SetPTOVlI.flfm9_BHHcK4nag6Nl1JRA"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1794090662.767216,
        "hostOnly": False,
        "httpOnly": True,
        "name": "D2SESS",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "1833d2044a78e7fcaf775ea399ca861a"
    },
    {
        "domain": ".www.dice.com",
        "expirationDate": 1791066580,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_zitok",
        "path": "/",
        "sameSite": "strict",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "880983b16f67d9b33a831759530578"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1762122661,
        "hostOnly": False,
        "httpOnly": False,
        "name": "identity",
        "path": "/",
        "sameSite": None,
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImE0YmNkMWZhLTgxZmUtNDk5Ni05MmE3LTcyNWE1YTRhMDU3MiJ9.eyJyb2xlIjoiY3VzdG9tZXIiLCJpc3MiOiJodHRwczovL2F1dGhuLWFwaS5kaWNlLmNvbS9hY2NvdW50L2dyYXBocWwiLCJ0b2tlbl91c2UiOiJpZGVudGl0eSIsImNsaWVudF9pZCI6IjUwdWZvYWc3MzltZ2hqamw3b2U0ZXAzY3N0ZSIsInNjb3BlcyI6WyJkaWNlLWN1c3RvbWVyLXJlY3J1aXRlciIsImRpY2UtdGFsZW50LXNlYXJjaCIsImRpY2UtY29tcGFueS1yZXBvcnRzIl0sInByaW5jaXBhbF9pZCI6IjgxODNkMTNjLTYzNjQtNDIzZi04MGI0LWI4OTFkZDY1ODA2MSIsImVtYWlsX3ZlcmlmaWVkIjoiZmFsc2UiLCJyZWNydWl0ZXJfaWQiOiIwMTE3OTBiMS0xOGI5LTRmNzQtYTkzYS1hYzZiYjNiMzBkYzgiLCJlbWFpbCI6InNuaWtlc2hAdGhpbmtsdXNpdmUuY29tIiwidXNlcl9pZCI6MjA4MTYxOSwiY29tcGFueV9pZCI6MjAzMjY4NSwibmFtZSI6IlNyYU5pa2VzaCIsImZhbWlseV9uYW1lIjoiUmFqYWJveWVuYSIsInNzbyI6ZmFsc2UsImlhdCI6MTc1OTUzMDY2MH0.l6w8lhDCUUiGYFPtYNfH0lGbxJhlMPMxLa0386UbGoqMsxrVKrK9iKMlq4sPwm3oBh7UyokprKS-Y2BFmnQQxO1Ltl29QlOwpYfaE1fhQPOSlmshSoT1TUORtq_JhUgODR3J7cKzytn5W24dj8ZxNg5X9BwzGsRdGY3HQeOXicIltXtuh3tl0sxMLiUW7mBgTfiHtL5JVwIxpWRJSfQaVGhaCVgcTqwvBer7MZb2Pbtw7d0mipW82rsWqwMaWeYRN23gm3FhWQHGyxwMuzp6YlgXYe5c9CaEa3pImjeQZmaGN52uVQNTs_bmeADXiLg93O7lU1w9QC5Uu6EgZCRyOC2cUIJBO5JcPumNADWb9Qznpw-NNYujdy4VTdOLTv1TL_gvvel2JqY685XzYvm-Jn7Mb5XEHghWdC3JQITp32cbMbdEKCPOr2SRm_48e-rgvOS7HGxZEaWNKiEopGN683GlP_SdpFFxU48cbmQ3yoLe3uPaekuuJwpkUMoVvplTkMWrNjOyH8cjAp2sPTJbDKmSpVxo07AkTnPsIh6hOD7yODeWPXWA2_8575Chu4OtKqGELiud0yxViuqDTB4qVr17mlkH1IT_ztArRFUG5JbDW5aANNZ1r_yQjatw_MZO66I9ig_NSjPx2KDH4QReTvNMKyrBHxXGIgylIi1TeCY"
    },
    {
        "domain": ".dice.com",
        "hostOnly": False,
        "httpOnly": True,
        "name": "ESESSIONID",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": True,
        "storeId": None,
        "value": "98F274FCD353691D4663110E16F97270"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1794091022.774778,
        "hostOnly": False,
        "httpOnly": False,
        "name": "__ssid",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "d568c92d8962e060b024d1365ca70b1"
    },
    {
        "domain": ".www.dice.com",
        "hostOnly": False,
        "httpOnly": True,
        "name": "_cfuvid",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": True,
        "storeId": None,
        "value": "gMxJBWvBca8f9uf79mGFOts8wJz1FNNpaXdZhWzv8pE-1759530590818-0.0.1.1-604800000"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1791066579,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_clck",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "1epb5ni%5E2%5Efzu%5E1%5E2102"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1759617975,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_clsk",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "wh0cab%5E1759531575824%5E11%5E0%5Ev.clarity.ms%2Fcollect"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1794091016.32622,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "GA1.1.419312708.1759530578"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1794091047.295193,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_QEM1ZGKRC2",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "GS2.1.s1759530578$o1$g1$t1759531047$j27$l0$h159019570"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1759616978,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gid",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "GA1.2.1888286981.1759530578"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1759617417,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_uetsid",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "726ea800a0a811f09db22de94cb0ab34"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1793227017,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_uetvid",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "726ea7f0a0a811f0a9a12916ad773890"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1762122661,
        "hostOnly": False,
        "httpOnly": False,
        "name": "access",
        "path": "/",
        "sameSite": None,
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImE0YmNkMWZhLTgxZmUtNDk5Ni05MmE3LTcyNWE1YTRhMDU3MiJ9.eyJyb2xlIjoiY3VzdG9tZXIiLCJpc3MiOiJodHRwczovL2F1dGhuLWFwaS5kaWNlLmNvbS9hY2NvdW50L2dyYXBocWwiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJjbGllbnRfaWQiOiI1MHVmb2FnNzM5bWdoamw3b2U0ZXAzY3N0ZSIsInNjb3BlcyI6WyJkaWNlLWN1c3RvbWVyLXJlY3J1aXRlciIsImRpY2UtdGFsZW50LXNlYXJjaCIsImRpY2UtY29tcGFueS1yZXBvcnRzIl0sInByaW5jaXBhbF9pZCI6IjgxODNkMTNjLTYzNjQtNDIzZi04MGI0LWI4OTFkZDY1ODA2MSIsImxlZ2FjeV90b2tlbiI6IjhkNWU2YWM3LTQyM2MtNTgzZi1iYjE4LTljZWEwYmY1NTNmNiIsImxlZ2FjeV9yZWZyZXNoIjoiZDZjOGQ2YmYtODJmNy01MWI2LWFiM2YtMDZiMzFjMjdlYTdiIiwiaW5hY3Rpdml0eV9leHAiOjE3NTk1NzM4NjAsInVzZXJfaWQiOjIwODE2MTksImNvbXBhbnlfaWQiOjIwMzI2ODUsImlhdCI6MTc1OTUzMDY2MCwiZXhwIjoxNzU5NTM2MDYwfQ.aih_LomgWqjI_vbefxizgHlDC6mbMoKiI-dds-OSO9TfqUvnI2E4wdAQSocwNVVCLoYZlo3FeNR--D3jMqMzWk8kHIbBwgKdoEs16QGEgqEpwX6gyt6Hr94J8b6rIzD4WH_-MStTcMtxEYnehpuBp_RKdBnJ2z5uvkW55CqpeQdlleklkJkESwWpNe-Lg6ZsE4Pq69qrfMB-Q37zPW0L0U_wy_RLKxA9UV5qP0B4FHDg4Up1V_-NdnRPECRkxEofhs2QvJFX8SoqpoUSvMWLpHGOeIfWEY_sX8zuxLM_Gd7TqSD-Ra11-BD1GPmvdYQK7BtwteQ4rxWI3CcRfQPoB9DREhPxDvWQzjDBzW9dAYJK7Sy13jZ7lB-iFda7dwACnGOxhVY4FC6pbaG47_7DL1QCz-kaz6dmncMUqpmDd68ffNbaRCaqm7pzQQ4kygEOSGzqRv3lxjn3FICgmZvj7xI-btidxuWk_bRSDWncojkwprgfuutBz50_VI1Lk82x39q8dZZ0zbCM0x4hHDz-ykU3wmd-G30z3u-OK7NCVNgWdilfr6zJJtlIln6QN2VxwI2OMNCWiPchJ8uI3nC-Rj_3i4jD9410DZmNmGmCoMzauaLh-sG6ETjpGI8ndBBJp4XMHqT8BGtQaOTKRRslWA7QCVgk7C4bg8hxjxWzEVs"
    },
    {
        "domain": ".dice.com",
        "hostOnly": False,
        "httpOnly": True,
        "name": "AWSELB",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": True,
        "storeId": None,
        "value": "7B0D6917189421B24041D595319EE45482B1339EADCD311BA02BB2D0972C91D25CF5C0AA84C410699BB61962C21D60E1E474A88EF8A6CAB23C0FE6AF0ACB0287ED654F9125D97A7A9E2C306CC03181284D2E8AEB06"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1794090669.178717,
        "hostOnly": False,
        "httpOnly": False,
        "name": "DHI-EMPLOYER",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "\"eyJjb21wYW55SWQiOjIwMzI2ODUsInJlY3J1aXRlclVVSUQiOiIwMTE3OTBiMS0xOGI5LTRmNzQtYTkzYS1hYzZiYjNiMzBkYzgiLCJpc0VtdWxhdGVkIjpmYWxzZSwiY3VzdG9tZXJJZCI6MjA4MTYxOSwiY3VzdG9tZXJBVG9rZW4iOiI4ZDVlNmFjNy00MjNjLTU4M2YtYmIxOC05Y2VhMGJmNTUzZjYiLCJjdXN0b21lclJUb2tlbiI6ImQ2YzhkNmJmLTgyZjctNTFiNi1hYjNmLTA2YjMxYzI3ZWE3YiJ9\""
    },
    {
        "domain": "www.dice.com",
        "expirationDate": 1794091018.100111,
        "hostOnly": True,
        "httpOnly": False,
        "name": "dice-recruiter-visited-011790b1-18b9-4f74-a93a-ac6bb3b30dc8",
        "path": "/",
        "sameSite": "strict",
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "true"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1759617061,
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLI",
        "path": "/",
        "sameSite": None,
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "1"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1794090662.767331,
        "hostOnly": False,
        "httpOnly": True,
        "name": "DLIC_D2SESS",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "1"
    },
    {
        "domain": ".dice.com",
        "hostOnly": False,
        "httpOnly": True,
        "name": "MERCURYDCSP",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": True,
        "storeId": None,
        "value": "JKkXygTGpd2MbJLBtL2JfgJCTnXpXtfCzxsCtBTdy89Pdggnh1Zk!-1294096399"
    },
    {
        "domain": "www.dice.com",
        "expirationDate": 1759532875.288857,
        "hostOnly": True,
        "httpOnly": True,
        "name": "SERVERID",
        "path": "/",
        "sameSite": "lax",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "20cc4ca7c9b9c245fbe09c63e9472dc6|0a0699b03fe504461f5b8983d4c3ca14"
    },
    {
        "domain": ".dice.com",
        "expirationDate": 1759534262.767061,
        "hostOnly": False,
        "httpOnly": False,
        "name": "srv_id",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "15e261f8038077915c3078019ae767a3"
    }
]

# User agents for anti-detection
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
]

def get_search_parameters():
    """Get search parameters from user input with validation"""
    print("\n" + "=" * 60)
    print("🔍 SEARCH PARAMETERS")
    print("=" * 60)

    # Get Location
    while True:
        location = input("\n📍 Enter location (min 3 characters, e.g., 'McLean, VA, USA'): ").strip()
        if len(location) < 3:
            print("❌ Error: Location must be at least 3 characters long!")
            continue
        break

    # Get Distance
    while True:
        distance_input = input("📏 Enter distance in miles (e.g., '50'): ").strip()
        if not distance_input.isdigit():
            print("❌ Error: Distance must be a numeric value!")
            continue
        distance = int(distance_input)
        if distance <= 0:
            print("❌ Error: Distance must be greater than 0!")
            continue
        break

    # Get Last Active Days
    while True:
        days_input = input("📅 Enter last active days (e.g., '30'): ").strip()
        if not days_input.isdigit():
            print("❌ Error: Days must be a numeric value!")
            continue
        days = int(days_input)
        if days <= 0:
            print("❌ Error: Days must be greater than 0!")
            continue
        break

    print("\n" + "=" * 60)
    print("✅ SEARCH PARAMETERS CONFIRMED")
    print("=" * 60)
    print(f"📍 Location: {location}")
    print(f"📏 Distance: {distance} miles")
    print(f"📅 Last Active: {days} days")
    print("=" * 60 + "\n")

    return location, distance, days

class DiceCompleteScraper:
    def __init__(self, debug_mode=False, max_pages=1):
        self.debug_mode = debug_mode
        self.max_pages = max_pages
        self.all_candidates = []
        self.console_messages = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.debug_folder = f"debug_{self.timestamp}"

        # Create debug folder if in debug mode
        if self.debug_mode:
            os.makedirs(self.debug_folder, exist_ok=True)

    def log(self, message, level="INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def take_screenshot(self, page, name):
        """Take screenshot if debug mode is enabled"""
        if self.debug_mode:
            try:
                # Save in debug folder with descriptive name
                filename = os.path.join(self.debug_folder, f"{name}.png")
                page.screenshot(path=filename, full_page=True)
                self.log(f"📸 Screenshot saved: {filename}")

                # Also save HTML for debugging
                html_filename = os.path.join(self.debug_folder, f"{name}.html")
                html_content = page.content()
                with open(html_filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                self.log(f"📄 HTML saved: {html_filename}")
            except Exception as e:
                self.log(f"⚠️ Could not save screenshot/HTML: {e}")

    def setup_browser(self):
        """Setup browser with anti-detection settings"""
        self.log("🚀 Setting up browser...")

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=not self.debug_mode,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-setuid-sandbox',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )

        self.context = self.browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True
        )

        self.page = self.context.new_page()

        # Setup console logging
        self.page.on("console", lambda msg: self.console_messages.append(f"[{msg.type}] {msg.text}"))
        if self.debug_mode:
            self.page.on("console", lambda msg: print(f"🌐 Browser: [{msg.type}] {msg.text}"))

        # Add cookies
        for cookie in cookies_json:
            try:
                playwright_cookie = {
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'domain': cookie['domain'],
                    'path': cookie['path'],
                    'httpOnly': cookie.get('httpOnly', False),
                    'secure': cookie.get('secure', False),
                    'sameSite': 'None' if cookie.get('sameSite') is None else cookie.get('sameSite')
                }

                if 'expirationDate' in cookie:
                    playwright_cookie['expires'] = cookie['expirationDate']

                self.context.add_cookies([playwright_cookie])
            except Exception as e:
                self.log(f"⚠️ Could not set cookie {cookie['name']}: {e}")

        self.log("✅ Browser setup complete")
        self.take_screenshot(self.page, "browser_setup")

    def apply_search_filters(self):
        """Apply search filters using JavaScript (comprehensive version from dice-filters.py)"""
        self.log("🎯 Applying search filters...")

        filter_js = f'''
(async () => {{
  const BOOLEAN = `{BOOLEAN}`;
  const LOCATION = `{LOCATION}`;
  const DISTANCE_MILES = {DISTANCE_MILES};
  const LAST_ACTIVE_DAYS = {LAST_ACTIVE_DAYS};

  // Track filter state
  const filterState = {{
    keywordApplied: false,
    locationApplied: false,
    distanceApplied: false,
    relocateApplied: false,
    lastActiveApplied: false,
    profileSourceApplied: false,
    contactMethodsCleared: false,
    additionalFiltersCleared: false,
    searchExecuted: false
  }};

  // Helper functions
  const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
  const setVal = (el, v) => {{
    el.value = v;
    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
  }};
  const clickIf = (el) => {{ if (el && !el.disabled) el.click(); }};

  // Helper to open accordion panels
  const ensureOpen = async (toggleSel, panelSel) => {{
    const toggle = document.querySelector(toggleSel);
    const panel = document.querySelector(panelSel);
    if (toggle && panel) {{
      console.log('🔓 Checking panel:', panelSel);
      if (panel.getAttribute('aria-hidden') === 'true') {{
        clickIf(toggle);
        await sleep(150);
        console.log('✅ Panel opened');
      }}
    }}
  }};

  try {{
    console.log('🚀 Starting comprehensive filter application...');

    // Step 0: Clear IntelliSearch
    console.log('🔧 Step 0: Clearing IntelliSearch...');
    const intelli = document.querySelector('#dhi-typeahead-text-area-search-barjob-titlesInput');
    if (intelli) {{
      setVal(intelli, '');
      console.log('✅ IntelliSearch cleared');
    }}

    // Step 1: Set Boolean search
    console.log('🔧 Step 1: Setting keyword search...');
    let kb = document.querySelector('#dhi-typeahead-text-area-keyword') ||
             document.querySelector('input[placeholder*="Keyword or Boolean"]') ||
             document.querySelector('textarea[placeholder*="Keyword or Boolean"]');

    if (!kb) {{
      const alternativeSelectors = [
        'input[placeholder*="keyword" i]',
        'textarea[placeholder*="keyword" i]',
        'input[aria-label*="keyword" i]',
        'textarea[aria-label*="keyword" i]'
      ];
      for (const selector of alternativeSelectors) {{
        kb = document.querySelector(selector);
        if (kb) break;
      }}
    }}

    if (kb) {{
      setVal(kb, '');
      await sleep(100);
      setVal(kb, BOOLEAN);
      await sleep(200);
      filterState.keywordApplied = kb.value.includes('Appian') && kb.value.includes('SAIL');
      console.log('✅ Boolean search applied, verified:', filterState.keywordApplied);
    }} else {{
      console.error('❌ Keyword field not found');
    }}

    // Step 2: Set Location
    console.log('\\n🔧 Step 2: Setting location...');
    const loc = document.querySelector('#google-location-search');
    if (loc) {{
      setVal(loc, '');
      await sleep(100);
      setVal(loc, LOCATION);
      await sleep(300);

      const list = document.getElementById('talent-search-location-search-typeahead-list');
      if (list) {{
        const options = Array.from(list.querySelectorAll('[role="option"], li, a, div'));
        const opt = options.find(x => (x.textContent || '').toLowerCase().includes(LOCATION.toLowerCase()));
        if (opt) {{
          clickIf(opt);
          await sleep(200);
          console.log('✅ Location selected from autocomplete');
        }}
      }}
      filterState.locationApplied = loc.value.includes(LOCATION);
      console.log('✅ Location set, verified:', filterState.locationApplied);
    }}

    // Step 3: Set Distance
    console.log('\\n🔧 Step 3: Setting distance...');
    const distanceInputs = Array.from(document.querySelectorAll('input[type="number"], input[type="text"]'));
    const distanceInput = distanceInputs.find(i => {{
      const ctx = (i.closest('.float-label-container')?.previousElementSibling?.textContent || '') +
                  (i.getAttribute('title') || '') +
                  (i.getAttribute('aria-label') || '') +
                  (i.placeholder || '');
      return /distance|miles/i.test(ctx);
    }});

    if (distanceInput) {{
      setVal(distanceInput, String(DISTANCE_MILES));
      await sleep(100);
      filterState.distanceApplied = distanceInput.value == String(DISTANCE_MILES);
      console.log('✅ Distance set to', DISTANCE_MILES, 'miles, verified:', filterState.distanceApplied);
    }}

    // Step 4: Willing to Relocate
    console.log('\\n🔧 Step 4: Setting willing to relocate...');
    const relocateBtn = document.querySelector('#searchBarWillingToRelocatePopoverToggle');
    if (relocateBtn) {{
      const wasExpanded = relocateBtn.getAttribute('aria-expanded') === 'true';
      if (!wasExpanded) {{
        clickIf(relocateBtn);
        await sleep(300);
      }}

      // UNCHECK "Willing to Relocate Anywhere"
      const relocateAnywhere = document.querySelector('#willingtorelocate-facet-option-willing-to-relocate');
      if (relocateAnywhere && relocateAnywhere.checked) {{
        clickIf(relocateAnywhere);
        await sleep(150);
        console.log('✅ Willing to relocate anywhere unchecked');
      }}

      // CHECK "Willing To Relocate To Included Location(s)"
      const relocateToIncluded = document.querySelector('#willingtorelocate-facet-option-exclude-no-work-area-preference') ||
                                 document.querySelector('[data-cy="exclude-candidates-without-preference-checkbox"]');
      if (relocateToIncluded && !relocateToIncluded.checked) {{
        clickIf(relocateToIncluded);
        await sleep(150);
        console.log('✅ Willing to relocate to included location(s) checked');
      }}

      // CHECK "Include Candidates Living in Location(s) Searched" toggle
      const includeLocals = document.querySelector('.popover-content input[data-cy="exclude-locals-checkbox"]') ||
                           document.querySelector('.popover-content #excludeLocals') ||
                           document.querySelector('.popover-content input[aria-label*="Include Candidates Living"]');
      if (includeLocals && !includeLocals.disabled && !includeLocals.checked) {{
        clickIf(includeLocals);
        await sleep(150);
        console.log('✅ Include candidates living in location(s) searched checked');
      }}

      if (!wasExpanded) {{
        clickIf(relocateBtn);
        await sleep(150);
      }}
      filterState.relocateApplied = relocateToIncluded ? relocateToIncluded.checked : false;
      console.log('✅ Willing to relocate configured, verified:', filterState.relocateApplied);
    }}

    // Step 5: Last Active Days
    console.log('\\n🔧 Step 5: Setting last active days...');
    await ensureOpen('#filter-accordion-date-updated-toggle', '#filter-accordion-date-updated-panel');
    const lastActiveInput = document.querySelector('#filterLastActiveOnBrand');
    if (lastActiveInput) {{
      setVal(lastActiveInput, String(LAST_ACTIVE_DAYS));
      filterState.lastActiveApplied = lastActiveInput.value == String(LAST_ACTIVE_DAYS);
      console.log('✅ Last active days set to', LAST_ACTIVE_DAYS, 'verified:', filterState.lastActiveApplied);
    }}

    // Step 6: Profile Source - Any
    console.log('\\n🔧 Step 6: Setting profile source...');
    const profileAny = document.querySelector('#profilesources-facet-option-0');
    if (profileAny && !profileAny.checked) {{
      profileAny.click();
      await sleep(100);
      console.log('✅ Profile source set to Any');
    }}
    filterState.profileSourceApplied = profileAny ? profileAny.checked : false;

    // Step 7: Uncheck Contact Methods
    console.log('\\n🔧 Step 7: Unchecking contact methods...');
    await ensureOpen('#filter-accordion-contact-methods-toggle', '#filter-accordion-contact-methods-panel');
    const contactPanel = document.querySelector('#filter-accordion-contact-methods-panel');
    if (contactPanel) {{
      const boxes = contactPanel.querySelectorAll('input[type="checkbox"]');
      boxes.forEach((cb, i) => {{
        if (cb.checked || cb.getAttribute('aria-checked') === 'true') {{
          cb.click();
          console.log('✅ Unchecked contact method', i+1);
        }}
      }});
      filterState.contactMethodsCleared = true;
    }}

    // Step 8: Uncheck Additional Filters
    console.log('\\n🔧 Step 8: Unchecking additional filters...');
    await ensureOpen('#filter-accordion-additional-filters-toggle', '#filter-accordion-additional-filters-panel');
    const addlPanel = document.querySelector('#filter-accordion-additional-filters-panel');
    if (addlPanel) {{
      const boxes = addlPanel.querySelectorAll('input[type="checkbox"]');
      boxes.forEach((cb, i) => {{
        if (cb.checked || cb.getAttribute('aria-checked') === 'true') {{
          cb.click();
          console.log('✅ Unchecked additional filter', i+1);
        }}
      }});
      filterState.additionalFiltersCleared = true;
    }}

    // Step 9: Execute Search
    console.log('\\n🔧 Step 9: Executing search...');
    const searchBtn = document.getElementById('searchButton') || document.querySelector('#searchButton');
    if (searchBtn) {{
      const isVisible = searchBtn.offsetParent !== null;
      const isEnabled = !searchBtn.disabled;
      if (isVisible && isEnabled) {{
        filterState.searchExecuted = true;
        searchBtn.click();
        console.log('✅ Search executed successfully');
      }} else {{
        console.log('❌ Search button not clickable');
      }}
    }} else {{
      console.log('❌ Search button not found');
    }}

    // Final verification
    console.log('\\n📊 === FILTER VERIFICATION ===');
    console.log('Filter state:', filterState);
    const successCount = Object.values(filterState).filter(Boolean).length;
    const totalFilters = Object.keys(filterState).length;
    console.log('✅', successCount, '/', totalFilters, 'filters applied successfully');

    return filterState;

  }} catch (error) {{
    console.error('❌ Error in filter application:', error);
    throw error;
  }}
}})();
'''

        try:
            result = self.page.evaluate(filter_js)
            self.log(f"✅ Filters applied successfully")
            self.log(f"📊 Filter verification: {result}")
            self.take_screenshot(self.page, "filters_applied")
            return True

        except Exception as e:
            self.log(f"❌ Error applying filters: {e}")
            self.take_screenshot(self.page, "filter_error")
            return False

    def extract_candidate_data(self):
        """Extract candidate data from current page (comprehensive version from dice_web_scrap.py)"""
        self.log("📊 Extracting candidate data...")

        extract_js = r"""
        () => {
            console.log('🎲 === Dice Scraper Data Extraction ===');
            console.log('🌐 Current URL:', window.location.href);
            console.log('📄 Page Title:', document.title);

            const candidates = [];

            // Debug function to analyze page structure
            const debugPageStructure = () => {
                console.log('🔍 === Page Structure Debug ===');

                // Check for various candidate card selectors
                const selectors = [
                    '[data-cy="profile-name-text"]',
                    '.profile-name-text',
                    '[class*="profile"]',
                    '[class*="candidate"]',
                    '[class*="result"]',
                    'card',
                    '[data-cy*="profile"]',
                    '[data-cy*="candidate"]'
                ];

                selectors.forEach(selector => {
                    const elements = document.querySelectorAll(selector);
                    if (elements.length > 0) {
                        console.log(`✅ Found ${elements.length} elements with selector: ${selector}`);
                    }
                });

                // Look for any links to profiles
                const profileLinks = document.querySelectorAll('a[href*="/employer/talent/profile/"]');
                console.log(`🔗 Found ${profileLinks.length} profile links`);

                return {
                    profileLinks: profileLinks.length
                };
            };

            // Debug page structure first
            const pageDebug = debugPageStructure();

            // Find all candidate cards/profiles with multiple selector strategies
            let candidateCards = [];

            // Strategy 1: Original selector
            candidateCards = Array.from(document.querySelectorAll('[data-cy="profile-name-text"], .profile-name-text'));
            console.log(`🎯 Strategy 1 - Found ${candidateCards.length} candidate name elements`);

            // Strategy 2: Find cards containing profile links
            if (candidateCards.length === 0) {
                const profileLinks = document.querySelectorAll('a[href*="/employer/talent/profile/"]');
                candidateCards = Array.from(profileLinks).map(link => {
                    const card = link.closest('div, card, article, section');
                    return card ? card.querySelector('h1, h2, h3, h4, [class*="name"], [data-cy*="name"]') : link;
                }).filter(el => el);
                console.log(`🎯 Strategy 2 - Found ${candidateCards.length} candidate elements via profile links`);
            }

            // Strategy 3: Find any elements with profile-related classes
            if (candidateCards.length === 0) {
                candidateCards = Array.from(document.querySelectorAll('[class*="profile"], [class*="candidate"], [class*="result"]'))
                    .map(card => card.querySelector('h1, h2, h3, h4, [class*="name"], [data-cy*="name"]'))
                    .filter(el => el);
                console.log(`🎯 Strategy 3 - Found ${candidateCards.length} candidate elements via profile classes`);
            }

            console.log(`🎯 Final candidate elements found: ${candidateCards.length}`);

            candidateCards.forEach((nameElement, index) => {
                try {
                    console.log(`👤 Processing candidate ${index + 1}...`);

                    // Get the candidate card container - search up the DOM tree more aggressively
                    // The nameElement is the h3 with profile-name-text
                    // We need to go up to find the full card that contains all the data
                    let card = null;

                    // Strategy 1: Go up parent chain until we find an element with the data we need
                    let parent = nameElement.parentElement;
                    for (let i = 0; i < 10 && parent; i++) {
                        // Look for an element that has both the name and other data fields
                        if (parent.querySelector('[data-cy="location"]') &&
                            parent.querySelector('[data-cy="pref-prev-job-title"]')) {
                            card = parent;
                            console.log(`✅ Found card via parent search at level ${i}`);
                            break;
                        }
                        parent = parent.parentElement;
                    }

                    // Strategy 2: If not found, try to find by common card class patterns
                    if (!card) {
                        card = nameElement.closest('card, .card, [class*="candidate-card"]');
                    }

                    // Strategy 3: Use document-wide search for the card containing this name
                    if (!card) {
                        console.log(`⚠️ Using fallback: searching whole document`);
                        // Get all cards and find the one containing this name text
                        const allCards = document.querySelectorAll('[class*="card"], article, section');
                        for (const potentialCard of allCards) {
                            if (potentialCard.textContent.includes(nameElement.textContent.trim())) {
                                if (potentialCard.querySelector('[data-cy="location"]')) {
                                    card = potentialCard;
                                    console.log(`✅ Found card via document-wide search`);
                                    break;
                                }
                            }
                        }
                    }

                    // Last resort: use the name element's parent
                    if (!card) {
                        console.log(`⚠️ Could not find card container for candidate ${index + 1}, using parent`);
                        card = nameElement.parentElement?.parentElement || nameElement;
                    }

                    console.log(`📦 Card container: tag=${card.tagName}, id=${card.id || 'none'}, classes=${card.className.substring(0, 80)}`);

                    const candidate = {};

                    // Helper function to find element with multiple selectors
                    const findElement = (selectors) => {
                        for (const selector of selectors) {
                            const element = card.querySelector(selector);
                            if (element && element.textContent.trim()) {
                                return element;
                            }
                        }
                        return null;
                    };

                    // 0. Profile Name - try to get from the nameElement first
                    let candidateName = nameElement.textContent.trim();

                    // If nameElement doesn't have text, search within card
                    if (!candidateName || candidateName.length < 2) {
                        const nameElement_final = card.querySelector('[data-cy="profile-name-text"], .profile-name-text, h1, h2, h3, h4');
                        candidateName = nameElement_final ? nameElement_final.textContent.trim() : '';
                    }

                    candidate['profile-name-text'] = candidateName;

                    if (candidate['profile-name-text']) {
                        console.log(`✅ Candidate ${index + 1} name: ${candidate['profile-name-text']}`);
                    } else {
                        console.log(`⚠️ Candidate ${index + 1}: No name found, skipping`);
                        console.log(`   NameElement text: "${nameElement.textContent.substring(0, 50)}"`);
                        console.log(`   NameElement tag: ${nameElement.tagName}`);
                        return; // Skip if no name found
                    }

                    // 0.1. Profile URL and Viewed Status
                    // Find the profile link - it's usually the parent of the nameElement or nearby
                    let linkElement = null;

                    // Strategy 1: Check if nameElement is inside a link
                    linkElement = nameElement.closest('a[href*="/employer/talent/profile/"]');

                    // Strategy 2: Look for link in the card
                    if (!linkElement) {
                        linkElement = card.querySelector('a[href*="/employer/talent/profile/"]');
                    }

                    if (linkElement) {
                        const href = linkElement.getAttribute('href');
                        candidate['profile-url'] = href.startsWith('http') ? href : `https://www.dice.com${href}`;

                        // Check if profile has been viewed (has 'viewed' class)
                        const hasViewedClass = linkElement.classList.contains('viewed');
                        candidate['profile-viewed'] = hasViewedClass ? 'Yes' : 'No';

                        // Debug: Show all classes on the link
                        const allClasses = Array.from(linkElement.classList).join(', ');
                        console.log(`🔗 Profile URL: ${candidate['profile-url']}`);
                        console.log(`👁️ Link classes: ${allClasses}`);
                        console.log(`👁️ Profile Viewed: ${candidate['profile-viewed']}`);
                    } else {
                        candidate['profile-url'] = '';
                        candidate['profile-viewed'] = 'Unknown';
                        console.log(`⚠️ No profile link found`);
                    }

                    // 1. Preferred Job Title
                    const jobTitleElement = findElement([
                        '[data-cy="pref-prev-job-title"]',
                        '.preferred-position',
                        '[class*="preferred"]',
                        '[class*="position"]',
                        '[class*="title"]'
                    ]);
                    candidate['pref-prev-job-title'] = jobTitleElement ? jobTitleElement.textContent.trim() : '';

                    // 2. Location
                    const locationElement = findElement([
                        '[data-cy="location"]',
                        '.location-name',
                        '[class*="location"]',
                        '[data-cy*="location"]'
                    ]);
                    candidate['location'] = locationElement ? locationElement.textContent.trim() : '';

                    // 3. Work Experience
                    const workExpElement = findElement([
                        '[data-cy="work-exp"]',
                        '.total-work-exp',
                        '[class*="experience"]',
                        '[class*="work"]'
                    ]);
                    candidate['work-exp'] = workExpElement ? workExpElement.textContent.trim() : '';

                    // 4. Work Permit
                    const workPermitElement = findElement([
                        '[data-cy="work-permit"]',
                        '.work-permits',
                        '[class*="permit"]',
                        '[class*="auth"]'
                    ]);
                    candidate['work-permit'] = workPermitElement ? workPermitElement.textContent.trim() : '';

                    // 5. Willing to Relocate
                    const relocateElement = findElement([
                        '[data-cy="willing-to-relocate"]',
                        '.willing-to-relocate',
                        '[class*="relocate"]'
                    ]);
                    candidate['willing-to-relocate'] = relocateElement ? relocateElement.textContent.trim() : '';

                    // 6. Compensation
                    const compensationElement = findElement([
                        '[data-cy="compensation"]',
                        '.salary-info',
                        '[class*="salary"]',
                        '[class*="comp"]'
                    ]);
                    candidate['compensation'] = compensationElement ? compensationElement.textContent.trim() : '';

                    // 7. Desired Work Setting
                    const workSettingElement = findElement([
                        '[data-cy="desired-work-setting"]',
                        '.desired-work-setting',
                        '[class*="remote"]',
                        '[class*="hybrid"]'
                    ]);
                    candidate['desired-work-setting'] = workSettingElement ? workSettingElement.textContent.trim() : '';

                    // 8. Date Updated
                    const dateUpdatedElement = findElement([
                        '[data-cy="date-updated"]',
                        '.last-updated',
                        '[class*="updated"]'
                    ]);
                    candidate['date-updated'] = dateUpdatedElement ? dateUpdatedElement.textContent.trim() : '';

                    // 9. Date Last Active
                    const dateLastActiveElement = findElement([
                        '[data-cy="date-last-active"]',
                        '.last-active-on-brand',
                        '[class*="active"]'
                    ]);
                    candidate['date-last-active'] = dateLastActiveElement ? dateLastActiveElement.textContent.trim() : '';

                    // 10. Likely to Switch
                    const likelyToSwitchElement = findElement([
                        '[data-cy="likely-to-switch-text"]',
                        '.likely-to-switch-text',
                        '[class*="switch"]',
                        '[class*="likely"]'
                    ]);
                    candidate['likely-to-switch'] = likelyToSwitchElement ? likelyToSwitchElement.textContent.trim() : '';

                    // Add metadata
                    candidate['scraped-date'] = new Date().toISOString();
                    candidate['page-number'] = typeof window.currentPageNumber !== 'undefined' ? window.currentPageNumber : 1;

                    // Log what we found for this candidate
                    const filledFields = Object.entries(candidate).filter(([key, value]) => {
                        if (!value) return false;
                        if (typeof value === 'string') return value.trim().length > 0;
                        return true; // Non-string values (like numbers) count as filled
                    }).length;
                    console.log(`📊 Candidate ${index + 1}: ${filledFields}/15 fields filled`);

                    if (filledFields >= 2) { // At least name + one other field
                        candidates.push(candidate);
                        console.log(`✅ Added candidate: ${candidate['profile-name-text']}`);
                    } else {
                        console.log(`⚠️ Candidate ${index + 1} skipped: insufficient data (only ${filledFields} fields)`);
                    }

                } catch (error) {
                    console.error(`❌ Error processing candidate ${index + 1}:`, error);
                }
            });

            console.log(`✅ Successfully extracted ${candidates.length} candidates with complete data`);

            // Log summary of found data
            if (candidates.length > 0) {
                console.log('📋 === Extraction Summary ===');
                candidates.forEach((candidate, i) => {
                    console.log(`Candidate ${i+1}: ${candidate['profile-name-text']} | ${candidate['location']} | ${candidate['pref-prev-job-title']}`);
                });
            }

            return candidates;
        }
        """

        try:
            candidates = self.page.evaluate(extract_js)
            self.log(f"✅ Extracted {len(candidates)} candidates from current page")

            # Show sample of extracted data
            if candidates and len(candidates) > 0:
                self.log(f"📋 Sample candidates:")
                for i, candidate in enumerate(candidates[:3], 1):
                    self.log(f"   {i}. {candidate.get('profile-name-text', 'N/A')} - {candidate.get('location', 'N/A')} - {candidate.get('pref-prev-job-title', 'N/A')}")

            return candidates
        except Exception as e:
            self.log(f"❌ Error extracting data: {e}")
            return []

    def navigate_and_verify(self):
        """Navigate to search page and verify"""
        self.log("🌐 Navigating to Dice talent search...")

        search_url = 'https://www.dice.com/employer/talent/search/'
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                self.log(f"🔄 Navigation attempt {attempt + 1}/{max_attempts}")

                self.page.goto(search_url, wait_until='domcontentloaded', timeout=30000)
                self.page.wait_for_load_state('networkidle', timeout=10000)

                current_url = self.page.url
                page_title = self.page.title()

                self.log(f"📍 URL: {current_url}")
                self.log(f"📄 Title: {page_title}")

                if 'talent/search' in current_url.lower():
                    self.log("✅ Successfully navigated to search page")
                    self.take_screenshot(self.page, "search_page_loaded")

                    # Wait for dynamic content
                    time.sleep(3)
                    return True
                else:
                    self.log("⚠️ Not on search page, retrying...")
                    if attempt < max_attempts - 1:
                        time.sleep(2)
                        continue

            except Exception as e:
                self.log(f"⚠️ Navigation attempt {attempt + 1} failed: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(2)
                    continue

        self.log("❌ Failed to navigate to search page")
        return False

    def scrape_multiple_pages(self):
        """Scrape multiple pages of results"""
        self.log(f"📄 Starting to scrape {self.max_pages} pages...")

        for page_num in range(1, self.max_pages + 1):
            self.log(f"\n📄 Processing page {page_num}/{self.max_pages}")

            # Wait for results to load
            time.sleep(3)

            # Update page number for tracking
            self.page.evaluate("window.currentPageNumber = " + str(page_num))

            # Extract data from current page
            candidates = self.extract_candidate_data()
            self.all_candidates.extend(candidates)

            if candidates:
                self.log(f"✅ Found {len(candidates)} candidates on page {page_num}")

                # Show sample
                for i, candidate in enumerate(candidates[:3], 1):
                    name = candidate.get('profile-name-text', 'N/A')
                    location = candidate.get('location', 'N/A')
                    title = candidate.get('pref-prev-job-title', 'N/A')
                    self.log(f"   {i}. {name} - {location} - {title}")
            else:
                self.log("❌ No candidates found on this page")

            # Take screenshot
            self.take_screenshot(self.page, f"page_{page_num}_results")

            # Navigate to next page if not the last page
            if page_num < self.max_pages:
                try:
                    next_button = self.page.query_selector('button[aria-label*="next"], a[aria-label*="next"], .pagination-next')
                    if next_button:
                        is_disabled = next_button.is_disabled()
                        if not is_disabled:
                            self.log("➡️ Navigating to next page...")
                            next_button.click()
                            self.page.wait_for_load_state('domcontentloaded', timeout=15000)
                            time.sleep(2)
                        else:
                            self.log("🏁 Next page button is disabled, ending scraping")
                            break
                    else:
                        self.log("🏁 No next page button found, ending scraping")
                        break
                except Exception as e:
                    self.log(f"⚠️ Error navigating to next page: {e}")
                    break

    def save_to_excel(self):
        """Save candidate data to Excel file - append to existing or create new"""
        if not self.all_candidates:
            self.log("❌ No candidates to save")
            return None

        # Get search parameters for metadata
        search_params = {
            'Boolean Query': BOOLEAN[:100] + '...' if len(BOOLEAN) > 100 else BOOLEAN,
            'Location': LOCATION,
            'Distance (miles)': DISTANCE_MILES,
            'Last Active (days)': LAST_ACTIVE_DAYS,
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Pages Scraped': self.max_pages,
            'Total Candidates Found': len(self.all_candidates)
        }

        # Define all columns (for internal processing)
        all_columns = [
            'candidate_profile_id',
            'profile-name-text',
            'profile-url',
            'profile-viewed',
            'pref-prev-job-title',
            'location',
            'work-exp',
            'work-permit',
            'willing-to-relocate',
            'compensation',
            'desired-work-setting',
            'date-updated',
            'date-last-active',
            'likely-to-switch',
            'scraped-date',
            'page-number'
        ]

        # Define columns to export (excluding profile-url)
        export_columns = [
            'candidate_profile_id',
            'profile-name-text',
            'profile-viewed',
            'pref-prev-job-title',
            'location',
            'work-exp',
            'work-permit',
            'willing-to-relocate',
            'compensation',
            'desired-work-setting',
            'date-updated',
            'date-last-active',
            'likely-to-switch',
            'scraped-date',
            'page-number'
        ]

        # Create DataFrame for new candidates
        new_df = pd.DataFrame(self.all_candidates)

        # Extract candidate_profile_id from profile-url
        # URL format: https://www.dice.com/employer/talent/profile/PROFILE_ID?searchId=...
        # We only want the UUID before the ?
        def extract_profile_id(url):
            if pd.isna(url) or url == '':
                return ''
            try:
                # Extract the last part of the URL path
                parts = url.rstrip('/').split('/')
                profile_id = parts[-1] if parts else ''
                # Remove query parameters (everything after ?)
                profile_id = profile_id.split('?')[0]
                return profile_id
            except:
                return ''

        new_df['candidate_profile_id'] = new_df['profile-url'].apply(extract_profile_id)

        # Reorder columns according to all_columns (keep profile-url for processing)
        new_df = new_df.reindex(columns=all_columns, fill_value='')

        # Find the most recent existing file
        import glob
        existing_files = glob.glob("dice_candidates_*.xlsx")

        try:
            if existing_files:
                # Sort by modification time, get the most recent
                existing_files.sort(key=os.path.getmtime, reverse=True)
                latest_file = existing_files[0]
                self.log(f"📂 Found existing file: {latest_file}")

                # Read existing data from Candidates sheet
                existing_df = pd.read_excel(latest_file, sheet_name='Candidates', engine='openpyxl')
                self.log(f"📊 Existing records: {len(existing_df)}")

                # Check if profile-url column exists in existing data
                if 'profile-url' not in existing_df.columns:
                    self.log("⚠️  Existing file doesn't have 'profile-url' column")
                    self.log("📝 Creating new file instead of appending...")
                    df = new_df
                    self.log(f"✅ {len(df)} new candidates to save")

                    # Delete the old file before creating new one
                    try:
                        os.remove(latest_file)
                        self.log(f"🗑️  Deleted old file: {latest_file}")
                    except Exception as e:
                        self.log(f"⚠️  Could not delete old file: {e}")
                else:
                    # Ensure existing_df has candidate_profile_id column
                    if 'candidate_profile_id' not in existing_df.columns:
                        self.log("🔧 Adding candidate_profile_id to existing data...")
                        existing_df['candidate_profile_id'] = existing_df['profile-url'].apply(extract_profile_id)
                    else:
                        # Re-extract profile IDs to ensure they don't have ?searchId
                        self.log("🔧 Cleaning candidate_profile_id in existing data...")
                        existing_df['candidate_profile_id'] = existing_df['profile-url'].apply(extract_profile_id)

                    # Get existing profile IDs for duplicate checking
                    existing_profile_ids = set(existing_df['candidate_profile_id'].dropna())
                    existing_profile_ids.discard('')  # Remove empty strings

                    self.log(f"🔍 Checking for duplicates against {len(existing_profile_ids)} existing profiles...")

                    # Filter out duplicates from new data
                    # Check only profile ID (since it's the unique identifier)
                    new_df_filtered = new_df[
                        ~(new_df['candidate_profile_id'].isin(existing_profile_ids))
                    ].copy()

                    duplicates_found = len(new_df) - len(new_df_filtered)
                    if duplicates_found > 0:
                        self.log(f"⚠️  Skipped {duplicates_found} duplicate candidate(s) found in existing data")
                        self.log(f"✅ {len(new_df_filtered)} new unique candidate(s) to add")
                    else:
                        self.log(f"✅ All {len(new_df_filtered)} candidates are new (no duplicates)")

                    if len(new_df_filtered) == 0:
                        self.log("ℹ️  No new candidates to add - all were duplicates")
                        # Still create new file with updated timestamp
                        df = existing_df
                    else:
                        # Append only non-duplicate new data
                        combined_df = pd.concat([existing_df, new_df_filtered], ignore_index=True)
                        self.log(f"➕ Added {len(new_df_filtered)} new records")
                        df = combined_df

                    # Delete the old file before creating new one
                    try:
                        os.remove(latest_file)
                        self.log(f"🗑️  Deleted old file: {latest_file}")
                    except Exception as e:
                        self.log(f"⚠️  Could not delete old file: {e}")

            else:
                self.log(f"📝 No existing files found - creating new file")
                df = new_df
                self.log(f"✅ {len(df)} new candidates to save")

            # Sort by date-updated (most recent first)
            if 'date-updated' in df.columns:
                try:
                    def parse_relative_time(time_str):
                        """Convert relative time strings to days for sorting"""
                        if not time_str or pd.isna(time_str):
                            return 999999  # Put empty values at the end

                        time_str = str(time_str).lower().strip()

                        # Extract number and unit
                        import re
                        match = re.search(r'(\d+)\s*(day|week|month|year)', time_str)
                        if not match:
                            return 999999  # Unknown format goes to end

                        number = int(match.group(1))
                        unit = match.group(2)

                        # Convert to days
                        if unit == 'day':
                            return number
                        elif unit == 'week':
                            return number * 7
                        elif unit == 'month':
                            return number * 30
                        elif unit == 'year':
                            return number * 365

                        return 999999

                    # Create temporary sort column
                    df['_temp_sort_days'] = df['date-updated'].apply(parse_relative_time)
                    df = df.sort_values(by='_temp_sort_days', ascending=True, na_position='last')
                    df = df.drop(columns=['_temp_sort_days'])
                    self.log(f"🔄 Sorted candidates by date-updated (most recent first)")
                except Exception as e:
                    self.log(f"⚠️  Could not sort by date-updated: {e}")

            # Save to timestamped file with multiple sheets
            timestamped_filename = f"dice_candidates_{self.timestamp}.xlsx"

            # Create Excel writer object
            with pd.ExcelWriter(timestamped_filename, engine='openpyxl') as writer:
                # Sheet 1: Candidates Data (First sheet) - Include profile-url for duplicate checking
                df[all_columns].to_excel(writer, sheet_name='Candidates', index=False)

                # Sheet 2: Search Parameters (Second sheet)
                params_df = pd.DataFrame(list(search_params.items()), columns=['Parameter', 'Value'])
                params_df.to_excel(writer, sheet_name='Search Parameters', index=False)

                # Hide the profile-url column (column C - index 2)
                workbook = writer.book
                worksheet = writer.sheets['Candidates']
                # Find profile-url column index
                profile_url_col_idx = all_columns.index('profile-url') + 1  # Excel is 1-indexed
                worksheet.column_dimensions[chr(64 + profile_url_col_idx)].hidden = True

                self.log(f"✅ Data saved to {timestamped_filename}")
                self.log(f"📊 Total records in file: {len(df)}")
                self.log(f"📋 Sheets: 'Candidates', 'Search Parameters'")
                self.log(f"🔒 profile-url column hidden (kept for duplicate checking)")

            # Return the filename for opening later
            saved_filename = timestamped_filename

            # Show sample data
            if existing_files and 'existing_profile_ids' in locals():
                self.log("\n📋 Sample of newly added unique candidates:")
                sample_df = new_df[
                    ~(new_df['candidate_profile_id'].isin(existing_profile_ids))
                ]
                for i, (idx, row) in enumerate(sample_df.head(3).iterrows(), 1):
                    name = row.get('profile-name-text', 'N/A')
                    location = row.get('location', 'N/A')
                    title = row.get('pref-prev-job-title', 'N/A')
                    profile_id = row.get('candidate_profile_id', 'N/A')
                    self.log(f"   {i}. {name} ({profile_id}) - {location} - {title}")
            else:
                self.log("\n📋 Sample of candidates:")
                for i, (idx, row) in enumerate(new_df.head(3).iterrows(), 1):
                    name = row.get('profile-name-text', 'N/A')
                    location = row.get('location', 'N/A')
                    title = row.get('pref-prev-job-title', 'N/A')
                    profile_id = row.get('candidate_profile_id', 'N/A')
                    self.log(f"   {i}. {name} ({profile_id}) - {location} - {title}")

            return saved_filename

        except Exception as e:
            self.log(f"❌ Error saving to Excel: {e}")
            import traceback
            self.log(f"🐛 Debug: {traceback.format_exc()}")

            # Fallback to CSV with same append/delete logic
            self.log("📋 Falling back to CSV format...")

            try:
                # Find existing CSV files
                import glob
                existing_csv_files = glob.glob("dice_candidates_*.csv")

                if existing_csv_files:
                    # Sort by modification time, get the most recent
                    existing_csv_files.sort(key=os.path.getmtime, reverse=True)
                    latest_csv = existing_csv_files[0]
                    self.log(f"📂 Found existing CSV: {latest_csv}")

                    # Read existing CSV data
                    existing_csv_df = pd.read_csv(latest_csv)
                    self.log(f"📊 Existing CSV records: {len(existing_csv_df)}")

                    # Check if profile-url column exists in existing CSV
                    if 'profile-url' not in existing_csv_df.columns:
                        self.log("⚠️  Existing CSV doesn't have 'profile-url' column")
                        self.log("📝 Creating new CSV instead of appending...")
                        csv_df = new_df

                        # Delete old CSV
                        try:
                            os.remove(latest_csv)
                            self.log(f"🗑️  Deleted old CSV: {latest_csv}")
                        except Exception as del_err:
                            self.log(f"⚠️  Could not delete old CSV: {del_err}")
                    else:
                        # Ensure candidate_profile_id exists
                        if 'candidate_profile_id' not in existing_csv_df.columns:
                            existing_csv_df['candidate_profile_id'] = existing_csv_df['profile-url'].apply(extract_profile_id)
                        else:
                            existing_csv_df['candidate_profile_id'] = existing_csv_df['profile-url'].apply(extract_profile_id)

                        # Get existing profile IDs
                        existing_csv_ids = set(existing_csv_df['candidate_profile_id'].dropna())
                        existing_csv_ids.discard('')

                        # Filter duplicates
                        new_csv_filtered = new_df[
                            ~(new_df['candidate_profile_id'].isin(existing_csv_ids))
                        ].copy()

                        duplicates = len(new_df) - len(new_csv_filtered)
                        if duplicates > 0:
                            self.log(f"⚠️  Skipped {duplicates} duplicate(s) in CSV")

                        if len(new_csv_filtered) == 0:
                            self.log("ℹ️  No new candidates for CSV - all duplicates")
                            csv_df = existing_csv_df
                        else:
                            csv_df = pd.concat([existing_csv_df, new_csv_filtered], ignore_index=True)
                            self.log(f"➕ Added {len(new_csv_filtered)} new records to CSV")

                        # Delete old CSV
                        try:
                            os.remove(latest_csv)
                            self.log(f"🗑️  Deleted old CSV: {latest_csv}")
                        except Exception as del_err:
                            self.log(f"⚠️  Could not delete old CSV: {del_err}")
                else:
                    csv_df = new_df
                    self.log("📝 Creating new CSV file")

                # Sort CSV data by date-updated (most recent first)
                if 'date-updated' in csv_df.columns:
                    try:
                        def parse_relative_time(time_str):
                            """Convert relative time strings to days for sorting"""
                            if not time_str or pd.isna(time_str):
                                return 999999  # Put empty values at the end

                            time_str = str(time_str).lower().strip()

                            # Extract number and unit
                            import re
                            match = re.search(r'(\d+)\s*(day|week|month|year)', time_str)
                            if not match:
                                return 999999  # Unknown format goes to end

                            number = int(match.group(1))
                            unit = match.group(2)

                            # Convert to days
                            if unit == 'day':
                                return number
                            elif unit == 'week':
                                return number * 7
                            elif unit == 'month':
                                return number * 30
                            elif unit == 'year':
                                return number * 365

                            return 999999

                        # Create temporary sort column
                        csv_df['_temp_sort_days'] = csv_df['date-updated'].apply(parse_relative_time)
                        csv_df = csv_df.sort_values(by='_temp_sort_days', ascending=True, na_position='last')
                        csv_df = csv_df.drop(columns=['_temp_sort_days'])
                        self.log(f"🔄 Sorted CSV candidates by date-updated (most recent first)")
                    except Exception as e:
                        self.log(f"⚠️  Could not sort CSV by date-updated: {e}")

                # Save new CSV with search parameters as header comments
                csv_filename = f"dice_candidates_{self.timestamp}.csv"

                # Write search parameters as comments at the top
                with open(csv_filename, 'w', encoding='utf-8') as f:
                    f.write("# SEARCH PARAMETERS\n")
                    for key, value in search_params.items():
                        f.write(f"# {key}: {value}\n")
                    f.write("#\n")

                # Append the actual data
                csv_df[export_columns].to_csv(csv_filename, index=False, mode='a')

                self.log(f"✅ Data saved to CSV: {csv_filename}")
                self.log(f"📊 Total CSV records: {len(csv_df)}")
                self.log(f"📋 CSV includes search parameters as header comments")
                self.log(f"🔒 Hidden column: profile-url (kept for duplicate checking)")

                return csv_filename

            except Exception as csv_error:
                self.log(f"❌ Error saving to CSV: {csv_error}")
                self.log(f"🐛 CSV Debug: {traceback.format_exc()}")
                return None

    def run_complete_process(self):
        """Run the complete process from login to data extraction"""
        start_time = time.time()

        self.log("🎲 === Complete Dice Scraper Process ===")
        self.log(f"🔍 Boolean Search: {BOOLEAN[:50]}...")
        self.log(f"📍 Location: {LOCATION}")
        self.log(f"📏 Distance: {DISTANCE_MILES} miles")
        self.log(f"📅 Last Active: {LAST_ACTIVE_DAYS} days")
        self.log(f"📄 Pages to scrape: {self.max_pages}")
        self.log(f"🔍 Debug Mode: {'ON' if self.debug_mode else 'OFF'}")

        try:
            # Step 1: Setup browser and login
            self.setup_browser()

            # Step 2: Navigate to search page
            if not self.navigate_and_verify():
                raise Exception("Failed to navigate to search page")

            # Step 3: Apply search filters
            self.log("\n🎯 Step 1: Applying search filters...")
            if not self.apply_search_filters():
                raise Exception("Failed to apply search filters")

            # Wait for search results
            self.log("⏳ Waiting for search results...")
            time.sleep(5)

            # Step 4: Extract candidate data
            self.log("\n📊 Step 2: Extracting candidate data...")
            self.scrape_multiple_pages()

            # Step 5: Save results
            self.log("\n💾 Step 3: Saving results...")
            saved_file = self.save_to_excel()

            # Final summary
            end_time = time.time()
            duration = end_time - start_time

            self.log(f"\n🎉 === PROCESS COMPLETED SUCCESSFULLY ===")
            self.log(f"⏱️ Total duration: {duration:.2f} seconds")
            self.log(f"👥 Total candidates extracted: {len(self.all_candidates)}")
            self.log(f"📄 Pages processed: {min(self.max_pages, len(set(c.get('page_number', 1) for c in self.all_candidates)))}")

            if self.debug_mode:
                self.log(f"\n📋 Console Messages Summary:")
                error_count = len([msg for msg in self.console_messages if '[error]' in msg.lower()])
                warning_count = len([msg for msg in self.console_messages if '[warning]' in msg.lower()])
                self.log(f"   Errors: {error_count}, Warnings: {warning_count}")
                self.log(f"   📁 Debug files saved in: {self.debug_folder}/")
                self.log(f"   💡 You can delete this folder later: rm -rf {self.debug_folder}")

            return saved_file

        except Exception as e:
            self.log(f"❌ Process failed: {e}")
            self.take_screenshot(self.page, "error_screenshot")
            return None

        finally:
            # Cleanup
            try:
                self.browser.close()
                self.playwright.stop()
                self.log("🧹 Browser cleanup complete")
            except:
                pass

def open_excel_file(filename):
    """Open Excel or CSV file with the default application"""
    if not filename:
        return False

    try:
        import platform
        system = platform.system()

        if system == 'Darwin':  # macOS
            subprocess.run(['open', filename], check=True)
        elif system == 'Windows':
            os.startfile(filename)
        elif system == 'Linux':
            subprocess.run(['xdg-open', filename], check=True)
        else:
            print(f"⚠️  Unable to open file automatically on {system}")
            print(f"📂 File location: {os.path.abspath(filename)}")
            return False

        print(f"📂 Opened file: {filename}")
        return True

    except Exception as e:
        print(f"⚠️  Could not open file automatically: {e}")
        print(f"📂 File location: {os.path.abspath(filename)}")
        return False

def main():
    """Main function with command line arguments"""
    import argparse

    parser = argparse.ArgumentParser(description='Complete Dice Talent Search and Scraping')
    parser.add_argument('--debug', action='store_true', help='Run in visible browser mode for debugging')
    parser.add_argument('--pages', type=int, default=1, help='Number of pages to scrape (default: 1, max: 10)')
    parser.add_argument('--generate-query', action='store_true', help='Generate Boolean query from job_description.txt before scraping')
    parser.add_argument('--force-generate', action='store_true', help='Force regenerate query even if Dice_string.txt exists')

    args = parser.parse_args()

    # Generate query if requested
    if args.generate_query or args.force_generate:
        print("\n🤖 Generating Boolean query from job_description.txt...")
        print("=" * 50)

        if not os.path.exists("job_description.txt"):
            print("❌ Error: job_description.txt not found!")
            print("💡 Create a job_description.txt file with your job requirements")
            return

        try:
            from dice_api import generate_dice_query_with_chatgpt

            # Check if we should regenerate
            if os.path.exists("Dice_string.txt") and not args.force_generate:
                print("⚠️  Dice_string.txt already exists")
                print("💡 Use --force-generate to overwrite")
                response = input("Generate new query? (y/N): ")
                if response.lower() != 'y':
                    print("📋 Using existing Dice_string.txt")
                    # Reload the query
                    global BOOLEAN
                    BOOLEAN = load_boolean_query()
                else:
                    query = generate_dice_query_with_chatgpt("job_description.txt", "Dice_string.txt")
                    if query:
                        print("✅ Query generated successfully!")
                        BOOLEAN = query
                    else:
                        print("❌ Failed to generate query")
                        return
            else:
                query = generate_dice_query_with_chatgpt("job_description.txt", "Dice_string.txt")
                if query:
                    print("✅ Query generated successfully!")
                    BOOLEAN = query
                else:
                    print("❌ Failed to generate query")
                    return

            print("=" * 50)
            print()
        except ImportError:
            print("❌ Error: dice_api.py not found!")
            print("💡 Make sure dice_api.py is in the same directory")
            return
        except Exception as e:
            print(f"❌ Error generating query: {e}")
            print("💡 Check your OpenAI API key in .env file")
            return

    # Check if help was requested (argparse handles -h automatically)
    if len(sys.argv) == 1:
        print("""
🎲 Complete Dice Talent Search and Scraping Script

This script handles the entire process:
1. 🔐 Login with saved cookies
2. 📝 Prompt for search parameters (location, distance, days)
3. 🎯 Apply search filters (Appian + SAIL, custom location, etc.)
4. 📊 Extract candidate data from search results
5. 💾 Save to Excel file with timestamp

Usage:
  python dice_complete.py                    # Headless mode, 1 page
  python dice_complete.py --debug           # Visible browser for debugging
  python dice_complete.py --pages 5        # Scrape 5 pages
  python dice_complete.py --debug --pages 3  # Debug mode, 3 pages

Search Configuration:
• Keywords: Loaded from Dice_string.txt (or default Appian query)
• Location: User input required (min 3 characters)
• Distance: User input required (numeric, in miles)
• Last Active: User input required (numeric, in days)

Output:
• Excel file: dice_candidates_YYYYMMDD_HHMMSS.xlsx
• Screenshots (debug mode): dice_*.png

Data Fields Extracted:
• Name, Title, Location, Experience, Work Permit
• Relocation preference, Compensation, Remote work preference
• Last updated, Last active, Likely to switch
• Profile URL, Scraped date, Page number

Examples:
  python dice_complete.py --debug --pages 3    # Debug mode, scrape 3 pages
  python dice_complete.py --pages 5           # Headless mode, scrape 5 pages
        """)
        return

    # Validate arguments
    max_pages = max(1, min(args.pages, 10))

    print(f"🎲 === Complete Dice Scraper ===")
    print(f"🔍 Debug Mode: {'ON' if args.debug else 'OFF'}")
    print(f"📄 Pages to scrape: {max_pages}")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # Get search parameters from user
    global LOCATION, DISTANCE_MILES, LAST_ACTIVE_DAYS
    LOCATION, DISTANCE_MILES, LAST_ACTIVE_DAYS = get_search_parameters()

    # Create and run scraper
    scraper = DiceCompleteScraper(debug_mode=args.debug, max_pages=max_pages)
    saved_file = scraper.run_complete_process()

    if saved_file:
        print(f"\n🎉 Success! Check the Excel files for candidate data.")
        print(f"📂 Saved file: {saved_file}")

        # Open the file automatically
        print(f"\n📂 Opening file...")
        open_excel_file(saved_file)
    else:
        print(f"\n❌ Process failed. Check the output above for details.")
        print(f"💡 Try running with --debug flag to see what's happening.")

if __name__ == "__main__":
    main()