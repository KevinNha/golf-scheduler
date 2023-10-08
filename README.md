# Golf Scheduler

A small side-project to help my father-in-law automate registering for his golf sessions. 

This is site-specific that I specify in a `.env` file. 

## Prerequisites

You must download [chromedriver](https://chromedriver.chromium.org/downloads) from here to allow Selenium to open a chrome driver.

## Get Started

Before you run the file, you must install venv and the required dependencies
```bash
> python -m venv venv

> #windows
> venv\Scripts\activate

> #mac
> source venv\lib\activate.bat

> pip install -r requirements.txt
```

Additionally for Windows, you may create an executable (`.exe`) file:
```bash
> python -m auto_py_to_exe
```
You can use the configuration in `./static/exe_config.json`