import pandas as pd
import glob


files = glob.glob("*.txt")

df = pd.DataFrame(columns=['Organization', 'Extension', 'Path', 'Score', 'URL'])
for file in files:
    my_file = open(file, "r")
      
    lines = my_file.read()
      
    data_into_list = lines.split("\n")
    
    i = 0
    data = []
    while i < len(data_into_list):
        if data_into_list[i][0:16] == 'Found result for':
            res = [file.split('.')[0]]
            
            tmp = data_into_list[i]
            tmp = tmp.split(':')
            res.append(tmp[1])
            
            tmp = data_into_list[i + 2]
            tmp = tmp.split(':')
            res.append(tmp[1])
            
            tmp = data_into_list[i + 3]
            tmp = tmp.split(':')
            res.append(tmp[1])
            
            tmp = data_into_list[i + 4]
            tmp = tmp.split(':')
            res.append(':'.join(tmp[1:]))
            
            i += 5
            df.loc[len(df)] = res
        else:
            i += 1
    
  
# printing the data
df.to_csv('newdata.csv')
#print(data)
#my_file.close()