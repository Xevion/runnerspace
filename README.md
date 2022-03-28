# runnerspace

A retro myspace clone for UTSA students.

## About

Made during Rowdy Hacks 2022, this myspace look-a-like was quickly made with intentions of serving the UTSA student community. We took heavy
inspiration from my-space and other social media services of it's era.

We made this app starting almost 5 hours after this 24-hour Hackathon started and in total I stayed up for around 36 hours straight to 

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
    - Post Feed + Comment Stats
- Appearance
    - Customized to look like MySpace; UTSA themed
    - CSS written to be usable on most laptops/desktops
    - MySpace-like Theme
        - Image used, although text-based logo fallback available
- Misc
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
- Other
    - Humanize
    - Faker

# Development Setup

Developed on Python 3.8.0 - thus we recommend this version specifically.

```bash
pip install pipenv
pipenv install
flask run
```

Not production ready yet.
