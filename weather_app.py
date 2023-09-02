from flet import *
# import json
import requests

def main(page: Page):
    page.horizontal_alignment = 'center'
    page.window_width = 445
    page.window_height = 585
    page.window_min_width = 445
    page.window_min_height = 585
    # page.bgcolor = 'white'

    def get_weather(city): # this function takes city as a string and returs the data from the API
        link = f'http://api.weatherapi.com/v1/current.json?key=8c1a30ab149f491884c123143230108&q={city}'
        try:
            r = requests.get(link).json()
            return r
        except: return "network error"
    
    def error(error): #function for showing error messages
        page.snack_bar = SnackBar(Text(error, text_align='center', size=20), bgcolor=colors.ERROR)
        page.snack_bar.open = True
        page.update()
    
    def submit(e):
        city.focus()
        if city.value != '':
            report = get_weather(city.value) # get weather report from the api with the city present in text field

            if 'No matching location found' in str(report):
                error("Incorrect City") # show error snack bar
                return
            
            if report == 'network error':
                error('Network error') # shows error snack bar
                return
            
            # We need to check how the api sends weather so we can use it
            # for that paste the link with city name in google :  https://api.weatherapi.com/v1/current.json?key=8c1a30ab149f491884c123143230108&q=london

            wind_directions = { # dictionary for wind directions that are manipulated from the value in the api response e.g. NNE
                'N': 'North',
                'NW': 'Northwest',
                'NNW': 'North-Northwest',
                'NE': 'Northeast',
                'NNE': 'North-Northeast',
                'S': 'South',
                'SW': 'Southwest',
                'SWW': 'South-Southwest',
                'SE': 'Southeast',
                'SSE': 'South-Southeast',
                'W': 'West',
                'WNW': 'West-Northwest',
                'WSW': 'West-Southwest',
                'E': 'East',
                'ENE': 'East-Northeast',
                'ESE': 'East-Southeast'
            }

            def swap_temp(e):
                if e.control.data == 'C':
                    weather.content.controls[1].controls[1].controls[3].controls[1].value = f"{report['current']['temp_f']} °F"
                    e.control.data = 'F'
                else:
                    weather.content.controls[1].controls[1].controls[3].controls[1].value = f"{report['current']['temp_c']} °C"
                    e.control.data = 'C'
                page.update()

            #now towards the main logic for showing the weather
            weather.content = Column(
            [
                Row(), #for spacing
                Row(
                [
                    Column(width=4), #for spacing
                    Column(
                        [
                            Text(
                                spans=[
                                    TextSpan('City: ', style=TextStyle(weight='bold', size=18)), 
                                    TextSpan(report['location']['name'], style=TextStyle(size=17)) # to get the city
                                ]
                            ),

                            Text(
                                spans=[
                                    TextSpan('Region: ', style=TextStyle(weight='bold', size=18)), 
                                    TextSpan(report['location']['region'], style=TextStyle(size=17)) 
                                ]
                            ),

                            Text(
                                spans=[
                                    TextSpan('Country: ', style=TextStyle(weight='bold', size=18)), 
                                    TextSpan(report['location']['country'], style=TextStyle(size=17)) 
                                ]
                            ),

                            Row([
                                # a button to swap between C and F
                                IconButton( icons.SWAP_HORIZ, on_click=swap_temp, data='C'), 
                                Text(f"{report['current']['temp_c']} °C", size= 40, weight='bold', width=160),

                                # images (flat icons) of sun or moon from google based on the value of 'is_day' key in api response dictionary https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJG1UZgY9gWlfMuTqTC25NpkU2V-RGfhEpXw&usqp=CAU https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRNSUclqheK40bl2XJZ1UmpM0FX3CTKIsJ5eFlQSwOqGtXLez83CsdPTvNGc-BQTK9DTo&usqp=CAU
                                # Image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5n0cu3OEjG6s-QU7Or7iDH4EVojrY7JhJeg&usqp=CAU' if report['current']['is_day'] == 1 else 'https://images.vexels.com/media/users/3/153630/isolated/lists/f157393ba1bbd3471c532c9516b894f2-crescent-moon-flat-icon.png', width=60, height=60, fit=ImageFit.CONTAIN)
                                Image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRj88iBwJ8PbzRZOKOn73Xzg1I31UVRqspkHA&usqp=CAU' if report['current']['is_day'] == 1 else 'https://images.vexels.com/media/users/3/153630/isolated/lists/f157393ba1bbd3471c532c9516b894f2-crescent-moon-flat-icon.png', width=60, height=60, fit=ImageFit.CONTAIN)
                                # Text("Day" if report['current']['is_day']==1 else "Night", size=40)
                            ]),

                            Text(
                                spans=[
                                    TextSpan('Condition: ', style=TextStyle(weight='bold', size=18)), 
                                    TextSpan(report['current']['condition']['text'], style=TextStyle(size=17)) 
                                ]
                            ),

                            Text(
                                spans=[
                                    TextSpan('Local time: ', style=TextStyle(weight='bold', size=18)), 
                                    TextSpan(report['location']['localtime'].split()[1], style=TextStyle(size=17)) 
                                ]
                            ),

                            Text(
                                spans=[
                                    TextSpan('Wind speed: ', style=TextStyle(weight='bold', size=18)), 
                                    TextSpan(f"{report['current']['wind_kph']} kph", style=TextStyle(size=17)),  
                                    TextSpan('    Gusts: ', style=TextStyle(weight='bold', size=18)), 
                                    TextSpan(f"{report['current']['gust_kph']} kph", style=TextStyle(size=17)) 
                                ]
                            ),

                            Text(
                                spans=[
                                    TextSpan('Wind direction: ', style=TextStyle(weight='bold', size=18)), 
                                    TextSpan(wind_directions.get(report['current']['wind_dir']), style=TextStyle(size=17)) 
                                ]
                            ),

                            Text(
                                spans=[
                                    TextSpan('Rainfall: ', style=TextStyle(weight='bold', size=18)), 
                                    TextSpan(f"{report['current']['precip_mm']} mm", style=TextStyle(size=17)) 
                                ]
                            ),

                        ]
                    )
                ]
                )
            ],
            width=400,
            height=400
            )
            page.update() # update after making changes

    #appbar
    page.appbar = AppBar(
        title = Text('Weather App', weight='bold', size=30),
        bgcolor = colors.PRIMARY_CONTAINER,
        center_title = True
    )

    # textfield for getting the city from the user
    city = TextField(
        hint_text="Enter a city",
        # hint_style=TextStyle(color='black'),
        width=235,
        text_size=20,
        height=60,
        border_color='white',
        cursor_color='white',
        focused_border_color='white',
        on_submit=submit
    )

    # button for submitting API request
    button = OutlinedButton(
        content=Text('Get Weather', size=18, color='white'),
        on_click=submit,
        height=60,
        style=ButtonStyle(shape=RoundedRectangleBorder(radius=6))
    )
    # The text field and button will be shown in a row

    weather = Card(width=410, height=400) # the main card that will show weather

    page.add(Row([city, button], alignment=MainAxisAlignment.SPACE_BETWEEN, width=400), weather)


app(main)