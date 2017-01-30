import os

class BaseConfig(object):
	DEBUG=False
	TESTING=False

class LocalConfig(BaseConfig):
	DEBUG=True
	TESTING=True

class DevelopmentConfig(BaseConfig):
	DEBUG=True
	TESTING=True

class StagingConfig(BaseConfig):
	DEBUG=True
	TESTING=True

class ProductionConfig(BaseConfig):
	DEBUG=False
	Testing=False

config = {
	"development": "app.config.DevelopmentConfig",
	"staging":"app.config.StagingConfig",
	"production":"app.config.ProductionConfig",
	"local":"app.config.LocalConfig"
}

def configure_app(app):
	config_name = os.getenv('FlASK_CONFIG','local')
	app.config.from_object(config[config_name])
