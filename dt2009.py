from scrapy import Spider, Item, Field, Request

class Family(Item):
    family_id = Field()
    family_name = Field()
    village = Field()
    father_name = Field()
    gp = Field()
    block = Field()
    district = Field()
    average_monthly_income = Field()
    operational_land_type = Field()
    own_land_of_iay = Field()
    social_category = Field()
    drinking_water_facility_plain = Field()
    drinking_water_facility_hilly = Field()
    operational_land_size_group = Field()
    house_type = Field()
    availability_of_normal_water = Field()
    food_security = Field()
    sanitation = Field()
    ownership_of_consumer_durables = Field()
    status_of_the_highest_literate_adult = Field()
    labour_force = Field()
    means_of_livelihood = Field()
    type_of_indebtedness = Field()
    migration = Field()
    assistance = Field()
    children_status = Field()

class BlogSpider(Spider):
    name = 'dt2009'
    cookies={"ASPSESSIONIDCCSDDDRS": "IJJAOOPBEOBBHPBMNBLPCNPP"}
    
    def start_requests(self):
        urls= []
        for i in range(0,1000):
            urls.append(Request("http://www.odishapanchayat.gov.in/dt2009/BPLSurveyDetails.asp?FamilyId=" + str(i) + "&page=Vil", cookies=self.cookies, callback=self.parse))
        return urls

    def parse(self, response):
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
        # Then look at the image value and determine the proper label
        if imgs[39] == u'images/SqurewithTik1.jpg':
            item['average_monthly_income'] = "Less than 250"
        if imgs[40] == u'images/SqurewithTik1.jpg':
            item['average_monthly_income'] = "250 - 499"
        if imgs[41] == u'images/SqurewithTik1.jpg':
            item['average_monthly_income'] = "500 - 1499"
        if imgs[42] == u'images/SqurewithTik1.jpg':
            item['average_monthly_income'] = "1500 - 2500"
        if imgs[43] == u'images/SqurewithTik1.jpg':
            item['average_monthly_income'] = "More than 2500"

        item['operational_land_type'] = "ERROR"
        if imgs[44] == u'images/SqurewithTik1.jpg':
            item['operational_land_type'] = "Owner"
        if imgs[45] == u'images/SqurewithTik1.jpg':
            item['operational_land_type'] = "Tenant"
        if imgs[46] == u'images/SqurewithTik1.jpg':
            item['operational_land_type'] = "Both Owner & Tenant"
        if imgs[47] == u'images/SqurewithTik1.jpg':
            item['operational_land_type'] = "None"

        item['own_land_of_iay'] = "ERROR"
        if imgs[48] == u'images/SqurewithTik1.jpg':
            item['own_land_of_iay'] = "Yes"
        if imgs[49] == u'images/SqurewithTik1.jpg':
            item['own_land_of_iay'] = "No"

        item['social_category'] = "ERROR"
        if imgs[50] == u'images/SqurewithTik1.jpg':
            item['social_category'] = "ST"
        if imgs[51] == u'images/SqurewithTik1.jpg':
            item['social_category'] = "SC"
        if imgs[52] == u'images/SqurewithTik1.jpg':
            item['social_category'] = "OBC"
        if imgs[53] == u'images/SqurewithTik1.jpg':
            item['social_category'] = "Other"

        item['drinking_water_facility_plain'] = "NONE"
        item['drinking_water_facility_hilly'] = "NONE"
        # image how the programmer who wrote the display part of this felt.
        if imgs[54] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_plain'] = "1.6 Km"
        if imgs[55] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_hilly'] = "> 100 mtrs elevation"
        if imgs[56] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_plain'] = "1.00 - 1.59 Km"
        if imgs[57] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_hilly'] = "50-100 mtrs elevation"
        if imgs[58] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_plain'] = "0.50 - 0.99 Km"
        if imgs[59] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_hilly'] = "< 50 mtrs elevation"
        if imgs[60] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_plain'] = "Less than 0.50 Km"
        if imgs[61] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_hilly'] = "Within the house"
        if imgs[62] == u'images/SqurewithTik1.jpg':
            item['drinking_water_facility_plain'] = "Within the house"

        # Question 1
        item['operational_land_size_group'] = "ERROR"
        if imgs[63] == u'images/SqurewithTik1.jpg':
            item['operational_land_size_group'] = "Nil"
        if imgs[64] == u'images/SqurewithTik1.jpg':
            item['operational_land_size_group'] = "Less than 1ha.of un-irrigated land(or less than 0.5 ha. of irrigated land)"
        if imgs[65] == u'images/SqurewithTik1.jpg':
            item['operational_land_size_group'] = "1ha.-2ha.of un-irrigated land(or 0.5-1.0 ha. of irrigated land)"
        if imgs[66] == u'images/SqurewithTik1.jpg':
            item['operational_land_size_group'] = "2 ha.-5 ha.of un-irrigated land(or 1.0.-2.5 ha.of irrigated land)"
        if imgs[67] == u'images/SqurewithTik1.jpg':
            item['operational_land_size_group'] = "More than 5ha.of un-irrigated land(or less than 2.5 ha.of irrigated land)"

        # Question 2
        item['house_type'] = "ERROR"
        if imgs[68] == u'images/SqurewithTik1.jpg':
            item['house_type'] = "House Less"
        if imgs[69] == u'images/SqurewithTik1.jpg':
            item['house_type'] = "Kutcha"
        if imgs[70] == u'images/SqurewithTik1.jpg':
            item['house_type'] = "Semi-Pucca"
        if imgs[71] == u'images/SqurewithTik1.jpg':
            item['house_type'] = "Pucca"
        if imgs[72] == u'images/SqurewithTik1.jpg':
            item['house_type'] = "Urban Type"

        # Question 3
        item['availability_of_normal_water'] = "ERROR"
        if imgs[73] == u'images/SqurewithTik1.jpg':
            item['availability_of_normal_water'] = "Less than 2"
        if imgs[74] == u'images/SqurewithTik1.jpg':
            item['availability_of_normal_water'] = "2 or more but less than 4"
        if imgs[75] == u'images/SqurewithTik1.jpg':
            item['availability_of_normal_water'] = "4 or more but less than 6"
        if imgs[76] == u'images/SqurewithTik1.jpg':
            item['availability_of_normal_water'] = "6 or more but less than 10"
        if imgs[77] == u'images/SqurewithTik1.jpg':
            item['availability_of_normal_water'] = "10 or more"

        # Question 4
        item['food_security'] = "ERROR"
        if imgs[78] == u'images/SqurewithTik1.jpg':
            item['food_security'] = "Less than one squire meal per day for major part of the year."
        if imgs[79] == u'images/SqurewithTik1.jpg':
            item['food_security'] = "Normally one squire meal per day but less than one squire meal occasionally."
        if imgs[80] == u'images/SqurewithTik1.jpg':
            item['food_security'] = "One squire meal per day through out the year."
        if imgs[81] == u'images/SqurewithTik1.jpg':
            item['food_security'] = "Two squire meal per day with occasionally shortage"
        if imgs[82] == u'images/SqurewithTik1.jpg':
            item['food_security'] = "Enough food through out the year"

        # Question 5
        item['sanitation'] = "ERROR"
        if imgs[83] == u'images/SqurewithTik1.jpg':
            item['sanitation'] = "Open defection"
        if imgs[84] == u'images/SqurewithTik1.jpg':
            item['sanitation'] = "Group Latrine with irregular water supply."
        if imgs[85] == u'images/SqurewithTik1.jpg':
            item['sanitation'] = "Group Latrine with regular water supply."
        if imgs[86] == u'images/SqurewithTik1.jpg':
            item['sanitation'] = "Clean group latrine with irregular water supply and regular sweeper."
        if imgs[87] == u'images/SqurewithTik1.jpg':
            item['sanitation'] = "Private latrine"

        # Question 6
        item['ownership_of_consumer_durables'] = "ERROR"
        if imgs[88] == u'images/SqurewithTik1.jpg':
            item['ownership_of_consumer_durables'] = "Nil"
        if imgs[89] == u'images/SqurewithTik1.jpg':
            item['ownership_of_consumer_durables'] = "Any one"
        if imgs[90] == u'images/SqurewithTik1.jpg':
            item['ownership_of_consumer_durables'] = "Two items only"
        if imgs[91] == u'images/SqurewithTik1.jpg':
            item['ownership_of_consumer_durables'] = "Any three or All items"
        if imgs[92] == u'images/SqurewithTik1.jpg':
            item['ownership_of_consumer_durables'] = "All items and / or ownership of any of the following"

        # Question 7
        item['status_of_the_highest_literate_adult'] = "ERROR"
        if imgs[93] == u'images/SqurewithTik1.jpg':
            item['status_of_the_highest_literate_adult'] = "Illiterate"
        if imgs[94] == u'images/SqurewithTik1.jpg':
            item['status_of_the_highest_literate_adult'] = "Up to primary (Class V)"
        if imgs[95] == u'images/SqurewithTik1.jpg':
            item['status_of_the_highest_literate_adult'] = "Completed Secondary (Passed class X)"
        if imgs[96] == u'images/SqurewithTik1.jpg':
            item['status_of_the_highest_literate_adult'] = "Graduate / Professional diploma"
        if imgs[97] == u'images/SqurewithTik1.jpg':
            item['status_of_the_highest_literate_adult'] = "Post Graduate / Professional Graduate"

        # Question 8
        item['labour_force'] = "ERROR"
        if imgs[98] == u'images/SqurewithTik1.jpg':
            item['labour_force'] = "Bonded labour"
        if imgs[99] == u'images/SqurewithTik1.jpg':
            item['labour_force'] = "Female and Child Labour"
        if imgs[100] == u'images/SqurewithTik1.jpg':
            item['labour_force'] = "Only adult females and no child labour"
        if imgs[101] == u'images/SqurewithTik1.jpg':
            item['labour_force'] = "Adult males only"
        if imgs[102] == u'images/SqurewithTik1.jpg':
            item['labour_force'] = "Others"

        # Question 9
        item['means_of_livelihood'] = "ERROR"
        if imgs[103] == u'images/SqurewithTik1.jpg':
            item['means_of_livelihood'] = "Causal labour"
        if imgs[104] == u'images/SqurewithTik1.jpg':
            item['means_of_livelihood'] = "Subsistence Cultivation"
        if imgs[105] == u'images/SqurewithTik1.jpg':
            item['means_of_livelihood'] = "Artisan"
        if imgs[106] == u'images/SqurewithTik1.jpg':
            item['means_of_livelihood'] = "Salary"
        if imgs[107] == u'images/SqurewithTik1.jpg':
            item['means_of_livelihood'] = "Others"

        # Question 10
        item['children_status'] = "ERROR"
        if imgs[108] == u'images/SqurewithTik1.jpg':
            item['children_status'] = "Not going to school and working"
        if imgs[109] == u'images/SqurewithTik1.jpg':
            item['children_status'] = "Going to school and working"
        if imgs[110] == u'images/SqurewithTik1.jpg':
            item['children_status'] = "Going to school and not working"

        # Question 11
        item['type_of_indebtedness'] = "ERROR"
        if imgs[111] == u'images/SqurewithTik1.jpg':
            item['type_of_indebtedness'] = "For daily consumption purpose from informal sources"
        if imgs[112] == u'images/SqurewithTik1.jpg':
            item['type_of_indebtedness'] = "For production purpose from informal sources"
        if imgs[113] == u'images/SqurewithTik1.jpg':
            item['type_of_indebtedness'] = "For other purpose from informal sources"
        if imgs[114] == u'images/SqurewithTik1.jpg':
            item['type_of_indebtedness'] = "Borrowing only Institutional Agencies"
        if imgs[115] == u'images/SqurewithTik1.jpg':
            item['type_of_indebtedness'] = "No indebtedness and possess assets"

        # Question 12
        item['migration'] = "ERROR"
        if imgs[116] == u'images/SqurewithTik1.jpg':
            item['migration'] = "Casual work"
        if imgs[117] == u'images/SqurewithTik1.jpg':
            item['migration'] = "Seasonal employment"
        if imgs[118] == u'images/SqurewithTik1.jpg':
            item['migration'] = "Other forms of livelihood"
        if imgs[119] == u'images/SqurewithTik1.jpg':
            item['migration'] = "Non-migrant"
        if imgs[120] == u'images/SqurewithTik1.jpg':
            item['migration'] = "Other purpose"

        # Question 13
        item['assistance'] = "ERROR"
        if imgs[121] == u'images/SqurewithTik1.jpg':
            item['assistance'] = "Wage employment/TPDS(Targeted Public Distribution System)"
        if imgs[122] == u'images/SqurewithTik1.jpg':
            item['assistance'] = "Self employment"
        if imgs[123] == u'images/SqurewithTik1.jpg':
            item['assistance'] = "Training and Skill upgradation"
        if imgs[124] == u'images/SqurewithTik1.jpg':
            item['assistance'] = "Housing"
        if imgs[125] == u'images/SqurewithTik1.jpg':
            item['assistance'] = "Loan/Subsidy more than Rs. 1 Lakh or no assistance needed"

        yield item
