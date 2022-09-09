# importing libraries
import scrapy, json
import re
from itertools import product
from ..items import AppellateItem

class RecordScraps(scrapy.spiders.Spider):
    name = "quick" #assigning a name to the spider
    
    def __init__(self, order_date): 
        '''Initializing parameters'''
        self.url = "https://itat.gov.in/judicial/tribunalorders" #initializing a url such that it can be accessible to all the methods
        self.date = order_date  #Input parameter from terminal
        

    def start_requests(self):              
        '''Default method'''
        yield scrapy.Request(url=self.url, callback=self.parse)  #we are calling parse as a callbck to the default method

    def parse(self, response):
        '''Extracts required paramaters to populate the website'''
        
        token = response.css('input[name="csrf_test_name"]::attr(value)').extract_first()
        iq = response.css('input[name="lq"]::attr(value)').extract_first()
        iqc = response.css('input[name="lqc"]::attr(value)').extract_first()
        
        #extracting values only such that empty strings are eliminated 
        city_values = [i for i in  response.css('select[id="bench2"] option::attr(value)').getall()  if i != '' and i != ' ']
        appeal_type = [i for i in response.css('select[id="appeal_type2"] option::attr(value)').getall()  if i != '' and i != ' ']
        
        combinations = list(product(city_values, appeal_type))
        
        for combination in combinations: #looping all the combinations of Bench and Appeal Type 
            needToExtract = {
                    "csrf_test_name": token,
                    "lq": iq,
                    "lqc": iqc,
                    "bench2": combination[0],
                    "appeal_type2": combination[1],
                    "orderdate": self.date,
                    "btnSubmit2": "submit2"}
         
            # Here we are passing the required parameters in a dictionary to raise the form request
            yield scrapy.http.FormRequest(url=self.url, formdata=needToExtract, callback=self.parse_page)
            
            
    def parse_page(self, response):
        '''Finding no. of pages for the results'''
        pages = response.xpath('//*[@id="enclosureform"]/input[@name="btnPage"]/@value').getall()
        for page in pages:
            nextPage = {'btnPage': page}
            #here we are using the prepopulated response to findout the count of no. of pages in results
            yield scrapy.http.FormRequest.from_response(response, formdata=nextPage, callback=self.parse_data)

        
    def parse_data(self, response):
        '''Extracting the result to scrape'''
        rows = response.xpath('//*[@id="content"]/div/table/tr') #from response, we extract rows from the result
        
        def formatdata(elements):
            '''Processing data such that new line, start line escape sequences and space are eliminated '''
            processed = []
            for element in elements:
                el = element.strip('\r\n').strip(' ')
                processed.append(el)
            return processed 
        
        items = AppellateItem() #instantiating items object
        
        if len(rows)>1:
            columns = formatdata(rows[0].css('td::text').getall()) #extracting keys from the first row of the result
            
            for row in rows[1:]:
                
                items[columns[0]] = formatdata(row.css('td::text').getall())[0]
                items[columns[1]] = formatdata(row.css('td::text').getall())[1]
                items[columns[2]] = formatdata(row.css('td::text').getall())[2]
                items[columns[3]] = formatdata(row.css('td::text').getall())[3]
                items[columns[4]] = formatdata(row.css('td::text').getall())[4]
                items[columns[5]] = formatdata(row.css('td::text').getall())[5]
                items[columns[6]] = formatdata(row.css('td::text').getall())[6]
                    
                yield items
                    
            
            
            