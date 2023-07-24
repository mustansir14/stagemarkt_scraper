# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Organization(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    organization_name = scrapy.Field()
    organization_description = scrapy.Field()
    organization_address = scrapy.Field()
    organization_website = scrapy.Field()
    organization_creator = scrapy.Field()
    organization_owner = scrapy.Field()
    organization_industry = scrapy.Field()


class Contact(scrapy.Item):

    contact_name = scrapy.Field()
    contact_organization = scrapy.Field()
    display_name = scrapy.Field()
    phone_number = scrapy.Field()
    email = scrapy.Field()


class Job(scrapy.Item):

    job_name = scrapy.Field()
    job_organization = scrapy.Field()
    job_description = scrapy.Field()
    job_creator = scrapy.Field()
    job_owner = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    office_address = scrapy.Field()
    job_status = scrapy.Field()
    contract_details = scrapy.Field()
