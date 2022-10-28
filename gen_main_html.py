#!/usr/bin/python
# -*- coding: utf-8 -*-


class Gen_main:
    def __init__(self):
        return


    def gen_body_head(self, place):

        if len(place) == 1:
            index_body_head = '''<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>My Place Watching Over Site</title>
            <meta name="viewport" content="width=device-width">
            <link href="https://fonts.googleapis.com/earlyaccess/nicomoji.css" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css?family=M+PLUS+Rounded+1c" rel="stylesheet">
            <link rel="stylesheet" href="css/style.css">
        </head>

        <body>
            <div class="container">
                <header>
                    <h1>My Place Watching Over Site</h1>
                </header>

                <section class="information">
                    <h1>Event records {PLACE0}</h1>
                </section>
            </div>'''.format(PLACE0 = place[0])

        else:
            index_body_head = '''<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>My Place Watching Over Site</title>
            <meta name="viewport" content="width=device-width">
            <link href="https://fonts.googleapis.com/earlyaccess/nicomoji.css" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css?family=M+PLUS+Rounded+1c" rel="stylesheet">
            <link rel="stylesheet" href="css/style.css">
        </head>

        <body>
            <div class="container">
                <header>
                    <h1>My Place Watching Over Site</h1>
                </header>

                <section class="information">
                    <h1>Event records from {PLACE0} to {PLACE_END}</h1>
                </section>
            </div>'''.format(PLACE0 = place[0],
                                PLACE_END = place[-1] )
        
        return index_body_head


    def gen_mid_body(self, place):

        each_body = []

        for i in range(len(place)):
            each_body.append('''        <div class="section2">
            <h2>{PLACE}</h2>
            <img src="img/place{I}.jpg" width="500">
            <ol>
                <li><a href="Place{I}/place{I}-1.html" target="_blank">latest</a></li>
                <li><a href="Place{I}/place{I}-2.html" target="_blank">1 time ago</a></li>
                <li><a href="Place{I}/place{I}-3.html" target="_blank">2 times ago</a></li>   
                <li><a href="Place{I}/place{I}-4.html" target="_blank">3 times ago</a></li>
                <li><a href="Place{I}/place{I}-5.html" target="_blank">4 times ago</a></li>
                <li><a href="Place{I}/place{I}-6.html" target="_blank">5 times ago</a></li> 
                <li><a href="Place{I}/place{I}-7.html" target="_blank">6 times ago</a></li>
                <li><a href="Place{I}/place{I}-8.html" target="_blank">7 times ago</a></li>
                <li><a href="Place{I}/place{I}-9.html" target="_blank">8 times ago</a></li>   
                <li><a href="Place{I}/place{I}-10.html" target="_blank">9 times ago</a></li>
                <li><a href="Place{I}/place{I}-11.html" target="_blank">10 times ago</a></li>
                <li><a href="Place{I}/place{I}-12.html" target="_blank">11 times ago</a></li>  
            </ol>
        </div>'''.format(PLACE = place[i],
                        I = str(i+1) ))
        return each_body


    def comb_index(self, index_body_head, each_body):

        html_body = ""

        if len(each_body) <= 2:
            body = ""
            for i in range(len(each_body)):
                body = body + each_body[i]
                print(each_body[0])
            html_body = '''    <div class="box1">
            {BODY}
        </div>'''.format(BODY = body)
            print(body)
            print(html_body)
        elif 2 < len(each_body) <= 4:
            body1 = ""
            body2 = ""
            for i in range(len(each_body)):
                if i < 2:
                    body1 = body1 + each_body[i]
                    print(each_body[i])
                elif 1 < i < 4:
                    body2 = body2 + each_body[i]
                    print(each_body[i])
            html_body = '''    <div class="box1">
            {BODY1}
        </div>
        <div class="box1">
            {BODY2}
        </div>'''.format(BODY1 = body1,
                            BODY2 = body2)
            print(body1)
            print(body2)
            print(html_body)

        index_html = index_body_head + html_body

        with open("./template/index.html", 'w', encoding='utf-8' ) as f: 
                f.write(index_html) 


#if __name__ == '__main__':
#    place = ["catbed1", "catbed2", "catbed3", "catbed4"]
#    main = Gen_main()
#    index_body_head = main.gen_body_head(place)
#    each_body = main.gen_mid_body(place)
#    main.comb_index(index_body_head, each_body)