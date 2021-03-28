import scrapy

class MedicalDictionarySpider(scrapy.Spider):

    name="medicaldictionary"

    start_urls = [
        "https://www.online-medical-dictionary.org"
        ]

    def parse(self, response):
        # get list of glossary links.
        #glossary_links = response.xpath("//div[@id='glossary']//a//@href")
        links = response.css('div.card-body')[1]
        for link in links.css("a"):
            #'name' : link.css("a::text").get(),
            glossary_link = link.css("a").attrib['href']
            yield response.follow(glossary_link, callback = self.parse_medicalterms)
    
    def parse_medicalterms(self, response):
        sublinks = response.css("li a")
        for slink in sublinks:
            syn_link= slink.css("a").attrib['href']
            yield response.follow(syn_link, callback = self.parse_synonyms)
    
    def parse_synonyms(self, response):
        lst_synonyms = response.css("h2::text").getall()
        medical_term = lst_synonyms[0]
        lst_synonyms.pop(0)
        yield {
            medical_term : lst_synonyms,
        }

            #yield {
            #    'medical_term' : slink.css("a::text").get(),
            #    'syn_link' : slink.css("a").attrib['href'],
            #}

            
            
            

            