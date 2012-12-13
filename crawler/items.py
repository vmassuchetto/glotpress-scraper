from scrapy.item import Item, Field

class LinkItem(Item):
    project = Field()
    url = Field()
