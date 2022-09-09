# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AppellateItem(scrapy.Item):
    def __init__(self):
        super().__init__()
        self.fields["Appeal Number"] = scrapy.Field()
        self.fields["Filed By"] = scrapy.Field()
        self.fields["Appellant"] = scrapy.Field()
        self.fields["Respondent"] = scrapy.Field()
        self.fields["Bench"] = scrapy.Field()
        self.fields["Case Status"] = scrapy.Field()
        self.fields["Details"] = scrapy.Field()
