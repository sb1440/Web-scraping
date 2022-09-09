We have scraped the following website "https://itat.gov.in/judicial/tribunalorders". 

The objective of this project is that given a Date of order to the Search by Order Date form available in the given url, we have to return the results of all the possible combinations of Bench and Appeal Type in .json format.

We have used anaconda distribution to implement this project.

After installing necessary libraries, the first command to execute is "scrapy startproject project_name" , we have named it as appellate.
Then the project directory is created.


Next step is to create a crawler object in the spider folder. <br/>
Steps taken to create a crawler:

1. Inherit the scrapy.spiders.Spider class to create a crawler object and name the crawler.
2. Inorder to pass the Date of order as argument at the time of command execution, I have declared it in self.__init__() of spider class and initialize the url too.
3. Raise a simple scrapy.Request and extract all the values for Benches and Appeal Type columns.
4. For each pair<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;raised a http form request and counted the no. of pages for the results
5. For every page<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;for every record in the result<br/> 
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;extracted the key:value pair
    
    
We have defined the Item class to create a container to store the extracted data and also created an Item pipeline to store the extracted data into a json file.
