#!/usr/bin/env python3
"""
Complete Dice Talent Search and Scraping Script
Handles: Login → Filter Application → Data Extraction → Export
"""

import sys
import time
import json
import random
from datetime import datetime
import os
import pandas as pd
from playwright.sync_api import sync_playwright

# ===== Configuration =====
BOOLEAN = '(Appian OR "Appian Developer" OR "Appian Engineer" OR "Appian Architect" OR "Appian BPM" OR "Appian Designer" OR "Appian Consultant") AND (SAIL OR "Appian UI" OR "Appian RPA" OR "Appian Integration" OR "Appian Automation") AND ("Business Process Management" OR BPM) AND (Java OR J2EE OR "JavaScript" OR C#) AND ("low-code" OR "low code" OR "low-code development") AND (workflow OR "process modeling" OR "workflow automation") AND (integration OR API OR "third-party systems") AND (SQL OR "data modeling" OR "data management") AND (AWS OR "Amazon Web Services" OR "Cloud Integration")'
LOCATION = ""                # set interactively
DISTANCE_MILES = None        # set interactively
LAST_ACTIVE_DAYS = 7         # set interactively

# ----- Bounds you asked for -----
MIN_DISTANCE, MAX_DISTANCE = 50, 100
MAX_LAST_ACTIVE_DAYS = 45

# Custom exception for constraint violations
class ConstraintError(Exception):
    pass

# ===== Login cookies (from dice_login.py) =====
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

# User agents
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
]

# ===== Interactive helpers =====
def prompt_int_with_bounds(prompt: str, *, min_val: int = None, max_val: int = None, default: int = None) -> int:
    """Interactive integer prompt that enforces bounds via exceptions."""
    while True:
        try:
            raw = input(f"{prompt}{' [' + str(default) + ']' if default is not None else ''}: ").strip()
            if not raw:
                if default is None:
                    raise ConstraintError("A value is required.")
                val = int(default)
            else:
                val = int(raw)  # raises ValueError for non-integers

            if min_val is not None and val < min_val:
                raise ConstraintError(f"Value must be ≥ {min_val}.")
            if max_val is not None and val > max_val:
                raise ConstraintError(f"Value must be ≤ {max_val}.")

            return val
        except ValueError:
            print("❌ Please enter a whole number (integer). Try again.")
        except ConstraintError as ce:
            print(f"❌ {ce} Try again.")

def prompt_location_or_blank(prompt: str, *, min_len: int = 3, default: str = "") -> str:
    """
    Interactive location prompt where:
      - blank input = nationwide (no location constraint)
      - otherwise must be at least `min_len` characters
    """
    while True:
        raw = input(
            f"\n{prompt}\n"
            "   Examples: 'McLean', 'Virginia', 'San Francisco', 'McLean, VA, USA'\n"
            "   (Press Enter to search nationwide / no location filter)\n"
            f"   Location{(' [' + default + ']') if default else ''}: "
        ).strip()

        # Blank => nationwide (no location constraint)
        if raw == "":
            print("✅ Location left blank → Nationwide search (no location filter).")
            return ""

        # Otherwise enforce min length
        if len(raw) >= min_len:
            print(f"✅ Location set to: {raw}")
            return raw

        print(f"❌ Error: Location must be at least {min_len} characters "
              f"or press Enter for nationwide. You entered: '{raw}' "
              f"({len(raw)} characters)")



class DiceCompleteScraper:
    def __init__(self, debug_mode=False, max_pages=1):
        self.debug_mode = debug_mode
        self.max_pages = max_pages
        self.all_candidates = []
        self.console_messages = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.debug_folder = f"debug_{self.timestamp}"
        if self.debug_mode:
            os.makedirs(self.debug_folder, exist_ok=True)

    def log(self, message, level="INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {level}: {message}")

    def take_screenshot(self, page, name):
        if self.debug_mode:
            try:
                filename = os.path.join(self.debug_folder, f"{name}.png")
                page.screenshot(path=filename, full_page=True)
                self.log(f"📸 Screenshot saved: {filename}")
                html_filename = os.path.join(self.debug_folder, f"{name}.html")
                with open(html_filename, "w", encoding="utf-8") as f:
                    f.write(page.content())
                self.log(f"📄 HTML saved: {html_filename}")
            except Exception as e:
                self.log(f"⚠️ Could not save screenshot/HTML: {e}")

    def setup_browser(self):
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
                self.log(f"⚠️ Could not set cookie {cookie.get('name','?')}: {e}")

        self.log("✅ Browser setup complete")
        self.take_screenshot(self.page, "browser_setup")

    def apply_search_filters(self):
        """Apply search filters using JavaScript (uses DISTANCE_MILES & LAST_ACTIVE_DAYS)."""
        self.log("🎯 Applying search filters...")
        filter_js = f'''
(async () => {{
  const BOOLEAN = `{BOOLEAN}`;
  const LOCATION = `{LOCATION}`;
  const DISTANCE_MILES = {DISTANCE_MILES if DISTANCE_MILES is not None else 'null'};  // <-
  const LAST_ACTIVE_DAYS = {LAST_ACTIVE_DAYS};

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

  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const setVal = (el, v) => {{ el.value = v; el.dispatchEvent(new Event('input', {{bubbles:true}})); el.dispatchEvent(new Event('change', {{bubbles:true}})); }};
  const clickIf = (el) => {{ if (el && !el.disabled) el.click(); }};

  const ensureOpen = async (toggleSel, panelSel) => {{
    const toggle = document.querySelector(toggleSel);
    const panel = document.querySelector(panelSel);
    if (toggle && panel && panel.getAttribute('aria-hidden') === 'true') {{
      clickIf(toggle);
      await sleep(150);
    }}
  }};

  try {{
    // Step 0: Clear IntelliSearch
    const intelli = document.querySelector('#dhi-typeahead-text-area-search-barjob-titlesInput');
    if (intelli) {{ setVal(intelli, ''); }}

    // Step 1: Keyword / Boolean
    let kb = document.querySelector('#dhi-typeahead-text-area-keyword') ||
             document.querySelector('input[placeholder*="Keyword or Boolean"]') ||
             document.querySelector('textarea[placeholder*="Keyword or Boolean"]');
    if (!kb) {{
      for (const sel of ['input[placeholder*="keyword" i]','textarea[placeholder*="keyword" i]','input[aria-label*="keyword" i]','textarea[aria-label*="keyword" i]']) {{
        kb = document.querySelector(sel); if (kb) break;
      }}
    }}
    if (kb) {{
      setVal(kb, '');
      await sleep(80);
      setVal(kb, BOOLEAN);
      await sleep(150);
      filterState.keywordApplied = !!kb.value;
    }}

    // Step 2 + 3: Location (optional) and Distance (only if location provided)
    const loc = document.querySelector('#google-location-search');
    
    if (LOCATION && LOCATION.trim().length > 0) {{
      // Apply location
      if (loc) {{
        setVal(loc, '');
        await sleep(80);
        setVal(loc, LOCATION);
        await sleep(200);
    
        const list = document.getElementById('talent-search-location-search-typeahead-list');
        if (list) {{
          const opt = Array.from(list.querySelectorAll('[role="option"], li, a, div'))
            .find(x => (x.textContent || '').toLowerCase().includes(LOCATION.toLowerCase()));
          if (opt) {{ clickIf(opt); await sleep(120); }}
        }}
        filterState.locationApplied = !!loc.value;
      }}
    
      // Distance ONLY when a location is set, and only if we actually have a number
      if (DISTANCE_MILES !== null) {{
        const distanceInputs = Array.from(document.querySelectorAll('input[type="number"], input[type="text"]'));
        const distanceInput = distanceInputs.find(i => {{
          const ctx = (i.closest('.float-label-container')?.previousElementSibling?.textContent || '')
            + (i.getAttribute('title') || '')
            + (i.getAttribute('aria-label') || '')
            + (i.placeholder || '');
          return /distance|miles/i.test(ctx);
        }});
        if (distanceInput) {{
          setVal(distanceInput, String(DISTANCE_MILES));
          await sleep(80);
          filterState.distanceApplied = (distanceInput.value == String(DISTANCE_MILES));
        }}
      }}
    }} else {{
      // Nationwide: clear any prefilled location & DO NOT apply distance
      if (loc) {{ setVal(loc, ''); await sleep(80); }}
      filterState.locationApplied = false;
      filterState.distanceApplied = false;
      console.log('🌍 Nationwide search: location & distance not applied.');
    }}



    // Step 4: Willing to relocate (optional)
    const relocateBtn = document.querySelector('#searchBarWillingToRelocatePopoverToggle');
    if (relocateBtn) {{
      const wasExpanded = relocateBtn.getAttribute('aria-expanded') === 'true';
      if (!wasExpanded) {{ clickIf(relocateBtn); await sleep(200); }}
      const relocateAnywhere = document.querySelector('#willingtorelocate-facet-option-willing-to-relocate');
      if (relocateAnywhere && !relocateAnywhere.checked) {{ clickIf(relocateAnywhere); await sleep(120); }}
      if (!wasExpanded) {{ clickIf(relocateBtn); await sleep(100); }}
      filterState.relocateApplied = relocateAnywhere ? relocateAnywhere.checked : false;
    }}

    // Step 5: Last active (days)
    await ensureOpen('#filter-accordion-date-updated-toggle', '#filter-accordion-date-updated-panel');
    const lastActiveInput = document.querySelector('#filterLastActiveOnBrand');
    if (lastActiveInput) {{
      setVal(lastActiveInput, String(LAST_ACTIVE_DAYS));
      await sleep(80);
      filterState.lastActiveApplied = lastActiveInput.value == String(LAST_ACTIVE_DAYS);
    }}

    // Step 6: Profile source Any
    const profileAny = document.querySelector('#profilesources-facet-option-0');
    if (profileAny && !profileAny.checked) {{ profileAny.click(); await sleep(80); }}
    filterState.profileSourceApplied = profileAny ? profileAny.checked : false;

    // Step 7: Uncheck contact methods
    await ensureOpen('#filter-accordion-contact-methods-toggle', '#filter-accordion-contact-methods-panel');
    const contactPanel = document.querySelector('#filter-accordion-contact-methods-panel');
    if (contactPanel) {{
      contactPanel.querySelectorAll('input[type="checkbox"]').forEach(cb => {{ if (cb.checked || cb.getAttribute('aria-checked')==='true') cb.click(); }});
      filterState.contactMethodsCleared = true;
    }}

    // Step 8: Uncheck additional filters
    await ensureOpen('#filter-accordion-additional-filters-toggle', '#filter-accordion-additional-filters-panel');
    const addlPanel = document.querySelector('#filter-accordion-additional-filters-panel');
    if (addlPanel) {{
      addlPanel.querySelectorAll('input[type="checkbox"]').forEach(cb => {{ if (cb.checked || cb.getAttribute('aria-checked')==='true') cb.click(); }});
      filterState.additionalFiltersCleared = true;
    }}

    // Step 9: Execute search
    const searchBtn = document.getElementById('searchButton') || document.querySelector('#searchButton');
    if (searchBtn && !searchBtn.disabled && searchBtn.offsetParent !== null) {{ filterState.searchExecuted = true; searchBtn.click(); }}

    return filterState;
  }} catch (e) {{
    console.error('Filter error:', e);
    throw e;
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
        """Extract candidate data from current page (comprehensive)."""
        self.log("📊 Extracting candidate data...")

        extract_js = r"""
        () => {
            console.log('🎲 === Dice Scraper Data Extraction ===');
            console.log('🌐 Current URL:', window.location.href);
            console.log('📄 Page Title:', document.title);

            const candidates = [];

            const debugPageStructure = () => {
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
                const profileLinks = document.querySelectorAll('a[href*="/employer/talent/profile/"]');
                console.log(`🔗 Found ${profileLinks.length} profile links`);
                return { profileLinks: profileLinks.length };
            };

            debugPageStructure();

            // Candidate "cards" to iterate
            let candidateCards = Array.from(document.querySelectorAll('[data-cy="profile-name-text"], .profile-name-text'));
            if (candidateCards.length === 0) {
                const profileLinks = document.querySelectorAll('a[href*="/employer/talent/profile/"]');
                candidateCards = Array.from(profileLinks).map(link => {
                    const card = link.closest('div, card, article, section');
                    return card ? card.querySelector('h1, h2, h3, h4, [class*="name"], [data-cy*="name"]') : link;
                }).filter(Boolean);
            }
            if (candidateCards.length === 0) {
                candidateCards = Array.from(document.querySelectorAll('[class*="profile"], [class*="candidate"], [class*="result"]'))
                    .map(card => card.querySelector('h1, h2, h3, h4, [class*="name"], [data-cy*="name"]'))
                    .filter(Boolean);
            }
            console.log(`🎯 Final candidate elements found: ${candidateCards.length}`);

            candidateCards.forEach((nameElement, index) => {
                try {
                    let card = null;

                    // climb up to find a container with other fields
                    let parent = nameElement.parentElement;
                    for (let i = 0; i < 10 && parent; i++) {
                        if (parent.querySelector('[data-cy="location"]') &&
                            parent.querySelector('[data-cy="pref-prev-job-title"]')) {
                            card = parent;
                            break;
                        }
                        parent = parent.parentElement;
                    }
                    if (!card) { card = nameElement.closest('card, .card, [class*="candidate-card"]'); }

                    if (!card) {
                        const allCards = document.querySelectorAll('[class*="card"], article, section');
                        for (const potentialCard of allCards) {
                            if ((potentialCard.textContent || '').includes((nameElement.textContent || '').trim())) {
                                if (potentialCard.querySelector('[data-cy="location"]')) {
                                    card = potentialCard;
                                    break;
                                }
                            }
                        }
                    }
                    if (!card) { card = nameElement.parentElement?.parentElement || nameElement; }

                    const candidate = {};
                    const findElement = (selectors) => {
                        for (const selector of selectors) {
                            const el = card.querySelector(selector);
                            if (el && (el.textContent || '').trim()) return el;
                        }
                        return null;
                    };

                    // Name
                    let candidateName = (nameElement.textContent || '').trim();
                    if (!candidateName || candidateName.length < 2) {
                        const nameEl = card.querySelector('[data-cy="profile-name-text"], .profile-name-text, h1, h2, h3, h4');
                        candidateName = nameEl ? nameEl.textContent.trim() : '';
                    }
                    candidate['profile-name-text'] = candidateName;
                    if (!candidate['profile-name-text']) return;

                    // Profile URL
                    const linkElement = card.querySelector('a[href*="/employer/talent/profile/"]');
                    if (linkElement) {
                        const href = linkElement.getAttribute('href') || '';
                        candidate['profile-url'] = href.startsWith('http') ? href : (href ? `https://www.dice.com${href}` : '');
                    } else {
                        candidate['profile-url'] = '';
                    }

                    // Preferred Job Title
                    const jobTitleElement = findElement([
                        '[data-cy="pref-prev-job-title"]',
                        '.preferred-position',
                        '[class*="preferred"]',
                        '[class*="position"]',
                        '[class*="title"]'
                    ]);
                    candidate['pref-prev-job-title'] = jobTitleElement ? jobTitleElement.textContent.trim() : '';

                    // Location
                    const locationElement = findElement([
                        '[data-cy="location"]',
                        '.location-name',
                        '[class*="location"]',
                        '[data-cy*="location"]'
                    ]);
                    candidate['location'] = locationElement ? locationElement.textContent.trim() : '';

                    // Work Experience
                    const workExpElement = findElement([
                        '[data-cy="work-exp"]',
                        '.total-work-exp',
                        '[class*="experience"]',
                        '[class*="work"]'
                    ]);
                    candidate['work-exp'] = workExpElement ? workExpElement.textContent.trim() : '';

                    // Work Permit
                    const workPermitElement = findElement([
                        '[data-cy="work-permit"]',
                        '.work-permits',
                        '[class*="permit"]',
                        '[class*="auth"]'
                    ]);
                    candidate['work-permit'] = workPermitElement ? workPermitElement.textContent.trim() : '';

                    // Willing to Relocate
                    const relocateElement = findElement([
                        '[data-cy="willing-to-relocate"]',
                        '.willing-to-relocate',
                        '[class*="relocate"]'
                    ]);
                    candidate['willing-to-relocate'] = relocateElement ? relocateElement.textContent.trim() : '';

                    // Compensation
                    const compensationElement = findElement([
                        '[data-cy="compensation"]',
                        '.salary-info',
                        '[class*="salary"]',
                        '[class*="comp"]'
                    ]);
                    candidate['compensation'] = compensationElement ? compensationElement.textContent.trim() : '';

                    // Desired Work Setting
                    const workSettingElement = findElement([
                        '[data-cy="desired-work-setting"]',
                        '.desired-work-setting',
                        '[class*="remote"]',
                        '[class*="hybrid"]'
                    ]);
                    candidate['desired-work-setting'] = workSettingElement ? workSettingElement.textContent.trim() : '';

                    // Date Updated
                    const dateUpdatedElement = findElement([
                        '[data-cy="date-updated"]',
                        '.last-updated',
                        '[class*="updated"]'
                    ]);
                    candidate['date-updated'] = dateUpdatedElement ? dateUpdatedElement.textContent.trim() : '';

                    // Date Last Active
                    const dateLastActiveElement = findElement([
                        '[data-cy="date-last-active"]',
                        '.last-active-on-brand',
                        '[class*="active"]'
                    ]);
                    candidate['date-last-active'] = dateLastActiveElement ? dateLastActiveElement.textContent.trim() : '';

                    // Likely to Switch
                    const likelyToSwitchElement = findElement([
                        '[data-cy="likely-to-switch-text"]',
                        '.likely-to-switch-text',
                        '[class*="switch"]',
                        '[class*="likely"]'
                    ]);
                    candidate['likely-to-switch'] = likelyToSwitchElement ? likelyToSwitchElement.textContent.trim() : '';

                    // Metadata
                    candidate['scraped-date'] = new Date().toISOString();
                    candidate['page-number'] = typeof window.currentPageNumber !== 'undefined' ? window.currentPageNumber : 1;

                    const filledFields = Object.entries(candidate).filter(([k,v]) => {
                        if (!v) return false;
                        if (typeof v === 'string') return v.trim().length > 0;
                        return true;
                    }).length;

                    if (filledFields >= 2) {
                        candidates.push(candidate);
                    }
                } catch (error) {
                    console.error(`❌ Error processing candidate ${index + 1}:`, error);
                }
            });

            console.log(`✅ Successfully extracted ${candidates.length} candidates with complete data`);
            return candidates;
        }
        """

        try:
            candidates = self.page.evaluate(extract_js)
            self.log(f"✅ Extracted {len(candidates)} candidates from current page")
            for i, c in enumerate(candidates[:3], 1):
                self.log(f"   {i}. {c.get('profile-name-text','N/A')} – {c.get('location','N/A')} – {c.get('pref-prev-job-title','N/A')}")
            return candidates
        except Exception as e:
            self.log(f"❌ Error extracting data: {e}")
            return []

    def navigate_and_verify(self):
        self.log("🌐 Navigating to Dice talent search...")
        search_url = 'https://www.dice.com/employer/talent/search/'
        for attempt in range(3):
            try:
                self.log(f"🔄 Navigation attempt {attempt + 1}/3")
                self.page.goto(search_url, wait_until='domcontentloaded', timeout=30000)
                self.page.wait_for_load_state('networkidle', timeout=10000)
                if 'talent/search' in self.page.url.lower():
                    self.log("✅ Successfully navigated to search page")
                    self.take_screenshot(self.page, "search_page_loaded")
                    time.sleep(3)
                    return True
                self.log("⚠️ Not on search page, retrying...")
            except Exception as e:
                self.log(f"⚠️ Navigation attempt {attempt + 1} failed: {e}")
            time.sleep(2)
        self.log("❌ Failed to navigate to search page")
        return False

    def scrape_multiple_pages(self):
        self.log(f"📄 Starting to scrape {self.max_pages} pages...")
        for page_num in range(1, self.max_pages + 1):
            self.log(f"\n📄 Processing page {page_num}/{self.max_pages}")
            time.sleep(3)
            self.page.evaluate("window.currentPageNumber = " + str(page_num))
            candidates = self.extract_candidate_data()
            self.all_candidates.extend(candidates)
            self.take_screenshot(self.page, f"page_{page_num}_results")
            if page_num < self.max_pages:
                try:
                    next_button = self.page.query_selector('button[aria-label*="next"], a[aria-label*="next"], .pagination-next')
                    if next_button and not next_button.is_disabled():
                        self.log("➡️ Navigating to next page...")
                        next_button.click()
                        self.page.wait_for_load_state('domcontentloaded', timeout=15000)
                        time.sleep(2)
                    else:
                        self.log("🏁 No next page available; stopping.")
                        break
                except Exception as e:
                    self.log(f"⚠️ Error navigating to next page: {e}")
                    break

    def save_to_excel(self):
        if not self.all_candidates:
            self.log("❌ No candidates to save")
            return
        columns = [
            'profile-name-text','profile-url','pref-prev-job-title','location','work-exp','work-permit',
            'willing-to-relocate','compensation','desired-work-setting','date-updated','date-last-active',
            'likely-to-switch','scraped-date','page-number'
        ]
        df = pd.DataFrame(self.all_candidates)
        df = df.reindex(columns=columns, fill_value='')
        filename = f"dice_candidates_{self.timestamp}.xlsx"
        try:
            df.to_excel(filename, index=False, engine='openpyxl')
            self.log(f"✅ Data saved to {filename}")
        except Exception as e:
            self.log(f"❌ Error saving to Excel: {e}")
            df.to_csv(filename.replace('.xlsx', '.csv'), index=False)
            self.log(f"✅ Saved CSV fallback.")

    def run_complete_process(self):
        start_time = time.time()
        self.log("🎲 === Complete Dice Scraper Process ===")
        self.log(f"🔍 Boolean Search: {BOOLEAN[:50]}...")
        self.log(f"📍 Location: {LOCATION or 'Nationwide (no filter)'}")

        if LOCATION and DISTANCE_MILES is not None:
            self.log(f"📏 Distance: {DISTANCE_MILES} miles")
        elif LOCATION:
            self.log("📏 Distance: (not provided)")
        else:
            self.log("📏 Distance: (not applied — nationwide)")

        self.log(f"📅 Last Active: {LAST_ACTIVE_DAYS} days")
        self.log(f"📄 Pages to scrape: {self.max_pages}")
        self.log(f"🔍 Debug Mode: {'ON' if self.debug_mode else 'OFF'}")

        try:
            self.setup_browser()
            if not self.navigate_and_verify():
                raise Exception("Failed to navigate to search page")
            self.log("\n🎯 Step 1: Applying search filters...")
            if not self.apply_search_filters():
                raise Exception("Failed to apply search filters")
            self.log("⏳ Waiting for search results...")
            time.sleep(5)
            self.log("\n📊 Step 2: Extracting candidate data...")
            self.scrape_multiple_pages()
            self.log("\n💾 Step 3: Saving results...")
            self.save_to_excel()
            duration = time.time() - start_time
            self.log(f"\n🎉 COMPLETED in {duration:.2f}s. Candidates: {len(self.all_candidates)}")
            return True
        except Exception as e:
            self.log(f"❌ Process failed: {e}")
            try:
                self.take_screenshot(self.page, "error_screenshot")
            except:
                pass
            return False
        finally:
            try:
                self.browser.close()
                self.playwright.stop()
                self.log("🧹 Browser cleanup complete")
            except:
                pass

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Complete Dice Talent Search and Scraping')
    parser.add_argument('--debug', action='store_true', help='Run in visible browser mode for debugging')
    parser.add_argument('--pages', type=int, default=1, help='Number of pages to scrape (default: 1, max: 10)')
    args = parser.parse_args()
    max_pages = max(1, min(args.pages, 10))

    # 🔹 Location (blank = nationwide / no location filter)
    global LOCATION
    LOCATION = prompt_location_or_blank(
        "📍 Enter location (city, state, or full address - min 3 chars, or press Enter for nationwide):",
        min_len=3,
        default=""
    )

    # 🔹 Distance: ONLY prompt if a location was provided
    if LOCATION:
        distance_input = prompt_int_with_bounds(
            f"Enter distance in miles ({MIN_DISTANCE}-{MAX_DISTANCE})",
            min_val=MIN_DISTANCE, max_val=MAX_DISTANCE, default=50
        )
    else:
        distance_input = None  # nationwide → no distance filter

    # 🔹 Last active: always required
    last_active_input = prompt_int_with_bounds(
        f"Enter last-active days (1-{MAX_LAST_ACTIVE_DAYS})",
        min_val=1, max_val=MAX_LAST_ACTIVE_DAYS, default=7
    )

    global DISTANCE_MILES, LAST_ACTIVE_DAYS
    DISTANCE_MILES = distance_input
    LAST_ACTIVE_DAYS = last_active_input

    print("🎲 === Complete Dice Scraper ===")
    if LOCATION:
        print(f"📍 Location: {LOCATION}")
        print(f"📏 Distance: {DISTANCE_MILES} miles")
    else:
        print("📍 Location: Nationwide (no filter)")
    print(f"📅 Last Active: {LAST_ACTIVE_DAYS} days")
    print(f"📄 Pages to scrape: {max_pages}")
    print(f"🔍 Debug Mode: {'ON' if args.debug else 'OFF'}")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    scraper = DiceCompleteScraper(debug_mode=args.debug, max_pages=max_pages)
    success = scraper.run_complete_process()
    if success:
        print("\n🎉 Success! Check the Excel file(s) for candidate data.")
    else:
        print("\n❌ Process failed. Run with --debug to inspect the UI and logs.")

if __name__ == "__main__":
    main()