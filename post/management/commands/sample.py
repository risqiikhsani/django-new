from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        parser.add_argument('my_num', nargs='+',type=int)
        # remove the nargs to make only one argument
        # remove the type to make the type string
        # change the file name to change the function name

    def handle(self, *args, **options):
        print(f"the number was {options.get('my_num')}")
