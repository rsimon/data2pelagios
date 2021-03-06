import csv

def esc(chars):
  return chars.replace('"','\'').replace('\\','')
  
def toInt(chars):
  # Some dates have '+' appended - we want to keep the date, but strip the +
  normalized = chars[0:len(chars) - 1] if chars.endswith('+') else chars
    
  try:
    toInt = int(normalized)
    return toInt
  except ValueError:
    return None

with open('PortolanPRECURSORS.csv') as f:
  output = open('portolanPRECURSORS.ttl', 'w')
  
  output.write('@prefix dcterms: <http://purl.org/dc/terms/> .\n')
  output.write('@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n')
  output.write('@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .\n')
  output.write('@prefix lawd: <http://lawd.info/ontology/> .\n')
  output.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
  output.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n')
  output.write('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n')

  reader = csv.reader(f, delimiter=';')
  next(reader, None)  # skip the header
  
  cnt_all = 0
  cnt_invalid = 0
  idx = 0
  
  for row in reader:
    idx += 1
    
    if len(row) < 11:
      cnt_invalid += 1
    else:
      cnt_all += 1
    
      sorting = row[0]
      modernName = row[2]
      nameOnChart = row[3]
      dateFirstSeen = toInt(row[5])
      dateLastSeen = toInt(row[10])
      coastalSection = row[4]
      chartMakerBlack = row[6]
      chartMakerRed = row[8]
      comments = row[23]
    
      output.write('<http://www.maphistory.info/portolans/record/' + str(idx) + '-' + sorting + '> a lawd:Place ;\n')
      output.write('  rdfs:label "' + esc(nameOnChart) + '" ;\n')
      
      description = 'Portolan chart name'
      if (coastalSection):
        description += ', coastal section ' + coastalSection
      else:
        description += '.'
        
      if (chartMakerBlack):
        description += ' Chartmaker (black name): ' + chartMakerBlack
      if (chartMakerRed):
        description += ', chartmaker (red name): ' + chartMakerRed + '.'
      else:
        description += '.'
        
      if (comments):
        description += ' (' + comments + ')'
        
      output.write('  dcterms:description "' + esc(description) + '" ;\n')
    
      if (dateFirstSeen and dateLastSeen):
        output.write('  dcterms:temporal "<' + str(dateFirstSeen) + '/' + str(dateLastSeen) + '>" ;\n')
      elif (dateFirstSeen):
        output.write('  dcterms:temporal "' + str(dateFirstSeen) + '" ;\n')
    
      if (modernName):
        output.write('  lawd:hasName [ lawd:primaryForm "' + esc(modernName) + '" ] ;\n')
      
      output.write('  .\n\n')
    
  print('Converted ' +  str(cnt_all) + ' places, ' + str(cnt_invalid) + ' invalid lines')
  output.close()
