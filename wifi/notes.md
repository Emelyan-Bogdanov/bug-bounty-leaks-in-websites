
# What to test : 


## "PATH_TRAVERSAL" : look for hidden directories or files & 
+ URL = `192.168.1.1/`
+ LINKS : 
    + `Internal`
        - /assets/logo_MA0416.600c8ad1.png
        - /assets/index.a20f2e3d.js
        - /assets/interface_close.8432fd6b.png
        - 
    + `External`
        - #/systemStatus/networkInfo
        - #/systemStatus/deviceInfo
    _____________

    + `400 : BAD_REQUEST : illegal filename`==> no path traversal allowed 
        - //**aything**
    + `404 : FILE_NOT_FOUND`
        - /**aything**


## Intercept requests

**POST** : 
    - URL : /cgi-bin/http.cgi
    - Data : 
        - cmd : `9f2861ee-baf8-4038-bab6-774ad4e930b0`
        - method : POST
        - sessionId
```json
        --[ RESPONSE ]--
            {
                "success":true,
                "cmd":1008,
                "web_logo_path":"logo_MA0416.png",
                "language_support":"3",
                "language_show":"1",
                "user_web_theme":"main.css",
                "web_theme":"theme-MA0416",
                "web_browser_title":"",
                "web_browser_logo":"ma0416_tab_icon.png.ico",
                "aeraId":"MA0416",
                "web_product_path":"",
                "language_list_support":"c2",
                "hide_no_account":"0",
                "first_login_flag":"0",
                "enable_rsa_encrypt_change_passwd":"",
                "user_login_times_limit":"",
                "dataRefreshInterval":"",
                "language":"en",
                "board_type":"ZLT T304",
                "fake_version":"1.0.9",
                "domain_value":"5b60531e7e48b9406f470eb8c7e5ab99",
                "build_type":"user",
                "ver_type":"user",
                "show_ussd":"1",
                "model_name":"IDU","support_hex_string":"000000000000000000000208000000101DFA01C0F2023F0FC2A3C36D5DF71668B0FEFAFFEFDF01740BFFDF7FA07DFD"
            }
```

    + 

## Identifiers
- Model     :   T304
- Software :    Version	1.0 9
- IMEI     :    862256080050482
- IMSI     :    604020297560965
- ICCID    :    8921202200211788220F
- MSISDN   :    212714589851