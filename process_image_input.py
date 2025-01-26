from kivy.uix.filechooser import FileChooserListView

def process_image_input(self):
    filechooser = FileChooserListView()
    filechooser.bind(on_submit=self.on_file_selected)

def on_file_selected(self, instance, selection):
    try:
        image_path = selection[0]  # Get the selected file path
        labels = process_image(image_path)
        bin_name = classify_item(labels)
        self.show_result(bin_name)
    except Exception as e:
        self.show_popup("Error", f"Failed to process image: {str(e)}")
