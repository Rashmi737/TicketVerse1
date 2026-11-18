# TicketVerse: Seat-Category Event Ticketing System (CP-064)

A menu-driven Python console app that sells seats by category (section) for a college fest or concert and prevents overselling.

## Features

**Core**
1. Set up a venue with sections, rows and price per section
2. Show available seats as a seat map (`O` = free, `X` = booked)
3. Book selected seats and generate a ticket id
4. Cancel tickets with a refund based on days left to the event
5. Show sales by section and total revenue

**Stretch**
- Group booking discount: 10% off when booking more than 5 seats

## How to run

```
python ticketverse.py
```

Requires Python 3. No extra libraries needed.

## How to use

1. Choose `1` and set the event name, date (YYYY-MM-DD), sections, rows, seats per row and price.
2. Choose `2` to view the seat map.
3. Choose `3`, pick a section, and type seats like `A1,A2,B5`. You get a ticket id.
4. Choose `4` and enter a ticket id to cancel and see the refund.
5. Choose `5` for the sales report.

## Rules

- A seat can only be booked once. If any chosen seat is taken or invalid, nothing is booked.
- Seats are named by row letter and seat number (row A, seat 1 = `A1`).
- Refund policy:

| Days left to event | Refund |
|---|---|
| 7 or more | 80% |
| 3 to 6 | 50% |
| 1 to 2 | 25% |
| Event day | 0% |

- Cancelled seats become free again, and the refund is deducted from revenue.
- Group discount: more than 5 seats in one booking gets 10% off.

## Design

- `sections`: dictionary of section name to price, rows, columns and a 2D grid. A free seat is `None`; a booked seat stores its ticket id.
- `tickets`: dictionary of ticket id to section, seats and amount paid.
- `revenue`: dictionary of section name to money earned after refunds.

## Input handling

Handles wrong menu choices, wrong date format, non-numeric or zero numbers, duplicate section names, seats that do not exist, already booked seats, unknown ticket ids, and actions before the venue is set up.

## Edge cases tested

- Booking an already booked seat
- Booking a seat outside the grid (e.g. `Z9`)
- Repeating the same seat in one booking
- Cancelling a ticket id that does not exist
- Cancelling after the event date
- Booking more than 5 seats (discount)
