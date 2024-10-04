#!/usr/bin/python3
""" Console Module """
import cmd
import re
import shlex
import sys
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    prompt = '(hbnb) '

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        arg_list = args.split(' ')
        if arg_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        obj = HBNBCommand.classes[arg_list[0]]()
        print(obj.id)

        # catch pattern <key name>=<value>
        pattern = re.compile(r'^(\w+)="?(([\w.@,-]|\\")+)"?,?$')
        arg_list = arg_list[1:]
        for param in arg_list:

            match = pattern.search(param)
            if not match:
                continue

            key = match.group(1)
            val = match.group(2).strip('"').replace('_', ' ')
            if key in HBNBCommand.types.keys():
                try:
                    setattr(obj, key, HBNBCommand.types[key](val))
                except Exception:
                    pass
            else:
                setattr(obj, key, str(val))

        obj.save()

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        if not args:
            print("** class name missing **")
            return

        args = args.split(' ')
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return

        key = args[0] + "." + args[1]
        try:
            storage.all()[key].delete()
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all().items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage.all().items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage.all().items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, arg):
        """ Updates a certain object with new info """
        if not arg:
            print("** class name missing **")
            return

        # arg copy needed further down
        arg_copy = str(arg)

        args = shlex.split(arg)
        if args[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return

        for i in range(len(args)):
            args[i] = args[i].strip(',')
        all_obj = storage.all()

        # catch dictionary pattern using RegEx
        pattern = r'{(["\'](\w)+["\']: ?["\']?([\w.@,-]|\\")+["\']?,? ?)+}'
        match = re.compile(pattern).search(arg_copy)
        # match = pattern.search(arg_copy)
        if match:
            obj_dict = eval(match.group(0))
            if type(obj_dict) is not dict:
                return
            key = args[0] + '.' + args[1].strip('"')
            try:
                obj = all_obj[key]
                for k in obj_dict.keys():
                    setattr(obj, k, obj_dict[k])
                obj.save()
                return
            except KeyError:
                print("** no instance found **")
                return

        for k, v in all_obj.items():
            obj_name = v.__class__.__name__
            obj_id = v.id
            if obj_name == args[0] and obj_id == args[1].strip('"'):
                if len(args) == 2:
                    print("** attribute name missing **")
                elif len(args) == 3:
                    print("** value missing **")
                else:
                    setattr(v, args[2], args[3])
                    v.save()
                return
        print("** no instance found **")

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
