"""TicketVerse - Seat-Category Event Ticketing System (CP-064)"""
from datetime import datetime, date

event = {"name": "", "date": None}
sections = {}   # section name -> {"price", "rows", "cols", "grid"}
tickets = {}    # ticket id -> {"section", "seats", "paid"}
revenue = {}    # section name -> money earned (after refunds)
next_id = 1001


def ask_int(msg):
    """Keep asking until the user types a positive whole number."""
    while True:
        s = input(msg).strip()
        if s.isdigit() and int(s) > 0:
            return int(s)
        print("Please enter a number greater than 0.")


def pick_section():
    """Ask for a section name until a valid one is typed."""
    while True:
        name = input(f"Section ({', '.join(sections)}): ").strip().upper()
        if name in sections:
            return name
        print("No such section.")


# ---------- Feature 1: set up venue ----------
def setup_venue():
    event["name"] = input("Event name: ").strip()
    while True:
        try:
            event["date"] = datetime.strptime(input("Event date (YYYY-MM-DD): "), "%Y-%m-%d").date()
            break
        except ValueError:
            print("Wrong date format, try again.")
    count = ask_int("How many sections? ")
    while len(sections) < count:
        name = input(f"Name of section {len(sections) + 1}: ").strip().upper()
        if name == "" or name in sections:
            print("Name is empty or already used.")
            continue
        rows = ask_int("  Rows (max 26): ")
        if rows > 26:
            print("  Max 26 rows.")
            continue
        cols = ask_int("  Seats per row: ")
        price = ask_int("  Price per seat: ")
        sections[name] = {"price": price, "rows": rows, "cols": cols,
                          "grid": [[None] * cols for _ in range(rows)]}
        revenue[name] = 0
    print("Venue ready!")


# ---------- Feature 2: seat map ----------
def show_map(name):
    sec = sections[name]
    print(f"\n{name} - Rs.{sec['price']} per seat   (O = free, X = booked)")
    print("   " + " ".join(f"{c + 1:2}" for c in range(sec["cols"])))
    for r in range(sec["rows"]):
        row = " ".join(" X" if t else " O" for t in sec["grid"][r])
        print(f" {chr(65 + r)} {row}")


def show_all_maps():
    for name in sections:
        show_map(name)


# ---------- Feature 3: book seats ----------
def parse_seat(text, sec):
    """'B3' -> (1, 2). Returns None if the seat does not exist."""
    if len(text) < 2 or not text[0].isalpha() or not text[1:].isdigit():
        return None
    r, c = ord(text[0]) - 65, int(text[1:]) - 1
    if 0 <= r < sec["rows"] and 0 <= c < sec["cols"]:
        return r, c
    return None


def book():
    global next_id
    name = pick_section()
    sec = sections[name]
    show_map(name)
    wanted = [s.strip().upper() for s in input("Seats to book (e.g. A1,A2,B5): ").split(",") if s.strip()]
    if not wanted or len(set(wanted)) != len(wanted):
        print("Enter at least one seat, no repeats.")
        return
    positions = []
    for s in wanted:
        pos = parse_seat(s, sec)
        if pos is None:
            print(f"Seat {s} does not exist.")
            return
        if sec["grid"][pos[0]][pos[1]]:
            print(f"Seat {s} is already booked. Nothing was booked.")
            return
        positions.append(pos)

    total = sec["price"] * len(positions)
    if len(positions) > 5:                      # stretch: group discount
        total = total * 90 // 100
        print("Group discount of 10% applied!")
    tid = next_id
    next_id += 1
    for r, c in positions:
        sec["grid"][r][c] = tid
    tickets[tid] = {"section": name, "seats": wanted, "paid": total}
    revenue[name] += total
    print(f"Booked! Ticket id: {tid}  Seats: {', '.join(wanted)}  Paid: Rs.{total}")


# ---------- Feature 4: cancel with refund ----------
def refund_percent(days_left):
    if days_left >= 7:
        return 80
    if days_left >= 3:
        return 50
    if days_left >= 1:
        return 25
    return 0


def cancel():
    tid = input("Ticket id to cancel: ").strip()
    if not tid.isdigit() or int(tid) not in tickets:
        print("Ticket not found.")
        return
    tid = int(tid)
    t = tickets[tid]
    days_left = (event["date"] - date.today()).days
    if days_left < 0:
        print("The event is over, cannot cancel.")
        return
    pct = refund_percent(days_left)
    refund = t["paid"] * pct // 100
    sec = sections[t["section"]]
    for s in t["seats"]:
        r, c = parse_seat(s, sec)
        sec["grid"][r][c] = None                # free the seat again
    revenue[t["section"]] -= refund
    del tickets[tid]
    print(f"{days_left} day(s) left -> {pct}% refund = Rs.{refund}")


# ---------- Feature 5: sales report ----------
def report():
    print(f"\nSales report - {event['name']}")
    total = 0
    for name, sec in sections.items():
        sold = sum(1 for row in sec["grid"] for t in row if t)
        print(f"{name}: {sold}/{sec['rows'] * sec['cols']} seats sold, revenue Rs.{revenue[name]}")
        total += revenue[name]
    print(f"TOTAL REVENUE: Rs.{total}")


# ---------- Main menu ----------
def main():
    print("=== TicketVerse ===")
    actions = {"2": show_all_maps, "3": book, "4": cancel, "5": report}
    while True:
        print("\n1 Setup venue  2 Seat map  3 Book  4 Cancel  5 Sales report  6 Exit")
        choice = input("Choice: ").strip()
        if choice == "6":
            print("Bye!")
            break
        elif choice == "1":
            if sections:
                print("Venue already set up.")
            else:
                setup_venue()
        elif choice in actions:
            if sections:
                actions[choice]()
            else:
                print("Set up the venue first (option 1).")
        else:
            print("Invalid choice.")


main()
