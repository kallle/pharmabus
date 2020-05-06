from control.app import app
import control.index
import control.registration
import control.order
import jinja2
import os

current_folder = os.path.dirname(os.path.realpath(__file__))
app.jinja_loader = jinja2.ChoiceLoader([app.jinja_loader,
                                        jinja2.FileSystemLoader([current_folder + '/templates/']),])
#app.run(port=5000, use_reloader=True, debug=True)
