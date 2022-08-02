from concurrent.futures import process
import cv2
import streamlit as st
from PIL import Image
import numpy as np
import img2pdf

def main():
    st.title("Chalkboard Image Processor")

    hideSt = """ 
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hideSt, unsafe_allow_html=True)

    st.sidebar.title("Image Editing Panel")

    link = '<meta http-equiv="refresh" content="0;url=https://haroldsonanders.netlify.app/">'
    # Button brings user back to website
    if st.button('Back to Website'):
        st.markdown(link, unsafe_allow_html=True)

    # Get an image file
    imgFile = st.file_uploader("Upload Image of a Chalkboard to Process", type=['jpg', 'png', 'jpeg'])
    if not imgFile:
        return None

    # Open image with PIL & add to numpy array
    img = Image.open(imgFile)
    img = np.array(img)

    # create slider for image tweaking
    slider = st.sidebar.slider('Adjust Intensity (127 Default)', 1, 255, 127, step=1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Grayscale the input image
    (thresh, blackwhite) = cv2.threshold(gray, slider, 255, cv2.THRESH_BINARY) # get black and white values
    whiteblack = cv2.bitwise_not(blackwhite) # invert the black and white image for optional printing
   
    #st.image([img, blackwhite, whiteblack])
    st.text("Original Image:")
    st.image(img)
    st.text("Black & White Image:")
    st.image(blackwhite)
    st.text("Black & White Inverted Image:")
    st.image(whiteblack)

    st.header("Print Images")
    st.markdown("This converts the image to a PDF to download for printing. The white image can be dragged from above and is created specifically to save on ink, as it prevents printing absurd amounts of black onto the paper.")

    # Button brings user back to website
    if st.button('Back to Website', 2):
        st.markdown(link, unsafe_allow_html=True)

    # Get file to convert to PDF
    convertedImgFile = st.file_uploader("Upload Image to Convert to PDF for Printing", type=['jpg', 'png', 'jpeg'])
    if not convertedImgFile:
        return None
    
    # Open & convert the image to a PDF
    convertedImg = Image.open(convertedImgFile)
    PDF = convertedImg.convert('RGB')
    PDF.save('out.pdf')

    # Making the PDF available for download 
    with open("out.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    # Button for user to download their image
    st.download_button(label="Download PDF",
                    data=PDFbyte,
                    file_name="chalkboardPDF.pdf",
                    mime='application/octet-stream')


if __name__ == '__main__':
    main()

