import sys,json

label = sys.argv[1]

data = json.loads(open('out.json').read())

main_file = [record['main_file'] for idx,record in enumerate(data) if str(record['label'])==label][0]

print main_file[:-3]+"_params.py"
