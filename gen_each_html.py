#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

class Gen_each:
    def __init__(self):
        self.TL_flag = ["latest",
                    "1 time ago",
                    "2 times ago",
                    "3 times ago",
                    "4 times ago",
                    "5 times ago",
                    "6 times ago",
                    "7 times ago",
                    "8 times ago",
                    "9 times ago",
                    "10 times ago",
                    "11 times ago"]
        os.makedirs("./template/Place1", exist_ok=True)
        os.makedirs("./template/Place2", exist_ok=True)
        os.makedirs("./template/Place3", exist_ok=True)
        os.makedirs("./template/Place4", exist_ok=True)
        return


    def gen_each_html(self, place):

        for j in range(len(place)):
            for i in range(12):
                html_body = '''<!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>{PLACE1}</title>
                </head>
                <body>
                    <h1>{PLACE1} {TL}</h1>
                    <video src="01.mp4" autoplay muted loop playsinline controls width=1024 height=768></video>
                </body>'''.format(PLACE1 = place[j],
                                    TL = self.TL_flag[i])

                with open("./template/Place" + str(j+1) + "/place" + str(j+1) + "-" + str(i+1) + ".html", 'w', encoding='utf-8' ) as f: 
                    f.write(html_body) 


#if __name__ == '__main__':
#    place = ["catbed1", "catbed2", "catbed3", "catbed4"]
#    each = Gen_each()
#    each.gen_each_html(place)