import csv
import json
from geopy import geocoders  

class formatCSV():
	"""format csv file, convert address to geo location"""
	def __init__(self, geo_type='google', file_format='csv'):
		if geo_type == "google":	
			self.g = geocoders.Google()  
		elif geo_type == "mapquest":	
			self.g =  geocoders.OpenMapQuest("0Fmjtd%7Cluua2d0r2l%2C2w%3Do5-hf7gl")
		self.rows = []
		self.file_format = file_format
		self.FIELDS = ["Institution - Link to Programs","Institution Name","Address1","Address2","City","State","Zip","inst_url","CEO Name","CEO Title","CEO Phone","CEO Fax","CEO Email","DIOI Name","DIOI Title","DIOI Phone","DIOI Fax","DIOIP","DIOI Email" ]  
	
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

			f = open( 'input.csv', 'r' )
			reader = csv.DictReader( f, fieldnames = self.FIELDS )
			#skip the head row
			next(reader)
			self.rows.extend(reader)
			f.close()
	
	def _geoAddress(self):
			for row in self.rows:
					if (row["lat"] is None or row["lat"] == ""):
							address = "%s %s %s" % (row["Address1"], row["City"], row["State"])             
							try:                
									place, (lat, lng) = self.g.geocode(address,False)[0]
									row["FullAddress"]  = address
									row["lat"]  = lat
									row["lng"]  = lng
									print "%s : completed" % address    
							except Exception, err:
									print "%s : failed" % address, err.message
									row["FullAddress"]  = address
	
	def _writeCSV(self):
			# DictWriter  
			csv_file = open('result.csv', 'wb')  
			writer = csv.DictWriter(csv_file, fieldnames=self.FIELDS)  
			# write header  
			writer.writerow(dict(zip(self.FIELDS, self.FIELDS)))  

			for row in self.rows:
					writer.writerow(row)
					
			csv_file.close() 
			
	
	def _writeJSON(self):
			out = json.dumps( [ row for row in self.rows if  row["lat"] != "" ] )
			#print out
			f = open('result.json','wb')
			f.write(out)
			f.close()

	
if __name__ == '__main__':
    f = formatCSV()
    f.format()
