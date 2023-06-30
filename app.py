
from short_ny import create_app
from .short_ny.config import config_dict

app = create_app()

if __name__=="__main__":
    app.run(debug=True)