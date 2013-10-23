#coding:utf-8

import csv
import json
from geopy import geocoders  

class formatCSV():
	"""format csv file, convert address to geo location"""
	def __init__(self, geo_type='google', file_format='json'):
		if geo_type == "google":	
			self.g = geocoders.GoogleV3()  
		elif geo_type == "mapquest":	
			self.g =  geocoders.OpenMapQuest("0Fmjtd%7Cluua2d0r2l%2C2w%3Do5-hf7gl")
		self.rows = []
		self.file_format = file_format
		self.FIELDS = ["City",	"State",	"Zip",	"Country"]  
	
	def format(self):
			self._readCSV()
			self._geoAddress()
			if self.file_format == "csv":    
					self._writeCSV()
			elif self.file_format == "json": 
					self._writeJSON()
					
	def _readCSV(self):
			# append new columns
			self.FIELDS.extend(["FullAddress","lat","lng"])

			f = open( 'fsl.csv', 'r' )
			reader = csv.DictReader( f, fieldnames = self.FIELDS )
			#skip the head row
			next(reader)
			self.rows.extend(reader)
			f.close()
	
	def _geoAddress(self):
			for row in self.rows:
					if (row["lat"] is None or row["lat"] != ""):
							address = self._formatAddress(row)
							#print address
							#continue
							try:                
									place, (lat, lng) = self.g.geocode(address,exactly_one=False)
									row["FullAddress"]  = address
									row["lat"]  = lat
									row["lng"]  = lng
									print "%s : completed" % address    
							except Exception, err:
									print "%s : failed" % address, err.message
									row["FullAddress"]  = address
	def _formatAddress(self,row):
		country = row["Country"]
		country = country.capitalize() if country !="USA" else country
		row["Country"] = country
		
		state = row["State"]
		state = state.capitalize() if len(state)>3 and state.isupper() else state
		row["State"] = state.replace(".","").replace("*","")
		
		city = row["City"]
		city = city.capitalize() if city.isupper() else city
		row["City"] = city.replace(".","").replace("*","")
		
		address = "%s %s %s %s" % (city, state, row["Zip"],  country)  
		address = address.replace(".","").replace("*","")

		return  address.decode("ISO-8859-1")
		
	def _writeCSV(self):
			# DictWriter  
			csv_file = open('result_fsl4.csv', 'wb')  
			writer = csv.DictWriter(csv_file, fieldnames=self.FIELDS)  
			# write header  
			writer.writerow(dict(zip(self.FIELDS, self.FIELDS)))  

			for row in self.rows:
					writer.writerow(row)
					
			csv_file.close() 
			
	
	def _writeJSON(self):
			'''
			for row in self.rows:
				try:  
					out = "%s %s" % out,json.dumps(row)
				except Exception, err:
					pass
			'''
			out = json.dumps(  [ row for row in self.rows if  row["lat"] != "" ] , encoding="ISO-8859-1")
			#print out
			f = open('result_fsl4.json','wb')
			f.write(out)
			f.close()

	
if __name__ == '__main__':
    f = formatCSV()
    f.format()
