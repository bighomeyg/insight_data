import glob


years=["2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014"]

old_abbrevs=["CRD", "TAM", "HTX", "RAM", "RAV", "RAI", "OTI", "GNB", "CLT", "NOR", "NWE", "JAX", "SDG", "KAN"]             

relocated_teams={'CRD' : 'ARI', 'RAV' : 'BAL', 'GNB' : 'GB', 'HTX' : 'HOU', 'CLT' : 'IND', 'JAX' : 'JAC', 'KAN' : 'KC', 'NWE' : 'NE', 'NOR' : 'NO', 'RAI' : 'OAK', 'RAM' : 'STL', 'TAM' : 'TB', 'OTI' : 'TEN', 'SDG' : 'SD'}

points={"Safety" : -2, "Field Goal" : 3, "Touchdown" : 6}

#Build counters
number_of_drives=[]
total_score=[]
for n in range(0,100):
	number_of_drives.append(0)
	total_score.append(0)


for year in years:
	for path in glob.glob(''.join(year + "/*drives.csv")):
		filename=open(path, "r")
		
 
		for line in filename:
			first_los=line.split(",")[4]
			offense=line.split(",")[0]
			result=line.split(",")[7].strip()
			if first_los == "50":
				to_go = 50
			if first_los != "50":
				try:
					side_of_field=line.split(",")[4].split(" ")[0]
					yardline = int(line.split(",")[4].split(" ")[1])
					if side_of_field in old_abbrevs:
						side_of_field = relocated_teams.get(side_of_field)
				except IndexError:
					continue
				if side_of_field == offense:
					to_go=(100-int(yardline))
				if side_of_field != offense:
					to_go=yardline
			if first_los == "None":
				continue
			number_of_drives[to_go]+=1
			if result in points.keys():
				total_score[to_go]+=points.get(result)

		
		
print number_of_drives
print total_score

for i in range(1,100):
	yard_value=float(total_score[i])/float(number_of_drives[i])
	print i, "\t", yard_value
	#print number_of_drives[i]