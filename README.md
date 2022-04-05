# runnerspace

[![Runnerspace Banner](banner-url)](heroku-url)

Runnerspace is a retro, UTSA-themed MySpace clone made in less than 36 hours during RowdyHacks 2022. It was intended for the 'Retro' challenge
and has been further overhauled afterwards to become a portfolio project, hosted on Heroku. Check it out by clicking on the banner or [here][heroku-url].

## About

Made during Rowdy Hacks 2022, this myspace look-a-like was quickly made with intentions of serving the UTSA student community. We took heavy
inspiration from my-space and other social media services of its era.

We made this app starting almost 5 hours after this 24-hour Hackathon started and were able to successfully present a finished demo for judging at RowdyHacks 2022.

## Features

- Accounts
    - Signup
    - Login/Logout + Remember Me
    - Administrative Access
    - Profile Editing
    - Profile Viewing
    - Online and Offline account flags
- Posts
    - Post Creation
      - Comment posting
    - Post Feed + Comment Stats
    - AJAX Post Liking System
- Appearance
    - Customized to look like MySpace; UTSA themed
    - CSS written to be usable on most laptops/desktops
    - MySpace-like Theme
        - Image used, although text-based logo fallback available
- Misc
    - Easy install & setup with `pipenv`
    - Hosted on [Heroku][heroku-url]!
    - Profanity filtering
    - Human + Computer Readable Timestamps
        - "3 minutes ago" and such...
    - Global Header & Footer
    - License Page
    - About Page
    - UTC Timestamped Page Rendering

## Tech Stack

- Flask
    - Jinja Templating
    - SQLAlchemy + SQLite
- Sass
- Font Awesome Icons
- Heroku
- Other
    - Humanize
    - Faker
    - `better-profanity`

# Development Setup

Developed on Python 3.8.0 - thus we recommend this version specifically.

```bash
pip install pipenv
pipenv install
flask run
```


[banner-url]: ./static/runnerspace-banner-slim.png
[heroku-url]: https://runnerspace-utsa.herokuapp.com/
