from http.server import BaseHTTPRequestHandler, HTTPServer


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = [line.rstrip() for line in file]
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def runserver(self):
        address = "127.0.0.1"
        port = 8000
        server_address = (address, port)
        httpd = HTTPServer(server_address, TasksServer)
        print(f"Started HTTP Server on http://{address}:{port}")
        httpd.serve_forever()

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help" or command is None:
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
# Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py ls
# Delete the incomplete item with the given priority number
$ python tasks.py del PRIORITY_NUMBER
# Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py done PRIORITY_NUMBER
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        self.read_current()
        try:
            priority = int(args[0])
            new_priority = int(args[0])
            task = args[1]
            if task == 0:
                print("No task given!")
            else:

                while priority in self.current_items:
                    priority += 1

                while new_priority < priority:
                    self.current_items[priority] = self.current_items[priority-1]
                    priority -= 1
                    

                self.current_items[priority] = task
                self.write_current()

                print(f"Added task: \"{task}\" with priority {priority}")

        except:
            print("First argument is not a number!!")


    def done(self, args):
        try:
            self.read_current()
            self.read_completed()

            priority = int(args[0])

            if priority in self.current_items.keys():
                self.completed_items.append(self.current_items[priority])
                self.current_items.pop(priority)

                self.write_completed()
                self.write_current()
                print(f"Marked item as done.")

            else:
                print(f"Error: no incomplete item with priority {
                      priority} exists.")

        except:
            print("First argument is not a number!!")

    def delete(self, args):
        try:
            self.read_current()
            priority = int(args[0])
            if priority in self.current_items.keys():
                self.current_items.pop(priority)
                self.write_current()
                print(f"Deleted item with priority {priority}")

            else:
                print(f"Error: item with priority {
                      priority} does not exist. Nothing deleted.")

            self.write_current()

        except:
            print("First argument is not a number!!")

    def ls(self):
        self.read_current()
        if self.current_items == {}:
            print("There is no pending tasks")
        else:
            i = 1
            for priority, task in self.current_items.items():
                print(f"{i}. {task} [{priority}]")
                i += 1

    def report(self):
        self.read_completed()
        self.read_current()

        print(f"Pending : {len(self.current_items)}")
        self.ls()
        print()

        print(f"Completed : {len(self.completed_items)}")

        i = 1
        for line in self.completed_items:
            print(f"{i}. {line}")

    def render_pending_tasks(self):
        # Complete this method to return all incomplete tasks as HTML
        incompleted = str()
        self.read_current()
        for i in self.current_items.values():
            i = f"<h1>{i}</h></br>"
            incompleted += i

        return incompleted

    def render_completed_tasks(self):
        completed = str()
        self.read_completed()
        for i in self.completed_items:
            i = f"<h1>{i}</h></br>"
            completed += i

        return completed


class TasksServer(TasksCommand, BaseHTTPRequestHandler):
    def do_GET(self):
        task_command_object = TasksCommand()
        if self.path == "/tasks":
            content = task_command_object.render_pending_tasks()
        elif self.path == "/completed":
            content = task_command_object.render_completed_tasks()
        
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())


serv = TasksCommand()
serv.runserver()