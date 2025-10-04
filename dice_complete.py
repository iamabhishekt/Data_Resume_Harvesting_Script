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
BOOLEAN = '(Appian OR "Appian Developer" OR "Appian Engineer" OR "Appian Architect" OR "Appian BPM" OR "Appian Designer" OR "Appian Consultant") AND (SAIL OR "Appian UI" OR "Appian RPA" OR "Appian Integration" OR "Appian Automation") AND ("Business Process Management" OR BPM) AND (Java OR J2EE OR "JavaScript" OR C#) AND ("low-code" OR "low code" OR "low-code development") AND (workflow OR "process modeling" OR "workflow automation") AND (integration OR API OR "third-party systems") AND (SQL OR "data modeling" OR "data management") AND (AWS OR "Amazon Web Services" OR "Cloud Integration")'
LOCATION = 'McLean, VA, USA'
DISTANCE_MILES = 50
LAST_ACTIVE_DAYS = 20

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

class DiceCompleteScraper:
    def __init__(self, debug_mode=False, max_pages=1):
        self.debug_mode = debug_mode
        self.max_pages = max_pages
        self.all_candidates = []
        self.console_messages = []

    def log(self, message, level="INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def take_screenshot(self, page, name):
        """Take screenshot if debug mode is enabled"""
        if self.debug_mode:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"dice_{name}_{timestamp}.png"
                page.screenshot(path=filename, full_page=True)
                self.log(f"📸 Screenshot saved: {filename}")
            except Exception as e:
                self.log(f"⚠️ Could not save screenshot: {e}")

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
        """Apply search filters using JavaScript"""
        self.log("🎯 Applying search filters...")

        try:
            # Apply filters step by step with proper JavaScript escaping
            self.log("🔍 Step 1: Clearing IntelliSearch...")
            self.page.evaluate('''
                const intelli = document.querySelector('#dhi-typeahead-text-area-search-barjob-titlesInput');
                if (intelli) {
                    intelli.value = '';
                    intelli.dispatchEvent(new Event('input', { bubbles: true }));
                    intelli.dispatchEvent(new Event('change', { bubbles: true }));
                    console.log('✅ IntelliSearch cleared');
                }
            ''')

            self.log("🔍 Step 2: Setting Boolean search...")
            self.page.evaluate(f'''
                const keywordField = document.querySelector('#dhi-typeahead-text-area-keyword') ||
                                  document.querySelector('input[placeholder*="Keyword or Boolean"], input[placeholder*="keyword" i], textarea[placeholder*="keyword" i]');
                if (keywordField) {{
                    keywordField.value = `{BOOLEAN}`;
                    keywordField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    keywordField.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    console.log('✅ Boolean search applied');
                }} else {{
                    throw new Error('Keyword field not found');
                }}
            ''')

            time.sleep(1)

            self.log("📍 Step 3: Setting location...")
            self.page.evaluate(f'''
                const locationField = document.querySelector('#google-location-search');
                if (locationField) {{
                    locationField.value = '{LOCATION}';
                    locationField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    locationField.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    console.log('✅ Location set');
                }}
            ''')

            time.sleep(1)

            # Handle location autocomplete
            self.log("⏳ Waiting for location autocomplete...")
            self.page.evaluate('''
                const list = document.getElementById('talent-search-location-search-typeahead-list');
                if (list) {
                    const options = Array.from(list.querySelectorAll('[role="option"], li, a, div'));
                    const opt = options.find(x => x.textContent && x.textContent.toLowerCase().includes('mclean'));
                    if (opt) {
                        opt.click();
                        console.log('✅ Location selected from autocomplete');
                    }
                }
            ''')

            time.sleep(1)

            self.log("📏 Step 4: Setting distance...")
            self.page.evaluate('''
                const distanceInputs = Array.from(document.querySelectorAll('input[type="number"], input[type="text"]'));
                const distanceInput = distanceInputs.find(i => {
                    const ctx = (i.closest('.float-label-container')?.previousElementSibling?.textContent || '') +
                               (i.getAttribute('title') || '') +
                               (i.getAttribute('aria-label') || '');
                    return /distance|miles/i.test(ctx);
                });

                if (distanceInput) {
                    distanceInput.value = '50';
                    distanceInput.dispatchEvent(new Event('input', { bubbles: true }));
                    distanceInput.dispatchEvent(new Event('change', { bubbles: true }));
                    console.log('✅ Distance set to 50 miles');
                }
            ''')

            self.log("📅 Step 5: Setting last active days...")
            self.page.evaluate('''
                const lastActiveInput = document.querySelector('#filterLastActiveOnBrand');
                if (lastActiveInput) {
                    lastActiveInput.value = '20';
                    lastActiveInput.dispatchEvent(new Event('input', { bubbles: true }));
                    lastActiveInput.dispatchEvent(new Event('change', { bubbles: true }));
                    console.log('✅ Last active days set to 20');
                }
            ''')

            self.log("🔄 Step 6: Setting willing to relocate...")
            self.page.evaluate('''
                const relocateBtn = document.querySelector('#searchBarWillingToRelocatePopoverToggle');
                if (relocateBtn) {
                    relocateBtn.click();
                    setTimeout(() => {
                        const relocateAnywhere = document.querySelector('#willingtorelocate-facet-option-willing-to-relocate');
                        if (relocateAnywhere && !relocateAnywhere.checked) {
                            relocateAnywhere.click();
                            console.log('✅ Willing to relocate checked');
                        }
                        relocateBtn.click(); // Close popover
                    }, 300);
                    console.log('✅ Willing to relocate set');
                }
            ''')

            time.sleep(1)

            self.log("🔍 Step 7: Executing search...")
            self.page.evaluate('''
                const searchBtn = document.getElementById('searchButton') ||
                                 document.querySelector('button[type="submit"], button');
                if (searchBtn && !searchBtn.disabled) {
                    searchBtn.click();
                    console.log('✅ Search executed');
                } else {
                    throw new Error('Search button not found or disabled');
                }
            ''')
            search_result = True

            self.take_screenshot(self.page, "filters_applied")
            return search_result

        except Exception as e:
            self.log(f"❌ Error applying filters: {e}")
            return False

    def extract_candidate_data(self):
        """Extract candidate data from current page"""
        self.log("📊 Extracting candidate data...")

        extract_js = """
        () => {
            const candidates = [];

            // Strategy 1: Find candidate cards with multiple selectors
            let candidateCards = [];

            const selectors = [
                '[data-cy="profile-name-text"]',
                '.profile-name-text',
                '[class*="profile"]',
                '[class*="candidate"]',
                '[class*="result"]'
            ];

            for (const selector of selectors) {
                const elements = document.querySelectorAll(selector);
                if (elements.length > 0) {
                    candidateCards = Array.from(elements);
                    console.log(`✅ Found ${candidateCards.length} candidates with selector: ${selector}`);
                    break;
                }
            }

            // Strategy 2: Find via profile links
            const profileLinks = document.querySelectorAll('a[href*="/employer/talent/profile/"]');
            if (candidateCards.length === 0) {
                candidateCards = Array.from(profileLinks);
            }

            console.log(`Processing ${profileLinks.length} profile links...`);

            profileLinks.forEach((link, index) => {
                try {
                    const candidate = {};

                    // Get name - simplest approach
                    let nameText = link.textContent.trim();
                    if (!nameText) {
                        // Try child elements
                        const childText = link.innerText || link.querySelector('span, div')?.textContent || '';
                        nameText = childText.trim();
                    }

                    candidate['name'] = nameText;
                    candidate['profile_url'] = link.href.startsWith('http') ? link.href : `https://www.dice.com${link.href}`;

                    if (!candidate['name']) return; // Skip if no name

                    // Extract other fields
                    const findElement = (selectors) => {
                        for (const selector of selectors) {
                            const element = card.querySelector(selector);
                            if (element && element.textContent.trim()) return element;
                        }
                        return null;
                    };

                    candidate['title'] = findElement(['[class*="title"], [class*="position"], [class*="role"]'])?.textContent?.trim() || '';
                    candidate['location'] = findElement(['[class*="location"], .location-name'])?.textContent?.trim() || '';
                    candidate['experience'] = findElement(['[class*="experience"], .total-work-exp'])?.textContent?.trim() || '';
                    candidate['work_permit'] = findElement(['[class*="permit"], .work-permits'])?.textContent?.trim() || '';
                    candidate['relocate'] = findElement(['[class*="relocate"], .willing-to-relocate'])?.textContent?.trim() || '';
                    candidate['compensation'] = findElement(['[class*="salary"], .salary-info'])?.textContent?.trim() || '';
                    candidate['remote'] = findElement(['[class*="remote"], [class*="hybrid"]'])?.textContent?.trim() || '';
                    candidate['updated'] = findElement(['[class*="updated"], .last-updated'])?.textContent?.trim() || '';
                    candidate['last_active'] = findElement(['[class*="active"], .last-active-on-brand'])?.textContent?.trim() || '';
                    candidate['likely_switch'] = findElement(['[class*="switch"], [class*="likely"]'])?.textContent?.trim() || '';

                    // Get profile URL
                    const linkElement = card.querySelector('a[href*="/employer/talent/profile/"]');
                    if (linkElement) {
                        const href = linkElement.getAttribute('href');
                        candidate['profile_url'] = href.startsWith('http') ? href : `https://www.dice.com${href}`;
                    } else {
                        candidate['profile_url'] = '';
                    }

                    // Add metadata
                    candidate['scraped_date'] = new Date().toISOString();
                    candidate['page_number'] = typeof window.currentPageNumber !== 'undefined' ? window.currentPageNumber : 1;

                    const filledFields = Object.entries(candidate).filter(([key, value]) => value && value.trim()).length;
                    if (filledFields > 0) { // At least name (less restrictive for testing)
                        candidates.push(candidate);
                        console.log(`✅ Added candidate: ${candidate['name']} (filled fields: ${filledFields})`);
                    } else {
                        console.log(`⚠️ Skipping candidate - no data extracted`);
                    }

                } catch (error) {
                    console.error(`Error processing candidate ${index + 1}:`, error);
                }
            });

            console.log(`✅ Successfully extracted ${candidates.length} candidates`);
            return candidates;
        }
        """

        try:
            candidates = self.page.evaluate(extract_js)
            self.log(f"✅ Extracted {len(candidates)} candidates from current page")
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
                    self.log(f"   {i}. {candidate['name']} - {candidate['location']} - {candidate['title']}")
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
        """Save candidate data to Excel file"""
        if not self.all_candidates:
            self.log("❌ No candidates to save")
            return

        # Define columns and order
        columns = [
            'name', 'title', 'location', 'experience', 'work_permit', 'relocate',
            'compensation', 'remote', 'updated', 'last_active', 'likely_switch',
            'profile_url', 'scraped_date', 'page_number'
        ]

        # Create DataFrame
        df = pd.DataFrame(self.all_candidates)

        # Reorder columns
        df = df.reindex(columns=columns, fill_value='')

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dice_candidates_{timestamp}.xlsx"

        try:
            df.to_excel(filename, index=False, engine='openpyxl')
            self.log(f"✅ Data saved to {filename}")
            self.log(f"📊 Total records: {len(df)}")

            # Show sample data
            self.log("\n📋 Sample data:")
            for i, row in df.head(3).iterrows():
                self.log(f"   {i+1}. {row['name']} - {row['location']} - {row['title']}")

        except Exception as e:
            self.log(f"❌ Error saving to Excel: {e}")
            # Fallback to CSV
            csv_filename = filename.replace('.xlsx', '.csv')
            df.to_csv(csv_filename, index=False)
            self.log(f"✅ Data saved to CSV instead: {csv_filename}")

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
            self.save_to_excel()

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
                self.log(f"   📸 Screenshots saved in current directory")

            return True

        except Exception as e:
            self.log(f"❌ Process failed: {e}")
            self.take_screenshot(self.page, "error_screenshot")
            return False

        finally:
            # Cleanup
            try:
                self.browser.close()
                self.playwright.stop()
                self.log("🧹 Browser cleanup complete")
            except:
                pass

def main():
    """Main function with command line arguments"""
    import argparse

    parser = argparse.ArgumentParser(description='Complete Dice Talent Search and Scraping')
    parser.add_argument('--debug', action='store_true', help='Run in visible browser mode for debugging')
    parser.add_argument('--pages', type=int, default=1, help='Number of pages to scrape (default: 1, max: 10)')

    args = parser.parse_args()

    # Check if help was requested (argparse handles -h automatically)
    if len(sys.argv) == 1:
        print("""
🎲 Complete Dice Talent Search and Scraping Script

This script handles the entire process:
1. 🔐 Login with saved cookies
2. 🎯 Apply search filters (Appian + SAIL, McLean VA, etc.)
3. 📊 Extract candidate data from search results
4. 💾 Save to Excel file with timestamp

Usage:
  python dice_complete.py                    # Headless mode, 1 page
  python dice_complete.py --debug           # Visible browser for debugging
  python dice_complete.py --pages 5        # Scrape 5 pages
  python dice_complete.py --debug --pages 3  # Debug mode, 3 pages

Search Configuration:
• Keywords: Appian OR "Appian Developer" OR "Appian Engineer" (with SAIL, BPM, etc.)
• Location: McLean, VA, USA
• Distance: 50 miles
• Last Active: 20 days

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

    # Create and run scraper
    scraper = DiceCompleteScraper(debug_mode=args.debug, max_pages=max_pages)
    success = scraper.run_complete_process()

    if success:
        print(f"\n🎉 Success! Check the Excel files for candidate data.")
    else:
        print(f"\n❌ Process failed. Check the output above for details.")
        print(f"💡 Try running with --debug flag to see what's happening.")

if __name__ == "__main__":
    main()