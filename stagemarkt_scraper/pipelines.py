# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

from stagemarkt_scraper import items


class StagemarktScraperPipeline:
    def __init__(self):
        self.org_file = 'organizations.csv'
        self.contact_file = 'contacts.csv'
        self.job_file = 'jobs.csv'
        self.orgs_seen = set()
        self.contacts_seen = set()
        self.jobs_seen = set()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_item(self, item, spider):
        if isinstance(item, items.Organization):
            self.process_organization_item(item)
        elif isinstance(item, items.Contact):
            self.process_contact_item(item)
        elif isinstance(item, items.Job):
            self.process_job_item(item)
        return item

    def process_organization_item(self, item):
        org_name = item['organization_name']
        if org_name not in self.orgs_seen:
            self.orgs_seen.add(org_name)
            self.write_to_csv(self.org_file, item)

    def process_contact_item(self, item):
        contact = (item['contact_name'], item['contact_organization'])
        if contact not in self.contacts_seen:
            self.contacts_seen.add(contact)
            self.write_to_csv(self.contact_file, item)

    def process_job_item(self, item):
        job = (item['job_name'], item['job_organization'])
        if job not in self.jobs_seen:
            self.jobs_seen.add(job)
            self.write_to_csv(self.job_file, item)

    def write_to_csv(self, filename, item):
        fieldnames = list(item.keys())
        converted_fieldnames = [self.convert_case(
            fieldname) for fieldname in fieldnames]
        item_dict = {}
        for fieldname, converted in zip(fieldnames, converted_fieldnames):
            item_dict[converted] = item[fieldname]
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=converted_fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(item_dict)

    def convert_case(self, string: str) -> str:
        return " ".join([s.capitalize() for s in string.split("_")])
