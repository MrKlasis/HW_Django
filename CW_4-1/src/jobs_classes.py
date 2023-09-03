class Vacancy:
    __slots__ = {'title', 'link', 'description', 'salary'}

    def __init__(self, title, link, description, salary):
        self.title = title
        self.link = link
        self.description = description
        self.salary = salary

    def __repr__(self):
        return f"Vacancy(title='{self.title}', link='{self.link}', description='{self.description}', salary='{self.salary}"

    def __str__(self):
        return self.title

    def __gt__(self, other):
        return self.salary > other.salary