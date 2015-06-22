from scrapy import Item, Field, Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import os

class Family(Item):
    family_id = Field()
    family_name = Field()
    village = Field()
    father_name = Field()
    gp = Field()
    block = Field()
    district = Field()
    average_monthly_income = Field()
    average_monthly_income_num = Field()
    operational_land_type = Field()
    operational_land_type_num = Field()
    own_land_of_iay = Field()
    own_land_of_iay_num = Field()
    social_category = Field()
    social_category_num = Field()
    drinking_water_facility_plain = Field()
    drinking_water_facility_plain_num = Field()
    drinking_water_facility_hilly = Field()
    drinking_water_facility_hilly_num = Field()
    operational_land_size_group = Field()
    operational_land_size_group_num = Field()
    house_type = Field()
    house_type_num = Field()
    availability_of_normal_water = Field()
    availability_of_normal_water_num = Field()
    food_security = Field()
    food_security_num = Field()
    sanitation = Field()
    sanitation_num = Field()
    ownership_of_consumer_durables = Field()
    ownership_of_consumer_durables_num = Field()
    status_of_the_highest_literate_adult = Field()
    status_of_the_highest_literate_adult_num = Field()
    labour_force = Field()
    labour_force_num = Field()
    means_of_livelihood = Field()
    means_of_livelihood_num = Field()
    type_of_indebtedness = Field()
    type_of_indebtedness_num = Field()
    migration = Field()
    migration_num = Field()
    assistance = Field()
    assistance_num = Field()
    children_status = Field()
    children_status_num = Field()

class BlogSpider(CrawlSpider):
    name = 'dt2009'
    district=os.environ['DISTRICT']
    block=os.environ['BLOCK']
    gp=os.environ['GP']
    village=os.environ['VILLAGE']
    start_urls = ["http://www.odishapanchayat.gov.in/dt2009/SearchVillageWise.asp?Submit=Submit&SelDist=" + district + "&SelBlock=" + block + "&SelGP=" + gp + "&SelVillage=" + village + "&gate=1&intsheet=1"]

    rules = (
        Rule(LinkExtractor(allow=['BPLSurveyDetails.asp']), callback='parse_family', follow=True),
        Rule(LinkExtractor(allow=['SearchVillageWise.asp']), follow=True),
    )

    def parse_family(self, response):
        item = Family()

        base = "/html/body/form/div[6]/table/tr/td/table/tr[2]/td[2]/table"
                               
        item['family_name'] = response.xpath("//span/text()")[0].extract().strip()
        if item['family_name'] == u'Village :':
            return

        base += "/tr[3]/td/table"

        item['family_id'] =   response.xpath(base + "/tr[1]/td/table/tr[1]/td[3]/text()")[0].extract().strip()
        item['village'] =     response.xpath(base + "/tr[1]/td/table/tr[1]/td[1]/text()")[0].extract().strip()
        item['father_name'] = response.xpath(base + "/tr[1]/td/table/tr[1]/td[2]/text()")[0].extract().strip()
        item['gp'] =          response.xpath(base + "/tr[1]/td/table/tr[2]/td[1]/text()")[0].extract().strip()
        item['block'] =       response.xpath(base + "/tr[1]/td/table/tr[2]/td[2]/text()")[0].extract().strip()[2:]
        item['district'] =    response.xpath(base + "/tr[1]/td/table/tr[2]/td[3]/text()")[0].extract().strip()

        # get all of the images on the page
        imgs = response.xpath("//img").xpath("@src").extract()
        #print item['family_id'], "Tik values:"
        #for i in range(0, len(imgs)):
        #    if imgs[i] == u'images/SqurewithTik1.jpg':
        #        print i, imgs[i]

        # First set the item to error to identify bad parsing
        item['average_monthly_income'] = "ERROR"
        item['average_monthly_income_num'] = "99"
        # Then look at the image value and determine the proper label
        if imgs[39] == u'images/SqurewithTik1.jpg':
            item['average_monthly_income'] = "Less than 250"
            item['average_monthly_income_num'] = "1"
        if imgs[40] == u'images/SqurewithTik1.jpg':
            item['average_monthly_income'] = "250 - 499"
            item['average_monthly_income_num'] = "2"
        if imgs[41] == u'images/SqurewithTik1.jpg':
            item['average_monthly_income'] = "500 - 1499"
            item['average_monthly_income_num'] = "3"
        if imgs[42] == u'images/SqurewithTik1.jpg':
            item['average_monthly_income'] = "1500 - 2500"
            item['average_monthly_income_num'] = "4"
        if imgs[43] == u'images/SqurewithTik1.jpg':
            item['average_monthly_income'] = "More than 2500"
            item['average_monthly_income_num'] = "5"

        item['operational_land_type'] = "ERROR"
        item['operational_land_type_num'] = "99"
        if imgs[44] == u'images/SqurewithTik1.jpg':
            item['operational_land_type'] = "Owner"
            item['operational_land_type_num'] = "1"
        if imgs[45] == u'images/SqurewithTik1.jpg':
            item['operational_land_type'] = "Tenant"
            item['operational_land_type_num'] = "2"
        if imgs[46] == u'images/SqurewithTik1.jpg':
            item['operational_land_type'] = "Both Owner & Tenant"
            item['operational_land_type_num'] = "3"
        if imgs[47] == u'images/SqurewithTik1.jpg':
            item['operational_land_type'] = "None"
            item['operational_land_type_num'] = "4"

        item['own_land_of_iay'] = "ERROR"
        item['own_land_of_iay_num'] = "99"
        if imgs[48] == u'images/SqurewithTik1.jpg':
            item['own_land_of_iay'] = "Yes"
            item['own_land_of_iay_num'] = "0"
        if imgs[49] == u'images/SqurewithTik1.jpg':
            item['own_land_of_iay'] = "No"
            item['own_land_of_iay_num'] = "1"

        item['social_category'] = "ERROR"
        item['social_category_num'] = "99"
        if imgs[50] == u'images/SqurewithTik1.jpg':
            item['social_category'] = "ST"
            item['social_category_num'] = "1"
        if imgs[51] == u'images/SqurewithTik1.jpg':
            item['social_category'] = "SC"
            item['social_category_num'] = "3"
        if imgs[52] == u'images/SqurewithTik1.jpg':
            item['social_category'] = "OBC"
            item['social_category_num'] = "2"
        if imgs[53] == u'images/SqurewithTik1.jpg':
            item['social_category'] = "Other"
            item['social_category_num'] = "4"

        item['drinking_water_facility_plain'] = "NONE"
        item['drinking_water_facility_plain_num'] = "99"
        item['drinking_water_facility_hilly'] = "NONE"
        item['drinking_water_facility_hilly_num'] = "99"
        # image how the programmer who wrote the display part of this felt.
        if imgs[54] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_plain'] = "1.6 Km"
            item['drinking_water_facility_plain_num'] = "1"
        if imgs[55] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_hilly'] = "> 100 mtrs elevation"
            item['drinking_water_facility_hilly_num'] = "6"
        if imgs[56] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_plain'] = "1.00 - 1.59 Km"
            item['drinking_water_facility_plain_num'] = "2"
        if imgs[57] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_hilly'] = "50-100 mtrs elevation"
            item['drinking_water_facility_hilly_num'] = "7"
        if imgs[58] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_plain'] = "0.50 - 0.99 Km"
            item['drinking_water_facility_plain_num'] = "3"
        if imgs[59] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_hilly'] = "< 50 mtrs elevation"
            item['drinking_water_facility_hilly_num'] = "8"
        if imgs[60] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_plain'] = "Less than 0.50 Km"
            item['drinking_water_facility_plain_num'] = "4"
        if imgs[61] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_hilly'] = "Within the house"
            item['drinking_water_facility_hilly_num'] = "9"
        if imgs[62] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_plain'] = "Within the house"
            item['drinking_water_facility_plain_num'] = "5"

        # Question 1
        item['operational_land_size_group'] = "ERROR"
        item['operational_land_size_group_num'] = "99"
        if imgs[63] == u'images/SqurewithTik1.jpg':
            item['operational_land_size_group'] = "Nil"
            item['operational_land_size_group_num'] = "0"
        if imgs[64] == u'images/SqurewithTik1.jpg':
            item['operational_land_size_group'] = "Less than 1ha.of un-irrigated land(or less than 0.5 ha. of irrigated land)"
            item['operational_land_size_group_num'] = "1"
        if imgs[65] == u'images/SqurewithTik1.jpg':
            item['operational_land_size_group'] = "1ha.-2ha.of un-irrigated land(or 0.5-1.0 ha. of irrigated land)"
            item['operational_land_size_group_num'] = "2"
        if imgs[66] == u'images/SqurewithTik1.jpg':
            item['operational_land_size_group'] = "2 ha.-5 ha.of un-irrigated land(or 1.0.-2.5 ha.of irrigated land)"
            item['operational_land_size_group_num'] = "3"
        if imgs[67] == u'images/SqurewithTik1.jpg':
            item['operational_land_size_group'] = "More than 5ha.of un-irrigated land(or less than 2.5 ha.of irrigated land)"
            item['operational_land_size_group_num'] = "4"

        # Question 2
        item['house_type'] = "ERROR"
        item['house_type_num'] = "99"
        if imgs[68] == u'images/SqurewithTik1.jpg':
            item['house_type'] = "House Less"
            item['house_type_num'] = "0"
        if imgs[69] == u'images/SqurewithTik1.jpg':
            item['house_type'] = "Kutcha"
            item['house_type_num'] = "1"
        if imgs[70] == u'images/SqurewithTik1.jpg':
            item['house_type'] = "Semi-Pucca"
            item['house_type_num'] = "2"
        if imgs[71] == u'images/SqurewithTik1.jpg':
            item['house_type'] = "Pucca"
            item['house_type_num'] = "3"
        if imgs[72] == u'images/SqurewithTik1.jpg':
            item['house_type'] = "Urban Type"
            item['house_type_num'] = "4"

        # Question 3
        item['availability_of_normal_water'] = "ERROR"
        item['availability_of_normal_water_num'] = "99"
        if imgs[73] == u'images/SqurewithTik1.jpg':
            item['availability_of_normal_water'] = "Less than 2"
            item['availability_of_normal_water_num'] = "0"
        if imgs[74] == u'images/SqurewithTik1.jpg':
            item['availability_of_normal_water'] = "2 or more but less than 4"
            item['availability_of_normal_water_num'] = "1"
        if imgs[75] == u'images/SqurewithTik1.jpg':
            item['availability_of_normal_water'] = "4 or more but less than 6"
            item['availability_of_normal_water_num'] = "2"
        if imgs[76] == u'images/SqurewithTik1.jpg':
            item['availability_of_normal_water'] = "6 or more but less than 10"
            item['availability_of_normal_water_num'] = "3"
        if imgs[77] == u'images/SqurewithTik1.jpg':
            item['availability_of_normal_water'] = "10 or more"
            item['availability_of_normal_water_num'] = "4"

        # Question 4
        item['food_security'] = "ERROR"
        item['food_security_num'] = "99"
        if imgs[78] == u'images/SqurewithTik1.jpg':
            item['food_security'] = "Less than one squire meal per day for major part of the year."
            item['food_security_num'] = "0"
        if imgs[79] == u'images/SqurewithTik1.jpg':
            item['food_security'] = "Normally one squire meal per day but less than one squire meal occasionally."
            item['food_security_num'] = "1"
        if imgs[80] == u'images/SqurewithTik1.jpg':
            item['food_security'] = "One squire meal per day through out the year."
            item['food_security_num'] = "2"
        if imgs[81] == u'images/SqurewithTik1.jpg':
            item['food_security'] = "Two squire meal per day with occasionally shortage"
            item['food_security_num'] = "3"
        if imgs[82] == u'images/SqurewithTik1.jpg':
            item['food_security'] = "Enough food through out the year"
            item['food_security_num'] = "4"

        # Question 5
        item['sanitation'] = "ERROR"
        item['sanitation_num'] = "99"
        if imgs[83] == u'images/SqurewithTik1.jpg':
            item['sanitation'] = "Open defection"
            item['sanitation_num'] = "0"
        if imgs[84] == u'images/SqurewithTik1.jpg':
            item['sanitation'] = "Group Latrine with irregular water supply."
            item['sanitation_num'] = "1"
        if imgs[85] == u'images/SqurewithTik1.jpg':
            item['sanitation'] = "Group Latrine with regular water supply."
            item['sanitation_num'] = "2"
        if imgs[86] == u'images/SqurewithTik1.jpg':
            item['sanitation'] = "Clean group latrine with irregular water supply and regular sweeper."
            item['sanitation_num'] = "3"
        if imgs[87] == u'images/SqurewithTik1.jpg':
            item['sanitation'] = "Private latrine"
            item['sanitation_num'] = "4"

        # Question 6
        item['ownership_of_consumer_durables'] = "ERROR"
        item['ownership_of_consumer_durables_num'] = "99"
        if imgs[88] == u'images/SqurewithTik1.jpg':
            item['ownership_of_consumer_durables'] = "Nil"
            item['ownership_of_consumer_durables_num'] = "0"
        if imgs[89] == u'images/SqurewithTik1.jpg':
            item['ownership_of_consumer_durables'] = "Any one"
            item['ownership_of_consumer_durables_num'] = "1"
        if imgs[90] == u'images/SqurewithTik1.jpg':
            item['ownership_of_consumer_durables'] = "Two items only"
            item['ownership_of_consumer_durables_num'] = "2"
        if imgs[91] == u'images/SqurewithTik1.jpg':
            item['ownership_of_consumer_durables'] = "Any three or All items"
            item['ownership_of_consumer_durables_num'] = "3"
        if imgs[92] == u'images/SqurewithTik1.jpg':
            item['ownership_of_consumer_durables'] = "All items and / or ownership of any of the following"
            item['ownership_of_consumer_durables_num'] = "4"

        # Question 7
        item['status_of_the_highest_literate_adult'] = "ERROR"
        item['status_of_the_highest_literate_adult_num'] = "99"
        if imgs[93] == u'images/SqurewithTik1.jpg':
            item['status_of_the_highest_literate_adult'] = "Illiterate"
            item['status_of_the_highest_literate_adult_num'] = "0"
        if imgs[94] == u'images/SqurewithTik1.jpg':
            item['status_of_the_highest_literate_adult'] = "Up to primary (Class V)"
            item['status_of_the_highest_literate_adult_num'] = "1"
        if imgs[95] == u'images/SqurewithTik1.jpg':
            item['status_of_the_highest_literate_adult'] = "Completed Secondary (Passed class X)"
            item['status_of_the_highest_literate_adult_num'] = "2"
        if imgs[96] == u'images/SqurewithTik1.jpg':
            item['status_of_the_highest_literate_adult'] = "Graduate / Professional diploma"
            item['status_of_the_highest_literate_adult_num'] = "3"
        if imgs[97] == u'images/SqurewithTik1.jpg':
            item['status_of_the_highest_literate_adult'] = "Post Graduate / Professional Graduate"
            item['status_of_the_highest_literate_adult_num'] = "4"

        # Question 8
        item['labour_force'] = "ERROR"
        item['labour_force_num'] = "99"
        if imgs[98] == u'images/SqurewithTik1.jpg':
            item['labour_force'] = "Bonded labour"
            item['labour_force_num'] = "0"
        if imgs[99] == u'images/SqurewithTik1.jpg':
            item['labour_force'] = "Female and Child Labour"
            item['labour_force_num'] = "1"
        if imgs[100] == u'images/SqurewithTik1.jpg':
            item['labour_force'] = "Only adult females and no child labour"
            item['labour_force_num'] = "2"
        if imgs[101] == u'images/SqurewithTik1.jpg':
            item['labour_force'] = "Adult males only"
            item['labour_force_num'] = "3"
        if imgs[102] == u'images/SqurewithTik1.jpg':
            item['labour_force'] = "Others"
            item['labour_force_num'] = "4"

        # Question 9
        item['means_of_livelihood'] = "ERROR"
        item['means_of_livelihood_num'] = "99"
        if imgs[103] == u'images/SqurewithTik1.jpg':
            item['means_of_livelihood'] = "Causal labour"
            item['means_of_livelihood'] = "0"
        if imgs[104] == u'images/SqurewithTik1.jpg':
            item['means_of_livelihood'] = "Subsistence Cultivation"
            item['means_of_livelihood'] = "1"
        if imgs[105] == u'images/SqurewithTik1.jpg':
            item['means_of_livelihood'] = "Artisan"
            item['means_of_livelihood'] = "2"
        if imgs[106] == u'images/SqurewithTik1.jpg':
            item['means_of_livelihood'] = "Salary"
            item['means_of_livelihood'] = "3"
        if imgs[107] == u'images/SqurewithTik1.jpg':
            item['means_of_livelihood'] = "Others"
            item['means_of_livelihood'] = "4"

        # Question 10
        item['children_status'] = "ERROR"
        item['children_status_num'] = "99"
        if imgs[108] == u'images/SqurewithTik1.jpg':
            item['children_status'] = "Not going to school and working"
            item['children_status_num'] = "0"
        if imgs[109] == u'images/SqurewithTik1.jpg':
            item['children_status'] = "Going to school and working"
            item['children_status_num'] = "1"
        if imgs[110] == u'images/SqurewithTik1.jpg':
            item['children_status'] = "Going to school and not working"
            item['children_status_num'] = "2"

        # Question 11
        item['type_of_indebtedness'] = "ERROR"
        item['type_of_indebtedness_num'] = "99"
        if imgs[111] == u'images/SqurewithTik1.jpg':
            item['type_of_indebtedness'] = "For daily consumption purpose from informal sources"
            item['type_of_indebtedness_num'] = "0"
        if imgs[112] == u'images/SqurewithTik1.jpg':
            item['type_of_indebtedness'] = "For production purpose from informal sources"
            item['type_of_indebtedness_num'] = "1"
        if imgs[113] == u'images/SqurewithTik1.jpg':
            item['type_of_indebtedness'] = "For other purpose from informal sources"
            item['type_of_indebtedness_num'] = "2"
        if imgs[114] == u'images/SqurewithTik1.jpg':
            item['type_of_indebtedness'] = "Borrowing only Institutional Agencies"
            item['type_of_indebtedness_num'] = "3"
        if imgs[115] == u'images/SqurewithTik1.jpg':
            item['type_of_indebtedness'] = "No indebtedness and possess assets"
            item['type_of_indebtedness_num'] = "4"

        # Question 12
        item['migration'] = "ERROR"
        item['migration_num'] = "99"
        if imgs[116] == u'images/SqurewithTik1.jpg':
            item['migration'] = "Casual work"
            item['migration_num'] = "0"
        if imgs[117] == u'images/SqurewithTik1.jpg':
            item['migration'] = "Seasonal employment"
            item['migration_num'] = "1"
        if imgs[118] == u'images/SqurewithTik1.jpg':
            item['migration'] = "Other forms of livelihood"
            item['migration_num'] = "2"
        if imgs[119] == u'images/SqurewithTik1.jpg':
            item['migration'] = "Non-migrant"
            item['migration_num'] = "3"
        if imgs[120] == u'images/SqurewithTik1.jpg':
            item['migration'] = "Other purpose"
            item['migration_num'] = "4"

        # Question 13
        item['assistance'] = "ERROR"
        item['assistance_num'] = "99"
        if imgs[121] == u'images/SqurewithTik1.jpg':
            item['assistance'] = "Wage employment/TPDS(Targeted Public Distribution System)"
            item['assistance_num'] = "0"
        if imgs[122] == u'images/SqurewithTik1.jpg':
            item['assistance'] = "Self employment"
            item['assistance_num'] = "1"
        if imgs[123] == u'images/SqurewithTik1.jpg':
            item['assistance'] = "Training and Skill upgradation"
            item['assistance_num'] = "2"
        if imgs[124] == u'images/SqurewithTik1.jpg':
            item['assistance'] = "Housing"
            item['assistance_num'] = "3"
        if imgs[125] == u'images/SqurewithTik1.jpg':
            item['assistance'] = "Loan/Subsidy more than Rs. 1 Lakh or no assistance needed"
            item['assistance_num'] = "4"

        yield item
