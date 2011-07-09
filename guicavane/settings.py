#!/usr/bin/env python
# encoding: utf-8

"""
Settings. Manages the gui of the settings.
"""

import gtk
from constants import SETTINGS_GUI_FILE


class Settings(object):
    """
    Settings interface manager.
    """

    def __init__(self, config):
        """
        Creates the window and initializes the attributes.
        """

        # Gtk builder
        self.builder = gtk.Builder()
        self.builder.add_from_file(SETTINGS_GUI_FILE)
        self.builder.connect_signals(self)

        # Config
        self.config = config

        # Widgets
        self.main_dialog = self.builder.get_object("settingsDialog")
        self.player_button = self.builder.get_object("playerLocationButton")
        self.cache_dir_button = self.builder.get_object("cachedirButton")
        self.automatic_marks_button = self.builder.get_object("automaticMarks")
        self.cached_percentage = self.builder.get_object("cachePercentageScale")

    def show(self):
        """
        Shows the window with the values correctly asigned.
        """

        # Get the config values
        player_location = self.config.get_key("player_location")
        cache_dir = self.config.get_key("cache_dir")
        automatic_marks = self.config.get_key("automatic_marks")
        cached_percentage = self.config.get_key("cached_percentage")

        # Set the values
        self.player_button.set_filename(player_location)
        self.cache_dir_button.set_filename(cache_dir)
        self.automatic_marks_button.set_active(automatic_marks)
        self.cached_percentage.set_value(cached_percentage)

        # Show the dialog and hide on close
        self.main_dialog.run()
        self.main_dialog.hide()

    def _on_save_settings(self, *args):
        """
        Saves the settings to the disk.
        """

        # Get the values
        player_location = self.player_button.get_filename()
        cache_dir = self.cache_dir_button.get_filename()
        automatic_marks = self.automatic_marks_button.get_active()
        cached_percentage = self.cached_percentage.get_value()

        # Save the new values to the config
        self.config.set_key("player_location", player_location)
        self.config.set_key("cache_dir", cache_dir)
        self.config.set_key("automatic_marks", automatic_marks)
        self.config.set_key("cached_percentage", cached_percentage)
        self.config.save()

        # Hide the dialog
        self.main_dialog.hide()
