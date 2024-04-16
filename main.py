import numpy as np  # Import NumPy library for numerical operations
import skimage.data as skd  # Import skimage.data for accessing sample images
from kivy.app import App  # Import the main Kivy application class
from kivy.uix.label import Label  # Import Label widget for displaying text
from kivy.uix.slider import Slider  # Import Slider widget for adjusting values
from kivy.uix.boxlayout import BoxLayout  # Import BoxLayout for arranging widgets
from kivy.uix.image import Image as KivyImage  # Import Image widget for displaying images
from kivy.graphics.texture import Texture  # Import Texture for working with image textures
from kivy.uix.button import Button  # Import Button widget for user interaction
from PIL import Image  # Import Image module from PIL library for image processing

class BasicApp(App):
    def build(self):
        # Define layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)  # Create a vertical BoxLayout
        
        # Create labels for sliders with color number
        self.red_label = Label(text="Red Factor (1.0)", size_hint=(None, None), size=(150, 30))  # Label for red slider
        self.green_label = Label(text="Green Factor (1.0)", size_hint=(None, None), size=(150, 30))  # Label for green slider
        self.blue_label = Label(text="Blue Factor (1.0)", size_hint=(None, None), size=(150, 30))  # Label for blue slider
        
        # Create sliders
        self.red_slider = Slider(min=0, max=2, value=1, size_hint=(None, None), size=(300, 30))  # Slider for adjusting red factor
        self.green_slider = Slider(min=0, max=2, value=1, size_hint=(None, None), size=(300, 30))  # Slider for adjusting green factor
        self.blue_slider = Slider(min=0, max=2, value=1, size_hint=(None, None), size=(300, 30))  # Slider for adjusting blue factor
        
        # Bind sliders to callback functions
        self.red_slider.bind(value=self.on_slider_change)  # Bind red slider to its callback function
        self.green_slider.bind(value=self.on_slider_change)  # Bind green slider to its callback function
        self.blue_slider.bind(value=self.on_slider_change)  # Bind blue slider to its callback function
        
        # Add widgets to layout
        layout.add_widget(self.red_label)  # Add red label to layout
        layout.add_widget(self.red_slider)  # Add red slider to layout
        layout.add_widget(self.green_label)  # Add green label to layout
        layout.add_widget(self.green_slider)  # Add green slider to layout
        layout.add_widget(self.blue_label)  # Add blue label to layout
        layout.add_widget(self.blue_slider)  # Add blue slider to layout
        
        # Add Default button
        default_button = Button(text="Default", size_hint=(None, None), size=(100, 50))  # Create default button
        default_button.bind(on_press=self.reset_sliders)  # Bind default button to its callback function
        layout.add_widget(default_button)  # Add default button to layout
        
        # Add Random button
        random_button = Button(text="Random", size_hint=(None, None), size=(100, 50))  # Create random button
        random_button.bind(on_press=self.randomize_sliders)  # Bind random button to its callback function
        layout.add_widget(random_button)  # Add random button to layout
        
        # Display image
        self.image_texture = Texture.create(size=(512, 512))  # Create texture for displaying image
        self.original_image = skd.astronaut()  # Load sample image
        self.modified_image = self.original_image.copy()  # Create a copy of the original image for modification
        self.update_image_texture()  # Update the image texture
        image_widget = KivyImage(texture=self.image_texture)  # Create image widget
        
        # Add image widget to layout
        layout.add_widget(image_widget)  # Add image widget to layout
        
        return layout  # Return the layout as the root widget
    
    def on_slider_change(self, instance, value):
        # Update modified image and texture based on slider values
        red_factor = self.red_slider.value  # Get red factor value from slider
        green_factor = self.green_slider.value  # Get green factor value from slider
        blue_factor = self.blue_slider.value  # Get blue factor value from slider
        self.modified_image = modify_colors(self.original_image, red_factor, green_factor, blue_factor)  # Modify image based on slider values
        self.update_image_texture()  # Update image texture with modified image
        # Update color factor labels
        self.red_label.text = "Red Factor ({:.2f})".format(red_factor)  # Update red label text with current red factor
        self.green_label.text = "Green Factor ({:.2f})".format(green_factor)  # Update green label text with current green factor
        self.blue_label.text = "Blue Factor ({:.2f})".format(blue_factor)  # Update blue label text with current blue factor
    
    def reset_sliders(self, instance):
        # Reset sliders to default values
        self.red_slider.value = 1  # Reset red slider value
        self.green_slider.value = 1  # Reset green slider value
        self.blue_slider.value = 1  # Reset blue slider value
        # Update color factor labels
        self.red_label.text = "Red Factor (1.0)"  # Reset red label text
        self.green_label.text = "Green Factor (1.0)"  # Reset green label text
        self.blue_label.text = "Blue Factor (1.0)"  # Reset blue label text
    
    def randomize_sliders(self, instance):
        # Generate random values for sliders
        self.red_slider.value = np.random.uniform(0, 2)  # Set red slider to a random value between 0 and 2
        self.green_slider.value = np.random.uniform(0, 2)  # Set green slider to a random value between 0 and 2
        self.blue_slider.value = np.random.uniform(0, 2)  # Set blue slider to a random value between 0 and 2
        # Trigger slider change to update the image
        self.on_slider_change(None, None)  # Update image based on new slider values
    
    def update_image_texture(self):
        # Convert modified image to texture and display
        img = Image.fromarray(self.modified_image)  # Convert modified image array to PIL Image
        buf = img.tobytes()  # Convert PIL Image to bytes
        self.image_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')  # Blit bytes to image texture
        self.image_texture.flip_vertical()  # Flip the image vertically for correct orientation

def modify_colors(image_array, red_factor=1.0, green_factor=1.0, blue_factor=1.0):
    modified_image = image_array.astype(np.float32)  # Convert image array to float32 for modification
    modified_image[:, :, 0] *= red_factor  # Modify red channel
    modified_image[:, :, 1] *= green_factor  # Modify green channel
    modified_image[:, :, 2] *= blue_factor  # Modify blue channel
    modified_image = np.clip(modified_image, 0, 255).astype(np.uint8)  # Clip values to ensure they are within valid range
    return modified_image  # Return modified image array

if __name__ == "__main__":
    BasicApp().run()  # Run the Kivy application