import csv 

final_references_withlabel = []
final_references_nolabel = []

## Processing each csv and extracting references
with open('D:/dev/mdpi-scraper/sample/temp/education.csv','r',encoding="utf-8") as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        if len(row) == 0: continue
        final_references_withlabel.append([row[0],row[1]])
        final_references_nolabel.append([row[0]])
    
with open('D:/dev/mdpi-scraper/sample/temp/engproc.csv','r',encoding="utf-8") as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        if len(row) == 0: continue
        final_references_withlabel.append([row[0],row[1]])
        final_references_nolabel.append([row[0]])
    
with open('D:/dev/mdpi-scraper/sample/temp/smartcities.csv','r',encoding="utf-8") as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        if len(row) == 0: continue
        final_references_withlabel.append([row[0],row[1]])
        final_references_nolabel.append([row[0]])
    
with open('D:/dev/mdpi-scraper/sample/temp/societies.csv','r',encoding="utf-8") as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        if len(row) == 0: continue
        final_references_withlabel.append([row[0],row[1]])
        final_references_nolabel.append([row[0]])
    
with open('D:/dev/mdpi-scraper/sample/temp/socsci.csv','r',encoding="utf-8") as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        if len(row) == 0: continue
        final_references_withlabel.append([row[0],row[1]])
        final_references_nolabel.append([row[0]])
    
with open('D:/dev/mdpi-scraper/sample/temp/technologies.csv','r',encoding="utf-8") as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        if len(row) == 0: continue
        final_references_withlabel.append([row[0],row[1]])
        final_references_nolabel.append([row[0]])
       
       
## Saving into final files
with open('D:/dev/mdpi-scraper/sample/final_references_withlabel.csv','w', newline='',encoding="utf-8") as f:
    csvwriter = csv.writer(f)
    for ref in final_references_withlabel:
        csvwriter.writerow(ref)

with open('D:/dev/mdpi-scraper/sample/final_references_nolabel.csv','w', newline='',encoding="utf-8") as f:
    csvwriter = csv.writer(f)
    for ref in final_references_nolabel:
        csvwriter.writerow(ref)