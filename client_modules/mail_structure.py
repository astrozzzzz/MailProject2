class Mail:
    def __init__(self, sender, addressee, date, title, main_text):
        self.sender = sender
        self.addressee = addressee
        self.date = date
        self.title = title
        self.main_text = main_text

    def get_short_mail(self):
        res = f"{self.sender}: {self.title}"
        if len(res) > 40:
            res = f"{res[:40]}..."
        return res