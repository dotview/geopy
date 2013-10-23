import csv
import json
from geopy import geocoders  


class formatCSV():
	"""format csv file, convert address to geo location"""
	def __init__(self, geo_type='google', file_format='csv'):
		if geo_type == "google":	
			#self.g = geocoders.Google(api_key='AIzaSyAia7GRtA7wyuaz1r4CIVHO-0J4CROVTHI') 
			self.g = geocoders.GoogleV3()  			
		elif geo_type == "mapquest":	
			self.g =  geocoders.OpenMapQuest("0Fmjtd%7Cluua2d0r2l%2C2w%3Do5-hf7gl")
		self.rows = []
		self.file_format = file_format
		self.FIELDS = ["dealerId",	"dealerName",	"productid",	"address",	"telephone",	"website",	"latitude",	"longitude"]  
	
	def format(self):
			self._readCSV()
			self._geoAddress()
			if self.file_format == "csv":    
					self._writeCSV()
			elif self.file_format == "json": 
					self._writeJSON()
					
	def _readCSV(self):
			# append new columns
			self.FIELDS.extend(["latitude","longitude"])

			f = open( 'dealer.csv', 'r' )
			reader = csv.DictReader( f, fieldnames = self.FIELDS )
			#skip the head row
			next(reader)
			self.rows.extend(reader)
			f.close()
	
	def _geoAddress(self):
			for row in self.rows:
					if (row["latitude"] is None or row["latitude"] == ""):
							address = row["address"]
							try:                
									place, (lat, lng) = self.g.geocode(address,False)
									row["latitude"]  = lat
									row["longitude"]  = lng
									print "update g3k_dealers set latitude='%s',longitude='%s' where id='%s'" % (lat,lng, row["dealerId"]  )  
									#print "%s : completed" % address    
							except Exception, err:
									print "%s : failed" % address, err
									
							#return
	def _writeCSV(self):
			# DictWriter  
			csv_file = open('dealer_result.csv', 'wb')  
			writer = csv.DictWriter(csv_file, fieldnames=self.FIELDS)  
			# write header  
			writer.writerow(dict(zip(self.FIELDS, self.FIELDS)))  

			for row in self.rows:
					writer.writerow(row)
					
			csv_file.close() 
			
	
	def _writeJSON(self):
			out = json.dumps( [ row for row in self.rows if  row["lat"] != "" ] )
			#print out
			f = open('ta_result.json','wb')
			f.write(out)
			f.close()

	
if __name__ == '__main__':
    f = formatCSV()
    f.format()
