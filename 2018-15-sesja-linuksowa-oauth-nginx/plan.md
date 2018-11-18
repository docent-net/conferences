1. Słowo wstępu
    0. To moja 5 sesja - dzięki!
    1. Pracuję obecnie w dość małej firmie, w której jestem jedynym devopsem
    2. Hostujemy się na AWSie i tam też mamy większość usług (plus GCP)
    3. Nie lubimy hostować swoich rozwiązań - albo budujemy coś swojego albo
       kupujemy.
2. Problem:
    1. Zdarzają się aplikacje, które nie są w ogóle uwierzytelniane - mamy
       złudne wrażenie, że VPN i sieć lokalna to wystarczające zabezpieczenie
    2. Są też aplikacje, które potrafią uwierzytelnić klienta, jednak posiadają
       swoją bazę loginów, dzięki czemu w menadżerach haseł mamy sporo wpisów
       i w ramach dnia pracy musimy się przelogowywać między serwisami (a to
       zabiera czas i komplikuje sprawy)
    3. Stworzenie własnego rozwiązania SSO może być trudne - choćby z powodu
       brakującej integracji z aplikacjami, które chcielibyśmy wintegrować.
3. Autentykacja i autoryzacja
    1. Co to jest i jakie są różnice
    2. Znane rozwiązania (AD, LDAP)
    3. Problemy tych rozwiązań (krowy ciężko utrzymywalne)
4. Oauth, Oauth2 - omówienie
    1. Schematy i wyjaśnienie
        - https://www.digitalocean.com/community/tutorials/an-introduction-to-oauth-2
        - https://aaronparecki.com/oauth-2-simplified/
        - https://www.oauth.com/
        - playground: https://www.oauth.com/oauth2-playground/
    2. Oauth vs OAuth2: https://stackoverflow.com/questions/4113934/how-is-oauth-2-different-from-oauth-1
    3. W naszej firmie używamy Google i Githuba
    4. Google Oauth2 (przykład, pokazać)
    5. Github Oauth2 (przykład, pokazać)
    6. Open - source
        - ORY: 
            - https://github.com/ory/oathkeeper
            - https://www.ory.sh/run-oauth2-server-open-source-api-security/
        - Gluu:
            - https://gluu.org/docs/ce/
            - https://github.com/GluuFederation/community-edition-setup
5. Pomysł na rozwiązanie problemu: Nginx + auth_request
    1. auth_request module: https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/
        - jego wymagania, kompilacja
        - omówić jak działa
    2. pokazac na przykładzie (najprostszy - dwie końcówki, jedna autoryzuje, druga nie)
            - http://sesja-1.demo/
            - http://sesja-1.demo/secured_will_fail/
            - http://sesja-1.demo/secured_will_succeed/
6. Nginx + auth_request + Python
    1. Omówić jak to może zadziałać
        - instalacja i konfiguracja
        - /etc/nginx/conf.d/sesja.conf
        - /etc/systemd/system/pyapp.service
        - /srv/sesja-2.demo.python (app.ini, wsgi.py, app.py, index.html)
    2. Pokazać prosty przykład - jeśli jesteś z dobrego IP to cię wpuszczamy, 
       inaczej nie (bezsensowny bo oczywiście można to zrobić za pomocą Nginxa)
        - http://sesja-2.demo/
        - http://sesja-2.demo/secured/
        - journalctl -u pyapp -f
        - journalctl -u nginx -f
7. A gdyby tak Nginx + auth_request + Oauth2_Proxy?
    1. Pokazać oauth2_proxy i omówić jak działa
        - pokazać ile ma możliwych integracji
        - instalacja i konfiguracja (paczka, unit file)
        - integracja z nginxem - pokazać configi i omówić
        - /etc/oauth2_proxy.cfg
        - /etc/nginx/conf.d/sesja.conf
        - /etc/systemd/system/oauth2_proxy.service
    2. Przykład działający - zabezpieczyć index.html za pomocą Google Oauth2
        - pokazać konfigurację w projekcie Google'owym
        - http://sesja-3.demo.com/
        - http://sesja-3.demo.com/secured/
    3. Wspomnieć o Cloudflare module https://github.com/cloudflare/nginx-google-oauth
8. Może pokazać jakiś skopiowany projekt z Pythonem i Oauth2 i Nginxem?
        - https://github.com/cheshirekow/oauthsub/tree/master/oauthsub
        - fajne bo Python i na prawdę prosty codebase - dobry do nauki (pokazać nawet)
        - instalacja i konfiguracja
        - /etc/nginx/conf.d/sesja.conf <- tym razem bez uwsgi
        - /etc/systemd/system/oauthsub.service
        - /etc/oauthsub.py
        - /srv/sesja-4
        - journalctl -u oauthsub -n 200 -f
        - http://sesja-4.demo/
9. Ostatnie demo - finał
    1. Opisać z czego się to demo składa - opisać preauthenticated w rundecku
        - instalacja i konfiguracja (paczka, unit file)
        - integracja z nginxem - pokazać configi i omówić
        - /etc/rundeck/framework.properties,profile,rundeck-config.properties
        - /var/lib/rundeck/exp/webapp/WEB-INF/web.xml
        - /etc/oauth2_proxy.cfg
        - /etc/nginx/conf.d/sesja.conf
        - /etc/systemd/system/oauth2_proxy.service
    1. Opisać problemy oauth2_proxy w odniesieniu do Rundecka:
        - user
        - rola użytkownika i brak jej przekazywania
        - pokazać PRki
            - https://github.com/rundeck/rundeck/pull/1883
            - https://github.com/bitly/oauth2_proxy/issues/386
            - https://github.com/bitly/oauth2_proxy/pull/61
            - https://gist.github.com/donaldguy/eaa99fb0d1f17c0576255c3cf3ffc7ea
            - https://github.com/bitly/oauth2_proxy/pull/277
    4. Pokazać jak to ładnie działa i dlaczego jest do dupy z punktu widzenia ról
10. Na zadanie domowe - przerobić tak oauthsub, aby przekazywało rolę usera do Rundecka