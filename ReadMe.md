# Disneyland Magic Key Reservation Checker V2 (in development)

As a Disney fan and current Magic Key holder, I know how frustrating it can be to secure park reservations for the exact dates you want—especially since they often sell out quickly. Constantly refreshing the reservation calendar isn’t practical, so I built this prototype project to automate that process.

This project uses web scraping with Selenium to monitor Disneyland’s Magic Key reservation calendar and notify me when specific dates become available. It’s designed as a proof of concept to test the scraping logic and reservation checking workflow.

This app is still a work in progress. Currently, it functions as a standalone prototype without a full frontend. The plan is to continue developing it into a larger application with a complete backend and frontend system. This project remains a personal coding portfolio piece and is not intended for public release.

## Features:
- **Selectable Dates**: Select pass type and day to watch for.
- **User authentication**: Secure login system to manage user's reservations (Max 4 per user). (to be added later in V2)

## Tech:
- **Typscript**: NextJS
- **Python**: FastAPI, SQLAlechemy, Pydantic
- **Selenium**: For web scraping and navigation of shadow DOM.


![Disneyland.com Screenshot](docs/screenshots/Disneyland.comScreenShot.jpg)
