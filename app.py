import io
import zipfile
import streamlit as st
from pdf2image import convert_from_bytes

st.set_page_config(
    page_title="PDF to Image Converter - VKR", page_icon="🖼️"
)

st.title("📄 PDF to Image (JPG) Converter")
st.write(
    "Upload your PDF file below to instantly convert and download pages as"
    " images."
)

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
  st.write("Processing your PDF... Please wait ⏳")

  bytes_data = uploaded_file.read()
  images = convert_from_bytes(bytes_data)

  st.success(f"Total Pages Found: {len(images)}")

  if len(images) == 1:
    img_byte_arr = io.BytesIO()
    images[0].save(img_byte_arr, format="JPEG")
    img_byte_arr = img_byte_arr.getvalue()

    st.image(images[0], caption="Converted Image", use_column_width=True)
    st.download_button(
        label="📥 Download JPG Image",
        data=img_byte_arr,
        file_name="converted_image.jpg",
        mime="image/jpeg",
    )
  else:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
      for i, image in enumerate(images):
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG")
        zip_file.writestr(f"page_{i+1}.jpg", img_byte_arr.getvalue())

    zip_buffer.seek(0)
    st.download_button(
        label="📥 Download All Images as ZIP",
        data=zip_buffer,
        file_name="pdf_images.zip",
        mime="application/zip",
    )