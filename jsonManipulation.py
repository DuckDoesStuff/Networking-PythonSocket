import json


# Data to be written
dictionary ={
    "name" : [
        "sathiyajith", 
        "ducky"
    ],
    "rollno" : 56,
    "cgpa" : 8.6,
    "phonenumber" : "9976770500",
    "address" : "111B"
}
  
# Serializing json aka convert python objects to JSON string 
json_object = json.dumps(dictionary, indent = 4)
  
# Open to write
outfile = open("sample.json", "w")
outfile.write(json_object)
outfile.close()

# Open to read
f = open('sample.json', 'r+')

file_data = json.load(f)
file_data['name'].append('John')
f.seek(0)

json.dump(file_data, f, indent=4)

f.close()