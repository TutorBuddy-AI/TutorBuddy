import os

from libcloud.storage.base import StorageDriver
from libcloud.storage.providers import get_driver
from libcloud.storage.types import ContainerDoesNotExistError, Provider
from sqlalchemy_file.storage import StorageManager

from src.config import config


def get_or_create_container(driver: StorageDriver, container_name: str):
    try:
        return driver.get_container(container_name)
    except ContainerDoesNotExistError:
        """This will just create a new directory inside the base directory for local storage."""
        return driver.create_container(container_name)


def configure_storage():
    os.makedirs(config.UPLOAD_FOLDER, 0o777, exist_ok=True)  # Create Base directory
    cls = get_driver(Provider.LOCAL)
    driver = cls(config.UPLOAD_FOLDER)

    StorageManager.add_storage("images", get_or_create_container(driver, "post-images"))
    StorageManager.add_storage("other_files", get_or_create_container(driver, "bin"))
