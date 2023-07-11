"""tmp = True
chunk = []
for line in f:
    #print(line)
    if line == "BEGIN:VEVENT\n":
        tmp = True
        
    if line == "END:VEVENT\n":
        tmp = False

    if tmp:
        chunk.append(f.readline())
    
    if not tmp:
        chunks.append(chunk)
        chunk = []

    if chunk == []:
        continue"""
    