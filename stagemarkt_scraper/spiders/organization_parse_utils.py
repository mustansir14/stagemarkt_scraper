from scrapy.http import HtmlResponse
from stagemarkt_scraper.items import Organization


def parse_organization_info_bar(response: HtmlResponse) -> Organization:

    organization = Organization()
    organization["organization_owner"] = "contact@internshipmatching.com"
    organization["organization_creator"] = "contact@internshipmatching.com"

    company_detail_section = response.xpath(
        '//div[@class="c-detail-company"]')[-1]
    lis = company_detail_section.xpath('./ul/li')
    organization['organization_name'] = lis[0].xpath(
        './strong/text()').get()
    organization['organization_address'] = "\n".join([lis[i].xpath(
        './text()').get() for i in range(1, 4)])
    for i in range(4, len(lis)):
        li_text = lis[i].xpath("./text()").get()
        if li_text and "Website" in li_text:
            organization['organization_website'] = lis[i].xpath(
                "./a/text()").get()
            break
    return organization
