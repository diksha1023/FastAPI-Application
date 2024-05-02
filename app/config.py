from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #provide list of env vars that we need to set as properties in the class
    database_hostname: str
    database_port: str
    database_password: str
    database_name : str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    #pydantic model ll perform all the validations for us to ensure that all of these ve been set.

    class Config:
        env_file = ".env"

#pydantic model will read the env vars and convert them to lowercase(case insensitive), and validate all the values and store it into 'settings' 
# var and we can directly access it using this var
settings = Settings()
