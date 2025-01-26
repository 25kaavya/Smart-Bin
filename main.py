from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from image_processing import process_image
from classifier import classify_item


class MainScreen(Screen):
    def open_file_chooser(self):
        """
        Opens a file chooser popup for selecting image files.
        """
        try:
            # Create a popup with a FileChooser for selecting images
            filechooser = FileChooserListView(filters=["*.jpg", "*.png", "*.jpeg"])  # Allow only image files
            filechooser.bind(on_submit=self.on_file_selected)
            popup = Popup(
                title="Select an Image File",
                content=filechooser,
                size_hint=(0.9, 0.9),
            )
            self.popup = popup
            popup.open()
        except Exception as e:
            self.show_popup("Error", f"Failed to open file chooser: {str(e)}")

    def on_file_selected(self, instance, selection, touch=None):
        """
        Handles the selected file from the file chooser.
        """
        try:
            # Debugging log for selected files
            print(f"[DEBUG] Selected files: {selection}")

            if selection:  # Check if a file was selected
                image_path = selection[0]  # Use the first selected file
                print(f"[DEBUG] Selected file path: {image_path}")
                self.popup.dismiss()  # Close the popup
                self.process_image_input(image_path)
            else:
                self.show_popup("Error", "No file selected.")
        except Exception as e:
            print(f"[DEBUG] Error in on_file_selected: {e}")
            self.show_popup("Error", f"Failed to process file selection: {str(e)}")

    def process_image_input(self, image_path):
        """
        Processes the selected image file for classification.
        """
        try:
            # Use the image path to process the image
            labels = process_image(image_path)
            bin_name = classify_item(labels)

            # Navigate to the result screen and update the result
            self.manager.get_screen("result").update_result(bin_name)
            self.manager.current = "result"
        except FileNotFoundError:
            self.show_popup("Error", f"File not found: {image_path}")
        except Exception as e:
            self.show_popup("Error", f"Failed to process image: {str(e)}")

    def process_text_input(self):
        """
        Processes text input from the user for classification.
        """
        try:
            text_input = self.ids.text_input.text.strip()
            if not text_input:
                self.show_popup("Error", "Please enter a valid item description.")
                return

            # Pass the text input to the classifier
            bin_name = classify_item([text_input.lower()])

            # Navigate to the result screen and update the result
            self.manager.get_screen("result").update_result(bin_name)
            self.manager.current = "result"
        except Exception as e:
            self.show_popup("Error", f"Failed to process text: {str(e)}")

    def show_popup(self, title, message):
        """
        Displays a popup with a message.
        """
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4),
        )
        popup.open()


class ResultScreen(Screen):
    def update_result(self, bin_name):
        """
        Updates the result label with the bin classification.
        """
        self.ids.result_label.text = f"Place the item in: {bin_name} bin"


class RecyclingApp(App):
    def build(self):
        """
        Builds the Kivy app using the KV file for layout.
        """
        return Builder.load_file("kivy_interface.kv")


if __name__ == "__main__":
    RecyclingApp().run()
