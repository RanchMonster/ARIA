import json 
import os
folder=os.path.dirname(os.path.abspath(__file__))
file_path=os.path.join(folder,'list.json')
def get_list(list=None):
    file= open(file_path)
    data =json.load(file)
    file.close()
    if list is not None:
        return data[list]
    else:
        return data
    
def add_item(list=None, item=None):
    if list not in get_list():
        return "list not found please make a list frist"
    elif list is not None:
        data=get_list()
        data[list].append(item)

        file= open(file_path,"w")
        json.dump(data,file)
        file.close()
        return item+"was added to "+list+" list"
    else:
        return "item must have a name"

def remove_item(list=None, item=None):
    data=get_list()
    try:
        if item in data[list]:
            
                data[list].remove(item)
                file= open(file_path,"w")
                json.dump(data,file)
                file.close()
                return item+"was removed from "+list+" list"
        else:
            return "item not in list or the list does not exist"
    except(KeyError):
        return "no list was found"
        
def create_list(list=None):
    data=get_list()
    try:
        if list not in data and list !=None:
            file =open(file_path,"w")
            place_holder=[]
            data[list]= place_holder
            json.dump(data,file)
            return "list has been made"
        elif list in data:
            return "list Already exist"
        else:
            return "list must have name"
    except:
        return "error could not make list"
    

def destroy_list(list=None):
    data=get_list()
    try:
        data.pop(list)
        file= open(file_path,"w")
        json.dump(data,file)
        file.close
    except:
        return "failed to get list"
    
def PassList(list=None,new_list=None):
    data=get_list()
    if list in data:data.pop(list)
    if list==None or new_list==None:Exception("list and new list name required")
    data[list]=new_list
    file= open(file_path,"w")
    json.dump(data,file)
    
        
                