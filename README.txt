Instructions to run the bot:
1)Download and Install Python.
2)Download and extract the file.
3)open cmd/terminal for windows/ubuntu respectively and go to the extracted folder.
4)then type this and press enter: pip install -r requirements.txt
5)then type this and press enter: python script.py DANCE_TYPE(any event type you want)

To add/change countries or cities:
1)open config.py file in a text editor.
2)add country or city names inside the square bracket between ''
for example lets add berlin to the list of locations:
    BEFORE:
    locations = ['france','paris','spain','portugal','warsaw']

    AFTER:
    locations = ['france','paris','spain','portugal','warsaw','berlin']
Similary you can remove or add any country or city
