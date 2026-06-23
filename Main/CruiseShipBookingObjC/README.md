# Cruise Ship Booking - Objective-C

Objective-C command-line version of the cruise ship restaurant booking question.

## Build

```sh
make
```

## Run

```sh
make run
```

The program keeps the same core behaviour as the Python version:

- displays today's date and table availability for Lunch, Early Dinner, and Late Dinner
- lets a passenger book a table
- stores passenger name, cabin number, session, dietary requirement, and table number
- displays vegetarian and vegan booking totals

The implementation avoids scanning every table to find a free table by tracking the next available table number for each dining session.
