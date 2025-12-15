import streamlit as st
import PIL.Image
import PIL.ImageEnhance # <--- NEW: Library to fix blurry images

# --- THE LOGIC ---
CHARS_HEAVY_TO_LIGHT = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
CHARS_LIGHT_TO_HEAVY = CHARS_HEAVY_TO_LIGHT[::-1]

def resize_image(image, new_width=100, vertical_scale=1.65):
    width, height = image.size
    # vertical_scale controls how "tall" the lines are. 
    # If the image looks stretched, increase this number.
    ratio = height / width / vertical_scale 
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image, char_set):
    pixels = image.getdata()
    max_char_index = len(char_set) - 1
    new_pixels = [char_set[int(pixel_val / 255 * max_char_index)] for pixel_val in pixels]
    return "".join(new_pixels)

# --- THE WEB APP UI ---
st.set_page_config(page_title="ASCII Art Pro", layout="wide")
st.title("🎨 ASCII Art Generator (High Quality)")

# 1. SIDEBAR CONTROLS
with st.sidebar:
    st.header("🔧 Fine-Tuning")
    
    # Resolution
    new_width = st.slider("Resolution (Width)", 50, 400, 150)
    
    st.write("---")
    st.write("**Fix Messy Images:**")
    
    # Contrast Booster (The most important fix!)
    contrast_val = st.slider("Contrast Booster", 0.5, 3.0, 1.5)
    st.caption("Increase this if the image looks 'muddy' or gray.")
    
    # Brightness Adjustment
    brightness_val = st.slider("Brightness", 0.5, 2.0, 1.0)
    
    # Invert
    st.write("---")
    invert = st.checkbox("Invert Colors (Dark Mode)", value=True)

uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    
    # --- PRE-PROCESSING (The Fix) ---
    # 1. Boost Contrast
    enhancer = PIL.ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_val)
    
    # 2. Adjust Brightness
    enhancer = PIL.ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_val)

    # Show the "Processed" image so user understands what the computer sees
    with st.expander("See what the computer sees (Grayscale Preview)"):
        st.image(grayify(image), width=300)

    # --- CONVERSION ---
    if invert:
        active_chars = CHARS_LIGHT_TO_HEAVY 
    else:
        active_chars = CHARS_HEAVY_TO_LIGHT

    processed_image = grayify(resize_image(image, new_width))
    ascii_str = pixels_to_ascii(processed_image, active_chars)
    
    pixel_count = len(ascii_str)
    ascii_image = "\n".join(ascii_str[i:(i+new_width)] for i in range(0, pixel_count, new_width))
    
    # --- RESULT ---
    st.subheader("ASCII Result:")
    # We use a smaller font size in the code block for better viewing
    st.code(ascii_image, language=None)