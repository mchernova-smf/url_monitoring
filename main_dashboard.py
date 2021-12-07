from jinja2 import Template
from utils.database import select_all
from itertools import groupby

DASHBOARD_NAME = "monitoring_dashboard"
DASHBOARD_TEMPLATE = f"utils/{DASHBOARD_NAME}.jinja2"


def group_items(items):
    def key_func_site(x):
        return x["site"]
    def key_func_last_update(x):
            return x["last_update"]
    items.sort(key=key_func_site)
    grouped_items = []
    for _, value in groupby(items, key_func_site):
        list_of_values = list(value)
        list_of_values.sort(key=key_func_last_update, reverse=True)
        item = list_of_values[0]
        item["meta"] = list_of_values
        grouped_items += [item]
    return grouped_items


def create_dashboard():
    # get all records
    items = select_all()

    grouped_items = group_items(items)

    # open the file object and read it into the variable filedata.
    with open(DASHBOARD_TEMPLATE, "r") as file:
        template_text = file.read()
        # Create Jinja2 Template object
        template = Template(template_text)

    # Render Template to html
    rendered = template.render(dashboard_name=DASHBOARD_NAME,
        title="Web Sites Status Dashboard",
        items=grouped_items)

    with open('output/dashboard.html', 'w') as f:
        f.write(rendered)

if __name__ == "__main__":
    create_dashboard()
