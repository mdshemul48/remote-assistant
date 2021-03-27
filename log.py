import json
from datetime import date


class Log:
    def __init__(self, log_file):
        self.log_file = log_file
        with open(log_file) as log_file:
            data = json.load(log_file)
        self.data = data

    def uploaded(self):
        now = date.today().strftime("%d/%m/%Y")
        if now in self.data["daily_report"].keys() and "uploaded" in self.data["daily_report"][now]:
            self.data["daily_report"][now]["uploaded"] += 1

        elif date not in self.data["daily_report"].keys():
            self.data["daily_report"][now] = {
                "uploaded": 1, "deleted": 0}

    def deleted(self):
        now = date.today().strftime("%d/%m/%Y")
        if now in self.data["daily_report"].keys() and "deleted" in self.data["daily_report"][now]:
            self.data["daily_report"][now]["deleted"] += 1

        elif now not in self.data["daily_report"].keys():
            self.data["daily_report"][now] = {
                "uploaded": 0, "deleted": 1}

    def save(self):
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    log = Log("data.json")
    log.uploaded()
    log.deleted()
    log.save()
