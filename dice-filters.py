import subprocess
import time
import sys
import os
import json
import random
from urllib.parse import urlencode

# ===== config =====
BOOLEAN = '(Appian OR "Appian Developer" OR "Appian Engineer" OR "Appian Architect" OR "Appian BPM" OR "Appian Designer" OR "Appian Consultant") AND (SAIL OR "Appian UI" OR "Appian RPA" OR "Appian Integration" OR "Appian Automation") AND ("Business Process Management" OR BPM) AND (Java OR J2EE OR "JavaScript" OR C#) AND ("low-code" OR "low code" OR "low-code development") AND (workflow OR "process modeling" OR "workflow automation") AND (integration OR API OR "third-party systems") AND (SQL OR "data modeling" OR "data management") AND (AWS OR "Amazon Web Services" OR "Cloud Integration")'
LOCATION = 'McLean, VA, USA'
DISTANCE_MILES = 50
LAST_ACTIVE_DAYS = 20

# Cookies from dice_login.py
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

def generate_javascript_code():
    """Generate the JavaScript code for browser automation with extensive debugging"""
    return f'''
(async () => {{
  // ===== config =====
  const BOOLEAN = '{BOOLEAN}';
  const LOCATION = '{LOCATION}';
  const DISTANCE_MILES = {DISTANCE_MILES};
  const LAST_ACTIVE_DAYS = {LAST_ACTIVE_DAYS};

  console.log('🎲 === Dice Filter Debug Script ===');
  console.log('🔍 Boolean Search:', BOOLEAN);
  console.log('📍 Location:', LOCATION);
  console.log('📏 Distance:', DISTANCE_MILES);
  console.log('📅 Last Active Days:', LAST_ACTIVE_DAYS);
  console.log('🌐 Current URL:', window.location.href);
  console.log('📄 Page Title:', document.title);

  // Global debug state tracking
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

  // ===== utils =====
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));
  const setVal = (el, val) => {{
    console.log('📝 Setting value:', val, 'on element:', el);
    console.log('🔍 Element details:', {{
      id: el.id,
      type: el.type,
      placeholder: el.placeholder,
      ariaLabel: el.ariaLabel,
      currentValue: el.value
    }});
    el.value = val;
    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
    console.log('✅ Value set, new value:', el.value);
  }};
  const clickIf = (el) => {{
    if (el) {{
      console.log('🖱️ Clicking element:', el);
      console.log('🔍 Element details:', {{
        id: el.id,
        class_name: el.className,
        textContent: el.textContent?.trim(),
        disabled: el.disabled
      }});
      el.click();
    }} else {{
      console.log('⚠️ Element not found for clicking');
    }}
  }};
  const ensureOpen = async (toggleSel, panelSel) => {{
    console.log('🔧 Ensuring panel open:', toggleSel, panelSel);
    const toggle = document.querySelector(toggleSel);
    const panel  = document.querySelector(panelSel);
    console.log('📋 Toggle found:', !!toggle, 'Panel found:', !!panel);

    if (toggle && panel) {{
      console.log('🔓 Panel aria-hidden:', panel.getAttribute('aria-hidden'));
      console.log('🔍 Toggle details:', {{
        id: toggle.id,
        class_name: toggle.className,
        ariaExpanded: toggle.getAttribute('aria-expanded')
      }});

      if (panel.getAttribute('aria-hidden') === 'true') {{
        clickIf(toggle);
        await sleep(150);
        console.log('✅ Panel opened, checking state...');
        // Verify panel is actually open
        const isNowOpen = panel.getAttribute('aria-hidden') !== 'true';
        console.log('🔓 Panel successfully opened:', isNowOpen);
        if (!isNowOpen) {{
          console.log('⚠️ Panel failed to open, trying again...');
          clickIf(toggle);
          await sleep(200);
        }}
      }} else {{
        console.log('ℹ️ Panel already open');
      }}
    }} else {{
      console.log('❌ Toggle or panel not found');
      console.log('🔍 Available toggles:', Array.from(document.querySelectorAll('[id*="toggle"], [role="button"]')).map(el => ({{id: el.id, className: el.className}})));
      console.log('🔍 Available panels:', Array.from(document.querySelectorAll('[id*="panel"], [role="region"]')).map(el => ({{id: el.id, className: el.className}})));
    }}
  }};

  // Comprehensive verification function
  const verifyFilterState = () => {{
    console.log('\\n🔍 === VERIFICATION CHECK ===');

    // Verify keyword search
    const keywordField = document.querySelector('#dhi-typeahead-text-area-keyword') ||
                        document.querySelector('input[placeholder*="Keyword or Boolean"], input[placeholder*="keyword" i], textarea[placeholder*="keyword" i], input[aria-label*="keyword" i], textarea[aria-label*="keyword" i]');
    if (keywordField) {{
      const actualValue = keywordField.value;
      const expectedValue = BOOLEAN;
      filterState.keywordApplied = actualValue.includes('Appian') && actualValue.includes('SAIL');
      console.log('🔍 Keyword field verification:', {{
        found: true,
        fieldId: keywordField.id,
        expected: expectedValue.substring(0, 50) + '...',
        actual: actualValue.substring(0, 50) + '...',
        matches: filterState.keywordApplied
      }});
    }} else {{
      console.log('❌ Keyword field not found for verification');
    }}

    // Verify location
    const locationField = document.querySelector('#google-location-search');
    if (locationField) {{
      const actualValue = locationField.value;
      filterState.locationApplied = actualValue.includes(LOCATION);
      console.log('📍 Location field verification:', {{
        found: true,
        expected: LOCATION,
        actual: actualValue,
        matches: filterState.locationApplied
      }});
    }} else {{
      console.log('❌ Location field not found for verification');
    }}

    // Verify distance
    const distanceInputs = Array.from(document.querySelectorAll('input[type="number"], input[type="text"]'));
    const distanceInput = distanceInputs.find(i => {{
      const ctx = (i.closest('.float-label-container')?.previousElementSibling?.textContent || '') +
                  (i.getAttribute('title') || '') +
                  (i.getAttribute('aria-label') || '') +
                  (i.placeholder || '');
      return /distance|miles/i.test(ctx);
    }});
    if (distanceInput) {{
      const actualValue = distanceInput.value;
      filterState.distanceApplied = actualValue == DISTANCE_MILES;
      console.log('📏 Distance field verification:', {{
        found: true,
        expected: DISTANCE_MILES,
        actual: actualValue,
        matches: filterState.distanceApplied
      }});
    }} else {{
      console.log('❌ Distance field not found for verification');
    }}

    // Verify last active days
    const lastActiveInput = document.querySelector('#filterLastActiveOnBrand');
    if (lastActiveInput) {{
      const actualValue = lastActiveInput.value;
      filterState.lastActiveApplied = actualValue == LAST_ACTIVE_DAYS;
      console.log('📅 Last active verification:', {{
        found: true,
        expected: LAST_ACTIVE_DAYS,
        actual: actualValue,
        matches: filterState.lastActiveApplied
      }});
    }} else {{
      console.log('❌ Last active input not found for verification');
    }}

    // Verify profile source
    const profileAny = document.querySelector('#profilesources-facet-option-0');
    if (profileAny) {{
      const isChecked = profileAny.checked;
      filterState.profileSourceApplied = isChecked;
      console.log('👤 Profile source verification:', {{
        found: true,
        expected: true,
        actual: isChecked,
        matches: filterState.profileSourceApplied
      }});
    }} else {{
      console.log('❌ Profile source option not found for verification');
    }}

    // Verify willing to relocate
    const relocateAnywhere = document.querySelector('#willingtorelocate-facet-option-willing-to-relocate');
    if (relocateAnywhere) {{
      const isChecked = relocateAnywhere.checked;
      filterState.relocateApplied = isChecked;
      console.log('🔄 Relocate verification:', {{
        found: true,
        expected: true,
        actual: isChecked,
        matches: filterState.relocateApplied
      }});
    }} else {{
      console.log('❌ Relocate option not found for verification');
    }}

    console.log('📊 Filter state summary:', filterState);
    const successCount = Object.values(filterState).filter(Boolean).length;
    const totalFilters = Object.keys(filterState).length;
    console.log('✅ ' + successCount + '/' + totalFilters + ' filters applied successfully');

    return filterState;
  }};

  // Debug function to check page elements
  const debugPage = () => {{
    console.log('🔍 === Page Debug Info ===');
    console.log('🌐 URL:', window.location.href);
    console.log('📄 Title:', document.title);

    // Check for search forms
    const allInputs = document.querySelectorAll('input, textarea, select');
    console.log('📊 Total form elements found:', allInputs.length);

    // Look for keyword/search inputs
    const keywordInputs = document.querySelectorAll('input[placeholder*="keyword" i], input[aria-label*="keyword" i], textarea[placeholder*="keyword" i], textarea[aria-label*="keyword" i]');
    console.log('🔍 Keyword inputs found:', keywordInputs.length);
    keywordInputs.forEach((inp, i) => {{
      console.log('  Keyword input ' + (i+1) + ':', inp.placeholder || inp.ariaLabel || 'no label');
    }});

    // Extended search for ANY input that might be for search terms
    const textInputs = document.querySelectorAll('input[type="text"], input:not([type]), textarea');
    console.log('🔍 Extended search - all text inputs:', textInputs.length);
    textInputs.forEach((inp, i) => {{
      const context = (inp.placeholder || '') + ' ' + (inp.ariaLabel || '') + ' ' + (inp.name || '') + ' ' + (inp.id || '');
      const isSearchRelated = /keyword|search|query|term|boolean/i.test(context);
      if (isSearchRelated || i < 5) {{  // Show first 5 or any search-related ones
        console.log(`  Extended input ${{i+1}}:`, {{
          id: inp.id,
          placeholder: inp.placeholder,
          ariaLabel: inp.ariaLabel,
          name: inp.name,
          className: inp.className,
          isSearchRelated: isSearchRelated
        }});
      }}
    }});

    // Look for location inputs
    const locationInputs = document.querySelectorAll('#google-location-search, input[placeholder*="location" i], input[aria-label*="location" i]');
    console.log('📍 Location inputs found:', locationInputs.length);
    locationInputs.forEach((inp, i) => {{
      console.log('  Location input ' + (i+1) + ':', inp.id || inp.placeholder || inp.ariaLabel || 'no label');
    }});

    // Look for search buttons
    const searchButtons = document.querySelectorAll('button[type="submit"], button');
    console.log('🔍 Search buttons found:', searchButtons.length);
    searchButtons.forEach((btn, i) => {{
      console.log('  Search button ' + (i+1) + ':', btn.textContent.trim() || btn.id || 'no text');
    }});

    // Check for candidate cards
    const candidateCards = document.querySelectorAll('[data-cy="profile-name-text"], .profile-name-text, .candidate-card, [class*="profile"], [class*="candidate"]');
    console.log('👥 Candidate elements found:', candidateCards.length);

    return {{
      inputs: allInputs.length,
      keywordInputs: keywordInputs.length,
      locationInputs: locationInputs.length,
      searchButtons: searchButtons.length,
      candidates: candidateCards.length
    }};
  }};

  try {{
    console.log('🚀 Starting filter application...');
    console.log('⏰ Timestamp:', new Date().toISOString());

    // Debug page before starting
    console.log('🔍 === BEFORE FILTER APPLICATION ===');
    const beforeDebug = debugPage();

    // Additional page analysis
    console.log('🔍 === PAGE STRUCTURE ANALYSIS ===');
    console.log('🌐 Current URL:', window.location.href);
    console.log('📄 Page Title:', document.title);
    console.log('📋 Ready State:', document.readyState);
    console.log('⚡ jQuery Available:', typeof jQuery !== 'undefined');
    console.log('🔧 React Available:', typeof React !== 'undefined');
    console.log('📦 Page HTML length:', document.documentElement.outerHTML.length);

    // Check for specific Dice.com search form structures
    const searchForms = document.querySelectorAll('form');
    console.log('📝 Search forms found:', searchForms.length);
    searchForms.forEach((form, i) => {{
      console.log(`  Form ${{i+1}}:`, {{
        id: form.id,
        class: form.className,
        action: form.action,
        method: form.method
      }});
    }});

    // Check for search containers
    const searchContainers = document.querySelectorAll('[class*="search"], [id*="search"], [class*="filter"], [id*="filter"]');
    console.log('🔍 Search/filter containers found:', searchContainers.length);

    // 0) Clear IntelliSearch "Job Titles" so it won't hijack the query
    console.log('🔧 Step 0: Clearing IntelliSearch Job Titles...');
    const intelli = document.querySelector('#dhi-typeahead-text-area-search-barjob-titlesInput');
    if (intelli) {{
      setVal(intelli, '');
      console.log('✅ IntelliSearch cleared');
    }} else {{
      console.log('ℹ️ IntelliSearch input not found');
    }}

    // 1) Put BOOLEAN into the Keyword or Boolean input
    console.log('🔧 Step 1: Setting keyword search...');
    let kb =
      document.querySelector('#dhi-typeahead-text-area-keyword') ||
      document.querySelector('input[placeholder*="Keyword or Boolean"]') ||
      document.querySelector('textarea[placeholder*="Keyword or Boolean"]') ||
      document.querySelector('input[aria-label*="Keyword or Boolean"]') ||
      document.querySelector('textarea[aria-label*="Keyword or Boolean"]');

    console.log('🔍 Keyword field found (first attempt):', !!kb);

    if (!kb) {{
      console.log('🔍 Trying alternative keyword field selectors...');
      const alternativeSelectors = [
        'input[placeholder*="keyword" i]',
        'textarea[placeholder*="keyword" i]',
        'input[aria-label*="keyword" i]',
        'textarea[aria-label*="keyword" i]',
        'input[type="search"]',
        'textarea[placeholder*="search" i]',
        'input[placeholder*="search" i]'
      ];

      for (const selector of alternativeSelectors) {{
        kb = document.querySelector(selector);
        if (kb) {{
          console.log('✅ Found keyword field with selector:', selector);
          break;
        }}
      }}
    }}

    if (!kb) {{
      console.log('🔍 Trying to find keyword field by label text...');
      const labels = Array.from(document.querySelectorAll('label'));
      console.log('📋 Total labels found:', labels.length);

      for (const label of labels) {{
        if (/keyword\\\\s*or\\\\s*boolean/i.test(label.textContent || '')) {{
          kb = label.parentElement.querySelector('input,textarea');
          console.log('✅ Found keyword field via label:', label.textContent);
          break;
        }}
      }}
    }}

    if (!kb) {{
      console.error('❌ Keyword/Boolean field not found. Available inputs:');
      document.querySelectorAll('input, textarea').forEach((inp, i) => {{
        console.log('  Input ' + (i+1) + ':', {{
          id: inp.id,
          type: inp.type,
          placeholder: inp.placeholder,
          ariaLabel: inp.ariaLabel,
          name: inp.name
        }});
      }});
      return;
    }}

    console.log('✅ Keyword field found, setting value...');
    console.log('🔍 Keyword field details:', {{
      id: kb.id,
      type: kb.type,
      placeholder: kb.placeholder,
      ariaLabel: kb.ariaLabel,
      currentValue: kb.value
    }});

    // Clear field first
    setVal(kb, '');
    await sleep(100);

    // Set the boolean value
    setVal(kb, BOOLEAN);
    await sleep(200);

    // Verify the value was set correctly
    const actualValue = kb.value;
    filterState.keywordApplied = actualValue.includes('Appian') && actualValue.includes('SAIL');
    console.log('🔍 Keyword verification:', {{
      expectedContains: ['Appian', 'SAIL'],
      actualLength: actualValue.length,
      applied: filterState.keywordApplied
    }});
    console.log('✅ Boolean search applied');

    // 2) Location (typeahead)
    console.log('\\n🔧 Step 2: Setting location...');
    const loc = document.querySelector('#google-location-search');
    console.log('📍 Location input found:', !!loc);

    if (loc) {{
      console.log('🔍 Location field details:', {{
        id: loc.id,
        type: loc.type,
        placeholder: loc.placeholder,
        currentValue: loc.value
      }});

      // Clear field first
      setVal(loc, '');
      await sleep(100);

      // Set location value
      setVal(loc, LOCATION);
      console.log('✅ Location value set, waiting for autocomplete...');
      await sleep(300);

      const list = document.getElementById('talent-search-location-search-typeahead-list');
      console.log('📍 Autocomplete list found:', !!list);

      if (list) {{
        const options = Array.from(list.querySelectorAll('[role="option"], li, a, div'));
        console.log('📍 Autocomplete options found:', options.length);
        console.log('📍 Available options:', options.slice(0, 3).map(o => o.textContent?.trim()));

        const opt = options.find(x => (x.textContent || '').toLowerCase().includes(LOCATION.toLowerCase()));
        console.log('📍 Matching option found:', !!opt);

        if (opt) {{
          console.log('📍 Clicking location option:', opt.textContent?.trim());
          clickIf(opt);
          await sleep(200);
          console.log('✅ Location selected from autocomplete');
        }} else {{
          console.log('⚠️ No matching location option found, pressing Enter');
          loc.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', bubbles: true }}));
          await sleep(200);
        }}
      }} else {{
        console.log('⚠️ No autocomplete list found, pressing Enter');
        loc.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', bubbles: true }}));
        await sleep(200);
      }}

      // Verify location was set
      const finalLocationValue = loc.value;
      filterState.locationApplied = finalLocationValue.includes(LOCATION);
      console.log('📍 Location verification:', {{
        expected: LOCATION,
        actual: finalLocationValue,
        applied: filterState.locationApplied
      }});

    }} else {{
      console.log('⚠️ Location input not found');
      console.log('🔍 Available location-related inputs:',
        Array.from(document.querySelectorAll('input[id*="location"], input[placeholder*="location" i]'))
          .map(el => ({{id: el.id, placeholder: el.placeholder}}))
      );
    }}

    // 3) Distance = {DISTANCE_MILES}
    console.log('\\n🔧 Step 3: Setting distance...');
    const distanceInputs = Array.from(document.querySelectorAll('input[type="number"], input[type="text"]'));
    console.log('📏 Distance-related inputs found:', distanceInputs.length);

    // Debug all potential distance inputs
    const potentialDistanceInputs = distanceInputs.map(i => {{
      const ctx =
        (i.closest('.float-label-container')?.previousElementSibling?.textContent || '') + ' ' +
        (i.getAttribute('title') || '') + ' ' +
        (i.getAttribute('aria-label') || '') + ' ' +
        (i.placeholder || '');
      return {{
        element: i,
        id: i.id,
        value: i.value,
        context: ctx.trim(),
        isDistance: /distance|miles/i.test(ctx)
      }};
    }});

    console.log('📏 Potential distance inputs:');
    potentialDistanceInputs.forEach((input, i) => {{
      if (input.isDistance || input.id.toLowerCase().includes('distance')) {{
        console.log('  Distance input ' + (i+1) + ':', {{
          id: input.id,
          context: input.context,
          currentValue: input.value
        }});
      }}
    }});

    const distanceInput = potentialDistanceInputs.find(input => input.isDistance)?.element;

    if (distanceInput) {{
      console.log('📏 Distance input found:', distanceInput.id);
      setVal(distanceInput, String(DISTANCE_MILES));
      await sleep(100);

      // Verify distance was set
      const actualDistance = distanceInput.value;
      filterState.distanceApplied = actualDistance == String(DISTANCE_MILES);
      console.log('📏 Distance verification:', {{
        expected: DISTANCE_MILES,
        actual: actualDistance,
        applied: filterState.distanceApplied
      }});
      console.log('✅ Distance set to', DISTANCE_MILES);
    }} else {{
      console.log('⚠️ Distance input not found');
      console.log('🔍 All number inputs:',
        distanceInputs.slice(0, 5).map(i => ({{id: i.id, value: i.value, placeholder: i.placeholder}}))
      );
    }}

    // 4) Willing to Relocate popover
    console.log('\\n🔧 Step 4: Setting willing to relocate...');
    const relocateBtn = document.querySelector('#searchBarWillingToRelocatePopoverToggle');
    console.log('🔄 Relocate button found:', !!relocateBtn);

    if (relocateBtn) {{
      console.log('🔍 Relocate button details:', {{
        id: relocateBtn.id,
        ariaExpanded: relocateBtn.getAttribute('aria-expanded'),
        disabled: relocateBtn.disabled
      }});

      const wasExpanded = relocateBtn.getAttribute('aria-expanded') === 'true';
      console.log('🔄 Relocate popover was expanded:', wasExpanded);

      if (!wasExpanded) {{
        console.log('🔓 Opening relocate popover...');
        clickIf(relocateBtn);
        await sleep(300);
        console.log('✅ Relocate popover opened');
      }}

      // Look for all relocate options
      const relocateOptions = document.querySelectorAll('[id*="willingtorelocate"], [id*="relocate"]');
      console.log('🔄 Relocate options found:', relocateOptions.length);
      relocateOptions.forEach((opt, i) => {{
        console.log('  Relocate option ' + (i+1) + ':', {{
          id: opt.id,
          type: opt.type,
          checked: opt.checked,
          textContent: opt.textContent?.trim()
        }});
      }});

      const relocateAnywhere = document.querySelector('#willingtorelocate-facet-option-willing-to-relocate');
      console.log('🔄 Relocate anywhere option found:', !!relocateAnywhere);

      if (relocateAnywhere) {{
        console.log('🔍 Relocate option details:', {{
          id: relocateAnywhere.id,
          type: relocateAnywhere.type,
          checked: relocateAnywhere.checked,
          disabled: relocateAnywhere.disabled
        }});

        const wasChecked = relocateAnywhere.checked;
        console.log('🔄 Relocate anywhere was checked:', wasChecked);

        if (!wasChecked) {{
          clickIf(relocateAnywhere);
          await sleep(150);
          console.log('✅ Willing to relocate checked');
        }}

        // Verify the checkbox state
        const isNowChecked = relocateAnywhere.checked;
        filterState.relocateApplied = isNowChecked;
        console.log('🔄 Relocate verification:', {{
          expected: true,
          actual: isNowChecked,
          applied: filterState.relocateApplied
        }});
      }} else {{
        console.log('❌ Relocate anywhere option not found');
      }}

      let includeLocals =
        document.querySelector('.popover-content input[data-cy="exclude-locals-checkbox"]') ||
        document.querySelector('.popover-content #excludeLocals') ||
        document.querySelector('.popover-content input[aria-label*="Include Candidates Living"]');

      console.log('🏠 Include locals checkbox found:', !!includeLocals);

      if (includeLocals && !includeLocals.disabled) {{
        const wasChecked = includeLocals.checked || includeLocals.getAttribute('aria-checked') === 'true';
        console.log('🏠 Include locals was checked:', wasChecked);

        if (!wasChecked) {{
          clickIf(includeLocals);
          await sleep(150);
          console.log('✅ Include locals checked');
        }}
      }} else {{
        console.log('⚠️ Include locals checkbox not found or disabled');
        console.log('🔍 Available checkboxes in popover:',
          Array.from(document.querySelectorAll('.popover-content input[type="checkbox"]'))
            .map(cb => ({{id: cb.id, checked: cb.checked, disabled: cb.disabled}}))
        );
      }}

      if (!wasExpanded) {{
        console.log('🔓 Closing relocate popover...');
        clickIf(relocateBtn);
        await sleep(150);
        console.log('✅ Relocate popover closed');
      }}
    }} else {{
      console.log('⚠️ Relocate button not found');
      console.log('🔍 Available relocate-related elements:',
        Array.from(document.querySelectorAll('[id*="relocate"], [id*="willing"]'))
          .map(el => ({{id: el.id, class_name: el.className}}))
      );
    }}

    // 5) Last Active (panel) -> {LAST_ACTIVE_DAYS}
    console.log('🔧 Step 5: Setting last active days...');
    await ensureOpen('#filter-accordion-date-updated-toggle', '#filter-accordion-date-updated-panel');
    const lastActiveInput = document.querySelector('#filterLastActiveOnBrand');
    console.log('📅 Last active input found:', !!lastActiveInput);

    if (lastActiveInput) {{
      setVal(lastActiveInput, String(LAST_ACTIVE_DAYS));
      console.log('✅ Last active days set to', LAST_ACTIVE_DAYS);
    }} else {{
      console.log('⚠️ Last active input not found');
    }}

    // 6) Profile Source: Any
    console.log('🔧 Step 6: Setting profile source...');
    const profileAny = document.querySelector('#profilesources-facet-option-0');
    console.log('👤 Profile source any option found:', !!profileAny);

    if (profileAny) {{
      const wasChecked = profileAny.checked;
      console.log('👤 Profile source any was checked:', wasChecked);

      if (!wasChecked) {{
        profileAny.click();
        console.log('✅ Profile source set to Any');
      }}
    }} else {{
      console.log('⚠️ Profile source any option not found');
    }}

    // 7) Contact Method -> uncheck ALL
    console.log('🔧 Step 7: Unchecking contact methods...');
    await ensureOpen('#filter-accordion-contact-methods-toggle', '#filter-accordion-contact-methods-panel');
    const contactPanel = document.querySelector('#filter-accordion-contact-methods-panel');
    console.log('📞 Contact panel found:', !!contactPanel);

    if (contactPanel) {{
      const boxes = contactPanel.querySelectorAll('input[type="checkbox"]');
      console.log('📞 Contact method checkboxes found:', boxes.length);

      boxes.forEach((cb, i) => {{
        const wasChecked = cb.checked || cb.getAttribute('aria-checked') === 'true';
        if (wasChecked) {{
          cb.click();
          console.log('✅ Unchecked contact method ' + (i+1));
        }}
      }});
    }} else {{
      console.log('⚠️ Contact panel not found');
    }}

    // 8) Additional Filters -> uncheck ALL
    console.log('🔧 Step 8: Unchecking additional filters...');
    await ensureOpen('#filter-accordion-additional-filters-toggle', '#filter-accordion-additional-filters-panel');
    const addlPanel = document.querySelector('#filter-accordion-additional-filters-panel');
    console.log('🔧 Additional filters panel found:', !!addlPanel);

    if (addlPanel) {{
      const boxes = addlPanel.querySelectorAll('input[type="checkbox"]');
      console.log('🔧 Additional filter checkboxes found:', boxes.length);

      boxes.forEach((cb, i) => {{
        const wasChecked = cb.checked || cb.getAttribute('aria-checked') === 'true';
        if (wasChecked) {{
          cb.click();
          console.log('✅ Unchecked additional filter ' + (i+1));
        }}
      }});
    }} else {{
      console.log('⚠️ Additional filters panel not found');
    }}

    // 9) Click Search (ONCE, at the end)
    console.log('\\n🔧 Step 9: Clicking search button...');
    console.log('🔍 === SEARCH BUTTON ANALYSIS ===');

    const searchBtn = document.getElementById('searchButton') || document.querySelector('#searchButton');
    console.log('🔍 Primary search button found:', !!searchBtn);

    if (searchBtn) {{
      console.log('✅ Primary search button details:', {{
        id: searchBtn.id,
        class: searchBtn.className,
        textContent: searchBtn.textContent?.trim(),
        disabled: searchBtn.disabled,
        type: searchBtn.type
      }});

      // Check if button is clickable
      const isVisible = searchBtn.offsetParent !== null;
      const isEnabled = !searchBtn.disabled;
      console.log('🔍 Button clickable:', {{ visible: isVisible, enabled: isEnabled }});

      if (isVisible && isEnabled) {{
        console.log('✅ Clicking primary search button');
        filterState.searchExecuted = true;
        searchBtn.click();
        console.log('✅ Search button clicked successfully');
      }} else {{
        console.log('❌ Search button not clickable (visible:', isVisible, ', enabled:', isEnabled, ')');
      }}
    }} else {{
      console.log('🔍 Looking for alternative search buttons...');
      const altButtons = Array.from(document.querySelectorAll('button[type="submit"], button'));
      console.log('🔍 Total buttons found:', altButtons.length);

      // List all buttons for debugging
      console.log('🔍 All available buttons:');
      altButtons.forEach((btn, i) => {{
        const text = btn.textContent?.trim();
        const isVisible = btn.offsetParent !== null;
        const isSubmitBtn = btn.type === 'submit' || /search/i.test(text);
        console.log(`  Button ${{i+1}}:`, {{
          text: text,
          id: btn.id,
          class: btn.className,
          type: btn.type,
          visible: isVisible,
          likelySearch: isSubmitBtn
        }});
      }});

      const searchBtn = altButtons.find(b => /^search$/i.test((b.textContent || '').trim()));
      console.log('🔍 Alternative search button found:', !!searchBtn);

      if (searchBtn) {{
        console.log('✅ Found alternative search button:', searchBtn.textContent.trim());
        console.log('🔍 Alternative button details:', {{
          id: searchBtn.id,
          class: searchBtn.className,
          disabled: searchBtn.disabled,
          visible: searchBtn.offsetParent !== null
        }});

        if (!searchBtn.disabled && searchBtn.offsetParent !== null) {{
          filterState.searchExecuted = true;
          clickIf(searchBtn);
        }} else {{
          console.log('❌ Alternative search button not clickable');
        }}
      }} else {{
        console.log('❌ No suitable search button found!');

        // Try to find any button that looks like a search button
        const possibleSearchBtns = altButtons.filter(btn => {{
          const text = btn.textContent?.toLowerCase() || '';
          const id = btn.id?.toLowerCase() || '';
          const className = btn.className?.toLowerCase() || '';
          return /search|find|submit|go/i.test(text + ' ' + id + ' ' + className);
        }});

        if (possibleSearchBtns.length > 0) {{
          console.log('🔍 Possible search buttons found:', possibleSearchBtns.length);
          possibleSearchBtns.forEach((btn, i) => {{
            console.log(`  Possible ${{i+1}}:`, btn.textContent?.trim(), btn.id);
          }});

          // Try the first one
          const firstPossible = possibleSearchBtns[0];
          console.log('🔧 Trying first possible search button...');
          filterState.searchExecuted = true;
          firstPossible.click();
        }} else {{
          console.log('❌ No search button could be identified!');
        }}
      }}
    }}

    // 10) Comprehensive final verification
    console.log('\\n⏳ Waiting for search results...');
    await sleep(3000); // Wait longer for results to load

    console.log('\\n🔍 === COMPREHENSIVE FINAL VERIFICATION ===');
    console.log('🌐 Final URL:', window.location.href);
    console.log('📄 Final Page Title:', document.title);

    // Run comprehensive verification
    const finalFilterState = verifyFilterState();

    // Check for search results
    const finalDebug = debugPage();

    // Additional specific checks for contact methods and additional filters
    console.log('\\n🔍 === Additional Filter Checks ===');
    const emailCheckbox = document.querySelector('#contactinfo-facet-option-contact-method-email');
    const phoneCheckbox = document.querySelector('#contactinfo-facet-option-contact-method-phone');

    if (emailCheckbox) {{
      const emailChecked = emailCheckbox.checked;
      filterState.contactMethodsCleared = !emailChecked; // Should be unchecked
      console.log('📧 Email checkbox:', {{
        found: true,
        checked: emailChecked,
        shouldBeUnchecked: !emailChecked
      }});
    }} else {{
      console.log('📧 Email checkbox not found');
    }}

    if (phoneCheckbox) {{
      const phoneChecked = phoneCheckbox.checked;
      console.log('📞 Phone checkbox:', {{
        found: true,
        checked: phoneChecked,
        shouldBeUnchecked: !phoneChecked
      }});
    }} else {{
      console.log('📞 Phone checkbox not found');
    }}

    // Check additional filters panel
    const excludeRecruiters = document.querySelector('#additionalfilters-facet-option-exclude-recruiters');
    const excludeFounders = document.querySelector('#additionalfilters-facet-option-exclude-founders');

    if (excludeRecruiters) {{
      const isUnchecked = !excludeRecruiters.checked;
      console.log('🚫 Exclude recruiters:', {{
        found: true,
        checked: excludeRecruiters.checked,
        shouldBeUnchecked: isUnchecked
      }});
    }} else {{
      console.log('🚫 Exclude recruiters checkbox not found');
    }}

    if (excludeFounders) {{
      const isUnchecked = !excludeFounders.checked;
      console.log('🚫 Exclude founders:', {{
        found: true,
        checked: excludeFounders.checked,
        shouldBeUnchecked: isUnchecked
      }});
    }} else {{
      console.log('🚫 Exclude founders checkbox not found');
    }}

    // Look for search results indicators
    const resultsCount = document.querySelector('[data-cy="results-count"], .results-count, .search-results-count');
    if (resultsCount) {{
      console.log('\\n📊 Search Results:');
      console.log('✅ Results count found:', resultsCount.textContent);
    }} else {{
      console.log('\\n📊 No results count element found');

      // Try alternative result indicators
      const alternativeResults = document.querySelectorAll('[class*="result"], [class*="candidate"], [class*="profile"]');
      console.log('🔍 Alternative result elements found:', alternativeResults.length);
    }}

    // Look for loading indicators
    const loading = document.querySelector('.loading, .spinner, [data-cy="loading"], .skeleton-loader');
    console.log('⏳ Loading indicator present:', !!loading);

    // Final success summary
    const successCount = Object.values(finalFilterState).filter(Boolean).length;
    const totalFilters = Object.keys(finalFilterState).length;
    const successRate = Math.round((successCount / totalFilters) * 100);

    console.log('\\n🎯 === FINAL SUMMARY ===');
    console.log('✅ ' + successCount + '/' + totalFilters + ' filters applied successfully (' + successRate + '%)');
    console.log('📊 Filter state breakdown:', finalFilterState);

    if (successRate >= 80) {{
      console.log('🎉 Filter application completed successfully!');
    }} else if (successRate >= 60) {{
      console.log('⚠️ Filter application partially successful - some filters may not have applied');
    }} else {{
      console.log('❌ Filter application failed - most filters did not apply correctly');
    }}

    console.log('\\n✅ Filter application script completed');

  }} catch (e) {{
    console.error('❌ Filter script error:', e);
    console.error('❌ Stack trace:', e.stack);
  }}
}})();
'''

def check_browser_available():
    """Check if a browser is available for automation"""
    browsers = ['google-chrome', 'chromium', 'chromium-browser', 'firefox', 'safari']
    for browser in browsers:
        try:
            subprocess.run([browser, '--version'], capture_output=True, check=True)
            return browser
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return None

def run_with_chrome(js_code):
    """Run the script using Google Chrome"""
    try:
        # Create a temporary HTML file with the JavaScript
        html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Dice Filters Automation</title>
</head>
<body>
    <h1>Dice Filters Automation</h1>
    <p>Running automation script...</p>
    <script>
        // Redirect to dice.com talent search and run the script
        window.location.href = "https://www.dice.com/employer/talent/search/";
        setTimeout(() => {{
            {js_code}
        }}, 3000);
    </script>
</body>
</html>
'''

        with open('/tmp/dice_automation.html', 'w') as f:
            f.write(html_content)

        # Run Chrome with the HTML file
        cmd = [
            'google-chrome',
            '--headless',
            '--disable-gpu',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',
            '--window-size=1920,1080',
            'file:///tmp/dice_automation.html'
        ]

        subprocess.run(cmd, check=True)
        print("Chrome automation completed successfully")

    except subprocess.CalledProcessError as e:
        print(f"Chrome automation failed: {e}")
        return False
    except Exception as e:
        print(f"Error running Chrome automation: {e}")
        return False
    return True

def run_with_firefox(js_code):
    """Run the script using Firefox"""
    try:
        # Create a temporary HTML file with the JavaScript
        html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Dice Filters Automation</title>
</head>
<body>
    <h1>Dice Filters Automation</h1>
    <p>Running automation script...</p>
    <script>
        // Redirect to dice.com talent search and run the script
        window.location.href = "https://www.dice.com/employer/talent/search/";
        setTimeout(() => {{
            {js_code}
        }}, 3000);
    </script>
</body>
</html>
'''

        with open('/tmp/dice_automation.html', 'w') as f:
            f.write(html_content)

        # Run Firefox with the HTML file
        cmd = [
            'firefox',
            '--headless',
            'file:///tmp/dice_automation.html'
        ]

        subprocess.run(cmd, check=True)
        print("Firefox automation completed successfully")

    except subprocess.CalledProcessError as e:
        print(f"Firefox automation failed: {e}")
        return False
    except Exception as e:
        print(f"Error running Firefox automation: {e}")
        return False
    return True

def run_with_playwright(headless=True):
    """Try to use Playwright if available - includes login functionality"""
    try:
        from playwright.sync_api import sync_playwright

        js_code = generate_javascript_code()

        with sync_playwright() as p:
            # Launch browser with anti-detection settings
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )

            # Create context with random user agent
            context = browser.new_context(
                user_agent=random.choice(USER_AGENTS),
                viewport={'width': 1920, 'height': 1080},
                ignore_https_errors=True
            )

            page = context.new_page()

            print("🔐 Setting up login cookies...")

            # Set cookies for login
            for cookie in cookies_json:
                try:
                    # Convert cookie format for Playwright
                    playwright_cookie = {
                        'name': cookie['name'],
                        'value': cookie['value'],
                        'domain': cookie['domain'],
                        'path': cookie['path'],
                        'httpOnly': cookie.get('httpOnly', False),
                        'secure': cookie.get('secure', False),
                        'sameSite': cookie.get('sameSite', 'None')
                    }

                    # Convert sameSite values
                    if playwright_cookie['sameSite'] is None:
                        playwright_cookie['sameSite'] = 'None'
                    elif playwright_cookie['sameSite'] == 'no_restriction':
                        playwright_cookie['sameSite'] = 'None'
                    elif playwright_cookie['sameSite'] == 'strict':
                        playwright_cookie['sameSite'] = 'Strict'
                    elif playwright_cookie['sameSite'] == 'lax':
                        playwright_cookie['sameSite'] = 'Lax'

                    # Add expiration date if available
                    if 'expirationDate' in cookie:
                        playwright_cookie['expires'] = cookie['expirationDate']

                    context.add_cookies([playwright_cookie])
                except Exception as e:
                    print(f"Warning: Could not set cookie {cookie['name']}: {e}")

            print("✅ Cookies set successfully")
            print("🌐 Navigating to Dice talent search...")

            # Navigate to talent search page with better timeout handling
            search_url = 'https://www.dice.com/employer/talent/search/'
            max_attempts = 3

            for attempt in range(max_attempts):
                try:
                    print(f"🌐 Navigation attempt {attempt + 1}/{max_attempts}...")

                    # Go directly to search page
                    page.goto(search_url, wait_until='domcontentloaded', timeout=30000)

                    # Wait for page to be ready
                    page.wait_for_load_state('networkidle', timeout=10000)

                    # Verify we're on the correct page
                    current_url = page.url
                    page_title = page.title()

                    print(f"📍 After navigation - URL: {current_url}")
                    print(f"📄 After navigation - Title: {page_title}")

                    # Check if we're actually on the search page
                    if 'talent/search' in current_url.lower() or 'search' in page_title.lower():
                        print("✅ Successfully navigated to search page")

                        # Additional wait for dynamic content
                        time.sleep(3)

                        # Verify search elements are present
                        search_elements = page.query_selector_all('input[type="text"], textarea, button')
                        print(f"🔍 Found {len(search_elements)} interactive elements on search page")

                        if len(search_elements) > 10:  # Should have many elements on search page
                            break
                        else:
                            print("⚠️ Few elements found, may still be loading...")
                            time.sleep(2)
                    else:
                        print(f"⚠️ Navigation may have failed - not on search page")
                        if attempt < max_attempts - 1:
                            print("🔄 Retrying navigation...")
                            time.sleep(2)
                            continue

                except Exception as e:
                    print(f"⚠️ Navigation attempt {attempt + 1} failed: {e}")
                    if attempt < max_attempts - 1:
                        print("🔄 Retrying navigation...")
                        time.sleep(2)
                        continue
                    else:
                        print("❌ All navigation attempts failed")
                        return False

            # Wait for key elements to load
            try:
                page.wait_for_selector('body', timeout=10000)
                print("✅ Page body loaded")
            except:
                print("⚠️ Could not verify page load, continuing...")

            time.sleep(3)  # Additional wait for dynamic content

            # Verify we're on the correct page after navigation
            final_url = page.url
            final_title = page.title()
            print(f"📍 Final verification - URL: {final_url}")
            print(f"📄 Final verification - Title: {final_title}")

            if 'talent/search' not in final_url.lower():
                print("❌ ERROR: Not on the search page after navigation!")
                print("🔍 This indicates a redirect or navigation issue")
                print("📸 Taking screenshot to diagnose the issue...")
                page.screenshot(path='dice_navigation_error.png', full_page=True)
                return False

            print("✅ Successfully on the search page, ready to apply filters")

            print("🔍 Applying search filters...")

            # Capture console logs
            console_messages = []
            def handle_console(msg):
                console_messages.append(f"[{msg.type}] {msg.text}")
                print(f"🌐 Browser Console: [{msg.type}] {msg.text}")

            page.on("console", handle_console)

            # Take initial screenshot
            page.screenshot(path='dice_before_filters.png', full_page=True)
            print("📸 Initial screenshot saved as dice_before_filters.png")

            # Try to execute the JavaScript filter code with error handling
            try:
                print("🔧 Executing JavaScript filter code...")
                result = page.evaluate(js_code)
                print("✅ JavaScript filter code executed successfully")
                print(f"📊 Total console messages captured: {len(console_messages)}")
            except Exception as e:
                print(f"❌ Error executing filter code: {e}")
                print("⚠️ Trying alternative approach...")

                # Take screenshot on error
                page.screenshot(path='dice_filter_error.png', full_page=True)
                print("📸 Error screenshot saved as dice_filter_error.png")

                # Try to wait for page to be more ready
                time.sleep(5)
                try:
                    result = page.evaluate(js_code)
                    print("✅ JavaScript filter code executed successfully on retry")
                except Exception as e2:
                    print(f"❌ Filter execution failed completely: {e2}")
                    print("🔍 Console messages received:")
                    for msg in console_messages[-10:]:  # Show last 10 messages
                        print(f"   {msg}")
                    return False

            time.sleep(5)  # Wait for script to complete

            # Take screenshot for verification
            try:
                page.screenshot(path='dice_search_results.png', full_page=True)
                print("📸 Final screenshot saved as dice_search_results.png")
            except:
                print("Could not save final screenshot")

            # Display console message summary
            print(f"\n🌐 === Browser Console Summary ===")
            if console_messages:
                print(f"📊 Total console messages: {len(console_messages)}")

                # Count message types
                log_count = len([m for m in console_messages if '[log]' in m])
                error_count = len([m for m in console_messages if '[error]' in m])
                warning_count = len([m for m in console_messages if '[warning]' in m])

                print(f"📝 Logs: {log_count}, ⚠️ Warnings: {warning_count}, ❌ Errors: {error_count}")

                # Show all error and warning messages
                if error_count > 0:
                    print("\n❌ Error Messages:")
                    for msg in console_messages:
                        if '[error]' in msg:
                            print(f"   {msg}")

                if warning_count > 0:
                    print("\n⚠️ Warning Messages:")
                    for msg in console_messages:
                        if '[warning]' in msg:
                            print(f"   {msg}")

                # Show key debugging messages (first few and last few)
                print("\n🔍 Key Debug Messages:")
                debug_messages = [m for m in console_messages if '🎲' in m or '🔧' in m or '✅' in m or '❌' in m or '🔍' in m]
                for msg in debug_messages[:5] + debug_messages[-5:]:
                    print(f"   {msg}")
            else:
                print("⚠️ No console messages captured - this might indicate a problem!")

            # Check final URL and page state
            final_url = page.url
            final_title = page.title()
            print(f"\n🌐 Final Page State:")
            print(f"   URL: {final_url}")
            print(f"   Title: {final_title}")

            # Look for key elements on the page
            try:
                keyword_field = page.query_selector('input[placeholder*="Keyword"], input[placeholder*="keyword" i], textarea[placeholder*="keyword" i]')
                location_field = page.query_selector('#google-location-search')
                search_button = page.query_selector('#searchButton, button[type="submit"]')

                print(f"\n🔍 Key Elements Found:")
                print(f"   Keyword field: {'✅' if keyword_field else '❌'}")
                print(f"   Location field: {'✅' if location_field else '❌'}")
                print(f"   Search button: {'✅' if search_button else '❌'}")

                # Check current values
                if keyword_field:
                    keyword_value = keyword_field.get_attribute('value') or ''
                    print(f"   Keyword value: {keyword_value[:100]}...")

                if location_field:
                    location_value = location_field.get_attribute('value') or ''
                    print(f"   Location value: {location_value}")

            except Exception as e:
                print(f"⚠️ Could not verify final page elements: {e}")

            browser.close()

        print("✅ Playwright automation completed successfully")
        return True

    except ImportError:
        print("❌ Playwright not installed. Install with: pip install playwright && playwright install")
        return False
    except Exception as e:
        print(f"❌ Playwright automation failed: {e}")
        return False

def run_with_pyppeteer():
    """Try to use Pyppeteer if available"""
    try:
        import pyppeteer
        import asyncio

        js_code = generate_javascript_code()

        async def run():
            browser = await pyppeteer.launch(headless=True)
            page = await browser.newPage()
            await page.goto('https://www.dice.com/employer/talent/search/')
            await asyncio.sleep(3)  # Wait for page to load
            await page.evaluate(js_code)
            await asyncio.sleep(5)  # Wait for script to complete
            await browser.close()

        asyncio.get_event_loop().run_until_complete(run())
        print("Pyppeteer automation completed successfully")
        return True

    except ImportError:
        print("Pyppeteer not installed. Install with: pip install pyppeteer")
        return False
    except Exception as e:
        print(f"Pyppeteer automation failed: {e}")
        return False

def main():
    """Main function to run the dice filters automation with login"""
    import sys  # Import here to avoid issues with the script structure

    # Check for help flag
    if '--help' in sys.argv or '-h' in sys.argv:
        print("🎲 Dice Talent Search Automation with Enhanced Debug")
        print("\nUsage:")
        print("  python dice-filters.py [options]")
        print("\nOptions:")
        print("  --visible, --debug    Run in visible browser mode for debugging")
        print("  --help, -h           Show this help message")
        print("\nDebug Features:")
        print("  • Comprehensive console logging")
        print("  • Step-by-step filter verification")
        print("  • Screenshots at each major step")
        print("  • Detailed element analysis")
        print("  • Filter success rate reporting")
        print("\nExamples:")
        print("  python dice-filters.py              # Run in headless mode")
        print("  python dice-filters.py --visible     # Run in visible mode for debugging")
        print("  python dice-filters.py --debug       # Same as --visible")
        return

    print("🎲 === Dice Talent Search Automation with Enhanced Debug ===")
    print(f"🔍 Boolean Search: {BOOLEAN[:50]}...")
    print(f"📍 Location: {LOCATION}")
    print(f"📏 Distance: {DISTANCE_MILES} miles")
    print(f"📅 Last Active Days: {LAST_ACTIVE_DAYS}")
    print("🔐 Using saved login cookies from dice_login.py")
    print("🐛 Enhanced debugging enabled - all filter steps will be verified")
    print()

    # Try different automation methods
    js_code = generate_javascript_code()

    # Validate configuration before starting
    print("🔧 Validating configuration...")
    try:
        assert BOOLEAN and len(BOOLEAN) > 10, "Boolean search query appears invalid"
        assert LOCATION and ',' in LOCATION, "Location format appears invalid"
        assert 1 <= DISTANCE_MILES <= 200, "Distance should be between 1-200 miles"
        assert 1 <= LAST_ACTIVE_DAYS <= 365, "Last active days should be between 1-365"
        print("✅ Configuration validation passed")
    except AssertionError as e:
        print(f"❌ Configuration validation failed: {e}")
        print("🔧 Please check the configuration variables at the top of the script")
        return

    # Check if we should run in visible mode for debugging
    visible_mode = '--visible' in sys.argv or '--debug' in sys.argv

    if visible_mode:
        print("🔍 DEBUG MODE: Running in visible browser for debugging")
        print("📝 Browser window will open - please don't close it manually")
        print("🐛 Watch the browser console for real-time debugging information")

    # Method 1: Try Playwright (recommended - includes login)
    mode_text = "visible mode" if visible_mode else "headless mode"
    print(f"\n🚀 Method 1: Trying Playwright ({mode_text})...")
    try:
        if run_with_playwright(headless=not visible_mode):
            print("\n✅ Automation completed successfully!")
            print("📝 Search filters have been applied and search executed.")
            if visible_mode:
                print("🐛 Browser window will remain open for inspection - close it manually when done")
            else:
                print("🐛 Check the console output above for detailed debugging information")
            return
        else:
            print(f"⚠️ Playwright {mode_text} method failed")
    except Exception as e:
        print(f"❌ Playwright {mode_text} method error: {e}")

    # If headless failed, try visible mode for debugging
    if not visible_mode:
        print("\n🔍 Headless mode failed, trying visible mode for debugging...")
        print("📝 Browser window will open - please don't close it manually")
        print("🐛 Watch the browser console for real-time debugging information")
        try:
            if run_with_playwright(headless=False):
                print("\n✅ Automation completed successfully!")
                print("📝 Search filters have been applied and search executed.")
                print("🐛 Browser window will remain open for inspection - close it manually when done")
                return
            else:
                print("⚠️ Playwright visible mode method failed")
        except Exception as e:
            print(f"❌ Playwright visible mode method error: {e}")

    # Method 2: Try Pyppeteer
    print("\n🔄 Method 2: Trying Pyppeteer...")
    try:
        if run_with_pyppeteer():
            return
        else:
            print("⚠️ Pyppeteer method failed")
    except Exception as e:
        print(f"❌ Pyppeteer method error: {e}")

    # Method 3: Try system browsers
    print("\n🌐 Method 3: Trying system browsers...")
    try:
        browser = check_browser_available()
        if browser:
            print(f"🌐 Found browser: {browser}")
            if 'chrome' in browser or 'chromium' in browser:
                if run_with_chrome(js_code):
                    return
                else:
                    print("⚠️ Chrome automation failed")
            elif 'firefox' in browser:
                if run_with_firefox(js_code):
                    return
                else:
                    print("⚠️ Firefox automation failed")
        else:
            print("⚠️ No suitable system browser found")
    except Exception as e:
        print(f"❌ System browser method error: {e}")

    print("\n❌ All automation methods failed. Troubleshooting steps:")
    print("1. 💻 Install Playwright (recommended): pip install playwright && playwright install")
    print("2. 🐍 Install Pyppeteer as alternative: pip install pyppeteer")
    print("3. 🌐 Ensure Chrome/Firefox is installed and accessible in system PATH")
    print("4. 🔐 Check if your login cookies have expired - re-run dice_login.py if needed")
    print("5. 🌐 Verify your internet connection and dice.com accessibility")
    print("6. 🐛 Run with visible browser mode to see what's happening in real-time")
    print("\n💡 Playwright is recommended as it includes proper login functionality with cookies.")
    print("🐛 Enhanced debugging provides detailed information about each filter step")

if __name__ == "__main__":
    main()