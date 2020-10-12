#Import 3 modules! The hashlib is used for a MD5 hash in the keys
import urllib.parse
import requests
import hashlib

#The main link to connect to the api to search a comic book character 
main_api = "http://gateway.marvel.com/v1/public/characters?"
#This is your public key
key = "..."
#You always need to provide a timestamp
timestamp = "1"
#This is your private key 
private_key = "..."
pre_hash = timestamp + private_key + key
#You'll need to use a MD5 hash before you can enter the API
result = hashlib.md5(pre_hash.encode())

print("Excelsior! Wanna find out about your most favorite avanger? Don't hesitate and dive into this beautiful world!")

while True:
    name = input("Which superhero/villain do you want to know more about? (type quit to stop)")
    if name == "quit" or name == "stop" or name == "I'm not mighty":
        break
    #The main url is built here to connect to the API
    url = main_api + urllib.parse.urlencode({"name": name, "ts":timestamp, "apikey":key, "hash":result.hexdigest()})
    #Let's print your own, personalized URL on the screen
    print("URL: " + url)
    #Some more information about the json data in the API
    json_data = requests.get(url).json()
    json_status = json_data["code"]
    #If the request is succesful, you'll receive the information
    if json_status == 200:
        #In this api, if you give in a wrong character, it still gives a success. But there are just 0 
        #total comics. This is some error handling in case you'll give in a wrong character. 
        if json_data["data"]["total"] == 0:
            print("This character doesn't exist")
        #If your character exists, run this code!
        else:
            print("API status: " + str(json_status) + " = You're worthy to lift Thor's hammer!\n")
            print("Name: " + name)
            print("Description: " + str(json_data["data"]["results"][0]["description"]))
            print("How many comics " + name + " appears in: " + str(json_data["data"]["results"][0]["comics"]["available"]))
            print("Here are a couple of comics " + name + " appears in. Enjoy!")
            print("================================================================")
            #Here we loop over the different comics
            for each in json_data["data"]["results"][0]["comics"]["items"]:
                print(each["name"])
            print("================================================================\n")
    #Some error handling of the page! There's only a 409 error available
    elif json_status == 409:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Oops, something went wrong. Did you fill in a superhero name? Remember that you can only fill in a maximum of 100 characters!")
        print("**********************************************\n")
