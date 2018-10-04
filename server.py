# from http.server import BaseHTTPRequestHandler, HTTPServer
import http.server
import socket
import psycopg2
import json

import database_handling as dh

class S(http.server.BaseHTTPRequestHandler):

    def _set_headers(self, content_type):
        self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        self.send_header('Content-type', content_type)
        self.end_headers()


    def serve_file(self, file_name):
        if file_name == "":
            file_name = "index.html"
        elif file_name == "favicon.ico":
            return
        self._set_headers("text/html")
        with open(file_name, "rb") as file:
            self.wfile.write(file.read())

    def get_table(self, cursor, table_name):
        if table_name == "militaryequipment":
            self._set_headers("")
            table = dh.get_all_from_ME(cursor)
            json_response = json.dumps(table)
            self.wfile.write(json_response.encode("utf-8"))
        elif table_name == "manufacturers":
            self._set_headers("")
            table = dh.get_all_from_MAN(cursor)
            json_response = json.dumps(table)
            self.wfile.write(json_response.encode("utf-8"))

    def update_data(self, cursor, path):
        if path[0] == "militaryequipment":
            name = path[1].replace("%20", " ")
            classification = path[2].replace("%20", " ")
            rowID = path[3].replace("%20", " ")
            dh.update_from_ME(cursor, name, classification, rowID)
        elif path[0] == "manufacturers":
            name = path[1].replace("%20", " ")
            rowID = path[2].replace("%20", " ")
            dh.update_from_MAN(cursor, name, rowID)

    def delete_data(self, cursor, table, rowID):
        if table == "militaryequipment":
            dh.delete_from_ME(cursor, rowID)
        elif table == "manufacturers":
            dh.delete_from_MAN(cursor, rowID)

    def add_data(self, cursor, table, path):
        if table == "militaryequipment":
            name = path[0].replace("%20", " ")
            classification = path[1].replace("%20", " ")
            manufacturer = path[2].replace("%20", " ")
            dh.add_to_ME(cursor, name, classification, manufacturer)
        elif table == "manufacturers":
            name = path[0].replace("%20", " ")
            print(name)
            dh.add_to_MAN(cursor, name)

    def do_GET(self):
        path = self.path.split("/")[1:]
        # print(path)
        if path[0] == "api" :
            with psycopg2.connect(host="localhost", database="postgres") as conn:
                with conn.cursor() as cursor:
                    if path[1] == "table":
                        self.get_table(cursor, path[2])
                    if path[1] == "update":
                        self.update_data(cursor, path[2:])
                        conn.commit()
                    if path[1] == "delete":
                        self.delete_data(cursor, path[2], path[3])
                        conn.commit()
                    if path[1] == "add":
                        self.add_data(cursor, path[2], path[3:])
                        conn.commit()
        else:
            self.serve_file(path[0])


    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8").split("\n")[5:-2]
        split_data = [row.split(",") for row in post_data]
        with psycopg2.connect(host="localhost", database="postgres") as conn:
            with conn.cursor() as cursor:
                for row in split_data:
                    dh.add_to_ME(cursor, row[0], row[1], row[2])
            conn.commit()
        
def run(server_class=http.server.HTTPServer, handler_class=S, port=8000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()