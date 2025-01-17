A social media website that allows users to: register accounts, post statuses, like posts, comment on posts etc. Fullstack django-html

Install and run:

    Clone the repo: git clone git@github.com:coddd3r/social-media-api.git
    run a virtual environment: virtualenv -p python3 env
    activate the env: source env/bin/activate
    install from requirements.txt: pip install -r requirements.txt
    ensure you have postgres installed, if uncomment and use the sqlite settings.
    Run python manage.py migrate to apply database migrations.
    Run python manage.py runserver

Hosting link:
    - The site is hosted on pythonanywhere: [https://ddinho.pythonanywhere.com]

Authentication:
    - UI Authentication is done at login/ endpoint on the site page
    - API auth is done at api/login using Token Authentication

        example: { "username": "johnDoe", "password": "password123" }
        Response:
        { "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c" }
