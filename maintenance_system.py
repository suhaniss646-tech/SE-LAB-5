"""Warehouse asset maintenance registry.

Registers machines, records service dates, raises alerts for overdue
inspections and exports a report to ``maintenance.json``.
"""

import json
import tempfile
from datetime import datetime, timedelta

# Global state
assets = {}
registration_log = []
config = {"service_interval_days": 90}


def register_asset(asset_id, machine_type):
    """Register an asset, rejecting empty or duplicate asset ids."""
    if not asset_id:
        print("Rejected registration with empty asset id")
        return
    if asset_id in assets:
        print("Duplicate asset id", asset_id, "- registration ignored")
        return
    assets[asset_id] = {
        "type": machine_type,
        "last_service": datetime.now().strftime("%Y-%m-%d"),
    }
    registration_log.append(asset_id)
    print("Registered", asset_id,
          "- total registrations this run:", len(registration_log))


def update_service_date(asset_id, date):
    """Set the last service date of an existing asset after validation."""
    if asset_id not in assets:
        print("Could not update", asset_id)
        return
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date", date, "- expected YYYY-MM-DD")
        return
    assets[asset_id]["last_service"] = date


def due_for_inspection():
    """Return the ids of assets whose last service is older than the
    configured inspection interval."""
    due = []
    for asset_id, record in assets.items():
        last = datetime.strptime(record["last_service"], "%Y-%m-%d")
        interval = timedelta(days=config["service_interval_days"])
        if datetime.now() - last > interval:
            due.append(asset_id)
    return due


def change_interval(days):
    """Update the inspection interval, rejecting non-positive values."""
    if days <= 0:
        print("Rejected invalid interval", days)
        return
    config["service_interval_days"] = days


def export_service_report(file="maintenance.json"):
    """Write the asset registry as JSON to the given file."""
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(assets, indent=2))
    print("Report written to " + file)


def write_scratch_copy():
    """Write a temporary scratch copy of the registry securely."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                     delete=False, encoding="utf-8") as f:
        f.write(json.dumps(assets))
        path = f.name
    print("Scratch copy at", path)


def print_alerts():
    """Print an alert for every asset due for inspection."""
    for asset_id in due_for_inspection():
        print("ALERT: inspection overdue for",
              asset_id, assets[asset_id]["type"])


def main():
    """Run the interactive maintenance registry demo."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("", "Pallet Jack")
    register_asset("FL-01", "Crane")
    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")
    change_interval(-30)
    d = input("Last service date for CV-07 (YYYY-MM-DD, Enter to skip): ")
    if d:
        update_service_date("CV-07", d)
    if not assets:
        print("No assets registered")
        return
    print_alerts()
    export_service_report()
    write_scratch_copy()


if __name__ == "__main__":
    main()
