# Load the .env file into the environment variables
load_dotenv(dotenv_path)

# Set the variables in our app to the already set environment variables
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")