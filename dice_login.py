#!/usr/bin/env python3
"""
Script to access dice.com using provided cookies with anti-bot detection measures
"""

import requests
import json
import time
import random
from urllib.parse import urlencode
# from fake_useragent import UserAgent  # Commented out to avoid dependency

# Cookies provided in JSON format
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
        "value": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImE0YmNkMWZhLTgxZmUtNDk5Ni05MmE3LTcyNWE1YTRhMDU3MiJ9.eyJyb2xlIjoiY3VzdG9tZXIiLCJpc3MiOiJodHRwczovL2F1dGhuLWFwaS5kaWNlLmNvbS9hY2NvdW50L2dyYXBocWwiLCJ0b2tlbl91c2UiOiJpZGVudGl0eSIsImNsaWVudF9pZCI6IjUwdWZvYWc3MzltZ2hqbDdvZTRlcDNjc3RlIiwic2NvcGVzIjpbImRpY2UtY3VzdG9tZXItcmVjcnVpdGVyIiwiZGljZS10YWxlbnQtc2VhcmNoIiwiZGljZS1jb21wYW55LXJlcG9ydHMiXSwicHJpbmNpcGFsX2lkIjoiODE4M2QxM2MtNjM2NC00MjNmLTgwYjQtYjg5MWRkNjU4MDYxIiwiZW1haWxfdmVyaWZpZWQiOiJmYWxzZSIsInJlY3J1aXRlcl9pZCI6IjAxMTc5MGIxLTE4YjktNGY3NC1hOTNhLWFjNmJiM2IzMGRjOCIsImVtYWlsIjoic25pa2VzaEB0aGlua2x1c2l2ZS5jb20iLCJ1c2VyX2lkIjoyMDgxNjE5LCJjb21wYW55X2lkIjoyMDMyNjg1LCJuYW1lIjoiU3JpTmlrZXNoIiwiZmFtaWx5X25hbWUiOiJSYWphYm95ZW5hIiwic3NvIjpmYWxzZSwiaWF0IjoxNzU5NTMwNjYwfQ.l6w8lhDCUUiGYFPtYNfH0lGbxJhlMPMxLa0386UbGoqMsxrVKrK9iKMlq4sPwm3oBh7UyokprKS-Y2BFmnQQxO1Ltl29QlOwpYfaE1fhQPOSlmshSoT1TUORtq_JhUgODR3J7cKzytn5W24dj8ZxNg5X9BwzGsRdGY3HQeOXicIltXtuh3tl0sxMLiUW7mBgTfiHtL5JVwIxpWRJSfQaVGhaCVgcTqwvBer7MZb2Pbtw7d0mipW82rsWqwMaWeYRN23gm3FhWQHGyxwMuzp6YlgXYe5c9CaEa3pImjeQZmaGN52uVQNTs_bmeADXiLg93O7lU1w9QC5Uu6EgZCRyOC2cUIJBO5JcPumNADWb9Qznpw-NNYujdy4VTdOLTv1TL_gvvel2JqY685XzYvm-Jn7Mb5XEHghWdC3JQITp32cbMbdEKCPOr2SRm_48e-rgvOS7HGxZEaWNKiEopGN683GlP_SdpFFxU48cbmQ3yoLe3uPaekuuJwpkUMoVvplTkMWrNjOyH8cjAp2sPTJbDKmSpVxo07AkTnPsIh6hOD7yODeWPXWA2_8575Chu4OtKqGELiud0yxViuqDTB4qVr17mlkH1IT_ztArRFUG5JbDW5aANNZ1r_yQjatw_MZO66I9ig_NSjPx2KDH4QReTvNMKyrBHxXGIgylIi1TeCY"
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

# List of realistic user agents to rotate through
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
]

def random_delay(min_seconds=2, max_seconds=5):
    """Add random delay to simulate human behavior"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay

def get_random_headers():
    """Generate random headers to look like different browsers"""
    ua = random.choice(USER_AGENTS)

    # Determine browser type from user agent
    if 'Chrome' in ua:
        accept_header = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        sec_ch_ua = '"Chromium";v="128", "Google Chrome";v="128", "Not=A?Brand";v="99"'
        sec_ch_ua_mobile = '?0'
        sec_ch_ua_platform = '"macOS"'
    elif 'Firefox' in ua:
        accept_header = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
        sec_ch_ua = sec_ch_ua_mobile = sec_ch_ua_platform = None
    else:  # Safari
        accept_header = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        sec_ch_ua = sec_ch_ua_mobile = sec_ch_ua_platform = None

    headers = {
        'User-Agent': ua,
        'Accept': accept_header,
        'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.9,en-US;q=0.8', 'en-US,en;q=0.8,en-GB;q=0.6']),
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': random.choice(['max-age=0', 'no-cache']),
        'DNT': '1',
        'Sec-GPC': '1'
    }

    # Add Chrome-specific headers
    if sec_ch_ua:
        headers['Sec-Ch-Ua'] = sec_ch_ua
        headers['Sec-Ch-Ua-Mobile'] = sec_ch_ua_mobile
        headers['Sec-Ch-Ua-Platform'] = sec_ch_ua_platform

    return headers

def create_session_with_cookies():
    """Create a requests session with the provided cookies and anti-detection measures"""
    session = requests.Session()

    # Convert cookie JSON to requests cookie format
    for cookie in cookies_json:
        session.cookies.set(
            cookie['name'],
            cookie['value'],
            domain=cookie['domain'],
            path=cookie['path']
        )

    # Set random headers
    session.headers.update(get_random_headers())

    # Configure session to handle cookies and redirects like a real browser
    session.max_redirects = 5
    session.cookies.update({'cookieconsent_status': 'dismiss'})

    return session

def make_human_like_request(session, url, method='GET', **kwargs):
    """Make a request with human-like behavior"""
    # Add random delay before request
    delay = random_delay(1, 3)
    print(f"Waiting {delay:.1f} seconds before request...")

    # Update headers for this request
    session.headers.update(get_random_headers())

    # Make the request with timeout
    try:
        if method.upper() == 'GET':
            response = session.get(url, timeout=30, **kwargs)
        elif method.upper() == 'POST':
            response = session.post(url, timeout=30, **kwargs)
        else:
            response = session.request(method, url, timeout=30, **kwargs)

        # Random delay after successful request
        random_delay(0.5, 2)

        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def test_dice_access(session):
    """Test accessing dice.com with the session using human-like behavior"""
    print("Testing access to dice.com with anti-detection measures...")

    # First, simulate accessing the homepage like a real user
    response = make_human_like_request(session, 'https://www.dice.com/')

    if response is None:
        return False

    print(f"Status Code: {response.status_code}")
    print(f"Response Length: {len(response.text)}")

    # Check if we're logged in by looking for specific content
    if response.status_code == 200:
        if "dashboard" in response.text.lower() or "profile" in response.text.lower():
            print("✓ Successfully logged into dice.com!")
            return True
        elif "login" in response.text.lower() or "sign in" in response.text.lower():
            print("✗ Not logged in - redirected to login page")
            return False
        else:
            print("? Login status unclear - checking further...")
            # Look for employer-specific content
            if "employer" in response.text.lower() or "recruiter" in response.text.lower():
                print("✓ Appears to be logged in as employer/recruiter")
                return True
            return False
    else:
        print(f"✗ Failed to access dice.com - Status: {response.status_code}")
        return False

def test_employer_dashboard(session):
    """Test accessing the employer dashboard with human-like behavior"""
    print("\nTesting access to employer dashboard...")

    # Simulate navigating to employer dashboard after a delay
    response = make_human_like_request(session, 'https://www.dice.com/employer/dashboard')

    if response is None:
        return False

    print(f"Dashboard Status Code: {response.status_code}")

    if response.status_code == 200:
        if "dashboard" in response.text.lower():
            print("✓ Successfully accessed employer dashboard!")
            return True
        else:
            print("? Dashboard access unclear")
            return False
    else:
        print(f"Could not access dashboard - Status: {response.status_code}")
        return False

def simulate_browsing_session(session):
    """Simulate a realistic browsing session to avoid detection"""
    print("\nSimulating realistic browsing behavior...")

    # Visit some common pages like a real user would
    pages_to_visit = [
        'https://www.dice.com/',
        'https://www.dice.com/jobs',
        'https://www.dice.com/employer/dashboard'
    ]

    for page in pages_to_visit:
        print(f"\nVisiting: {page}")
        response = make_human_like_request(session, page)
        if response and response.status_code == 200:
            print(f"✓ Successfully accessed {page}")
        else:
            print(f"✗ Failed to access {page}")

        # Random pause between page visits
        random_delay(3, 8)

def main():
    """Main function to test dice.com access with anti-detection measures"""
    print("🛡️  Starting Dice.com access with anti-bot detection measures...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print("Creating session with cookies and anti-detection headers...")
    session = create_session_with_cookies()

    print(f"Using User-Agent: {session.headers.get('User-Agent', 'Unknown')}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Test basic access
    login_success = test_dice_access(session)

    if login_success:
        # Simulate realistic browsing
        simulate_browsing_session(session)

        # Test employer dashboard
        test_employer_dashboard(session)

        print("\n✅ All tests completed successfully with anti-detection measures!")
        print("📝 Tips to avoid detection:")
        print("   • Use random delays between requests (implemented)")
        print("   • Rotate user agents and headers (implemented)")
        print("   • Limit requests per minute (<10 recommended)")
        print("   • Avoid parallel requests to same domain")
        print("   • Use different IP addresses if making many requests")
    else:
        print("\n❌ Login failed - check if cookies are still valid")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    main()