import scrapy
from scrapy.http import Request, HtmlResponse

from stagemarkt_scraper import items
from stagemarkt_scraper.spiders.organization_parse_utils import parse_organization_info_bar


class StagemarktSpider(scrapy.Spider):
    name = "stagemarkt"
    allowed_domains = ["stagemarkt.nl"]
    base_url = "https://stagemarkt.nl/vacatures/?Termen=&PlaatsPostcode=&Straal=0&Land=00000000-0000-0000-0000-000000000000&ZoekenIn=A&Longitude=&Latitude=&Regio=&Plaats=&Niveau=&SBI=&Kwalificatie=&Sector=&RandomSeed=885&Leerweg=&Bedrijfsgrootte=&Opleidingsgebied=&Internationaal=&Beschikbaarheid=&AlleWerkprocessenUitvoerbaar=&LeerplaatsGewijzigd=&Sortering=0&Bron=STA&Focus=&LeerplaatsKenmerk=&OrganisatieKenmerk=&Page="

    def start_requests(self):
        for i in range(1, 220):
            yield Request(url=self.base_url + str(i))

    def parse(self, response: HtmlResponse):
        links = response.xpath(
            "//a[@class='c-link-blocks-single']/@href").getall()
        for link in links:
            yield Request(url="https://stagemarkt.nl" + link, callback=self.parse_job)

    def parse_job(self, response: HtmlResponse):

        organization = parse_organization_info_bar(response)
        yield organization

        company_detail_section = response.xpath(
            '//div[@class="c-detail-company"]')[-1]
        uls = company_detail_section.xpath("./ul")
        for ul in uls[1:]:
            if "Contactpersoon" in ul.xpath("./li/strong/text()").get():
                contact = items.Contact()
                lis = ul.xpath("./li")[1:]
                contact['contact_name'] = lis[0].xpath('./text()').get()
                contact['display_name'] = contact['contact_name']
                contact['contact_organization'] = organization['organization_name']
                for li in lis[1:]:
                    li_text = li.xpath('./text()').get()
                    a_text = li.xpath("./a/text()").get()
                    if "Tel:" in li_text:
                        contact['phone_number'] = a_text
                    elif "E-mail:" in li_text:
                        contact['email'] = a_text
                yield contact
                break

        job = items.Job()
        job["job_creator"] = "contact@internshipmatching.com"
        job["job_owner"] = "contact@internshipmatching.com"
        job['job_status'] = "active"
        job['contract_details'] = "internship"
        job["job_organization"] = organization['organization_name']

        job["job_name"] = response.xpath("//h1/text()").get().replace("\n", "")
        job["job_description"] = "\n".join(response.xpath(
            "//div[@class='c-detail-text']/article//text()").getall())
        extra = ["zoek school die deze opleiding aanbiedt",
                 "solliciteer nu", "of neem contact op", "lees verder"]
        for string in extra:
            job['job_description'] = job["job_description"].replace(string, "")

        job['job_description'] = job['job_description'].strip()
        detail_lines = response.xpath(
            "//div[@class='div-table-stagedetails-row']")
        for detail_line in detail_lines:
            detail_line_text = "\n".join(
                detail_line.xpath(".//text()").getall())
            if "locatie" in detail_line_text:
                job['city'] = detail_line.xpath(
                    "./div[@class='div-table-stagedetails-value']/text()").get()
                break
        job['country'] = organization['organization_address'].split('\n')[-1]
        job['office_address'] = organization['organization_address']
        yield job
