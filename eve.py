from urllib import request
import sys

titles = 0
links = 0

try:
    # Getting url from console
    url_param = sys.argv[1]


    if "youtube." in url_param.strip():
        # Opening url
        response = request.urlopen(url_param)
        # Reading the url data in bytes
        url_data = response.read()
        # Converting bytes to string
        url_html = str(url_data)

        with open("entries.txt", "w") as output:

            # Splitting the file into lines by the "{" symbol
            for lines in url_html.split("{"):
                
                # If the line has these 2 indicators in it, then there is a title in this line
                if '"text":"' in lines and '"}],"accessibility":' in lines:
                    # Formatting to get the title and write it in the new file
                    print(str(titles+1)+ ". " + lines[8:-20], file=output)
                    # Adding to the titles counter
                    titles += 1
                
                # If these indicators exist in the line and the number of link 
                # is not equal to the number of titles. Then there is a link present
                elif ',"webPageType":"WEB_PAGE_TYPE_WATCH","rootVe"' in lines and '}},"watchEndpoint":' in lines and links != titles:
                    
                    fslash_pos = lines.index("/")
                    bslash_pos = lines.index("\\")

                    # Formatting to get the link and write it in the new file
                    print("https://www.youtube.com"+lines[fslash_pos:bslash_pos] + "\n", file=output)
                    # Adding to the links counter
                    links += 1

        with open("entries.txt", "r+") as out:
            content = out.read()
            out.seek(0)
            print("Extracted {} entries from this playlist.\n\n".format(titles) + content, file=out)

        print("\nSuccesfully extracted {} entries!\n".format(titles))

    elif "youtube." is not url_param.strip():
        print("\nNot a valid YouTube link.\n")

    else:
        print("\nFailed to extract!\n")

except IndexError:
    print("\nNot a valid YouTube link.\n")