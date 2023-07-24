import scrapy
from scrapy.http import Request, HtmlResponse

from stagemarkt_scraper.spiders.organization_parse_utils import parse_organization_info_bar


class StagemarktOrganizationsSpider(scrapy.Spider):
    name = "stagemarkt_organizations"
    allowed_domains = ["stagemarkt.nl"]
    base_url = "https://stagemarkt.nl/leerbedrijven/?Termen=&PlaatsPostcode=&Straal=0&Land=00000000-0000-0000-0000-000000000000&ZoekenIn=A&Longitude=&Latitude=&Regio=&Plaats=&Niveau=&SBI=&Kwalificatie=&Sector=&RandomSeed=648&Leerweg=&Bedrijfsgrootte=&Opleidingsgebied=&Internationaal=&Beschikbaarheid=&AlleWerkprocessenUitvoerbaar=&LeerplaatsGewijzigd=&Sortering=0&Bron=ORG&Focus=&LeerplaatsKenmerk=&OrganisatieKenmerk=&Page="

    def start_requests(self):
        for i in range(1, 724):
            yield Request(url=self.base_url + str(i))

    def parse(self, response: HtmlResponse):
        links = response.xpath(
            "//a[@class='c-link-blocks-single']/@href").getall()
        for link in links:
            yield Request(url="https://stagemarkt.nl" + link, callback=self.parse_organization)

    def parse_organization(self, response: HtmlResponse):

        organization = parse_organization_info_bar(response)
        lis = []
        for info_ul in response.xpath(
                "//ul[@class='c-company__info__list u-reset-ul']"):
            lis.extend(info_ul.xpath("./li"))
        for li in lis:
            li_text = li.xpath('./span/strong/text()').get()
            li_value = li.xpath(
                './span[2]/text()').get()
            if "Informatie Student" in li_text or "Omschrijving" in li_text:
                organization['organization_description'] = li_value
            elif "Bedrijfsindeling" in li_text:
                organization['organization_industry'] = li_value
        yield organization
